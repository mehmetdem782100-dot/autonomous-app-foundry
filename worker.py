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
        # Alaka düzeyi ve güncellik hesabı
        relevance_score = 1.0 / (distance + 0.01)
        now = time.time()
        age_seconds = now - float(timestamp)
        recency_score = 1.0 / (np.log1p(age_seconds / 3600) + 1)
        return (relevance_score * 0.7) + (recency_score * 0.3)

    def retrieve_context(self, query_text, top_n=5):
        try:
            collection = self.client._get_collection_sync(self.collection_name)
            results = collection.query(query_texts=[query_text], n_results=top_n)
            if not results['documents'] or not results['documents'][0]:
                return []
            
            scored_memories = []
            for i in range(len(results['documents'][0])):
                score = self._calculate_score(results['distances'][0][i], results['metadatas'][0][i]['timestamp'])
                scored_memories.append({
                    "content": results['documents'][0][i],
                    "score": score
                })
            return scored_memories
        except Exception as e:
            print(f"[❌] Hafıza erişim hatası: {e}")
            return []

    def save_experience(self, task_type, content, result):
        try:
            task_id = str(uuid.uuid4())
            collection = self.client._get_collection_sync(self.collection_name)
            collection.add(
                documents=[f"Görev: {task_type} | İçerik: {content} | Sonuç: {result}"],
                metadatas=[{"task_type": task_type, "timestamp": str(time.time())}],
                ids=[task_id]
            )
            print(f"[🧠] Hafızaya kaydedildi: {task_id}")
        except Exception as e:
            print(f"[❌] Hafıza kayıt hatası: {e}")

# --- 💡 AKIL YÜRÜTME MOTORU (ADIM 2) ---
class ReasoningEngine:
    def evaluate_strategy(self, current_task, memories):
        if not memories:
            return "İLK DENEYİM: Standart protokol uygulanıyor."
        
        # En yüksek skorlu anıya göre strateji belirle
        best_memory = max(memories, key=lambda x: x['score'])
        
        if "Hata" in best_memory['content']:
            return f"⚠️ DİKKAT: Benzer görevde hata yapıldı. Önceki hata verisinden kaçın."
        return "✅ REFERANS: Geçmiş başarılar rehberliğinde ilerle."

# --- 🏗️ PLANLAMA MOTORU (ADIM 3) ---
class PlanningEngine:
    def decompose(self, goal):
        """Karmaşık hedefi mantıksal alt adımlara böler."""
        print(f"[🗺️] PLANLANIYOR: {goal}")
        
        goal_lower = goal.lower()
        if "rapor" in goal_lower or "analiz" in goal_lower:
            return ["Verileri Sınıflandır", "İstatistikleri Hesapla", "Özeti Oluştur"]
        elif "email" in goal_lower or "mesaj" in goal_lower:
            return ["Taslak Metni Hazırla", "Hafıza Kontrolü Yap", "İletiyi Gönder"]
        
        return [f"Genel Görev: {goal}"]

# --- ⚙️ SİSTEM ENTEGRASYONU & GÜVENLİK ---
memory = MemoryManager()
reasoning = ReasoningEngine()
planner = PlanningEngine()

def callback(ch, method, properties, body):
    # 🛡️ GÜVENLİK 1: JSON Format Kontrolü
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        print("[❌] HATA: Gelen mesaj geçerli bir JSON değil. Pas geçiliyor.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    task_type, content = data.get("task", "unknown"), data.get("content", "")
    
    print(f"\n[🚀] ANA HEDEF ALINDI: {task_type.upper()}")
    
    # 🕵️ Hatırla ve Düşün
    memories = memory.retrieve_context(content)
    strategy = reasoning.evaluate_strategy(content, memories)
    print(f"[💡 STRATEJİ]: {strategy}")
    
    # 🏗️ Planla
    plan = planner.decompose(content)
    
    # Adımları Uygula (Simülasyon)
    for i, sub_task in enumerate(plan, 1):
        print(f"  [📍] ADIM {i}: {sub_task}")
        time.sleep(0.3)
        
    result = f"Görev {len(plan)} adımda başarıyla tamamlandı."
    memory.save_experience(task_type, content, result)
    
    print(f"[🏁] TÜM SÜREÇ BİTTİ.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    # 🛡️ GÜVENLİK 2: Ortam Değişkeni Kontrolü
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASS')
    host = os.getenv('RABBITMQ_HOST')

    if not all([user, password, host]):
        print("[❌] KRİTİK HATA: RabbitMQ bağlantı bilgileri (ENV) eksik!")
        return

    try:
        url = f"amqps://{user}:{password}@{host}/{user}"
        connection = pika.BlockingConnection(pika.URLParameters(url))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_consume(queue='task_queue', on_message_callback=callback)
        
        print(' [*] Hafıza Evreni v3.0 Aktif: Tam Kapasite Çalışıyor...')
        channel.start_consuming()
    except Exception as e:
        print(f"[❌] Bağlantı hatası: {e}")

if __name__ == "__main__":
    start_worker()
