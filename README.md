# rod-manager
## SETUP 
### Requirements
- Install docker desktop: https://www.docker.com/products/docker-desktop
- Have docker deamon running

### Launch
In the root folder of the project, run:
```shell
docker-compose up -d --build 
```

### Generate new certificates
In the root folder of the project, run:
```shell
docker-compose up -d --build 
```

### KAFKA
Requirements:
- Install kafka: https://kafka.apache.org/quickstart
- Install zookeeper: https://zookeeper.apache.org/doc/r3.6.3/zookeeperStarted.html

```shell
sudo /opt/kafka_2.13-3.6.0/bin/zookeeper-server-start.sh /opt/kafka_2.13-3.6.0/config/zookeeper.properties
sudo /opt/kafka_2.13-3.6.0/bin/kafka-server-start.sh /opt/kafka_2.13-3.6.0/config/server.properties
/opt/kafka_2.13-3.6.0/bin/kafka-topics.sh --create --topic water-meters --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
python -m rodManager.kafka.kafka_consumer
python -m water_meters.meter_raport
```