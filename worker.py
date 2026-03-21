import pika, json, os, sys

def callback(ch, method, properties, body):
    print(f" [✅] Worker (Env üzerinden) mesajı aldı: {json.loads(body)}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    user = os.getenv('RABBITMQ_USER', 'guest')
    password = os.getenv('RABBITMQ_PASS', 'guest')
    host = os.getenv('RABBITMQ_HOST', 'localhost')

    # Bağlantı adresini tıpkı testte yaptığımız gibi güvenli (amqps) formatta oluşturuyoruz
    url = f"amqps://{user}:{password}@{host}/{user}"
    parameters = pika.URLParameters(url)

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_consume(queue='task_queue', on_message_callback=callback)
        print(' [*] Worker dinlemede (Güvenli Mod)...')
        channel.start_consuming()
    except Exception as e:
        print(f"❌ Worker Bağlantı Hatası: {e}")

if __name__ == "__main__":
    main()
