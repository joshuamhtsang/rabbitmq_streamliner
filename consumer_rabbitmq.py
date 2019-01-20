#!/usr/bin/env python3

import pika
import json


class Consumer:
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.exchange = config['exchange']
        self.queue = config['queue']
        self.routing_key = config["routing_key"]
        if "virtual_host" in config.keys():
            self.virtual_host = config["virtual_host"]
        else:
            self.virtual_host = "/"

    def consume(self, callback):
        connection = None
        try:
            connection = self._create_connection()
            channel = connection.channel()
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                callback,
                queue=self.queue
            )
            print('Waiting for messages. To exit press CTRL+C.')
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
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
            credentials=credentials,
            virtual_host=self.virtual_host
        )
        return pika.BlockingConnection(parameters)

    def callback(self, channel, method, properties, body):
        # Parse the message body to a Python dict.
        if isinstance(body, bytes):
            body = str(body.decode("UTF-8"))
        try:
            request = json.loads(body)
        except:
            pass

        self._do_something(request)

        return True

    def _do_something(self, request):
        return True


if __name__ == "__main__":
    # Set up the consumer
    import config_rabbitmq

    consumer = Consumer(config_rabbitmq.request)
    consumer.consume(callback=consumer.callback)
