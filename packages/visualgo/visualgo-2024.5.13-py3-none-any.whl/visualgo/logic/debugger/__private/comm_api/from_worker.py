from abc import ABC, abstractmethod
from typing import Any, Callable


class FromWorker(ABC):
    @abstractmethod
    def send_message(self, mes_id: str, data: Any):
        """
        Send a message to the main program. This will interrupt the main to handle the message as soon as possible
        :param mes_id: The message id
        :param data: The associated data. **HAS TO BE PICKLEABLE**
        :return: None
        """
        ...

    @abstractmethod
    def wait_for_main_messages(self) -> list[(str, Any)]:
        """
        Wait for messages from the main program. There are two possible cases:
        - The main has already sent some messages since last call of this method -> returns immediately with what the
        main has sent.
        - The message queue is empty -> Hangs until the message queue has at least 1 message pending.

        Each call of this method will flush the message queue.
        :return: The content of the message queue if it wasn't
        empty, or hangs until the message queue has at least 1 message pending then returns the queue.
        """
        ...


__to_worker_impl: FromWorker


def set_implementation(impl: FromWorker):
    """
    Sets the current implementation of the communication API for the worker side.
    :param impl: the communication API implementation for the current engine
    :return: None
    """
    global __to_worker_impl
    __to_worker_impl = impl


def get_implementation():
    """
    Gets the current implementation of the communication API
    :return: the current implementation of the communication API
    """
    return __to_worker_impl
