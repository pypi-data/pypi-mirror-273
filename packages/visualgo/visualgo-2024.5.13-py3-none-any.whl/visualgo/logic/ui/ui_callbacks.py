from abc import ABC, abstractmethod

from .types import TransferVariables
from ..types import Statistics

from ..static.types import CodeVariablesAndUserFunctions

class UICallbacksInterface(ABC):
    """
    Interface for the UI Callbacks in order to communicate with the UI.

    :demand: F.1.7
    """

    @abstractmethod
    def set_current_line(self, line: int) -> None:
        """
        Update the UI to show that the last executed line is `line`.

        :param variables: TransferVariables
        :return: None
        """
        pass

    @abstractmethod
    def update_variables(self, variables: TransferVariables) -> None:
        """
        Updates the variables in the UI with the given `variables`.

        :param variables: TransferVariables
        :return: None
        """
        pass

    @abstractmethod
    def update_statistics(self, statistics: Statistics) -> None:
        """
        Updates the statistics in the UI with the given `statistics`.

        :demand: F.1.5
        :param statistics: Statistics
        :return: None
        """
        pass

    @abstractmethod
    def execution_paused(self) -> None:
        """
        Tells the UI that the execution has been paused and all interaction should be enabled.

        :return: None
        """
        pass


    @abstractmethod
    def show_error(self, error: str) -> None:
        """
        Shows the error in the UI with the given `error`.

        :param error: str
        :return: None
        """
        pass

    @abstractmethod
    def show_message(self, message: str) -> None:
        """
        Shows the message in the UI with the given `message`.

        :param error: str
        :return: None
        """
        pass

    @abstractmethod
    def get_code(self) -> str:
        """
        Returns the user code from the UI.

        :return: str
        """
        pass

    @abstractmethod
    def debugger_ready(self) -> None:
        """
        Tells the UI that the controller is ready to receive the code.

        :return: None
        """
        pass

    @abstractmethod
    def debugger_interrupted(self) -> None:
        """
        Tells the UI that the controller has been interrupted and all interaction should be disabled.
        The UI should assume that this is the first state when instantiating the controller.

        :return: None
        """
        pass

    @abstractmethod
    def set_static_variables_and_user_fun(self, variables: CodeVariablesAndUserFunctions) -> None:
        """
        Sets the static variables in the UI with the given `variables`.

        :param variables: TransferVariables
        :return: None
        """
        pass

    @abstractmethod
    def set_csv(self, csv: str) -> None:
        """
        Used to return the values of statistics at the checkpoints and breakpoints in a csv format.

        :param csv: str
        :return: None
        """
        pass

    @abstractmethod
    def code_is_over(self) -> None:
        """
        Tell to know when the code has reach the end of execution and can no longer go forward again.

        :return: None
        """
        pass

    @abstractmethod
    def set_running_code(self) -> None:
        """
        Tell the UI that code is being run

        :return: None
        """
        ...