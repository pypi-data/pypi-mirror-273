from typing import TypeVar
import sys

from ..controller_callbacks import ControllerCallbacksInterface
from .__private.comm_api import to_worker
from .debugger import AbstractDebugger

T = TypeVar("T")


class PyDebugger(AbstractDebugger):
    """
    Python language support of the AbstractDebugger.
    """

    def __init__(self, callbacks: ControllerCallbacksInterface) -> None:
        super().__init__(callbacks)
        to_worker.get_implementation().set_message_handler(self.dispatch_calls)
        # print("PyDebugger created")

    def dispatch_calls(self, mes_id: str, mes_data):
        if mes_id == "EXEC_PAUSED":
            # TODO Temporary solution to make it work
            self.callbacks.execution_paused(mes_data)
        elif mes_id == "EXEC_DONE":
            self.callbacks.execution_done(mes_data)
        elif mes_id == "EXEC_THROWED":
            self.callbacks.on_error(mes_data[0])
        elif mes_id == "INTERRUPTED":
            self.callbacks.on_interrupted()
        elif mes_id == "INITIALIZED":
            self.callbacks.on_initialized()
        else:
            print(f"Unexpected message: {mes_id}", file=sys.stderr)

    def stop(self) -> None:
        # print("worker interrupted", file=sys.stderr)
        to_worker.get_implementation().interrupt_worker()  # TODO: A voir

    def set_code(self, code: str) -> None:
        # print("Received code in PyDebugger" + code)
        to_worker.get_implementation().send_message("SET_CODE", code)

    def add_breakpoints(self, breakpoints: list[[int, str]]) -> None:
        to_worker.get_implementation().send_message("ADD_BP", breakpoints)

    def del_breakpoints(self, line_numbers: list[int]) -> None:
        to_worker.get_implementation().send_message("DEL_BP", line_numbers)

    def backward_step(self) -> None:
        to_worker.get_implementation().send_message("BW_S", None)

    def forward_step(self) -> None:
        to_worker.get_implementation().send_message("FW_S", None)
    
    def step_into(self) -> None:
        to_worker.get_implementation().send_message("FW_N", None)

    def do_continue(self) -> None:
        to_worker.get_implementation().send_message("CONT", None)

