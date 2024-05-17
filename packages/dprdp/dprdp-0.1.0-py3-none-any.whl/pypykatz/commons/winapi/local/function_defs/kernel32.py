from .defines import *

PAGE_NOACCESS = 0x01
PAGE_READONLY = 0x02
PAGE_READWRITE = 0x04
PAGE_WRITECOPY = 0x08
PAGE_EXECUTE = 0x10
PAGE_EXECUTE_READ = 0x20
PAGE_EXECUTE_READWRITE = 0x40
PAGE_EXECUTE_WRITECOPY = 0x80
PAGE_GUARD = 0x100
PAGE_NOCACHE = 0x200
PAGE_WRITECOMBINE = 0x400
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
MEM_DECOMMIT = 0x4000
MEM_RELEASE = 0x8000
MEM_FREE = 0x10000
MEM_PRIVATE = 0x20000
MEM_MAPPED = 0x40000
MEM_RESET = 0x80000
MEM_TOP_DOWN = 0x100000
MEM_WRITE_WATCH = 0x200000
MEM_PHYSICAL = 0x400000
MEM_LARGE_PAGES = 0x20000000
MEM_4MB_PAGES = 0x80000000
SEC_FILE = 0x800000
SEC_IMAGE = 0x1000000
SEC_RESERVE = 0x4000000
SEC_COMMIT = 0x8000000
SEC_NOCACHE = 0x10000000
SEC_LARGE_PAGES = 0x80000000
MEM_IMAGE = SEC_IMAGE
WRITE_WATCH_FLAG_RESET = 0x01
FILE_MAP_ALL_ACCESS = 0xF001F

PROCESS_DUP_HANDLE = 0x0040


class UserModeHandle(HANDLE):
    _TYPE = HANDLE

    def _close(self):
        raise NotImplementedError()

    @property
    def _as_parameter_(self):
        return self._TYPE(self.value)

    @staticmethod
    def from_param(value):
        return self._TYPE(self.value)

    @property
    def inherit(self):
        return False

    @property
    def protectFromClose(self):
        return False

    def dup(self):
        raise NotImplementedError()

    def wait(self, dwMilliseconds=None):
        raise NotImplementedError()


class MemoryBasicInformation(object):
    READABLE = (
            PAGE_EXECUTE_READ |
            PAGE_EXECUTE_READWRITE |
            PAGE_EXECUTE_WRITECOPY |
            PAGE_READONLY |
            PAGE_READWRITE |
            PAGE_WRITECOPY
    )

    WRITEABLE = (
            PAGE_EXECUTE_READWRITE |
            PAGE_EXECUTE_WRITECOPY |
            PAGE_READWRITE |
            PAGE_WRITECOPY
    )

    COPY_ON_WRITE = (
            PAGE_EXECUTE_WRITECOPY |
            PAGE_WRITECOPY
    )

    EXECUTABLE = (
            PAGE_EXECUTE |
            PAGE_EXECUTE_READ |
            PAGE_EXECUTE_READWRITE |
            PAGE_EXECUTE_WRITECOPY
    )

    EXECUTABLE_AND_WRITEABLE = (
            PAGE_EXECUTE_READWRITE |
            PAGE_EXECUTE_WRITECOPY
    )

    def __init__(self, mbi=None):

        if mbi is None:
            self.BaseAddress = None
            self.AllocationBase = None
            self.AllocationProtect = None
            self.RegionSize = None
            self.State = None
            self.Protect = None
            self.Type = None
        else:
            self.BaseAddress = mbi.BaseAddress
            self.AllocationBase = mbi.AllocationBase
            self.AllocationProtect = mbi.AllocationProtect
            self.RegionSize = mbi.RegionSize
            self.State = mbi.State
            self.Protect = mbi.Protect
            self.Type = mbi.Type

            if hasattr(mbi, 'content'):
                self.content = mbi.content
            if hasattr(mbi, 'filename'):
                self.content = mbi.filename

    def __contains__(self, address):

        return self.BaseAddress <= address < (self.BaseAddress + self.RegionSize)

    def is_free(self):

        return self.State == MEM_FREE

    def is_reserved(self):

        return self.State == MEM_RESERVE

    def is_commited(self):

        return self.State == MEM_COMMIT

    def is_image(self):

        return self.Type == MEM_IMAGE

    def is_mapped(self):

        return self.Type == MEM_MAPPED

    def is_private(self):

        return self.Type == MEM_PRIVATE

    def is_guard(self):

        return self.is_commited() and bool(self.Protect & PAGE_GUARD)

    def has_content(self):

        return self.is_commited() and not bool(self.Protect & (PAGE_GUARD | PAGE_NOACCESS))

    def is_readable(self):

        return self.has_content() and bool(self.Protect & self.READABLE)

    def is_writeable(self):

        return self.has_content() and bool(self.Protect & self.WRITEABLE)

    def is_copy_on_write(self):

        return self.has_content() and bool(self.Protect & self.COPY_ON_WRITE)

    def is_executable(self):

        return self.has_content() and bool(self.Protect & self.EXECUTABLE)

    def is_executable_and_writeable(self):

        return self.has_content() and bool(self.Protect & self.EXECUTABLE_AND_WRITEABLE)


