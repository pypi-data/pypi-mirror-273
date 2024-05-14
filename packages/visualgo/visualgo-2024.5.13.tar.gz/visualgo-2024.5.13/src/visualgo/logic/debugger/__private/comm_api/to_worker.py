from abc import ABC, abstractmethod
from typing import Callable, Any


class ToWorker(ABC):

    @abstractmethod
    def set_message_handler(self, message_handler: Callable[[str, Any], None]):
        """
        Sets the message handler that will be called whenever the worker sends us a message.
        :param message_handler: method to be called whenever the worker sends us a message.
        :return: None
        """
        ...

    @abstractmethod
    def send_message(self, mes_id: str, mes_data: Any):
        """
        Puts the message into the message queue.
        :param mes_id: The message id
        :param mes_data: The message data. **HAS TO BE PICKLEABLE**
        :return: None
        """
        ...

    @abstractmethod
    def start_worker(self):
        """
        Starts the worker.
        :return: None
        """
        ...

    @abstractmethod
    def interrupt_worker(self):
        """
        Interrupts the worker immediately.
        :return: None
        """
        ...


__to_worker_impl: ToWorker


def set_implementation(impl: ToWorker):
    """
    Sets the implementation of the communication API for the main side.
    :param impl: the implementation of the communication API
    :return: None
    """
    global __to_worker_impl
    __to_worker_impl = impl


def get_implementation():
    """
    Returns the implementation of the communication API for the main side.
    :return: the implementation of the communication API
    """
    return __to_worker_impl
