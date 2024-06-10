import json
import logging

from confluent_kafka import Consumer, KafkaError
import asyncio
import websockets


class KafkaConnectorConsumer:
    def __init__(self, server: str, group_id: str) -> None:
        con_config = {
            "bootstrap.servers": server,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }

        self.consumer = Consumer(con_config)
            

    async def consume_messages(self):
        self.consumer.subscribe(["water-meters"])
        logging.info("Subscribed to topic")
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logging.error(f"Reached end of partition {msg.topic()} [{msg.partition()}]")
                else:
                    # Error
                    logging.error(f"Error occurred: {msg.error().str()}")
            received_data = json.loads(msg.value().decode("utf-8"))
            logging.info(f"Received: {received_data}")


    def close_consumer(self):
        self.consumer.close()

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.consume_messages())


# run kafka consumer
bootstrap_servers = 'localhost:9092'
group_id = 'rod-meters'
consumer = KafkaConnectorConsumer(bootstrap_servers, group_id)
consumer.run()