def GetLastError():
    _GetLastError = windll.kernel32.GetLastError
    _GetLastError.argtypes = []
    _GetLastError.restype = DWORD
    return _GetLastError()


class MEMORY_BASIC_INFORMATION(Structure):
    _fields_ = [
        ('BaseAddress', SIZE_T),
        ('AllocationBase', SIZE_T),
        ('AllocationProtect', DWORD),
        ('RegionSize', SIZE_T),
        ('State', DWORD),
        ('Protect', DWORD),
        ('Type', DWORD),
    ]


PMEMORY_BASIC_INFORMATION = POINTER(MEMORY_BASIC_INFORMATION)


def CloseHandle(hHandle):
    if hasattr(hHandle, 'close'):

        hHandle.close()
    else:
        _CloseHandle = windll.kernel32.CloseHandle
        _CloseHandle.argtypes = [HANDLE]
        _CloseHandle.restype = bool
        _CloseHandle.errcheck = RaiseIfZero
    _CloseHandle(hHandle)


def GetCurrentProcessId():
    _GetCurrentProcessId = windll.kernel32.GetCurrentProcessId
    _GetCurrentProcessId.argtypes = []
    _GetCurrentProcessId.restype = DWORD
    return _GetCurrentProcessId()


def GetCurrentProcess():
    _GetCurrentProcess = windll.kernel32.GetCurrentProcess
    _GetCurrentProcess.argtypes = []
    _GetCurrentProcess.restype = HANDLE
    return _GetCurrentProcess()


def QueryFullProcessImageNameW(hProcess, dwFlags=0):
    _QueryFullProcessImageNameW = windll.kernel32.QueryFullProcessImageNameW
    _QueryFullProcessImageNameW.argtypes = [HANDLE, DWORD, LPWSTR, PDWORD]
    _QueryFullProcessImageNameW.restype = bool

    dwSize = MAX_PATH
    while 1:
        lpdwSize = DWORD(dwSize)
        lpExeName = ctypes.create_unicode_buffer('', lpdwSize.value + 1)
        success = _QueryFullProcessImageNameW(hProcess, dwFlags, lpExeName, byref(lpdwSize))
        if success and 0 < lpdwSize.value < dwSize:
            break
        error = GetLastError()
        if error != ERROR_INSUFFICIENT_BUFFER:
            raise ctypes.WinError(error)
        dwSize += 256
        if dwSize > 0x1000:
            raise ctypes.WinError(error)
    return lpExeName.value


def OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId):
    _OpenProcess = windll.kernel32.OpenProcess
    _OpenProcess.argtypes = [DWORD, BOOL, DWORD]
    _OpenProcess.restype = HANDLE

    hProcess = _OpenProcess(dwDesiredAccess, bool(bInheritHandle), dwProcessId)
    if hProcess == NULL:
        raise ctypes.WinError()
    return hProcess


