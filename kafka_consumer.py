from kafka import KafkaConsumer

# Initialize the consumer
consumer = KafkaConsumer(
    'test-topic',  # Topic to subscribe to
    bootstrap_servers='localhost:9092',  # Kafka broker address
    auto_offset_reset='earliest',  # Read from the beginning if no offset is set
    group_id='my-python-group',  # Consumer group ID
    value_deserializer=lambda v: v.decode('utf-8')  # Deserialize bytes to string
)

# Read messages from the topic
print("Listening for messages...")
for message in consumer:
    print(f"Received: {message.value}")
