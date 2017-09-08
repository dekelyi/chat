"""
threading utils
"""
import threading
import ctypes


class KillableThread(threading.Thread):
    """
    A thread that can be killed by outsiders
    """
    def _raise(self, excobj):
        """
        Raise a exception inside the thread

        :param type excobj: type of exception
        """
        if not self.isAlive():
            return

        exc = ctypes.py_object(excobj)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def kill(self):
        """
        Terminate the thread
        """
        self._raise(SystemExit)
