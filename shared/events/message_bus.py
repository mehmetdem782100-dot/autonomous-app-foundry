import json
import aio_pika
from typing import Callable, Awaitable
from core.config import settings
from core.logger import get_logger

logger = get_logger("MESSAGE_BUS")

class MessageBus:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.dlx_exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        
        self.dlx_exchange = await self.channel.declare_exchange(
            "cognita_dlx", aio_pika.ExchangeType.DIRECT, durable=True
        )
        
        self.exchange = await self.channel.declare_exchange(
            "cognita_main", aio_pika.ExchangeType.DIRECT, durable=True
        )

    async def publish(self, queue_name: str, payload: dict):
        if not self.channel:
            await self.connect()
            
        queue = await self.channel.declare_queue(
            queue_name, 
            durable=True,
            arguments={
                "x-dead-letter-exchange": "cognita_dlx",
                "x-dead-letter-routing-key": f"{queue_name}_dead"
            }
        )
        await queue.bind(self.exchange, routing_key=queue_name)

        message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await self.exchange.publish(message, routing_key=queue_name)

    async def consume(self, queue_name: str, callback: Callable[[dict], Awaitable[None]]):
        if not self.channel:
            await self.connect()

        dlq_name = f"{queue_name}_dead"
        dlq = await self.channel.declare_queue(dlq_name, durable=True)
        await dlq.bind(self.dlx_exchange, routing_key=dlq_name)

        queue = await self.channel.declare_queue(
            queue_name, 
            durable=True,
            arguments={
                "x-dead-letter-exchange": "cognita_dlx",
                "x-dead-letter-routing-key": dlq_name
            }
        )
        await queue.bind(self.exchange, routing_key=queue_name)
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(requeue=False, reject_on_redelivered=True):
                    try:
                        data = json.loads(message.body.decode())
                        await callback(data)
                    except Exception as e:
                        logger.error(f"Mesaj islenirken hata (Mesaj DLX'e atiliyor): {e}")
                        message.reject(requeue=False) 

    async def close(self):
        if self.connection:
            await self.connection.close()

bus = MessageBus()