def ReadProcessMemory(hProcess, lpBaseAddress, nSize):
    _ReadProcessMemory = windll.kernel32.ReadProcessMemory
    _ReadProcessMemory.argtypes = [HANDLE, LPVOID, LPVOID, SIZE_T, POINTER(SIZE_T)]
    _ReadProcessMemory.restype = bool

    lpBuffer = ctypes.create_string_buffer(nSize)
    lpNumberOfBytesRead = SIZE_T(0)
    success = _ReadProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, byref(lpNumberOfBytesRead))
    if not success and GetLastError() != ERROR_PARTIAL_COPY:
        raise ctypes.WinError()
    return lpBuffer.raw[:lpNumberOfBytesRead.value]


def WriteProcessMemory(hProcess, lpBaseAddress, lpBuffer):
    _WriteProcessMemory = windll.kernel32.WriteProcessMemory
    _WriteProcessMemory.argtypes = [HANDLE, LPVOID, LPVOID, SIZE_T, POINTER(SIZE_T)]
    _WriteProcessMemory.restype = bool

    nSize = len(lpBuffer)
    lpBuffer = ctypes.create_string_buffer(lpBuffer)
    lpNumberOfBytesWritten = SIZE_T(0)
    success = _WriteProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, byref(lpNumberOfBytesWritten))
    if not success and GetLastError() != ERROR_PARTIAL_COPY:
        raise ctypes.WinError()
    return lpNumberOfBytesWritten.value


def VirtualQueryEx(hProcess, lpAddress):
    _VirtualQueryEx = windll.kernel32.VirtualQueryEx
    _VirtualQueryEx.argtypes = [HANDLE, LPVOID, PMEMORY_BASIC_INFORMATION, SIZE_T]
    _VirtualQueryEx.restype = SIZE_T

    lpBuffer = MEMORY_BASIC_INFORMATION()
    dwLength = sizeof(MEMORY_BASIC_INFORMATION)
    success = _VirtualQueryEx(hProcess, lpAddress, byref(lpBuffer), dwLength)
    if success == 0:
        raise ctypes.WinError()
    return MemoryBasicInformation(lpBuffer)


def LocalFree(hMem):
    _LocalFree = windll.kernel32.LocalFree
    _LocalFree.argtypes = [HLOCAL]
    _LocalFree.restype = HLOCAL

    result = _LocalFree(hMem)
    if result != NULL:
        ctypes.WinError()


class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [
        ('nLength', DWORD),
        ('lpSecurityDescriptor', LPVOID),
        ('bInheritHandle', BOOL),
    ]


LPSECURITY_ATTRIBUTES = POINTER(SECURITY_ATTRIBUTES)

PPROC_THREAD_ATTRIBUTE_LIST = LPVOID
LPPROC_THREAD_ATTRIBUTE_LIST = PPROC_THREAD_ATTRIBUTE_LIST

PROC_THREAD_ATTRIBUTE_NUMBER = 0x0000FFFF
PROC_THREAD_ATTRIBUTE_THREAD = 0x00010000
PROC_THREAD_ATTRIBUTE_INPUT = 0x00020000
PROC_THREAD_ATTRIBUTE_ADDITIVE = 0x00040000

ProcThreadAttributeParentProcess = 0
ProcThreadAttributeExtendedFlags = 1
ProcThreadAttributeHandleList = 2
ProcThreadAttributeGroupAffinity = 3
ProcThreadAttributePreferredNode = 4
ProcThreadAttributeIdealProcessor = 5
ProcThreadAttributeUmsThread = 6
ProcThreadAttributeMitigationPolicy = 7
ProcThreadAttributeMax = 8

