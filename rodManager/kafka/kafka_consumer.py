import json
import logging

from confluent_kafka import Consumer, KafkaError
import asyncio
import websockets

from rodManager.kafka.AESCipher import AESCipher
from rodManager.kafka.aes_config import AES_KEY

class KafkaConnectorConsumer:
    def __init__(self, server: str, group_id: str) -> None:
        con_config = {
            "bootstrap.servers": server,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "broker.address.family": "v4",
        }

        self.consumer = Consumer(con_config)
        self.cipher = AESCipher(AES_KEY)


    async def consume_messages(self):
        self.consumer.subscribe(["water-meters"])
        logging.info("Subscribed to topic")
        while True:
            msg = self.consumer.poll(0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logging.error(f"Reached end of partition {msg.topic()} [{msg.partition()}]")
                else:
                    # Error
                    logging.error(f"Error occurred: {msg.error().str()}")
            try:
                decrypted = self.cipher.decrypt(msg.value().decode("utf-8"))
                new_decrypted = str(rf"{decrypted}")

                end_of_json = new_decrypted.rfind("}")

                if end_of_json != -1:
                    new_decrypted = new_decrypted[: end_of_json + 1]

                msg_value_dict = json.loads(new_decrypted)
                logging.info(f"Received: {msg_value_dict}")
            except json.decoder.JSONDecodeError:
                logging.error("Failed to decode valid json message")

    def close_consumer(self):
        self.consumer.close()

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.consume_messages())


# run kafka consumer
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bootstrap_servers = 'localhost:9092'
    group_id = 'rod-meters'
    consumer = KafkaConnectorConsumer(bootstrap_servers, group_id)
    consumer.run()
