
from src.interfaces.messaging import IMessagePublisher

import json
from kombu import Connection, Exchange, Queue
from pika import BasicProperties, BlockingConnection, ConnectionParameters
import uuid
import pika

class RabbitMQPublisher(IMessagePublisher):
    def __init__(self):
        self.connection_params = pika.ConnectionParameters('rabbitmq')
        self.exchange_name = 'lancamentos'
        self.routing_key = 'lancamento_criado'
        self.task_name = 'processar_lancamento'
        
        # Declaração inicial do exchange e queue
        try:
            connection = pika.BlockingConnection(self.connection_params)
            channel = connection.channel()
            channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='topic',
                durable=True
            )
            channel.queue_declare(
                queue=self.routing_key,
                durable=True
            )
            channel.queue_bind(
                exchange=self.exchange_name,
                queue=self.routing_key,
                routing_key=self.routing_key
            )
            connection.close()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"[RabbitMQPublisher] Erro ao conectar ao RabbitMQ: {str(e)}")
        except Exception as e:
            print(f"[RabbitMQPublisher] Erro inesperado: {str(e)}")


    def publish(self, routing_key: str, message: dict) -> bool:
        try:
            connection = pika.BlockingConnection(self.connection_params)
            channel = connection.channel()
            
            task_payload = {
                "id": str(uuid.uuid4()),
                "task": self.task_name,
                "args": [json.dumps(message)],
                "kwargs": {},
                "retries": 0,
                "eta": None
            }

            channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=json.dumps(task_payload),
                properties=BasicProperties(
                    headers={'id': str(uuid.uuid4()), 'task': 'processar_lancamento'},
                    content_type='application/json',
                    delivery_mode=2  # Persistente
                )
            )
            connection.close()
            return True
        
        except Exception as e:
            print(f"Erro detalhado ao publicar: {str(e)}")
            if 'connection' in locals():
                connection.close()
            raise