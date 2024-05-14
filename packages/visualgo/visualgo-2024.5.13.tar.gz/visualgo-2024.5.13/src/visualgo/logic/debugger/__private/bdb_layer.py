import bdb
import linecache
import re
import sys
from pkgutil import iter_modules
from sys import stderr
from types import FrameType
from typing import Any

from ..types import DebugContext
from .comm_api import from_worker

_FILE_NAME = "__visualgo_code.py"

_MESSAGE_QUEUE = []
# All those regexes are not an exact match, but it's enough to know if it should be "skipped"
_ANNOTATION_REGEX = re.compile(r"@[a-zA-Z_0-9]*")
_FUNCTION_DEFINITION_REGEX = re.compile(r"def [a-zA-Z_0-9]*\(.*\):")
_IMPORT_NAME_REGEX = re.compile(r"import [a-zA-Z_0-9.]+")
_IMPORT_FROM_REGEX = re.compile(r"from [a-zA-Z_0-9.]+ import [a-zA-Z_0-9*]+")


def _append_to_message_queue(lst: list):
    global _MESSAGE_QUEUE
    _MESSAGE_QUEUE += lst


def _is_message_queue_empty() -> bool:
    return len(_MESSAGE_QUEUE) == 0


def _pop_first_message():
    global _MESSAGE_QUEUE
    return _MESSAGE_QUEUE.pop(0)


def _run_bdb_task():
    from_worker.get_implementation().send_message("INITIALIZED", None)
    # print("BDB initialized, waiting for SET_CODE message")
    code = ""
    dbg = BdbLayer()
    while True:
        breakpoints = []
        # print("debugger has been reset")
        dbg.reset()
        dbg.reset_internal()
        while True:
            mes_queue = from_worker.get_implementation().wait_for_main_messages()
            _append_to_message_queue(mes_queue)
            contains_code = False
            while not _is_message_queue_empty():  # This time, just consume all the message queue...
                # print(_MESSAGE_QUEUE)
                mes_id, mes_data = _pop_first_message()
                if mes_id == "SET_CODE":
                    contains_code = True
                    code = mes_data + "\npass"
                if mes_id == "ADD_BP":
                    for lineno_and_cond in mes_data:
                        breakpoints.append(lineno_and_cond)
                if mes_id == "DEL_BP":
                    # print("deleting breakpoints")
                    # print("before :", breakpoints)
                    breakpoints = list(filter(lambda bp: bp[0] not in mes_data, breakpoints))
                    # print("after :", breakpoints)
                if mes_id == "CONT":
                    # _append_to_message_queue([(mes_id, mes_data)])
                    dbg.set_continue()
                    break
            if contains_code:
                break
        CANONIC_FILE_NAME = dbg.canonic(_FILE_NAME)
        with open(CANONIC_FILE_NAME, "w") as f:
            f.write(code)
            f.flush()
            try:
                cmd = compile(code, CANONIC_FILE_NAME, "exec")
                dbg.set_source(code)
                # print("bdb_layer: set code")
                dbg.set_break(CANONIC_FILE_NAME, len(dbg.lines))
                # print(breakpoints)
                dbg.do_add_breakpoints(breakpoints)
                # print("bdb_layer: running code")
                dbg.run(cmd)
                # print("bdb_layer: Code ran")
            except SyntaxError as e:
                print("Invalid code.")


def _should_skip_frame(frame: FrameType):
    globs = frame.f_globals if frame else None
    cur_line = linecache.getline(_FILE_NAME, frame.f_lineno, globs).strip()
    if (_ANNOTATION_REGEX.fullmatch(cur_line)
            or _FUNCTION_DEFINITION_REGEX.fullmatch(cur_line)
            or _IMPORT_NAME_REGEX.fullmatch(cur_line)
            or _IMPORT_FROM_REGEX.fullmatch(cur_line)):
        return True
    return False


