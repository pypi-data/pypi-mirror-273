from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod
from functools import wraps
import asyncio
import time
from typing import Union

from .types import Statistics, SymbolDescription
from .controller_callbacks import ControllerCallbacksInterface

from .debugger.types import DebugContext, DebugVariables
from .debugger.debugger import AbstractDebugger

from .static.types import CodeVariablesAndUserFunctions, StaticSymbolDescription, StaticBasicDescription
from .static.static_analysis import StaticAnalyser

from .ui.types import TransferVariable, TransferVariables
from .ui.ui_callbacks import UICallbacksInterface


@dataclass
class Tracker:
    value: int
    lines: list[int]


class ExecutionState(Enum):
    """
    Enum for the different states of the execution for the Controller.

    :demand: F.2.4
    """
    WAITING_DEBUGGER_INITIALIZATION = 0
    CODE_NOT_INITIALIZED = 1
    RUNNING = 2
    RUNNING_IGNORE_CHECKPOINTS = 3
    PAUSED = 4


class ControllerInterface(ABC):
    """
    Interface for the Controller class.
    """

    # Execution control

    @abstractmethod
    def initialize(self) -> None:
        """
        Initializes the Debugger, the Controller will get the code from the UI callbacks.

        :demand: F.1.6
        :return: None
        """
        pass

    @abstractmethod
    async def step_forward_automatic(self):
        """
        Starts/Resume the execution of the code in automatic mode.

        :demand: F.1.6
        :return: None
        """
        pass

    @abstractmethod
    def pause(self):
        """
        Pauses the execution of the code.

        :demand: F.1.6
        :return: None
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Kills the execution of the code. Basically asks to reset the debugger.

        :demand: ?
        :return:
        """
        pass

    @abstractmethod
    def set_step_time(self, time: int) -> None:
        """
        Sets the time of the step to `time` in milliseconds.

        :param time: int
            The time to set for the step.
        :raises ValueError:
            If the specified time is less than or equal to 0.
        :return: None
        """
        pass

    @abstractmethod
    def forward_step(self) -> None:
        """
        Executes the next line of the code.

        :return: None
        """
        pass

    @abstractmethod
    def do_continue(self) -> None:
        """
        Executes the next line of the code without entering into the user function.

        :return: None
        """
        pass

    @abstractmethod
    def backward_step(self) -> None:
        """
        Executes the previous line of the code.

        :return: None
        """
        pass

    # Checkpoints
    # TODO reflect the change where we transfer a list of checkpoints/breakpoints instead of one at a time
    @abstractmethod
    def new_checkpoint(self, line_number: int, cond: Union[str, None]) -> None:
        """
        Add a new checkpoint at the given `line_number`.

        :param line_number: int
        :param cond: str
        :return: None
        """
        pass

    @abstractmethod
    def del_checkpoint(self, line_number: int) -> None:
        """
        Delete the checkpoint at the given `line_number`.

        :param line_number: int
        :return: None
        """
        pass

    # Breakpoints
    @abstractmethod
    def new_breakpoint(self, line_number: int, cond: Union[str, None]) -> None:
        """
        Add a new breakpoint at the given `line_number`.

        :param line_number: int
        :param cond: str
        :return: None
        """
        pass

    @abstractmethod
    def del_breakpoint(self, line_number: int) -> None:
        """
        Delete the breakpoint at the given `line_number`.

        :param line_number: int
        :return: None
        """
        pass

    @abstractmethod
    def new_tracker(self, line_number: int) -> None:
        """
        Add a new tracker at the given `line_number`.

        :param line_number: int
        :return: None
        """
        pass

    @abstractmethod
    def del_tracker(self, line_number: int) -> None:
        """
        Delete the tracker at the given `line_number`.

        :param line_number: int
        :return: None
        """
        pass

    # Tracking for drawings
    @abstractmethod
    def hide_variable(self, variable: SymbolDescription) -> None:
        """
        Hide the variable from the variables returned to the UI.

        :demand: F.2.7
        :param variable: SymbolDescription
        :return: None
        """
        pass

    @abstractmethod
    def show_variable(self, variable: SymbolDescription) -> None:
        """
        Do not hide the variable from the variables returned to the UI.

        :demand: F.2.7
        :param variable: SymbolDescription
        :return: None
        """
        pass

    @abstractmethod
    def hide_variables_in_user_fun(self, fun: SymbolDescription) -> None:
        """
        Hide all local variables of the user function from the variables returned to the UI.

        :demand: F.2.7
        :param fun: SymbolDescription
        :return: None
        """
        pass

    @abstractmethod
    def show_variables_in_user_fun(self, fun: SymbolDescription) -> None:
        """
        Do not hide all local variables of the user function from the variables returned to the UI.

        :demand: F.2.7
        :param fun: SymbolDescription
        :return: None
        """
        pass

    @abstractmethod
    def get_static_variables_and_user_fun(self) -> CodeVariablesAndUserFunctions:
        """
        Returns the variables defined in the code before the execution.

        :demand: F.2.7
        :return: Variables
        """
        pass

    # Statistics
    @abstractmethod
    def get_csv(self) -> str:
        """
        Returns the evolution of the statistics at the checkpoints/breakpoints in a CSV format.
        Format of the CSV to be determined...

        :return: str
        """
        pass


