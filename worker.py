import pika, json, os, time

def callback(ch, method, properties, body):
    data = json.loads(body)
    task_type = data.get("task", "unknown")
    content = data.get("content", "")
    
    print(f"\n[⚙️] YENİ GÖREV ALINDI: {task_type.upper()}")
    print(f"[📄] İÇERİK: {content}")
    
    # Gerçek bir iş simülasyonu
    print("[⏳] İşlem başlatıldı...")
    time.sleep(2) 
    print(f"[✅] GÖREV TAMAMLANDI: {task_type}\n" + "-"*30)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
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
    
    print(' [*] İşçi uyanık ve emir bekliyor... (Durdurmak için CTRL+C)')
    channel.start_consuming()

if __name__ == "__main__":
    main()
