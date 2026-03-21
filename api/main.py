from fastapi import FastAPI, BackgroundTasks
import pika, json, os

app = FastAPI(title="Otonom App Foundry API")

def send_to_queue(task_data: dict):
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASS')
    host = os.getenv('RABBITMQ_HOST')
    url = f"amqps://{user}:{password}@{host}/{user}"
    
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(task_data),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

@app.get("/")
async def root():
    return {"status": "online", "message": "Otonom sistem hazır."}

@app.post("/gorev-ekle")
async def add_task(task_type: str, message: str):
    task_data = {"task": task_type, "content": message}
    send_to_queue(task_data)
    return {"message": "Görev kuyruğa eklendi", "data": task_data}
