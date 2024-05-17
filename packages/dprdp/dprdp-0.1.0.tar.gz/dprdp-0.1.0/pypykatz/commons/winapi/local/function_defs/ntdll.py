from ctypes import windll
from ctypes.wintypes import ULONG, BOOL

from pypykatz.commons.winapi.local.function_defs.defines import *

SystemHandleInformation = 16
ObjectBasicInformation = 0
ObjectNameInformation = 1
ObjectTypeInformation = 2

POOL_TYPE = ctypes.c_int
NonPagedPool = 1
PagedPool = 2
NonPagedPoolMustSucceed = 3
DontUseThisType = 4
NonPagedPoolCacheAligned = 5
PagedPoolCacheAligned = 6
NonPagedPoolCacheAlignedMustS = 7


class GENERIC_MAPPING(Structure):
    _fields_ = [
        ("GenericRead", ACCESS_MASK),
        ("GenericWrite", ACCESS_MASK),
        ("GenericExecute", ACCESS_MASK),
        ("GenericAll", ACCESS_MASK),
    ]


PGENERIC_MAPPING = POINTER(GENERIC_MAPPING)


class SYSTEM_HANDLE(Structure):
    _fields_ = [
        ("ProcessId", ULONG),
        ("ObjectTypeNumber", BYTE),
        ("Flags", BYTE),
        ("Handle", USHORT),
        ("Object", PVOID),
        ("GrantedAccess", ACCESS_MASK),
    ]


PSYSTEM_HANDLE = POINTER(SYSTEM_HANDLE)


class OBJECT_TYPE_INFORMATION(Structure):
    _fields_ = [
        ("Name", UNICODE_STRING),
        ("TotalNumberOfObjects", ULONG),
        ("TotalNumberOfHandles", ULONG),
        ("TotalPagedPoolUsage", ULONG),
        ("TotalNonPagedPoolUsage", ULONG),
        ("TotalNamePoolUsage", ULONG),
        ("TotalHandleTableUsage", ULONG),
        ("HighWaterNumberOfObjects", ULONG),
        ("HighWaterNumberOfHandles", ULONG),
        ("HighWaterPagedPoolUsage", ULONG),
        ("HighWaterNonPagedPoolUsage", ULONG),
        ("HighWaterNamePoolUsage", ULONG),
        ("HighWaterHandleTableUsage", ULONG),
        ("GenericMapping", GENERIC_MAPPING),
        ("ValidAccess", ULONG),
        ("SecurityRequired", BOOLEAN),
        ("MaintainHandleCount", BOOLEAN),
        ("MaintainTypeList", USHORT),
        ("PoolType", POOL_TYPE),
        ("PagedPoolUsage", ULONG),
        ("NonPagedPoolUsage", ULONG),
    ]


POBJECT_TYPE_INFORMATION = POINTER(OBJECT_TYPE_INFORMATION)


def RtlAdjustPrivilege(privilige_id, enable=True, thread_or_process=False):
    _RtlAdjustPrivilege = windll.ntdll.RtlAdjustPrivilege
    _RtlAdjustPrivilege.argtypes = [ULONG, BOOL, BOOL, POINTER(BOOL)]
    _RtlAdjustPrivilege.restype = NTSTATUS

    CurrentThread = thread_or_process
    Enabled = BOOL()

    status = _RtlAdjustPrivilege(privilige_id, enable, CurrentThread, ctypes.byref(Enabled))
    if status != 0:
        raise Exception('Failed call to RtlAdjustPrivilege! Status: %s' % status)

    return Enabled.value


def NtQuerySystemInformation(info_type):
    _NtQuerySystemInformation = windll.ntdll.NtQuerySystemInformation
    _NtQuerySystemInformation.argtypes = [ULONG, PVOID, ULONG, PULONG]
    _NtQuerySystemInformation.restype = ULONG

    handleinfos = {}

    if info_type != 16:
        raise Exception('info_type only the value 16 is supported!')

    size = DWORD(0x10)
    data = ctypes.create_string_buffer(size.value)
    while True:

        size = DWORD(size.value * 2)
        data = ctypes.create_string_buffer(size.value)
        status = _NtQuerySystemInformation(info_type, ctypes.byref(data), size, ctypes.byref(size))
        if status == 0:
            break
        if status != 0xC0000004:
            raise Exception('NtQuerySystemInformation returned %s' % hex(status))

        status = _NtQuerySystemInformation(info_type, ctypes.byref(data), size, ctypes.byref(size))

    data_bytes = bytearray(data.raw[:size.value])

    hc = ULONG.from_buffer(data_bytes)

    class SYSTEM_HANDLE_INFORMATION(Structure):
        _fields_ = [
            ("HandleCount", ULONG),
            ("Handles", SYSTEM_HANDLE * hc.value),
        ]

    syshandleinfo = SYSTEM_HANDLE_INFORMATION.from_buffer(data_bytes)

    for i in range(syshandleinfo.HandleCount):
        if not syshandleinfo.Handles[i].ProcessId in handleinfos:
            handleinfos[syshandleinfo.Handles[i].ProcessId] = []
        handleinfos[syshandleinfo.Handles[i].ProcessId].append(syshandleinfo.Handles[i])

    return handleinfos


def NtDuplicateObject(SourceProcessHandle, SourceHandle, TargetProcessHandle, DesiredAccess=0):
    _NtDuplicateObject = windll.ntdll.NtDuplicateObject
    _NtDuplicateObject.argtypes = [HANDLE, HANDLE, HANDLE, PHANDLE, ACCESS_MASK, ULONG, ULONG]
    _NtDuplicateObject.restype = ULONG

    oHandle = HANDLE()
    status = _NtDuplicateObject(SourceProcessHandle, SourceHandle, TargetProcessHandle, ctypes.byref(oHandle),
                                DesiredAccess, 0, 0)
    if status != 0:
        raise Exception('Failed call to NtDuplicateObject! Status: %s' % status)

    return oHandle


def NtQueryObject(ObjectHandle, ObjectInformationClass):
    _NtQueryObject = windll.ntdll.NtQueryObject
    _NtQueryObject.argtypes = [HANDLE, ULONG, PVOID, ULONG, PULONG]
    _NtQueryObject.restype = ULONG

    if ObjectInformationClass != ObjectTypeInformation:
        raise Exception('Unsupported ObjectInformationClass value %s.' % ObjectInformationClass)

    size = ULONG(0x10)
    oinfo_data = ctypes.create_string_buffer(size.value)

    while True:
        oinfo_data = ctypes.create_string_buffer(size.value)
        status = _NtQueryObject(ObjectHandle, ObjectInformationClass, oinfo_data, size, ctypes.byref(size))
        if status == 0xc0000004:
            continue
        if status != 0:
            raise Exception('Failed call to NtDuplicateObject! Status: %s' % hex(status))

        break

    if ObjectInformationClass == ObjectNameInformation:
        raise NotImplementedError('TODO: implement me when needed!')
    elif ObjectInformationClass == ObjectTypeInformation:
        oinfo = OBJECT_TYPE_INFORMATION.from_buffer(bytearray(oinfo_data.raw[:size.value]))

    return oinfo
