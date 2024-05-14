import os
from queue import Empty
import signal
from multiprocessing import Queue
from typing import Any

from ..comm_api.from_worker import FromWorker


class PythonProcessFromWorker(FromWorker):
    """
    An implementation of the communication for the CPython engine for the worker side.

    This uses a shared queue to get the messages from the main and a pipe end we can only send message into
    to communicate with the main.

    **Except some very specific use cases, this class should not be used directly as it is instantiated by the
    PythonProcessToWorker class!**
    """

    def __init__(self, queue: Queue, send_conn, parent_pid):
        self.queue = queue
        self.send_conn = send_conn
        self.parent_pid = parent_pid

    def send_message(self, mes_id: str, data: Any):
        self.send_conn.send((mes_id, data))
        os.kill(self.parent_pid, signal.SIGUSR1)

    def wait_for_main_messages(self) -> (str, Any):
        res = []
        has_at_least_one = False
        while True:
            try:
                res.append(self.queue.get_nowait())
                has_at_least_one = True
            except Empty:
                if has_at_least_one:
                    return res
                else:
                    return [self.queue.get()]