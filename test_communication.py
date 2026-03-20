import pika, json, os

# Şifreleri sistemden (env) çekiyoruz
user = os.getenv('RABBITMQ_USER', 'guest')
password = os.getenv('RABBITMQ_PASS', 'guest')
host = os.getenv('RABBITMQ_HOST', 'localhost')

credentials = pika.PlainCredentials(user, password)
parameters = pika.ConnectionParameters(host=host, credentials=credentials)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    message = {"task": "test", "content": "Güvenli P1 Testi Başarılı!"}
    channel.basic_publish(
        exchange='', routing_key='task_queue', body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print("🚀 Güvenli test mesajı gönderildi!")
    connection.close()
except Exception as e:
    print(f"❌ Hata: {e}")
