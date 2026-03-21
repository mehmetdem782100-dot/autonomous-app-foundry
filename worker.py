import pika
import json
import time
import os
import uuid
import numpy as np
from memory.vector_store.chroma_client import VectorDBClient

# --- 🧠 BELLEK YÖNETİCİSİ (ADIM 1) ---
class MemoryManager:
    def __init__(self):
        self.client = VectorDBClient()
        self.collection_name = "system_memory"

    def _calculate_score(self, distance, timestamp):
        relevance_score = 1.0 / (distance + 0.01)
        now = time.time()
        age_seconds = now - float(timestamp)
        recency_score = 1.0 / (np.log1p(age_seconds / 3600) + 1)
        return (relevance_score * 0.7) + (recency_score * 0.3)

    def retrieve_context(self, query_text, top_n=5):
        try:
            # Düzeltme: Başına _ eklendi
            collection = self.client._get_collection_sync(self.collection_name)
            results = collection.query(query_texts=[query_text], n_results=top_n)
            if not results['documents'] or not results['documents'][0]:
                return []
            
            scored_memories = []
            for i in range(len(results['documents'][0])):
                score = self._calculate_score(results['distances'][0][i], results['metadatas'][0][i]['timestamp'])
                scored_memories.append({
                    "content": results['documents'][0][i],
                    "score": score,
                    "type": results['metadatas'][0][i].get('task_type', 'unknown')
                })
            return scored_memories
        except Exception as e:
            print(f"[❌] Hafıza okuma hatası: {e}")
            return []

    def save_experience(self, task_type, content, result):
        try:
            task_id = str(uuid.uuid4())
            # Düzeltme: Başına _ eklendi
            collection = self.client._get_collection_sync(self.collection_name)
            collection.add(
                documents=[f"Görev: {task_type} | İçerik: {content} | Sonuç: {result}"],
                metadatas=[{"task_type": task_type, "timestamp": str(time.time())}],
                ids=[task_id]
            )
            print(f"[🧠] Hafızaya kaydedildi: {task_id}")
        except Exception as e:
            print(f"[❌] Hafıza kayıt hatası: {e}")

# --- 💡 AKIL YÜRÜTME MOTORU (ADIM 2 - ÇİFT HATLI) ---
class ReasoningEngine:
    def evaluate_strategy(self, current_task, memories):
        if not memories:
            return "İLK DENEYİM: Standart protokol uygulanıyor."

        failures = [m for m in memories if "Hata" in m['content'] or "Başarısız" in m['content']]
        successes = [m for m in memories if "Başarıyla" in m['content'] or "Tamamlandı" in m['content']]

        instructions = []
        
        if failures:
            worst_failure = max(failures, key=lambda x: x['score'])
            instructions.append(f"⚠️ DİKKAT: Geçmişteki hatayı tekrarlama -> {worst_failure['content']}")

        if successes:
            best_success = max(successes, key=lambda x: x['score'])
            instructions.append(f"✅ REFERANS: Şu başarılı yöntemi izle -> {best_success['content']}")

        if not instructions:
            return "Nötr bağlam saptandı. Genel prosedürü takip et."

        return " | ".join(instructions)

# --- ⚙️ SİSTEM ENTEGRASYONU ---
memory = MemoryManager()
reasoning = ReasoningEngine()

def callback(ch, method, properties, body):
    data = json.loads(body)
    task_type, content = data.get("task"), data.get("content")
    
    print(f"\n[🚀] İŞLEM BAŞLIYOR: {task_type.upper()}")
    
    memories = memory.retrieve_context(content)
    strategy = reasoning.evaluate_strategy(content, memories)
    print(f"[💡 STRATEJİ]: {strategy}")

    time.sleep(1)
    status = "Başarıyla" if "⚠️" not in strategy else "Düzeltilerek Başarıyla"
    result = f"{status} tamamlandı. ({strategy[:30]}...)"
    
    memory.save_experience(task_type, content, result)
    
    print(f"[🏁] GÖREV BİTTİ.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    user, password, host = os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'), os.getenv('RABBITMQ_HOST')
    url = f"amqps://{user}:{password}@{host}/{user}"
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print(' [*] Hafıza Evreni v2.0 Aktif: Akıl Yürütme Modu...')
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
