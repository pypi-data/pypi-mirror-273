import os
import signal
from typing import Any, Callable

from ..comm_api.to_worker import ToWorker
from .python_process_from_worker import PythonProcessFromWorker
from multiprocessing import Process, Queue, Pipe


def _wrapper_task(task, shared_queue: Queue, send_conn, parent_pid):
    from ..comm_api.from_worker import set_implementation
    impl = PythonProcessFromWorker(shared_queue, send_conn, parent_pid)
    set_implementation(impl)
    impl.send_message("INITIALIZED", None)
    task()


def signal_handler(message_handler, recv_conn, sig, frame):
    mes_id, mes_data = recv_conn.recv()
    message_handler(mes_id, mes_data)


class PythonProcessToWorker(ToWorker):
    """
    An implementation of the communication API for the CPython engine for the main side.
    This will start the worker in another process and use a shared Queue to communicate with it and a simplex Pipe for
    the worker to send messages to us.

    This implementation uses the signal `SIGUSR1` so the worker can interrupt us whenever it needs to send us a message.
    """
    def __init__(self, task: Callable[[], None], message_handler: Callable[[str, Any], None]):
        self.message_value: [str, Any] = None
        self.task: Callable[[], None] = task
        self.worker_message_queue = Queue()
        self.recv_conn, send_conn = Pipe(False)  # no duplex
        self.worker_process = Process(target=_wrapper_task,
                                      args=(task, self.worker_message_queue, send_conn, os.getpid()))
        self.message_handler: Callable[[str, Any], None] = message_handler
        signal.signal(signal.SIGUSR1,
                      lambda sig, frame: signal_handler(self.message_handler, self.recv_conn, sig, frame))

    def set_message_handler(self, message_handler: Callable[[str, Any], None]):
        self.message_handler = message_handler

    def send_message(self, mes_id: str, mes_data: Any):
        self.worker_message_queue.put((mes_id, mes_data))

    def start_worker(self):
        self.worker_process.start()

    def interrupt_worker(self):
        self.worker_process.terminate()
