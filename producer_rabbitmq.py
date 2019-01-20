import pika
import json


class Publisher:
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.delivery_mode = config['delivery_mode']
        self.exchange = config['exchange']
        self.routing_key = config['routing_key']

    def publish(self, message):
        connection = None
        try:
            connection = self._create_connection()
            channel = connection.channel()
            channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=self.delivery_mode)
            )
            print("Message published to routing_key: ", self.routing_key)
        except Exception as e:
            print(repr(e))
            raise e
        finally:
            if connection:
                connection.close()

    def _create_connection(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials
        )
        return pika.BlockingConnection(parameters)