PROC_THREAD_ATTRIBUTE_PARENT_PROCESS = ProcThreadAttributeParentProcess | PROC_THREAD_ATTRIBUTE_INPUT
PROC_THREAD_ATTRIBUTE_EXTENDED_FLAGS = ProcThreadAttributeExtendedFlags | PROC_THREAD_ATTRIBUTE_INPUT | PROC_THREAD_ATTRIBUTE_ADDITIVE
PROC_THREAD_ATTRIBUTE_HANDLE_LIST = ProcThreadAttributeHandleList | PROC_THREAD_ATTRIBUTE_INPUT
PROC_THREAD_ATTRIBUTE_GROUP_AFFINITY = ProcThreadAttributeGroupAffinity | PROC_THREAD_ATTRIBUTE_THREAD | PROC_THREAD_ATTRIBUTE_INPUT
PROC_THREAD_ATTRIBUTE_PREFERRED_NODE = ProcThreadAttributePreferredNode | PROC_THREAD_ATTRIBUTE_INPUT
PROC_THREAD_ATTRIBUTE_IDEAL_PROCESSOR = ProcThreadAttributeIdealProcessor | PROC_THREAD_ATTRIBUTE_THREAD | PROC_THREAD_ATTRIBUTE_INPUT
PROC_THREAD_ATTRIBUTE_UMS_THREAD = ProcThreadAttributeUmsThread | PROC_THREAD_ATTRIBUTE_THREAD | PROC_THREAD_ATTRIBUTE_INPUT
PROC_THREAD_ATTRIBUTE_MITIGATION_POLICY = ProcThreadAttributeMitigationPolicy | PROC_THREAD_ATTRIBUTE_INPUT

PROCESS_CREATION_MITIGATION_POLICY_DEP_ENABLE = 0x01
PROCESS_CREATION_MITIGATION_POLICY_DEP_ATL_THUNK_ENABLE = 0x02
PROCESS_CREATION_MITIGATION_POLICY_SEHOP_ENABLE = 0x04


class PROCESS_INFORMATION(Structure):
    _fields_ = [
        ('hProcess', HANDLE),
        ('hThread', HANDLE),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD),
    ]


LPPROCESS_INFORMATION = POINTER(PROCESS_INFORMATION)


class STARTUPINFO(Structure):
    _fields_ = [
        ('cb', DWORD),
        ('lpReserved', LPSTR),
        ('lpDesktop', LPSTR),
        ('lpTitle', LPSTR),
        ('dwX', DWORD),
        ('dwY', DWORD),
        ('dwXSize', DWORD),
        ('dwYSize', DWORD),
        ('dwXCountChars', DWORD),
        ('dwYCountChars', DWORD),
        ('dwFillAttribute', DWORD),
        ('dwFlags', DWORD),
        ('wShowWindow', WORD),
        ('cbReserved2', WORD),
        ('lpReserved2', LPVOID),
        ('hStdInput', HANDLE),
        ('hStdOutput', HANDLE),
        ('hStdError', HANDLE),
    ]


LPSTARTUPINFO = POINTER(STARTUPINFO)


class STARTUPINFOEX(Structure):
    _fields_ = [
        ('StartupInfo', STARTUPINFO),
        ('lpAttributeList', PPROC_THREAD_ATTRIBUTE_LIST),
    ]


LPSTARTUPINFOEX = POINTER(STARTUPINFOEX)


class STARTUPINFOW(Structure):
    _fields_ = [
        ('cb', DWORD),
        ('lpReserved', LPWSTR),
        ('lpDesktop', LPWSTR),
        ('lpTitle', LPWSTR),
        ('dwX', DWORD),
        ('dwY', DWORD),
        ('dwXSize', DWORD),
        ('dwYSize', DWORD),
        ('dwXCountChars', DWORD),
        ('dwYCountChars', DWORD),
        ('dwFillAttribute', DWORD),
        ('dwFlags', DWORD),
        ('wShowWindow', WORD),
        ('cbReserved2', WORD),
        ('lpReserved2', LPVOID),
        ('hStdInput', HANDLE),
        ('hStdOutput', HANDLE),
        ('hStdError', HANDLE),
    ]


