from time import time
from typing import Union
from config import ZMQ_SERVER
import zmq

class ZMQBase:
    def __init__(self, socket_type):
        self._context = zmq.Context()
        self._socket = self._context.socket(socket_type)
        self._timeout = 30.0
        #self._address = "tcp://10.133.29.226:5556"
        self._address = ZMQ_SERVER

    def _check_recieved(self):
        try:
            msg = self._socket.recv_pyobj()
            return msg
        except zmq.ZMQError:
            return None

    def _send(self, message) -> None:
        sent = False
        t0 = time()
        while not sent:
            try:
                self._socket.send_pyobj(message)
                sent = True
            except zmq.ZMQError as e:
                if time() > t0 + self._timeout:
                    raise TimeoutError(
                        "Sending %s on %s timedout" % (message, self._address)
                    )
        return

    def close(self):
        """Disconnect the link to the socket."""
        if self._socket.closed:
            return
        self._socket.close()
        self._context.destroy()

    def __del__(self):
        self.close()


class ZMQClient(ZMQBase):
    def __init__(self):
        super().__init__(zmq.REQ)
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.connect(self._address)

    def _await_results(self):
        result = None
        while result is None:
            result = self._check_recieved()
        return result
