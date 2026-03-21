import asyncio
import os
from aio_pika import connect_robust, Message, DeliveryMode

async def main():
    user = os.getenv("RABBITMQ_USER")
    password = os.getenv("RABBITMQ_PASS")
    host = os.getenv("RABBITMQ_HOST")
    
    # Parçaları birleştirip tam adresi oluşturuyoruz (vhost genelde kullanıcı adıyla aynıdır)
    url = f"amqps://{user}:{password}@{host}/{user}"
    
    try:
        connection = await connect_robust(url)
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue("task_queue", durable=True)
            msg = Message(
                body=b'{"task": "test", "content": "Harici test basarili!"}',
                delivery_mode=DeliveryMode.PERSISTENT
            )
            await channel.default_exchange.publish(msg, routing_key="task_queue")
            print("🚀 Mesaj başarıyla RabbitMQ'ya gönderildi!")
    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")

asyncio.run(main())
