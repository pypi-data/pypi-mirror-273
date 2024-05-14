from abc import ABC, abstractmethod

from .debugger.types import DebugContext

class ControllerCallbacksInterface(ABC):
    """
    Interface so that the debugger can call when it has finished an action asked by the controller.
    """

    @abstractmethod
    def execution_paused(self, frames: DebugContext) -> None:
        """
        Update the visualisation once the debugger has finished executing code and is awaiting
        further instructions. Occurs on steps, next and continues.
        :param context:
        :return:
        """
        ...

    @abstractmethod
    def execution_done(self, frames: DebugContext) -> None:
        """
        Update the visualisation once the end of the code has been reached in the debugger.

        :param context: DebugContext
        :return: None
        """
        pass

    @abstractmethod
    def on_error(self, error: str) -> None:
        """
        Show an error in the visualisation when the debugged code throws an un-caught exception

        :param error: str
        :return: None
        """
        pass

    @abstractmethod
    def on_message(self, message: str) -> None:
        """
        Show a message in the visualisation when one is printed in the client code by the debugger.

        :param message: str
        :return: None
        """
        pass

    @abstractmethod
    def on_initialized(self) -> None:
        """
        Tell the controller that the debugger has been initialized and is ready to receive the code.

        :param message: str
        :return: None
        """
        pass

    @abstractmethod
    def on_interrupted(self) -> None:
        """
        Tell the controller that the debugger has been interrupted and is no longer running.
        It needs to be re-initialized before it can be used again.

        :return: None
        """
        pass