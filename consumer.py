import pika
import asyncio
import json

async def minha_funcao_assincrona():
    await asyncio.sleep(2) 
    print("Tarefa assíncrona completada",flush=True)


class RabbitmqConsumer:
    def __init__(self, queue_name, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = queue_name
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel
    
    def start(self):
        print(f'Listen RabbitMQ on Port {self.__port}')
        self.__channel.start_consuming()

def minha_callback(ch, method, properties, body):
    print("\n++++++++Receives data from RabbitMQ++++++++")
    # print("Channel: ",ch)
    # print("Method: ",method)
    # print("Properties: ",properties)
    data_str = body.decode('utf-8')
    data_dict = json.loads(data_str)
    print("Body: ",data_dict["value"])
    print("\n++++++++++++++++")
    asyncio.create_task(minha_funcao_assincrona())



async def main():
    rabitmq_consumer = RabbitmqConsumer("fila1",minha_callback)
    rabitmq_consumer.start()

asyncio.run(main())