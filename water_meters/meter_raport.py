import json
import logging
import time
import random
from confluent_kafka import Producer

"""Example program to simulate water meters and send their data to a Kafka topic."""

class KafkaConnectorProducer:
    def __init__(self, server: str) -> None:
        prod_config = {"bootstrap.servers": server}
        self.producer = Producer(prod_config)

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            logging.error(f"Message delivery failed: {err}")
        else:
            logging.debug(
                f"Message delivered to {msg.topic()} [{msg.partition()}] at time {time.time()}"
            )

    def send_one(self, data, key: int):
        # Trigger any available delivery report callbacks from previous produce() calls
        self.producer.poll(0)

        # Asynchronously produce a message. The delivery report callback will
        # be triggered from the call to poll() above, or flush() below, when the
        # message has been successfully delivered or failed permanently.
        self.producer.produce(
            "water-meters",
            data,
            callback=self.delivery_report,
            key=str(key),
        )

    def flush(self):
        self.producer.flush()


class Meter:
    def __init__(self, meter_id: int, connector: KafkaConnectorProducer) -> None:
        self.meter_id = meter_id
        self.connector = connector
        self.meter_state = (random.randint(10, 1000) / 10)

        # Send meter info
        self.send_meter_info()

    def get_current_state(self):
        # Return meter info
        return {"meter_id": self.meter_id, "meter_state": self.meter_state, "timestamp": time.time()}
    
    def simulate_meter_increase(self):
        # Increase meter state
        self.meter_state += random.randint(1, 10) / 10

    def send_meter_info(self):
        logging.info(f"Beginning work as meter {self.meter_id}")

        for _ in range(10):
            connector.send_one(json.dumps(self.get_current_state()), self.meter_id)
            self.simulate_meter_increase()
            time.sleep(1)

# Run main meter code
bootstrap_servers = 'localhost:9092'
connector = KafkaConnectorProducer(bootstrap_servers)
meter_id = random.randint(1, 100)
meter = Meter(meter_id, connector)
