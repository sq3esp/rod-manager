# Start zookeeper and kafka server in separate terminal windows

gnome-terminal -e "sudo /opt/kafka_2.13-3.6.0/bin/zookeeper-server-start.sh /opt/kafka_2.13-3.6.0/config/zookeeper.properties"
gnome-terminal -e "sudo /opt/kafka_2.13-3.6.0/bin/kafka-server-start.sh /opt/kafka_2.13-3.6.0/config/server.properties"

gnome-terminal -e "/opt/kafka_2.13-3.6.0/bin/kafka-topics.sh --create --topic water-meters --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1"