class BdbLayer(bdb.Bdb):
    def __init__(self, skip=None):
        # super().__init__(["visualgo.*", "importlib", "importlib.*", "zipimport", "typing"])
        self.continue_state = False
        modules_to_skip = {x.name for x in iter_modules()}
        modules_to_skip.update({x.name + ".*" for x in iter_modules()})
        # print("SKIP:", modules_to_skip)
        super().__init__(modules_to_skip)
        self.curframe = None
        self.lines = None
        self.actions = {
            "SET_CODE": self.do_set_code,
            "CONT": self.do_continue,
            "ADD_BP": self.do_add_breakpoints,
            "DEL_BP": self.do_del_breakpoints,
            "FW_S": self.do_forward_step,
            "BW_S": self.do_backwards_step,
            "FW_N": self.do_forward_next
        }

    def reset_internal(self):  # Have to do this stupid thing because self.reset() is called whenever run() is called :)
        self.lines = None
        self.curframe = None
        self.continue_state = False

    def set_continue(self):
        self.continue_state = True
        super().set_continue()

    def get_continue_state(self) -> bool:
        """
        Consume the current continue state. This means that a call to this method will set the current continue state to
        false!

        :returns: the continue state before being consumed.
        """
        prev = self.continue_state
        self.continue_state = False
        return prev

    def do_add_breakpoints(self, data):
        global _FILE_NAME
        for lineno, cond in data:
            # print("bdb_layer: Adding breakpoint at line", lineno)
            self.set_break(self.canonic(_FILE_NAME), lineno, cond=cond)
            # print("bdb_layer: Breakpoint added at line", lineno)
        return False

    def do_del_breakpoints(self, data):
        global _FILE_NAME
        for lineno in data:
            # print("bdb_layer: Removing breakpoint at line", lineno)
            self.clear_break(self.canonic(_FILE_NAME), lineno)
            # print("bdb_layer: Removed breakpoint at line", lineno)
        return False

    def do_forward_step(self, data):
        self.set_step()
        return True

    def do_backwards_step(self, data):
        print("Call to backwards step. It is NOT implemented!", file=stderr)
        return True

    def do_forward_next(self, data):
        self.set_next(self.curframe)
        return True

    def do_set_code(self, data):
        print("Call to set_code. It is NOT implemented!", file=stderr)
        return True

    def do_continue(self, data):
        self.set_continue()
        return True

    def _cmdloop(self):
        should_exit = False
        while not should_exit:
            mes_queue = from_worker.get_implementation().wait_for_main_messages()
            _append_to_message_queue(mes_queue)
            while not should_exit and not _is_message_queue_empty():
                mes_id, mes_data = _pop_first_message()
                should_exit |= self.actions[mes_id](mes_data)

    def user_line(self, frame):
        self.curframe = frame
        ctx = DebugContext.list_from_frame(frame, self.botframe)
        if _should_skip_frame(frame):
            return
        if self.get_continue_state() and not self.break_here(frame):
            self.set_continue()
            return
        # print("FRAME MODULE", ctx[0].variables.globals["__name__"])
        # print("DBG CONTEXT GLOBALS:", ctx[0].variables.globals.keys())
        # print("DBG CONTEXT LOCALS:", ctx[0].variables.locals.keys())
        # print("LENGTH DBG CONTEXT:", len(ctx))
        if frame.f_lineno == len(self.lines):
            from_worker.get_implementation().send_message("EXEC_DONE", ctx)
        else:
            from_worker.get_implementation().send_message("EXEC_PAUSED", ctx)
            self._cmdloop()

    def user_return(self, frame, return_value):
        pass

    def user_call(self, frame, argument_list):
        pass

    def user_exception(self, frame, exc_info):
        from_worker.get_implementation().send_message("EXEC_THROWED",
                                                      (exc_info[0], DebugContext.list_from_frame(frame, self.botframe)))

    def set_source(self, code: str):
        self.lines = code.split("\n")

    def run(self, cmd, _globals=None, _locals=None):
        import __main__
        __main__.__dict__.clear()
        __main__.__dict__.update({"__name__": "__main__",
                                  "__file__": _FILE_NAME,
                                  "__builtins__": __builtins__,
                                  })
        try:
            super().run(cmd, _globals, _locals)
        except SystemExit as e:
            pass
        except:
            ex_type, ex, t = sys.exc_info()
            while t.tb_next:
                t = t.tb_next
            frame = t.tb_frame
            from_worker.get_implementation().send_message("EXEC_THROWED",
                                                          (ex, DebugContext.list_from_frame(frame, self.botframe)))
