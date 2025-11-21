from kafka import KafkaProducer


def kafka_python_producer_sync(producer, msg, topic):
    producer.send(topic, bytes(msg, encoding='utf-8'))
    print("Sending " + msg)
    producer.flush(timeout=60)


def success(metadata):
    print(metadata.topic)


def error(exception):
    print(exception)


def kafka_python_producer_async(producer, msg, topic):
    producer.send(topic, bytes(msg, encoding='utf-8')).add_callback(success).add_errback(error)
    producer.flush()


if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers='34.27.168.47:9092')  # use your VM's external IP Here!
    with open('C:\\teaching\\DE2025\\lab9\\data\\wordstream.txt') as f:   # change this path to the path in your laptop
        lines = f.readlines()

    for line in lines:
        kafka_python_producer_sync(producer, line, 'word')

    f.close()
