import ctypes
from ctypes import windll
from ctypes.wintypes import ULONG, BOOL, LONG

from .privileges_types import *

STATUS_SUCCESS = 0
NTSTATUS = LONG
POINTER = ctypes.POINTER


def NtError(status):
    err = windll.ntdll.RtlNtStatusToDosError(status)
    return ctypes.WinError(err)


def RtlAdjustPrivilege(privilige_id, enable=True, thread_or_process=False):
    _RtlAdjustPrivilege = windll.ntdll.RtlAdjustPrivilege
    _RtlAdjustPrivilege.argtypes = [ULONG, BOOL, BOOL, POINTER(BOOL)]
    _RtlAdjustPrivilege.restype = NTSTATUS

    CurrentThread = thread_or_process
    Enabled = BOOL()

    status = _RtlAdjustPrivilege(privilige_id, enable, CurrentThread, ctypes.byref(Enabled))
    if status != STATUS_SUCCESS:
        raise Exception(NtError(status))

    return True


def enable_debug_privilege():
    RtlAdjustPrivilege(PrivilegeValues.SE_DEBUG.value)


if __name__ == '__main__':
    enable_debug_privilege()