def needs_initialization(func):
    """
    Decorator to check if the Controller was initialized before calling a method.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._Controller__execution_state == ExecutionState.CODE_NOT_INITIALIZED:
            return None
        return func(self, *args, **kwargs)

    return wrapper


class Controller(ControllerCallbacksInterface, ControllerInterface):
    """
    Controller class that manages the interaction between the UI and the Debugger.
    Implements the ControllerCallbacksInterface to receive notifications from
    the Debugger, and the ControllerInterface to receive calls from the UI.
    """

    def __init__(self, debugger_class: type,
                 ui_callbacks: UICallbacksInterface,
                 max_recursion_depth: int = None) -> None:
        """
        Initializes the Controller with the given a `debugger_class` that will be instantiated and
        a `ui_callbacks` to communicate with the UI. 
        Also can use the `max_recursion_depth` for testing purposes.

        :demand: F.1.5
        :demand: F.2.7
        :demand: F.2.8
        :param debugger_class: type
        :param ui_callbacks: UICallbacksInterface
        :return: None
        """
        # private attributes
        self.__ui_callbacks: UICallbacksInterface = ui_callbacks
        self.__execution_state: ExecutionState = ExecutionState.WAITING_DEBUGGER_INITIALIZATION

        # self.__current_statistics: Statistics = None
        # self.__current_variables: DebugVariables = None
        self.__hidden_vars: list[SymbolDescription] = []
        self.__hidden_fun_vars: list[SymbolDescription] = []
        self.__tracked_funs: list[str] = []
        self.__hidden_types: list[str] = []

        self.__checkpoints: list[int] = []
        self.__breakpoints: list[[int, Union[str, None]]] = []
        self.__trackers: dict[str, Tracker] = {}

        self.__step_time: int = 1000
        self.__debugger: AbstractDebugger = debugger_class(self)
        self.__static_analyser: StaticAnalyser = StaticAnalyser()

        self.__recursion_depth: int = 0
        self.__max_recursion_depth: int = max_recursion_depth
        self.__number_of_loop_forward_step = 0
        self.__number_of_loop_do_continue = 0

        self.__autoplay = False

    # -- Private methods -- #

    def __initialize_debugger(self, code: str) -> None:
        """
        Initializes the debugger with the given `code`.

        :param code: str
        :return: None
        """
        self.__debugger.add_breakpoints(self.__breakpoints)
        self.__debugger.add_breakpoints([(lineno, None) for lineno in self.__checkpoints])
        self.__debugger.set_code(code)
        self.__execution_state = ExecutionState.RUNNING

    def __get_ui_stats(self, stats: Statistics) -> Statistics:
        """
        Returns the statistics of the execution given the debugger `stats`
        and the user parameters `tracked_types` and `tracked_funs`.

        :demand: F.1.5
        :param stats: Statistics
        :param tracked_types: list[SymbolDescription]
        :param tracked_funs: list[SymbolDescription]
        :return: Statistics
        """
        tracked_types = self.__hidden_types
        tracked_funs = self.__tracked_funs
        pass

    def __transform_in_transfer_vars(
            self, vars: DebugVariables, function_name: str, depth: int) -> TransferVariables:
        """
        Returns the variables of the execution given the `frame`.

        :param vars: DebugVariables
        :param function_name: str
        :param depth: int
        :return: TransferVariables
        """
        res = []
        # iterate variable by variable
        for name, value in vars.locals.items():
            desc = SymbolDescription(name, function_name, depth)
            ui_var = TransferVariable(desc, value)
            res.append(ui_var)
        return res

    def __get_ui_vars(
            self, context: DebugContext) -> TransferVariables:
        """
        Returns the variables of the execution given the debugger
        `variables` and the user parameters `tracked_vars`.

        :param context: DebugContext
        :param tracked_vars: typing.List[SymbolDescription]
        :return: TransferVariables
        """
        hidden_vars = self.__hidden_vars
        hidden_fun_vars = self.__hidden_fun_vars
        res = []
        depth = 0
        # iterate frame by frame
        for frame in context[::-1]:  # iterate in reverse order to get the "lowest" frames first
            # TODO: Once merged, function_name will probably be in DebugVariables
            # (and thus accessible from debug_vars)
            res += self.__transform_in_transfer_vars(frame.variables, frame.function_name, depth)
            depth += 1

        if len(hidden_vars) == 0 and len(hidden_fun_vars) == 0:
            return TransferVariables(res)

        hidden = [var.description for var in hidden_vars]
        hidden_fun = [var.description for var in hidden_fun_vars]

        for var in res:
            if var.description in hidden:
                res.remove(var)
            elif var.description.name in hidden_fun.name and var.description.depth in hidden_fun.depth:
                res.remove(var)

        return TransferVariables(res)

    def __update_ui(self, context: DebugContext) -> None:
        """
        Updates the UI with the given `context`.

        :param context: DebugContext
        :return: None
        """
        vars = self.__get_ui_vars(context)
        self.__ui_callbacks.update_variables(vars)

    def __pause_if_max_recursion_reached(self) -> None:
        if self.__max_recursion_depth is not None:
            if self.__recursion_depth >= self.__max_recursion_depth:
                self.__execution_state = ExecutionState.PAUSED

    def __add_recursion_depth(self) -> None:
        self.__recursion_depth += 1
        self.__pause_if_max_recursion_reached()

    # async def __loop_forward_step(self) -> None:
    #     # print("in __loop_forward_step")
    #     self.__number_of_loop_forward_step += 1
    #     if self.__number_of_loop_forward_step != 1:  # protect against multiple different calls
    #         return
    #
    #     # # protect against the debugger not answering in time before __step_time at least
    #     # if self.__execution_state == ExecutionState.RUNNING and self.__no_answer_from_debugger_yet:
    #     #     self.__execution_state = ExecutionState.PAUSED
    #     #     self.__ui_callbacks.show_error("Debugger is not responding, automatic execution paused.")
    #     #     self.__ui_callbacks.execution_paused()
    #     #     return
    #
    #     if self.__execution_state == ExecutionState.RUNNING:
    #         self.__no_answer_from_debugger_yet = True
    #         self.forward_step()
    #         await asyncio.sleep(self.__step_time / 1000)
    #         self.__number_of_loop_forward_step -= 1
    #         self.__add_recursion_depth()
    #         await self.__loop_forward_step()
    #
    # async def __loop_do_continue(self) -> None:
    #     # print("in __loop_do_continue")
    #     self.__number_of_loop_do_continue += 1
    #     if self.__number_of_loop_do_continue != 1:  # protect against multiple different calls
    #         return
    #
    #     # # protect against the debugger not answering in time before __step_time at least
    #     # if self.__execution_state == ExecutionState.RUNNING and self.__no_answer_from_debugger_yet:
    #     #     self.__execution_state = ExecutionState.PAUSED
    #     #     self.__ui_callbacks.show_error("Debugger is not responding, automatic execution paused.")
    #     #     self.__ui_callbacks.execution_paused()
    #     #     return
    #
    #     if self.__execution_state == ExecutionState.RUNNING:
    #         self.__no_answer_from_debugger_yet = True
    #         self.__debugger.do_continue()
    #         await asyncio.sleep(self.__step_time / 1000)
    #         self.__number_of_loop_do_continue -= 1
    #         self.__add_recursion_depth()
    #         await self.__loop_do_continue()
    #
    #         # -- ControllerCallbacksInterface -- #

    async def __call_debugger_later(self):
        await asyncio.sleep(self.__step_time / 1000)
        if self.__execution_state != ExecutionState.RUNNING:
            return
        if len(self.__checkpoints) == 0 and len(self.__breakpoints) == 0:
            self.forward_step()
        else:
            self.__debugger.do_continue()

    def __update_trackers(self, line_number: int) -> bool:
        for key, tracker in self.__trackers.items():
            if line_number in tracker.lines:
                # print(f"Tracker {key} at line {line_number}, new value: {tracker.value + 1}")
                self.__trackers[key].value += 1
                return True
        return False

    def __update_full_ui(self, current_line_number: int, contexts: list[DebugContext]) -> None:
        self.__ui_callbacks.set_current_line(current_line_number)

        # At every execution stop we update the UI
        self.__update_ui(contexts)
        if self.__execution_state != ExecutionState.RUNNING:
            self.__ui_callbacks.execution_paused()

    def execution_paused(self, context: DebugContext) -> None:
        """
        Update the visualisation once the debugger has finished executing some part of a code
        and is awaiting further instructions.
        Occurs on steps, next and continues.
        TODO: Update statistics here.

        :param context: DebugContext
        :return: None
        """
        # print("in controller execution_paused, line:", context[0].lineno)

        line_number = context[0].lineno
        for lineno, _ in self.__breakpoints:
            if line_number == lineno:
                self.pause()
                self.__update_full_ui(line_number, context)
                self.__update_trackers(line_number)  # Update tracker on the same line
                return
        if self.__execution_state == ExecutionState.RUNNING_IGNORE_CHECKPOINTS:
            for lineno in self.__checkpoints:
                if line_number == lineno:
                    self.__update_trackers(line_number)  # Update tracker on the same line
                    self.do_continue()
                    return
        if self.__update_trackers(line_number):  # No breakpoint here, but we still check if there's a tracker
            if self.__execution_state == ExecutionState.RUNNING_IGNORE_CHECKPOINTS:
                self.do_continue()
                return
            if self.__autoplay:
                if len(self.__checkpoints) == 0 and len(self.__breakpoints) == 0:
                    self.forward_step()
                else:
                    self.__debugger.do_continue()
                return
        # print("No trackers nor breakpoints nor ignored checkpoints found")
        self.__update_full_ui(line_number, context)
        if self.__autoplay:
            asyncio.create_task(self.__call_debugger_later())

    def execution_done(self, context: DebugContext) -> None:
        # print("in execution_done")
        line_number = context[0].lineno
        self.__update_ui(context)
        self.__ui_callbacks.set_current_line(line_number)  # Could be 0 too
        self.__ui_callbacks.code_is_over()
        self.__execution_state = ExecutionState.CODE_NOT_INITIALIZED
        self.__autoplay = False

    def on_error(self, error: str) -> None:
        self.__execution_state = ExecutionState.WAITING_DEBUGGER_INITIALIZATION
        self.__ui_callbacks.show_error(error)

    def on_message(self, message: str) -> None:
        self.__ui_callbacks.show_message(message)

    def on_initialized(self) -> None:
        self.__execution_state = ExecutionState.CODE_NOT_INITIALIZED
        self.__ui_callbacks.debugger_ready()

    def on_interrupted(self) -> None:
        self.__execution_state = ExecutionState.WAITING_DEBUGGER_INITIALIZATION
        self.__number_of_loop_forward_step = 0
        self.__number_of_loop_do_continue = 0
        self.__ui_callbacks.debugger_interrupted()

    # -- ControllerInterface -- #

    def initialize(self) -> None:
        # print("initialize")
        if self.__execution_state == ExecutionState.CODE_NOT_INITIALIZED:
            code = self.__ui_callbacks.get_code()
            self.__initialize_debugger(code)
            self.__reset_trackers()
            self.__execution_state = ExecutionState.PAUSED
        # else:
            # print("Did nothing in initialize")

    async def step_forward_automatic(self) -> None:
        # print("step_forward_automatic")
        if self.__execution_state == ExecutionState.PAUSED:

            self.__recursion_depth = 0
            self.__execution_state = ExecutionState.RUNNING
            self.__autoplay = True

            if len(self.__checkpoints) == 0 and len(self.__breakpoints) == 0:
                # considere that there are 1 checkpoint per line
                self.forward_step()
            else:
                # take into account the user checkpoints and breakpoints
                self.__debugger.do_continue()

        else:
            # print("did nothing in step_forward_automatic")
            self.__ui_callbacks.code_is_over()

    def pause(self) -> None:
        if self.__execution_state == ExecutionState.RUNNING or self.__execution_state == ExecutionState.RUNNING_IGNORE_CHECKPOINTS:
            self.__autoplay = False
            self.__execution_state = ExecutionState.PAUSED
            self.__number_of_loop_forward_step = 0
            self.__number_of_loop_do_continue = 0

    @needs_initialization
    def stop(self) -> None:
        """
        Stops the execution of the code. Basically resets the debugger

        :demand: ?
        :return:
        """
        self.__autoplay = False
        self.__debugger.stop()
        self.__execution_state = ExecutionState.WAITING_DEBUGGER_INITIALIZATION

    def set_step_time(self, time: int) -> None:
        if time <= 0:
            self.__ui_callbacks.show_error("Time must be greater than 0")
        else:
            self.__step_time = time

    @needs_initialization
    def forward_step(self) -> None:
        self.__ui_callbacks.set_running_code()
        self.__debugger.forward_step()

    @needs_initialization
    def do_continue(self) -> None:
        self.__recursion_depth = 0
        self.__execution_state = ExecutionState.RUNNING_IGNORE_CHECKPOINTS
        # for _checkpoint in self.__checkpoints:
        #     # print("Controller: removing checkpoint at line", _checkpoint)
        #     self.__debugger.del_breakpoints(_checkpoint)
        # print("controller calling do_continue")
        self.__ui_callbacks.set_running_code()
        self.__debugger.do_continue()
        # print("controller called do_continue()")

    @needs_initialization
    def backward_step(self) -> None:
        self.__debugger.backward_step()

    # Checkpoints
    def new_checkpoint(self, line_number: int, cond: Union[str, None] = None) -> None:
        # TODO change how the condition is passed
        self.__debugger.add_breakpoints([(line_number, None)])
        self.__checkpoints.append(line_number)

    def del_checkpoint(self, line_number: int) -> None:
        # print("Controller: del checkpoint at line", line_number)
        self.__debugger.del_breakpoints([line_number])
        self.__checkpoints.remove(line_number)
        # print("Controller: delleted checkpoint at line", line_number)

    # Breakpoints
    def new_breakpoint(self, line_number: int, cond: Union[str, None] = None) -> None:
        # TODO change how the condition is passed
        # print("Controller: new breakpoint at line", line_number)
        self.__debugger.add_breakpoints([(line_number, cond)])
        self.__breakpoints.append((line_number, cond))
        # print("Controller: breakpoint added at line", line_number)

    def del_breakpoint(self, line_number: int) -> None:
        self.__debugger.del_breakpoints([line_number])
        self.__breakpoints = list(filter(lambda bp: bp[0] != line_number, self.__breakpoints))

    # Trackers
    def __reset_trackers(self) -> None:
        for key in self.__trackers.keys():
            self.__trackers[key].value = 0

    def new_tracker(self, name: str, line_number: int) -> None:
        self.__debugger.add_breakpoints([(line_number, None)])
        if name in self.__trackers:
            self.__trackers[name].lines.append(line_number)
        else:
            self.__trackers[name] = Tracker(0, [line_number])

    def del_tracker(self, name: str, line_number: int) -> None:
        self.__debugger.del_breakpoints(line_number)
        if name in self.__trackers.keys():
            self.__trackers[name].lines.remove(line_number)
            if len(self.__trackers[name].lines) == 0:
                del self.__trackers[name]

    # Tracking for drawings
    def hide_variable(self, variable: SymbolDescription) -> None:
        if variable not in self.__hidden_vars:
            self.__hidden_vars.append(variable)

    def show_variable(self, variable: SymbolDescription) -> None:
        if variable in self.__hidden_vars:
            self.__hidden_vars.remove(variable)

    def hide_variables_in_user_fun(self, fun: SymbolDescription) -> None:
        if fun not in self.__hidden_fun_vars:
            self.__hidden_fun_vars.append(fun)

    def show_variables_in_user_fun(self, fun: SymbolDescription) -> None:
        if fun in self.__hidden_fun_vars:
            self.__hidden_fun_vars.remove(fun)

    def get_static_variables_and_user_fun(self) -> None:
        code_vars_and_user_fun = self.__static_analyser.get_code_variables_and_user_functions(
            self.__ui_callbacks.get_code())
        new_vars = []
        for var in code_vars_and_user_fun.variables:
            var_state = True
            if var.description in self.__hidden_vars:
                var_state = False
            new_vars.append(StaticSymbolDescription(var.description, var_state))

        new_funcs = []
        for fun in code_vars_and_user_fun.user_functions:
            # print("fun:", fun, self.__hidden_fun_vars)
            fun_state = True
            if fun.description in self.__hidden_fun_vars:
                fun_state = False
            new_funcs.append(StaticSymbolDescription(fun.description, fun_state))

        self.__ui_callbacks.set_static_variables_and_user_fun(CodeVariablesAndUserFunctions(new_vars, new_funcs))

    # Statistics
    def get_csv(self) -> str:
        return self.__trackers

    # -- Other public methods -- #

    @property
    def recursion_depth(self) -> int:
        return self.__recursion_depth
