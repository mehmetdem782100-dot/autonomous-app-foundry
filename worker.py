import pika
import json
import time
import os
import uuid
from memory.vector_store.chroma_client import VectorDBClient

# --- BELLEK AYARI ---
memory = VectorDBClient()

# --- ARAÇLAR (TOOLS) ---

def memory_save(task_type, content, result):
    """Görev sonucunu hafızaya (Vektör DB) kaydeder."""
    task_id = str(uuid.uuid4())
    metadata = {"task_type": task_type, "timestamp": str(time.time())}
    
    # ChromaDB'ye asenkron olmayan (sync) kayıt
    collection = memory.get_collection_sync("system_memory")
    collection.add(
        documents=[f"Görev: {task_type} | İçerik: {content} | Sonuç: {result}"],
        metadatas=[metadata],
        ids=[task_id]
    )
    print(f"[🧠 MEMORY] Görev hafızaya kazındı. ID: {task_id}")

def email_taslagi_olustur(mesaj):
    print(f"[📧 EMAIL TOOL] Taslak hazırlanıyor: '{mesaj}'")
    time.sleep(1)
    result = f"Taslak oluşturuldu: {mesaj[:20]}..."
    memory_save("email", mesaj, result)
    return result

def veri_analizi_ve_kayit(mesaj):
    print(f"[📊 ANALİZ TOOL] Veri işleniyor: '{mesaj}'")
    time.sleep(1)
    result = f"Analiz raporu: {len(mesaj)} karakter işlendi."
    memory_save("analiz", mesaj, result)
    return result

# --- ANA İŞLEYİCİ ---

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        gorev_tipi = data.get("task")
        icerik = data.get("content")

        print(f"\n[⚙️] YENİ GÖREV ALINDI: {gorev_tipi.upper()}")

        if gorev_tipi == "email":
            email_taslagi_olustur(icerik)
        elif gorev_tipi == "analiz":
            veri_analizi_ve_kayit(icerik)
        else:
            print(f"[⚠️] Tanımlanamayan görev tipi: {gorev_tipi}")

        print(f"[🏁] GÖREV BİTTİ.\n")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[❌] İşleme hatası: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

# --- BAĞLANTI ---

def start_worker():
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASS')
    host = os.getenv('RABBITMQ_HOST')
    
    url = f"amqps://{user}:{password}@{host}/{user}"
    params = pika.URLParameters(url)
    
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(' [*] İşçi uyanık ve BELLEK (Memory) modunda emir bekliyor...')
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
