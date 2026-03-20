import os
import pika
import json

class Orchestrator:
    def __init__(self):
        # 🔌 Bağlantı Ayarları (Environment variables üzerinden)
        self.rabbit_url = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        self.user = os.getenv('RABBITMQ_USER', 'aaf_user')
        self.password = os.getenv('RABBITMQ_PASS', 'aaf_pass')

    def create_task(self, goal: str):
        """
        Görevi veritabanına 'PENDING' durumuyla kaydeder.
        """
        print(f"📝 Yeni görev oluşturuluyor: {goal}")
        # Şimdilik temsili bir ID dönüyoruz, DB entegrasyonunda burayı bağlayacağız
        task_id = 1
        return task_id

    def dispatch_task(self, task_id: int, data: dict):
        """
        Görevi RabbitMQ üzerinden işçilere gönderir.
        """
        credentials = pika.PlainCredentials(self.user, self.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.rabbit_url, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        
        message = {"task_id": task_id, "data": data}
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"📦 Görev {task_id} sahaya sürüldü.")
        connection.close()

    def update_state(self, task_id: int, new_state: str):
        """
        Görevin durumunu günceller. (State Transition)
        """
        print(f"🚦 Görev {task_id} durumu güncellendi: {new_state}")
