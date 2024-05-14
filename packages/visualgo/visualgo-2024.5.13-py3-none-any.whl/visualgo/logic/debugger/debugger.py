from abc import ABC, abstractmethod
from typing import TypeVar

from ..controller_callbacks import ControllerCallbacksInterface

T = TypeVar("T")


class AbstractDebugger(ABC):
    """
    Interface for the Debugger class.

    :call: callbacks.on_initialized() once it is fully initialized.
    :call: callbacks.on_interrupted() when it is fully stopped and don't want to receive any more messages.
    """
    @abstractmethod
    def __init__(self, callbacks: ControllerCallbacksInterface) -> None:
        """
        Constructor of the debugger.
        Initializes debugger with the corresponding callbacks

        :param callbacks: ControllerCallbacksInterface
        """
        self.callbacks = callbacks

    @abstractmethod
    def set_code(self, code: str) -> None:
        """
        Set or reset the code to be executed.

        :param code: str
        :return: None
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stops the debugger. This is basically a reset.

        :return: None
        """
        ...

    @abstractmethod
    def add_breakpoints(self, breakpoints: list[[int, str]]) -> None:
        """
        Add a new breakpoint at the given `line_number` with a condition `cond`.
        Or update the condition of the breakpoint at the given `line_number`.

        :param breakpoints: list[[int, str]]
        :return: None
        """
        pass


    @abstractmethod
    def del_breakpoints(self, line_numbers: list[int]) -> None:
        """
        Remove the breakpoint at the given `line_number`.

        :param line_numbers: list[int]
        :return: None
        """
        pass

    @abstractmethod
    def step_into(self) -> None:
        """
        Make a forward 'forward_next' the execution, it will not enter in the function if it is a function call.

        :call: callbacks.execution_paused(context) if it is paused.
        :call: callbacks.execution_done(context) if the code has reached the end.
        :return: None
        """
        pass

    @abstractmethod
    def forward_step(self) -> None:
        """
        Make a forward 'step' in the execution, it will enter in the function if it is a function call.

        :call: callbacks.execution_paused(context) if it is paused.
        :call: callbacks.execution_done(context) if the code has reached the end.
        :return: None
        """
        pass

    @abstractmethod
    def backward_step(self) -> None:
        """
        Make a backward 'step' in the execution, it will exit the function if it was a function call.

        :call: callbacks.execution_paused(context) if it is paused.
        :call: callbacks.execution_done(context) if the code has reached the end.
        :return: None
        """
        pass

    @abstractmethod
    def do_continue(self) -> None:
        """
        Continue the execution until the next breakpoint.

        :call: callbacks.execution_paused(context) if it is paused.
        :call: callbacks.execution_done(context) if the code has reached the end.
        :return: None
        """
        pass
