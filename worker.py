import pika, json, os, sys

def callback(ch, method, properties, body):
    print(f" [✅] Worker (Env üzerinden) mesajı aldı: {json.loads(body)}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    user = os.getenv('RABBITMQ_USER', 'guest')
    password = os.getenv('RABBITMQ_PASS', 'guest')
    host = os.getenv('RABBITMQ_HOST', 'localhost')

    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host=host, credentials=credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print(' [🚀] Worker dinlemede (Güvenli Mod)...')
    channel.start_consuming()

if __name__ == "__main__":
    main()
