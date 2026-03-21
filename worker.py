import pika
import json
import time
import os

# --- ARAÇLAR (TOOLS) ---

def email_taslagi_olustur(mesaj):
    print(f"[📧 EMAIL TOOL] Taslak hazırlanıyor: '{mesaj}'")
    time.sleep(2)
    print(f"[✅ EMAIL TOOL] Taslak hazırlandı ve kaydedildi.")

def veri_analizi_ve_kayit(mesaj):
    print(f"[📊 ANALİZ TOOL] Veri işleniyor: '{mesaj}'")
    time.sleep(2)
    print(f"[✅ ANALİZ TOOL] Veri yapılandırıldı ve DB'ye işlendi.")

# --- ANA İŞLEYİCİ ---

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        gorev_tipi = data.get("task")
        icerik = data.get("content")

        print(f"\n[⚙️] YENİ GÖREV ALINDI: {gorev_tipi.upper() if gorev_tipi else 'BİLİNMEYEN'}")

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

# --- BAĞLANTI AYARLARI ---

def start_worker():
    # API ile aynı değişkenleri kullanarak URL oluşturuyoruz
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASS')
    host = os.getenv('RABBITMQ_HOST')
    
    if not all([user, password, host]):
        print("[❌] HATA: RabbitMQ kimlik bilgileri eksik!")
        return

    url = f"amqps://{user}:{password}@{host}/{user}"
    params = pika.URLParameters(url)
    
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task_queue', on_message_callback=callback)

        print(' [*] İşçi uyanık ve akıllı modda emir bekliyor...')
        channel.start_consuming()
    except Exception as e:
        print(f"[❌] Bağlantı hatası: {e}")

if __name__ == "__main__":
    start_worker()