LPSTARTUPINFOW = POINTER(STARTUPINFOW)


class STARTUPINFOEXW(Structure):
    _fields_ = [
        ('StartupInfo', STARTUPINFOW),
        ('lpAttributeList', PPROC_THREAD_ATTRIBUTE_LIST),
    ]


LPSTARTUPINFOEXW = POINTER(STARTUPINFOEXW)


def VirtualProtectEx(hProcess, lpAddress, dwSize, flNewProtect=PAGE_EXECUTE_READWRITE):
    _VirtualProtectEx = windll.kernel32.VirtualProtectEx
    _VirtualProtectEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD, PDWORD]
    _VirtualProtectEx.restype = bool
    _VirtualProtectEx.errcheck = RaiseIfZero

    flOldProtect = DWORD(0)
    _VirtualProtectEx(hProcess, lpAddress, dwSize, flNewProtect, byref(flOldProtect))
    return flOldProtect.value


def VirtualFreeEx(hProcess, lpAddress, dwSize=0, dwFreeType=MEM_RELEASE):
    _VirtualFreeEx = windll.kernel32.VirtualFreeEx
    _VirtualFreeEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD]
    _VirtualFreeEx.restype = bool
    _VirtualFreeEx.errcheck = RaiseIfZero
    _VirtualFreeEx(hProcess, lpAddress, dwSize, dwFreeType)


def VirtualAllocEx(hProcess, lpAddress=0, dwSize=0x1000, flAllocationType=MEM_COMMIT | MEM_RESERVE,
                   flProtect=PAGE_EXECUTE_READWRITE):
    _VirtualAllocEx = windll.kernel32.VirtualAllocEx
    _VirtualAllocEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD, DWORD]
    _VirtualAllocEx.restype = LPVOID

    lpAddress = _VirtualAllocEx(hProcess, lpAddress, dwSize, flAllocationType, flProtect)
    if lpAddress == NULL:
        raise ctypes.WinError()
    return lpAddress


def CreateRemoteThread(hProcess, lpThreadAttributes, dwStackSize, lpStartAddress, lpParameter, dwCreationFlags):
    _CreateRemoteThread = windll.kernel32.CreateRemoteThread
    _CreateRemoteThread.argtypes = [HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T, LPVOID, LPVOID, DWORD, LPDWORD]
    _CreateRemoteThread.restype = HANDLE

    if not lpThreadAttributes:
        lpThreadAttributes = None
    else:
        lpThreadAttributes = byref(lpThreadAttributes)
    dwThreadId = DWORD(0)
    hThread = _CreateRemoteThread(hProcess, lpThreadAttributes, dwStackSize, lpStartAddress, lpParameter,
                                  dwCreationFlags, byref(dwThreadId))
    if not hThread:
        raise ctypes.WinError()
    return hThread, dwThreadId.value


def GetProcAddressW(hModule, lpProcName):
    _GetProcAddress = windll.kernel32.GetProcAddress
    _GetProcAddress.argtypes = [HMODULE, LPVOID]
    _GetProcAddress.restype = LPVOID

    if type(lpProcName) in (type(0), type(0)):
        lpProcName = LPVOID(lpProcName)
        if lpProcName.value & (~0xFFFF):
            raise ValueError('Ordinal number too large: %d' % lpProcName.value)
    elif type(lpProcName) == type(""):
        lpProcName = ctypes.create_string_buffer(lpProcName.encode('ascii'))
    elif type(lpProcName) == type(b""):
        lpProcName = ctypes.c_char_p(lpProcName)
    else:
        raise TypeError(str(type(lpProcName)))
    return _GetProcAddress(hModule, lpProcName)


def LoadLibraryW(pszLibrary):
    _LoadLibraryW = windll.kernel32.LoadLibraryW
    _LoadLibraryW.argtypes = [LPWSTR]
    _LoadLibraryW.restype = HMODULE
    hModule = _LoadLibraryW(pszLibrary)
    if hModule == NULL:
        raise ctypes.WinError()
    return hModule
