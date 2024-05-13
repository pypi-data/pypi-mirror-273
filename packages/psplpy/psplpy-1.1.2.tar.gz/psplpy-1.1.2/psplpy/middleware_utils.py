import threading
from typing import Any, Callable
import pika
from serialization_utils import Serializer


class Rabbitmq:
    HOST = 'localhost'
    PORT = 5672
    JSON = 'j'
    PICKLE = 'p'

    def __init__(self, host: str = None, port: int = None, serializer: str = JSON, compress: bool = False):
        self.host = host or self.HOST
        self.port = port or self.PORT
        self.serializer = serializer
        self.compress = compress

        self._serializer = Serializer()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port))
        self.channel = self.connection.channel()

        self._stop_consuming = False
        self._suppress_error = False

    def _serialize(self, data: Any) -> bytes:
        if self.serializer == self.PICKLE:
            return self.PICKLE.encode() + self._serializer.dump_pickle(data, compress=self.compress)
        elif self.serializer == self.JSON:
            return self.JSON.encode() + self._serializer.dump_json(data, compress=self.compress)
        else:
            raise ValueError(f'Unsupported serializer: {self.serializer}')

    def _deserialize(self, data: bytes) -> Any:
        serializer = chr(data[0])
        data = data[1:]
        if serializer == self.JSON:
            return self._serializer.load_json(data, decompress=self.compress)
        elif serializer == self.PICKLE:
            return self._serializer.load_pickle(data, decompress=self.compress)
        else:
            raise ValueError(f'Unsupported serializer: {self.serializer}')

    @staticmethod
    def _default_callback(ch, method, properties, body) -> None:
        print(body)

    def _callback(self, ch, method, properties, body) -> None:
        body = self._deserialize(body)
        self.callback(ch, method, properties, body)
        if self._stop_consuming:
            ch.stop_consuming()

    def send_init(self, exchange: str, routing_keys: list[str]) -> None:
        self.exchange = exchange
        self.routing_keys = routing_keys
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

    def recv_init(self, exchange: str, binding_keys: list[str], callback: Callable = None) -> None:
        self.send_init(exchange, routing_keys=binding_keys)
        self.callback = callback or self._default_callback
        queue = self.channel.queue_declare('', exclusive=True)
        self.queue_name = queue.method.queue
        for routing_key in self.routing_keys:
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=routing_key)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self._callback, auto_ack=True)

    def basic_publish(self, body: Any) -> None:
        for routing_key in self.routing_keys:
            self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=self._serialize(body))

    def _start_consuming(self) -> None:
        try:
            self.channel.start_consuming()
        except Exception as e:
            if not self._suppress_error:
                raise e

    def start_consuming(self) -> threading.Thread:
        t = threading.Thread(target=self._start_consuming)
        t.start()
        return t

    def stop_consuming(self):
        self._stop_consuming = True

    def close(self, suppress_error: bool = False) -> None:
        self._suppress_error = suppress_error
        try:
            self.connection.close()
        except Exception as e:
            if not self._suppress_error:
                raise e
