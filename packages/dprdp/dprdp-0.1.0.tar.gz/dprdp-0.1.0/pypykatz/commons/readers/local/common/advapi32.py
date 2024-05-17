from .defines import *
from .kernel32 import *

_all = None
_all = set(vars().keys())

SE_ASSIGNPRIMARYTOKEN_NAME = "SeAssignPrimaryTokenPrivilege"
SE_AUDIT_NAME = "SeAuditPrivilege"
SE_BACKUP_NAME = "SeBackupPrivilege"
SE_CHANGE_NOTIFY_NAME = "SeChangeNotifyPrivilege"
SE_CREATE_GLOBAL_NAME = "SeCreateGlobalPrivilege"
SE_CREATE_PAGEFILE_NAME = "SeCreatePagefilePrivilege"
SE_CREATE_PERMANENT_NAME = "SeCreatePermanentPrivilege"
SE_CREATE_SYMBOLIC_LINK_NAME = "SeCreateSymbolicLinkPrivilege"
SE_CREATE_TOKEN_NAME = "SeCreateTokenPrivilege"
SE_DEBUG_NAME = "SeDebugPrivilege"
SE_ENABLE_DELEGATION_NAME = "SeEnableDelegationPrivilege"
SE_IMPERSONATE_NAME = "SeImpersonatePrivilege"
SE_INC_BASE_PRIORITY_NAME = "SeIncreaseBasePriorityPrivilege"
SE_INCREASE_QUOTA_NAME = "SeIncreaseQuotaPrivilege"
SE_INC_WORKING_SET_NAME = "SeIncreaseWorkingSetPrivilege"
SE_LOAD_DRIVER_NAME = "SeLoadDriverPrivilege"
SE_LOCK_MEMORY_NAME = "SeLockMemoryPrivilege"
SE_MACHINE_ACCOUNT_NAME = "SeMachineAccountPrivilege"
SE_MANAGE_VOLUME_NAME = "SeManageVolumePrivilege"
SE_PROF_SINGLE_PROCESS_NAME = "SeProfileSingleProcessPrivilege"
SE_RELABEL_NAME = "SeRelabelPrivilege"
SE_REMOTE_SHUTDOWN_NAME = "SeRemoteShutdownPrivilege"
SE_RESTORE_NAME = "SeRestorePrivilege"
SE_SECURITY_NAME = "SeSecurityPrivilege"
SE_SHUTDOWN_NAME = "SeShutdownPrivilege"
SE_SYNC_AGENT_NAME = "SeSyncAgentPrivilege"
SE_SYSTEM_ENVIRONMENT_NAME = "SeSystemEnvironmentPrivilege"
SE_SYSTEM_PROFILE_NAME = "SeSystemProfilePrivilege"
SE_SYSTEMTIME_NAME = "SeSystemtimePrivilege"
SE_TAKE_OWNERSHIP_NAME = "SeTakeOwnershipPrivilege"
SE_TCB_NAME = "SeTcbPrivilege"
SE_TIME_ZONE_NAME = "SeTimeZonePrivilege"
SE_TRUSTED_CREDMAN_ACCESS_NAME = "SeTrustedCredManAccessPrivilege"
SE_UNDOCK_NAME = "SeUndockPrivilege"
SE_UNSOLICITED_INPUT_NAME = "SeUnsolicitedInputPrivilege"

SE_PRIVILEGE_ENABLED_BY_DEFAULT = 0x00000001
SE_PRIVILEGE_ENABLED = 0x00000002
SE_PRIVILEGE_REMOVED = 0x00000004
SE_PRIVILEGE_USED_FOR_ACCESS = 0x80000000

TOKEN_ADJUST_PRIVILEGES = 0x00000020

LOGON_WITH_PROFILE = 0x00000001
LOGON_NETCREDENTIALS_ONLY = 0x00000002

TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_DUPLICATE = 0x0002
TOKEN_IMPERSONATE = 0x0004
TOKEN_QUERY = 0x0008
TOKEN_QUERY_SOURCE = 0x0010
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_ADJUST_GROUPS = 0x0040
TOKEN_ADJUST_DEFAULT = 0x0080
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_READ = (STANDARD_RIGHTS_READ | TOKEN_QUERY)
TOKEN_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | TOKEN_ASSIGN_PRIMARY |
                    TOKEN_DUPLICATE | TOKEN_IMPERSONATE | TOKEN_QUERY | TOKEN_QUERY_SOURCE |
                    TOKEN_ADJUST_PRIVILEGES | TOKEN_ADJUST_GROUPS | TOKEN_ADJUST_DEFAULT |
                    TOKEN_ADJUST_SESSIONID)

HKEY_CLASSES_ROOT = 0x80000000
HKEY_CURRENT_USER = 0x80000001
HKEY_LOCAL_MACHINE = 0x80000002
HKEY_USERS = 0x80000003
HKEY_PERFORMANCE_DATA = 0x80000004
HKEY_CURRENT_CONFIG = 0x80000005

KEY_ALL_ACCESS = 0xF003F
KEY_CREATE_LINK = 0x0020
KEY_CREATE_SUB_KEY = 0x0004
KEY_ENUMERATE_SUB_KEYS = 0x0008
KEY_EXECUTE = 0x20019
KEY_NOTIFY = 0x0010
KEY_QUERY_VALUE = 0x0001
KEY_READ = 0x20019
KEY_SET_VALUE = 0x0002
KEY_WOW64_32KEY = 0x0200
KEY_WOW64_64KEY = 0x0100
KEY_WRITE = 0x20006

REG_NONE = 0
REG_SZ = 1
REG_EXPAND_SZ = 2
REG_BINARY = 3
REG_DWORD = 4
REG_DWORD_LITTLE_ENDIAN = REG_DWORD
REG_DWORD_BIG_ENDIAN = 5
REG_LINK = 6
REG_MULTI_SZ = 7
REG_RESOURCE_LIST = 8
REG_FULL_RESOURCE_DESCRIPTOR = 9
REG_RESOURCE_REQUIREMENTS_LIST = 10
REG_QWORD = 11
REG_QWORD_LITTLE_ENDIAN = REG_QWORD


class LUID(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),
    ]


PLUID = POINTER(LUID)


class LUID_AND_ATTRIBUTES(Structure):
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", DWORD),
    ]


class TOKEN_PRIVILEGES(Structure):
    _fields_ = [
        ("PrivilegeCount", DWORD),

        ("Privileges", LUID_AND_ATTRIBUTES),
    ]


PTOKEN_PRIVILEGES = POINTER(TOKEN_PRIVILEGES)

TOKEN_INFORMATION_CLASS = ctypes.c_int

TokenUser = 1
TokenGroups = 2
TokenPrivileges = 3
TokenOwner = 4
TokenPrimaryGroup = 5
TokenDefaultDacl = 6
TokenSource = 7
TokenType = 8
TokenImpersonationLevel = 9
TokenStatistics = 10
TokenRestrictedSids = 11
TokenSessionId = 12
TokenGroupsAndPrivileges = 13
TokenSessionReference = 14
TokenSandBoxInert = 15
TokenAuditPolicy = 16
TokenOrigin = 17
TokenElevationType = 18
TokenLinkedToken = 19
TokenElevation = 20
TokenHasRestrictions = 21
TokenAccessInformation = 22
TokenVirtualizationAllowed = 23
TokenVirtualizationEnabled = 24
TokenIntegrityLevel = 25
TokenUIAccess = 26
TokenMandatoryPolicy = 27
TokenLogonSid = 28
TokenIsAppContainer = 29
TokenCapabilities = 30
TokenAppContainerSid = 31
TokenAppContainerNumber = 32
TokenUserClaimAttributes = 33
TokenDeviceClaimAttributes = 34
TokenRestrictedUserClaimAttributes = 35
TokenRestrictedDeviceClaimAttributes = 36
TokenDeviceGroups = 37
TokenRestrictedDeviceGroups = 38
TokenSecurityAttributes = 39
TokenIsRestricted = 40
MaxTokenInfoClass = 41

TOKEN_TYPE = ctypes.c_int
PTOKEN_TYPE = POINTER(TOKEN_TYPE)

TokenPrimary = 1
TokenImpersonation = 2

TokenElevationTypeDefault = 1
TokenElevationTypeFull = 2
TokenElevationTypeLimited = 3

TOKEN_ELEVATION_TYPE = ctypes.c_int
PTOKEN_ELEVATION_TYPE = POINTER(TOKEN_ELEVATION_TYPE)

SecurityAnonymous = 0
SecurityIdentification = 1
SecurityImpersonation = 2
SecurityDelegation = 3

SECURITY_IMPERSONATION_LEVEL = ctypes.c_int
PSECURITY_IMPERSONATION_LEVEL = POINTER(SECURITY_IMPERSONATION_LEVEL)


class SID_AND_ATTRIBUTES(Structure):
    _fields_ = [
        ("Sid", PSID),
        ("Attributes", DWORD),
    ]


PSID_AND_ATTRIBUTES = POINTER(SID_AND_ATTRIBUTES)


class TOKEN_USER(Structure):
    _fields_ = [
        ("User", SID_AND_ATTRIBUTES),
    ]


PTOKEN_USER = POINTER(TOKEN_USER)


class TOKEN_MANDATORY_LABEL(Structure):
    _fields_ = [
        ("Label", SID_AND_ATTRIBUTES),
    ]


PTOKEN_MANDATORY_LABEL = POINTER(TOKEN_MANDATORY_LABEL)


class TOKEN_OWNER(Structure):
    _fields_ = [
        ("Owner", PSID),
    ]


PTOKEN_OWNER = POINTER(TOKEN_OWNER)


class TOKEN_PRIMARY_GROUP(Structure):
    _fields_ = [
        ("PrimaryGroup", PSID),
    ]


PTOKEN_PRIMARY_GROUP = POINTER(TOKEN_PRIMARY_GROUP)


class TOKEN_APPCONTAINER_INFORMATION(Structure):
    _fields_ = [
        ("TokenAppContainer", PSID),
    ]


PTOKEN_APPCONTAINER_INFORMATION = POINTER(TOKEN_APPCONTAINER_INFORMATION)


class TOKEN_ORIGIN(Structure):
    _fields_ = [
        ("OriginatingLogonSession", LUID),
    ]


PTOKEN_ORIGIN = POINTER(TOKEN_ORIGIN)


class TOKEN_LINKED_TOKEN(Structure):
    _fields_ = [
        ("LinkedToken", HANDLE),
    ]


PTOKEN_LINKED_TOKEN = POINTER(TOKEN_LINKED_TOKEN)


class TOKEN_STATISTICS(Structure):
    _fields_ = [
        ("TokenId", LUID),
        ("AuthenticationId", LUID),
        ("ExpirationTime", LONGLONG),
        ("TokenType", TOKEN_TYPE),
        ("ImpersonationLevel", SECURITY_IMPERSONATION_LEVEL),
        ("DynamicCharged", DWORD),
        ("DynamicAvailable", DWORD),
        ("GroupCount", DWORD),
        ("PrivilegeCount", DWORD),
        ("ModifiedId", LUID),
    ]


PTOKEN_STATISTICS = POINTER(TOKEN_STATISTICS)

SidTypeUser = 1
SidTypeGroup = 2
SidTypeDomain = 3
SidTypeAlias = 4
SidTypeWellKnownGroup = 5
SidTypeDeletedAccount = 6
SidTypeInvalid = 7
SidTypeUnknown = 8
SidTypeComputer = 9
SidTypeLabel = 10

WCT_MAX_NODE_COUNT = 16
WCT_OBJNAME_LENGTH = 128
WCT_ASYNC_OPEN_FLAG = 1
WCTP_OPEN_ALL_FLAGS = WCT_ASYNC_OPEN_FLAG
WCT_OUT_OF_PROC_FLAG = 1
WCT_OUT_OF_PROC_COM_FLAG = 2
WCT_OUT_OF_PROC_CS_FLAG = 4
WCTP_GETINFO_ALL_FLAGS = WCT_OUT_OF_PROC_FLAG | WCT_OUT_OF_PROC_COM_FLAG | WCT_OUT_OF_PROC_CS_FLAG

HWCT = LPVOID

WCT_OBJECT_TYPE = DWORD

WctCriticalSectionType = 1
WctSendMessageType = 2
WctMutexType = 3
WctAlpcType = 4
WctComType = 5
WctThreadWaitType = 6
WctProcessWaitType = 7
WctThreadType = 8
WctComActivationType = 9
WctUnknownType = 10
WctMaxType = 11

WCT_OBJECT_STATUS = DWORD

WctStatusNoAccess = 1
WctStatusRunning = 2
WctStatusBlocked = 3
WctStatusPidOnly = 4
WctStatusPidOnlyRpcss = 5
WctStatusOwned = 6
WctStatusNotOwned = 7
WctStatusAbandoned = 8
WctStatusUnknown = 9
WctStatusError = 10
WctStatusMax = 11


class _WAITCHAIN_NODE_INFO_STRUCT_1(Structure):
    _fields_ = [
        ("ObjectName", WCHAR * WCT_OBJNAME_LENGTH),
        ("Timeout", LONGLONG),
        ("Alertable", BOOL),
    ]


class _WAITCHAIN_NODE_INFO_STRUCT_2(Structure):
    _fields_ = [
        ("ProcessId", DWORD),
        ("ThreadId", DWORD),
        ("WaitTime", DWORD),
        ("ContextSwitches", DWORD),
    ]


class _WAITCHAIN_NODE_INFO_UNION(Union):
    _fields_ = [
        ("LockObject", _WAITCHAIN_NODE_INFO_STRUCT_1),
        ("ThreadObject", _WAITCHAIN_NODE_INFO_STRUCT_2),
    ]


class WAITCHAIN_NODE_INFO(Structure):
    _fields_ = [
        ("ObjectType", WCT_OBJECT_TYPE),
        ("ObjectStatus", WCT_OBJECT_STATUS),
        ("u", _WAITCHAIN_NODE_INFO_UNION),
    ]


PWAITCHAIN_NODE_INFO = POINTER(WAITCHAIN_NODE_INFO)


class WaitChainNodeInfo(object):

    def __init__(self, aStructure):
        self.ObjectType = aStructure.ObjectType
        self.ObjectStatus = aStructure.ObjectStatus
        if self.ObjectType == WctThreadType:
            self.ProcessId = aStructure.u.ThreadObject.ProcessId
            self.ThreadId = aStructure.u.ThreadObject.ThreadId
            self.WaitTime = aStructure.u.ThreadObject.WaitTime
            self.ContextSwitches = aStructure.u.ThreadObject.ContextSwitches
            self.ObjectName = u''
        else:
            self.ObjectName = aStructure.u.LockObject.ObjectName.value


class ThreadWaitChainSessionHANDLE(HANDLE):

    def __init__(self, aHANDLE=None):
        super(ThreadWaitChainSessionHANDLE, self).__init__(aHANDLE,
                                                           bOwnership=True)

    def _close(self):
        if self.value is None:
            raise ValueError("HANDLE was already closed!")
        CloseThreadWaitChainSession(self.value)

    def dup(self):
        raise NotImplementedError()

    def wait(self, dwMilliseconds=None):
        raise NotImplementedError()

    @property
    def inherit(self):
        return False

    @property
    def protectFromClose(self):
        return False


SAFER_LEVEL_HANDLE = HANDLE

SAFER_SCOPEID_MACHINE = 1
SAFER_SCOPEID_USER = 2

SAFER_LEVEL_OPEN = 1

SAFER_LEVELID_DISALLOWED = 0x00000
SAFER_LEVELID_UNTRUSTED = 0x01000
SAFER_LEVELID_CONSTRAINED = 0x10000
SAFER_LEVELID_NORMALUSER = 0x20000
SAFER_LEVELID_FULLYTRUSTED = 0x40000

SAFER_POLICY_INFO_CLASS = DWORD
SaferPolicyLevelList = 1
SaferPolicyEnableTransparentEnforcement = 2
SaferPolicyDefaultLevel = 3
SaferPolicyEvaluateUserScope = 4
SaferPolicyScopeFlags = 5

SAFER_TOKEN_NULL_IF_EQUAL = 1
SAFER_TOKEN_COMPARE_ONLY = 2
SAFER_TOKEN_MAKE_INERT = 4
SAFER_TOKEN_WANT_FLAGS = 8
SAFER_TOKEN_MASK = 15

SC_HANDLE = HANDLE

SERVICES_ACTIVE_DATABASEW = u"ServicesActive"
SERVICES_FAILED_DATABASEW = u"ServicesFailed"

SERVICES_ACTIVE_DATABASEA = "ServicesActive"
SERVICES_FAILED_DATABASEA = "ServicesFailed"

SC_GROUP_IDENTIFIERW = u'+'
SC_GROUP_IDENTIFIERA = '+'

SERVICE_NO_CHANGE = 0xffffffff

SC_STATUS_TYPE = ctypes.c_int
SC_STATUS_PROCESS_INFO = 0

SC_ENUM_TYPE = ctypes.c_int
SC_ENUM_PROCESS_INFO = 0

SERVICE_ALL_ACCESS = 0xF01FF
SERVICE_QUERY_CONFIG = 0x0001
SERVICE_CHANGE_CONFIG = 0x0002
SERVICE_QUERY_STATUS = 0x0004
SERVICE_ENUMERATE_DEPENDENTS = 0x0008
SERVICE_START = 0x0010
SERVICE_STOP = 0x0020
SERVICE_PAUSE_CONTINUE = 0x0040
SERVICE_INTERROGATE = 0x0080
SERVICE_USER_DEFINED_CONTROL = 0x0100

SC_MANAGER_ALL_ACCESS = 0xF003F
SC_MANAGER_CONNECT = 0x0001
SC_MANAGER_CREATE_SERVICE = 0x0002
SC_MANAGER_ENUMERATE_SERVICE = 0x0004
SC_MANAGER_LOCK = 0x0008
SC_MANAGER_QUERY_LOCK_STATUS = 0x0010
SC_MANAGER_MODIFY_BOOT_CONFIG = 0x0020

SERVICE_BOOT_START = 0x00000000
SERVICE_SYSTEM_START = 0x00000001
SERVICE_AUTO_START = 0x00000002
SERVICE_DEMAND_START = 0x00000003
SERVICE_DISABLED = 0x00000004

SERVICE_ERROR_IGNORE = 0x00000000
SERVICE_ERROR_NORMAL = 0x00000001
SERVICE_ERROR_SEVERE = 0x00000002
SERVICE_ERROR_CRITICAL = 0x00000003

SERVICE_ACTIVE = 1
SERVICE_INACTIVE = 2
SERVICE_STATE_ALL = 3

SERVICE_KERNEL_DRIVER = 0x00000001
SERVICE_FILE_SYSTEM_DRIVER = 0x00000002
SERVICE_ADAPTER = 0x00000004
SERVICE_RECOGNIZER_DRIVER = 0x00000008
SERVICE_WIN32_OWN_PROCESS = 0x00000010
SERVICE_WIN32_SHARE_PROCESS = 0x00000020
SERVICE_INTERACTIVE_PROCESS = 0x00000100

SERVICE_DRIVER = 0x0000000B
SERVICE_WIN32 = 0x00000030

SERVICE_STOPPED = 0x00000001
SERVICE_START_PENDING = 0x00000002
SERVICE_STOP_PENDING = 0x00000003
SERVICE_RUNNING = 0x00000004
SERVICE_CONTINUE_PENDING = 0x00000005
SERVICE_PAUSE_PENDING = 0x00000006
SERVICE_PAUSED = 0x00000007

SERVICE_ACCEPT_STOP = 0x00000001
SERVICE_ACCEPT_PAUSE_CONTINUE = 0x00000002
SERVICE_ACCEPT_SHUTDOWN = 0x00000004
SERVICE_ACCEPT_PARAMCHANGE = 0x00000008
SERVICE_ACCEPT_NETBINDCHANGE = 0x00000010
SERVICE_ACCEPT_HARDWAREPROFILECHANGE = 0x00000020
SERVICE_ACCEPT_POWEREVENT = 0x00000040
SERVICE_ACCEPT_SESSIONCHANGE = 0x00000080
SERVICE_ACCEPT_PRESHUTDOWN = 0x00000100

SERVICE_RUNS_IN_SYSTEM_PROCESS = 0x00000001

SERVICE_CONTROL_STOP = 0x00000001
SERVICE_CONTROL_PAUSE = 0x00000002
SERVICE_CONTROL_CONTINUE = 0x00000003
SERVICE_CONTROL_INTERROGATE = 0x00000004
SERVICE_CONTROL_SHUTDOWN = 0x00000005
SERVICE_CONTROL_PARAMCHANGE = 0x00000006
SERVICE_CONTROL_NETBINDADD = 0x00000007
SERVICE_CONTROL_NETBINDREMOVE = 0x00000008
SERVICE_CONTROL_NETBINDENABLE = 0x00000009
SERVICE_CONTROL_NETBINDDISABLE = 0x0000000A
SERVICE_CONTROL_DEVICEEVENT = 0x0000000B
SERVICE_CONTROL_HARDWAREPROFILECHANGE = 0x0000000C
SERVICE_CONTROL_POWEREVENT = 0x0000000D
SERVICE_CONTROL_SESSIONCHANGE = 0x0000000E

SERVICE_ACCEPT_STOP = 0x00000001
SERVICE_ACCEPT_PAUSE_CONTINUE = 0x00000002
SERVICE_ACCEPT_SHUTDOWN = 0x00000004
SERVICE_ACCEPT_PARAMCHANGE = 0x00000008
SERVICE_ACCEPT_NETBINDCHANGE = 0x00000010
SERVICE_ACCEPT_HARDWAREPROFILECHANGE = 0x00000020
SERVICE_ACCEPT_POWEREVENT = 0x00000040
SERVICE_ACCEPT_SESSIONCHANGE = 0x00000080
SERVICE_ACCEPT_PRESHUTDOWN = 0x00000100
SERVICE_ACCEPT_TIMECHANGE = 0x00000200
SERVICE_ACCEPT_TRIGGEREVENT = 0x00000400
SERVICE_ACCEPT_USERMODEREBOOT = 0x00000800

SC_ACTION_NONE = 0
SC_ACTION_RESTART = 1
SC_ACTION_REBOOT = 2
SC_ACTION_RUN_COMMAND = 3

SERVICE_CONFIG_DESCRIPTION = 1
SERVICE_CONFIG_FAILURE_ACTIONS = 2


class SERVICE_STATUS(Structure):
    _fields_ = [
        ("dwServiceType", DWORD),
        ("dwCurrentState", DWORD),
        ("dwControlsAccepted", DWORD),
        ("dwWin32ExitCode", DWORD),
        ("dwServiceSpecificExitCode", DWORD),
        ("dwCheckPoint", DWORD),
        ("dwWaitHint", DWORD),
    ]


LPSERVICE_STATUS = POINTER(SERVICE_STATUS)


class SERVICE_STATUS_PROCESS(Structure):
    _fields_ = SERVICE_STATUS._fields_ + [
        ("dwProcessId", DWORD),
        ("dwServiceFlags", DWORD),
    ]


LPSERVICE_STATUS_PROCESS = POINTER(SERVICE_STATUS_PROCESS)


class ENUM_SERVICE_STATUSA(Structure):
    _fields_ = [
        ("lpServiceName", LPSTR),
        ("lpDisplayName", LPSTR),
        ("ServiceStatus", SERVICE_STATUS),
    ]


class ENUM_SERVICE_STATUSW(Structure):
    _fields_ = [
        ("lpServiceName", LPWSTR),
        ("lpDisplayName", LPWSTR),
        ("ServiceStatus", SERVICE_STATUS),
    ]


LPENUM_SERVICE_STATUSA = POINTER(ENUM_SERVICE_STATUSA)
LPENUM_SERVICE_STATUSW = POINTER(ENUM_SERVICE_STATUSW)


class ENUM_SERVICE_STATUS_PROCESSA(Structure):
    _fields_ = [
        ("lpServiceName", LPSTR),
        ("lpDisplayName", LPSTR),
        ("ServiceStatusProcess", SERVICE_STATUS_PROCESS),
    ]


class ENUM_SERVICE_STATUS_PROCESSW(Structure):
    _fields_ = [
        ("lpServiceName", LPWSTR),
        ("lpDisplayName", LPWSTR),
        ("ServiceStatusProcess", SERVICE_STATUS_PROCESS),
    ]


LPENUM_SERVICE_STATUS_PROCESSA = POINTER(ENUM_SERVICE_STATUS_PROCESSA)
LPENUM_SERVICE_STATUS_PROCESSW = POINTER(ENUM_SERVICE_STATUS_PROCESSW)


class ServiceStatus(object):

    def __init__(self, raw):
        self.ServiceType = raw.dwServiceType
        self.CurrentState = raw.dwCurrentState
        self.ControlsAccepted = raw.dwControlsAccepted
        self.Win32ExitCode = raw.dwWin32ExitCode
        self.ServiceSpecificExitCode = raw.dwServiceSpecificExitCode
        self.CheckPoint = raw.dwCheckPoint
        self.WaitHint = raw.dwWaitHint


class ServiceStatusProcess(object):

    def __init__(self, raw):
        self.ServiceType = raw.dwServiceType
        self.CurrentState = raw.dwCurrentState
        self.ControlsAccepted = raw.dwControlsAccepted
        self.Win32ExitCode = raw.dwWin32ExitCode
        self.ServiceSpecificExitCode = raw.dwServiceSpecificExitCode
        self.CheckPoint = raw.dwCheckPoint
        self.WaitHint = raw.dwWaitHint
        self.ProcessId = raw.dwProcessId
        self.ServiceFlags = raw.dwServiceFlags


class ServiceStatusEntry(object):

    def __init__(self, raw):

        self.ServiceName = raw.lpServiceName
        self.DisplayName = raw.lpDisplayName
        self.ServiceType = raw.ServiceStatus.dwServiceType
        self.CurrentState = raw.ServiceStatus.dwCurrentState
        self.ControlsAccepted = raw.ServiceStatus.dwControlsAccepted
        self.Win32ExitCode = raw.ServiceStatus.dwWin32ExitCode
        self.ServiceSpecificExitCode = raw.ServiceStatus.dwServiceSpecificExitCode
        self.CheckPoint = raw.ServiceStatus.dwCheckPoint
        self.WaitHint = raw.ServiceStatus.dwWaitHint

    def __str__(self):
        output = []
        if self.ServiceType & SERVICE_INTERACTIVE_PROCESS:
            output.append("Interactive service")
        else:
            output.append("Service")
        if self.DisplayName:
            output.append("\"%s\" (%s)" % (self.DisplayName, self.ServiceName))
        else:
            output.append("\"%s\"" % self.ServiceName)
        if self.CurrentState == SERVICE_CONTINUE_PENDING:
            output.append("is about to continue.")
        elif self.CurrentState == SERVICE_PAUSE_PENDING:
            output.append("is pausing.")
        elif self.CurrentState == SERVICE_PAUSED:
            output.append("is paused.")
        elif self.CurrentState == SERVICE_RUNNING:
            output.append("is running.")
        elif self.CurrentState == SERVICE_START_PENDING:
            output.append("is starting.")
        elif self.CurrentState == SERVICE_STOP_PENDING:
            output.append("is stopping.")
        elif self.CurrentState == SERVICE_STOPPED:
            output.append("is stopped.")
        return " ".join(output)


class ServiceStatusProcessEntry(object):

    def __init__(self, raw):

        self.ServiceName = raw.lpServiceName
        self.DisplayName = raw.lpDisplayName
        self.ServiceType = raw.ServiceStatusProcess.dwServiceType
        self.CurrentState = raw.ServiceStatusProcess.dwCurrentState
        self.ControlsAccepted = raw.ServiceStatusProcess.dwControlsAccepted
        self.Win32ExitCode = raw.ServiceStatusProcess.dwWin32ExitCode
        self.ServiceSpecificExitCode = raw.ServiceStatusProcess.dwServiceSpecificExitCode
        self.CheckPoint = raw.ServiceStatusProcess.dwCheckPoint
        self.WaitHint = raw.ServiceStatusProcess.dwWaitHint
        self.ProcessId = raw.ServiceStatusProcess.dwProcessId
        self.ServiceFlags = raw.ServiceStatusProcess.dwServiceFlags

    def __str__(self):
        output = []
        if self.ServiceType & SERVICE_INTERACTIVE_PROCESS:
            output.append("Interactive service ")
        else:
            output.append("Service ")
        if self.DisplayName:
            output.append("\"%s\" (%s)" % (self.DisplayName, self.ServiceName))
        else:
            output.append("\"%s\"" % self.ServiceName)
        if self.CurrentState == SERVICE_CONTINUE_PENDING:
            output.append(" is about to continue")
        elif self.CurrentState == SERVICE_PAUSE_PENDING:
            output.append(" is pausing")
        elif self.CurrentState == SERVICE_PAUSED:
            output.append(" is paused")
        elif self.CurrentState == SERVICE_RUNNING:
            output.append(" is running")
        elif self.CurrentState == SERVICE_START_PENDING:
            output.append(" is starting")
        elif self.CurrentState == SERVICE_STOP_PENDING:
            output.append(" is stopping")
        elif self.CurrentState == SERVICE_STOPPED:
            output.append(" is stopped")
        if self.ProcessId:
            output.append(" at process %d" % self.ProcessId)
        output.append(".")
        return "".join(output)


class TokenHandle(HANDLE):
    pass


class RegistryKeyHandle(UserModeHandle):
    _TYPE = HKEY

    def _close(self):
        RegCloseKey(self.value)


class SaferLevelHandle(UserModeHandle):
    _TYPE = SAFER_LEVEL_HANDLE

    def _close(self):
        SaferCloseLevel(self.value)


class ServiceHandle(UserModeHandle):
    _TYPE = SC_HANDLE

    def _close(self):
        CloseServiceHANDLE(self.value)


class ServiceControlManagerHandle(UserModeHandle):
    _TYPE = SC_HANDLE

    def _close(self):
        CloseServiceHANDLE(self.value)


def GetUserNameA():
    _GetUserNameA = windll.advapi32.GetUserNameA
    _GetUserNameA.argtypes = [LPSTR, LPDWORD]
    _GetUserNameA.restype = bool

    nSize = DWORD(0)
    _GetUserNameA(None, byref(nSize))
    error = GetLastError()
    if error != ERROR_INSUFFICIENT_BUFFER:
        raise ctypes.WinError(error)
    lpBuffer = ctypes.create_string_buffer('', nSize.value + 1)
    success = _GetUserNameA(lpBuffer, byref(nSize))
    if not success:
        raise ctypes.WinError()
    return lpBuffer.value


def GetUserNameW():
    _GetUserNameW = windll.advapi32.GetUserNameW
    _GetUserNameW.argtypes = [LPWSTR, LPDWORD]
    _GetUserNameW.restype = bool

    nSize = DWORD(0)
    _GetUserNameW(None, byref(nSize))
    error = GetLastError()
    if error != ERROR_INSUFFICIENT_BUFFER:
        raise ctypes.WinError(error)
    lpBuffer = ctypes.create_unicode_buffer(u'', nSize.value + 1)
    success = _GetUserNameW(lpBuffer, byref(nSize))
    if not success:
        raise ctypes.WinError()
    return lpBuffer.value


GetUserName = DefaultStringType(GetUserNameA, GetUserNameW)


def LookupAccountNameA(lpSystemName, lpAccountName):
    _LookupAccountNameA = windll.advapi32.LookupAccountNameA
    _LookupAccountNameA.argtypes = [LPSTR, LPSTR, PSID, LPDWORD, LPSTR, LPDWORD, LPDWORD]
    _LookupAccountNameA.restype = BOOL

    cbSid = DWORD(0)
    cchReferencedDomainName = DWORD(0)
    peUse = DWORD(0)
    _LookupAccountNameA(lpSystemName, lpAccountName, None, byref(cbSid), None, byref(cchReferencedDomainName),
                        byref(peUse))
    error = GetLastError()
    if error != ERROR_INSUFFICIENT_BUFFER:
        raise (ctypes.WinError(error))
    sid = ctypes.create_string_buffer('', cbSid.value)
    psid = ctypes.cast(ctypes.pointer(sid), PSID)
    lpReferencedDomainName = ctypes.create_string_buffer('', cchReferencedDomainName.value + 1)
    success = _LookupAccountNameA(lpSystemName, lpAccountName, psid, byref(cbSid), lpReferencedDomainName,
                                  byref(cchReferencedDomainName), byref(peUse))
    if not success:
        raise ctypes.WinError()
    return psid, lpReferencedDomainName.value, peUse.value


def LookupAccountNameW(lpSystemName, lpAccountName):
    _LookupAccountNameW = windll.advapi32.LookupAccountNameW
    _LookupAccountNameW.argtypes = [LPWSTR, LPWSTR, PSID, LPDWORD, LPWSTR, LPDWORD, LPDWORD]
    _LookupAccountNameW.restype = BOOL

    cbSid = DWORD(0)
    cchReferencedDomainName = DWORD(0)
    peUse = DWORD(0)
    _LookupAccountNameW(lpSystemName, lpAccountName, None, byref(cbSid), None, byref(cchReferencedDomainName),
                        byref(peUse))
    error = GetLastError()
    if error != ERROR_INSUFFICIENT_BUFFER:
        raise (ctypes.WinError(error))
    sid = ctypes.create_string_buffer('', cbSid.value)
    psid = ctypes.cast(ctypes.pointer(sid), PSID)
    lpReferencedDomainName = ctypes.create_unicode_buffer(u'', cchReferencedDomainName.value + 1)
    success = _LookupAccountNameW(lpSystemName, lpAccountName, psid, byref(cbSid), lpReferencedDomainName,
                                  byref(cchReferencedDomainName), byref(peUse))
    if not success:
        raise ctypes.WinError()
    return psid, lpReferencedDomainName.value, peUse.value


LookupAccountName = GuessStringType(LookupAccountNameA, LookupAccountNameW)


def LookupAccountSidA(lpSystemName, lpSid):
    _LookupAccountSidA = windll.advapi32.LookupAccountSidA
    _LookupAccountSidA.argtypes = [LPSTR, PSID, LPSTR, LPDWORD, LPSTR, LPDWORD, LPDWORD]
    _LookupAccountSidA.restype = bool

    cchName = DWORD(0)
    cchReferencedDomainName = DWORD(0)
    peUse = DWORD(0)
    _LookupAccountSidA(lpSystemName, lpSid, None, byref(cchName), None, byref(cchReferencedDomainName), byref(peUse))
    error = GetLastError()
    if error != ERROR_INSUFFICIENT_BUFFER:
        raise ctypes.WinError(error)
    lpName = ctypes.create_string_buffer('', cchName + 1)
    lpReferencedDomainName = ctypes.create_string_buffer('', cchReferencedDomainName + 1)
    success = _LookupAccountSidA(lpSystemName, lpSid, lpName, byref(cchName), lpReferencedDomainName,
                                 byref(cchReferencedDomainName), byref(peUse))
    if not success:
        raise ctypes.WinError()
    return lpName.value, lpReferencedDomainName.value, peUse.value


def LookupAccountSidW(lpSystemName, lpSid):
    _LookupAccountSidW = windll.advapi32.LookupAccountSidW
    _LookupAccountSidW.argtypes = [LPSTR, PSID, LPWSTR, LPDWORD, LPWSTR, LPDWORD, LPDWORD]
    _LookupAccountSidW.restype = bool

    cchName = DWORD(0)
    cchReferencedDomainName = DWORD(0)
    peUse = DWORD(0)
    _LookupAccountSidW(lpSystemName, lpSid, None, byref(cchName), None, byref(cchReferencedDomainName), byref(peUse))
    error = GetLastError()
    if error != ERROR_INSUFFICIENT_BUFFER:
        raise ctypes.WinError(error)
    lpName = ctypes.create_unicode_buffer(u'', cchName.value + 1)
    lpReferencedDomainName = ctypes.create_unicode_buffer(u'', cchReferencedDomainName.value + 1)
    success = _LookupAccountSidW(lpSystemName, lpSid, lpName, byref(cchName), lpReferencedDomainName,
                                 byref(cchReferencedDomainName), byref(peUse))
    if not success:
        raise ctypes.WinError()
    return lpName.value, lpReferencedDomainName.value, peUse.value


LookupAccountSid = GuessStringType(LookupAccountSidA, LookupAccountSidW)


def ConvertSidToStringSidA(Sid):
    _ConvertSidToStringSidA = windll.advapi32.ConvertSidToStringSidA
    _ConvertSidToStringSidA.argtypes = [PSID, POINTER(LPSTR)]
    _ConvertSidToStringSidA.restype = bool
    _ConvertSidToStringSidA.errcheck = RaiseIfZero

    pStringSid = LPSTR()
    _ConvertSidToStringSidA(Sid, byref(pStringSid))
    try:
        StringSid = pStringSid.value
    finally:
        LocalFree(pStringSid)
    return StringSid.decode()


def ConvertSidToStringSidW(Sid):
    _ConvertSidToStringSidW = windll.advapi32.ConvertSidToStringSidW
    _ConvertSidToStringSidW.argtypes = [PSID, POINTER(LPWSTR)]
    _ConvertSidToStringSidW.restype = bool
    _ConvertSidToStringSidW.errcheck = RaiseIfZero

    pStringSid = LPWSTR()
    _ConvertSidToStringSidW(Sid, byref(pStringSid))
    try:
        StringSid = pStringSid.value
    finally:
        LocalFree(pStringSid)
    return StringSid


ConvertSidToStringSid = DefaultStringType(ConvertSidToStringSidA, ConvertSidToStringSidW)


def ConvertStringSidToSidA(StringSid):
    _ConvertStringSidToSidA = windll.advapi32.ConvertStringSidToSidA
    _ConvertStringSidToSidA.argtypes = [LPSTR, PVOID]
    _ConvertStringSidToSidA.restype = bool
    _ConvertStringSidToSidA.errcheck = RaiseIfZero

    Sid = PVOID()
    _ConvertStringSidToSidA(StringSid, ctypes.pointer(Sid))
    return Sid.value


def ConvertStringSidToSidW(StringSid):
    _ConvertStringSidToSidW = windll.advapi32.ConvertStringSidToSidW
    _ConvertStringSidToSidW.argtypes = [LPWSTR, PVOID]
    _ConvertStringSidToSidW.restype = bool
    _ConvertStringSidToSidW.errcheck = RaiseIfZero

    Sid = PVOID()
    _ConvertStringSidToSidW(StringSid, ctypes.pointer(Sid))
    return Sid.value


ConvertStringSidToSid = GuessStringType(ConvertStringSidToSidA, ConvertStringSidToSidW)


def IsValidSid(pSid):
    _IsValidSid = windll.advapi32.IsValidSid
    _IsValidSid.argtypes = [PSID]
    _IsValidSid.restype = bool
    return _IsValidSid(pSid)


def EqualSid(pSid1, pSid2):
    _EqualSid = windll.advapi32.EqualSid
    _EqualSid.argtypes = [PSID, PSID]
    _EqualSid.restype = bool
    return _EqualSid(pSid1, pSid2)


def GetLengthSid(pSid):
    _GetLengthSid = windll.advapi32.GetLengthSid
    _GetLengthSid.argtypes = [PSID]
    _GetLengthSid.restype = DWORD
    return _GetLengthSid(pSid)


def CopySid(pSourceSid):
    _CopySid = windll.advapi32.CopySid
    _CopySid.argtypes = [DWORD, PVOID, PSID]
    _CopySid.restype = bool
    _CopySid.errcheck = RaiseIfZero

    nDestinationSidLength = GetLengthSid(pSourceSid)
    DestinationSid = ctypes.create_string_buffer('', nDestinationSidLength)
    pDestinationSid = ctypes.cast(ctypes.pointer(DestinationSid), PVOID)
    _CopySid(nDestinationSidLength, pDestinationSid, pSourceSid)
    return ctypes.cast(pDestinationSid, PSID)


def FreeSid(pSid):
    _FreeSid = windll.advapi32.FreeSid
    _FreeSid.argtypes = [PSID]
    _FreeSid.restype = PSID
    _FreeSid.errcheck = RaiseIfNotZero
    _FreeSid(pSid)


def OpenProcessToken(ProcessHANDLE, DesiredAccess=TOKEN_ALL_ACCESS):
    _OpenProcessToken = windll.advapi32.OpenProcessToken
    _OpenProcessToken.argtypes = [HANDLE, DWORD, PHANDLE]
    _OpenProcessToken.restype = bool
    _OpenProcessToken.errcheck = RaiseIfZero

    NewTokenHandle = HANDLE(INVALID_HANDLE_VALUE)
    _OpenProcessToken(ProcessHANDLE, DesiredAccess, byref(NewTokenHandle))
    return TokenHandle(NewTokenHandle.value)


def OpenThreadToken(ThreadHANDLE, DesiredAccess, OpenAsSelf=True):
    _OpenThreadToken = windll.advapi32.OpenThreadToken
    _OpenThreadToken.argtypes = [HANDLE, DWORD, BOOL, PHANDLE]
    _OpenThreadToken.restype = bool
    _OpenThreadToken.errcheck = RaiseIfZero

    NewTokenHandle = HANDLE(INVALID_HANDLE_VALUE)
    _OpenThreadToken(ThreadHANDLE, DesiredAccess, OpenAsSelf, byref(NewTokenHandle))
    return TokenHandle(NewTokenHandle.value)


def DuplicateToken(ExistingTokenHandle, ImpersonationLevel=SecurityImpersonation):
    _DuplicateToken = windll.advapi32.DuplicateToken
    _DuplicateToken.argtypes = [HANDLE, SECURITY_IMPERSONATION_LEVEL, PHANDLE]
    _DuplicateToken.restype = bool
    _DuplicateToken.errcheck = RaiseIfZero

    DuplicateTokenHandle = HANDLE(INVALID_HANDLE_VALUE)
    _DuplicateToken(ExistingTokenHandle, ImpersonationLevel, byref(DuplicateTokenHandle))
    return TokenHandle(DuplicateTokenHandle.value)


def DuplicateTokenEx(hExistingToken, dwDesiredAccess=TOKEN_ALL_ACCESS, lpTokenAttributes=None,
                     ImpersonationLevel=SecurityImpersonation, TokenType=TokenPrimary):
    _DuplicateTokenEx = windll.advapi32.DuplicateTokenEx
    _DuplicateTokenEx.argtypes = [HANDLE, DWORD, LPSECURITY_ATTRIBUTES, SECURITY_IMPERSONATION_LEVEL, TOKEN_TYPE,
                                  PHANDLE]
    _DuplicateTokenEx.restype = bool
    _DuplicateTokenEx.errcheck = RaiseIfZero

    DuplicateTokenHandle = HANDLE(INVALID_HANDLE_VALUE)
    _DuplicateTokenEx(hExistingToken, dwDesiredAccess, lpTokenAttributes, ImpersonationLevel, TokenType,
                      byref(DuplicateTokenHandle))
    return TokenHandle(DuplicateTokenHandle.value)


def IsTokenRestricted(hTokenHandle):
    _IsTokenRestricted = windll.advapi32.IsTokenRestricted
    _IsTokenRestricted.argtypes = [HANDLE]
    _IsTokenRestricted.restype = bool
    _IsTokenRestricted.errcheck = RaiseIfNotErrorSuccess

    SetLastError(ERROR_SUCCESS)
    return _IsTokenRestricted(hTokenHandle)


def LookupPrivilegeValueA(lpSystemName, lpName):
    _LookupPrivilegeValueA = windll.advapi32.LookupPrivilegeValueA
    _LookupPrivilegeValueA.argtypes = [LPSTR, LPSTR, PLUID]
    _LookupPrivilegeValueA.restype = bool
    _LookupPrivilegeValueA.errcheck = RaiseIfZero

    lpLuid = LUID()
    if not lpSystemName:
        lpSystemName = None
    _LookupPrivilegeValueA(lpSystemName, lpName, byref(lpLuid))
    return lpLuid


def LookupPrivilegeValueW(lpSystemName, lpName):
    _LookupPrivilegeValueW = windll.advapi32.LookupPrivilegeValueW
    _LookupPrivilegeValueW.argtypes = [LPWSTR, LPWSTR, PLUID]
    _LookupPrivilegeValueW.restype = bool
    _LookupPrivilegeValueW.errcheck = RaiseIfZero

    lpLuid = LUID()
    if not lpSystemName:
        lpSystemName = None
    _LookupPrivilegeValueW(lpSystemName, lpName, byref(lpLuid))
    return lpLuid


LookupPrivilegeValue = GuessStringType(LookupPrivilegeValueA, LookupPrivilegeValueW)


def LookupPrivilegeNameA(lpSystemName, lpLuid):
    _LookupPrivilegeNameA = windll.advapi32.LookupPrivilegeNameA
    _LookupPrivilegeNameA.argtypes = [LPSTR, PLUID, LPSTR, LPDWORD]
    _LookupPrivilegeNameA.restype = bool
    _LookupPrivilegeNameA.errcheck = RaiseIfZero

    cchName = DWORD(0)
    _LookupPrivilegeNameA(lpSystemName, byref(lpLuid), NULL, byref(cchName))
    lpName = ctypes.create_string_buffer("", cchName.value)
    _LookupPrivilegeNameA(lpSystemName, byref(lpLuid), byref(lpName), byref(cchName))
    return lpName.value


def LookupPrivilegeNameW(lpSystemName, lpLuid):
    _LookupPrivilegeNameW = windll.advapi32.LookupPrivilegeNameW
    _LookupPrivilegeNameW.argtypes = [LPWSTR, PLUID, LPWSTR, LPDWORD]
    _LookupPrivilegeNameW.restype = bool
    _LookupPrivilegeNameW.errcheck = RaiseIfZero

    cchName = DWORD(0)
    _LookupPrivilegeNameW(lpSystemName, byref(lpLuid), NULL, byref(cchName))
    lpName = ctypes.create_unicode_buffer(u"", cchName.value)
    _LookupPrivilegeNameW(lpSystemName, byref(lpLuid), byref(lpName), byref(cchName))
    return lpName.value


LookupPrivilegeName = GuessStringType(LookupPrivilegeNameA, LookupPrivilegeNameW)


def AdjustTokenPrivileges(TokenHandle, NewState=()):
    _AdjustTokenPrivileges = windll.advapi32.AdjustTokenPrivileges
    _AdjustTokenPrivileges.argtypes = [HANDLE, BOOL, LPVOID, DWORD, LPVOID, LPVOID]
    _AdjustTokenPrivileges.restype = bool

    if not NewState:
        _AdjustTokenPrivileges.errcheck = RaiseIfZero
        _AdjustTokenPrivileges(TokenHandle, TRUE, NULL, 0, NULL, NULL)
    else:
        success = True
        errcode = 0
        for (privilege, enabled) in NewState:
            if not isinstance(privilege, LUID):
                privilege = LookupPrivilegeValue(NULL, privilege)
            if enabled == True:
                flags = SE_PRIVILEGE_ENABLED
            elif enabled == False:
                flags = SE_PRIVILEGE_REMOVED
            elif enabled == None:
                flags = 0
            else:
                flags = enabled
            laa = LUID_AND_ATTRIBUTES(privilege, flags)
            tp = TOKEN_PRIVILEGES(1, laa)
            if _AdjustTokenPrivileges(TokenHandle, FALSE, byref(tp), sizeof(tp), NULL, NULL) == 0:
                success = False
                errcode = GetLastError()
        if not success:
            raise ctypes.WinError(errcode)


def GetTokenInformation(hTokenHandle, TokenInformationClass):
    if TokenInformationClass <= 0 or TokenInformationClass > MaxTokenInfoClass:
        raise ValueError("Invalid value for TokenInformationClass (%i)" % TokenInformationClass)

    if TokenInformationClass == TokenUser:
        TokenInformation = TOKEN_USER()
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.User.Sid.value

    if TokenInformationClass == TokenOwner:
        TokenInformation = TOKEN_OWNER()
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.Owner.value

    if TokenInformationClass == TokenOwner:
        TokenInformation = TOKEN_PRIMARY_GROUP()
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.PrimaryGroup.value

    if TokenInformationClass == TokenAppContainerSid:
        TokenInformation = TOKEN_APPCONTAINER_INFORMATION()
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.TokenAppContainer.value

    if TokenInformationClass == TokenIntegrityLevel:
        TokenInformation = TOKEN_MANDATORY_LABEL()
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.Label.Sid.value, TokenInformation.Label.Attributes

    if TokenInformationClass == TokenOrigin:
        TokenInformation = TOKEN_ORIGIN()
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.OriginatingLogonSession

    if TokenInformationClass == TokenType:
        TokenInformation = TOKEN_TYPE(0)
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.value

    if TokenInformationClass == TokenElevation:
        TokenInformation = TOKEN_ELEVATION(0)
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.value

    if TokenInformationClass == TokenElevation:
        TokenInformation = SECURITY_IMPERSONATION_LEVEL(0)
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.value

    if TokenInformationClass in (TokenSessionId, TokenAppContainerNumber):
        TokenInformation = DWORD(0)
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation.value

    if TokenInformationClass in (TokenSandBoxInert, TokenHasRestrictions, TokenUIAccess,
                                 TokenVirtualizationAllowed, TokenVirtualizationEnabled):
        TokenInformation = DWORD(0)
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return bool(TokenInformation.value)

    if TokenInformationClass == TokenLinkedToken:
        TokenInformation = TOKEN_LINKED_TOKEN(0)
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenHandle(TokenInformation.LinkedToken.value, bOwnership=True)

    if TokenInformationClass == TokenStatistics:
        TokenInformation = TOKEN_STATISTICS()
        _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation)
        return TokenInformation

    raise NotImplementedError("TokenInformationClass(%i) not yet supported!" % TokenInformationClass)


def _internal_GetTokenInformation(hTokenHandle, TokenInformationClass, TokenInformation):
    _GetTokenInformation = windll.advapi32.GetTokenInformation
    _GetTokenInformation.argtypes = [HANDLE, TOKEN_INFORMATION_CLASS, LPVOID, DWORD, PDWORD]
    _GetTokenInformation.restype = bool
    _GetTokenInformation.errcheck = RaiseIfZero

    ReturnLength = DWORD(0)
    TokenInformationLength = sizeof(TokenInformation)
    _GetTokenInformation(hTokenHandle, TokenInformationClass, byref(TokenInformation), TokenInformationLength,
                         byref(ReturnLength))
    if ReturnLength.value != TokenInformationLength:
        raise ctypes.WinError(ERROR_INSUFFICIENT_BUFFER)

    return TokenInformation


def GetTokenInformation_sid(hTokenHandle):
    _GetTokenInformation = windll.advapi32.GetTokenInformation
    _GetTokenInformation.argtypes = [HANDLE, TOKEN_INFORMATION_CLASS, LPVOID, DWORD, PDWORD]
    _GetTokenInformation.restype = bool
    _GetTokenInformation.errcheck = RaiseIfZero

    ReturnLength = DWORD(0)
    try:

        _GetTokenInformation(hTokenHandle, 1, None, ReturnLength, byref(ReturnLength))
    except Exception as e:
        pass

    TokenInformationLength = ReturnLength.value
    ReturnLength = DWORD(0)
    ti = (BYTE * TokenInformationLength)()
    _GetTokenInformation(hTokenHandle, 1, byref(ti), TokenInformationLength, byref(ReturnLength))
    if ReturnLength.value != TokenInformationLength:
        raise ctypes.WinError(ERROR_INSUFFICIENT_BUFFER)

    t = ctypes.cast(ti, POINTER(TOKEN_USER)).contents
    return t.User.Sid


def CreateProcessWithLogonW(lpUsername=None, lpDomain=None, lpPassword=None, dwLogonFlags=0, lpApplicationName=None,
                            lpCommandLine=None, dwCreationFlags=0, lpEnvironment=None, lpCurrentDirectory=None,
                            lpStartupInfo=None):
    _CreateProcessWithLogonW = windll.advapi32.CreateProcessWithLogonW
    _CreateProcessWithLogonW.argtypes = [LPWSTR, LPWSTR, LPWSTR, DWORD, LPWSTR, LPWSTR, DWORD, LPVOID, LPWSTR, LPVOID,
                                         LPPROCESS_INFORMATION]
    _CreateProcessWithLogonW.restype = bool
    _CreateProcessWithLogonW.errcheck = RaiseIfZero

    if not lpUsername:
        lpUsername = None
    if not lpDomain:
        lpDomain = None
    if not lpPassword:
        lpPassword = None
    if not lpApplicationName:
        lpApplicationName = None
    if not lpCommandLine:
        lpCommandLine = None
    else:
        lpCommandLine = ctypes.create_unicode_buffer(lpCommandLine, max(MAX_PATH, len(lpCommandLine) + 1))
    if not lpEnvironment:
        lpEnvironment = None
    else:
        lpEnvironment = ctypes.create_unicode_buffer(lpEnvironment)
    if not lpCurrentDirectory:
        lpCurrentDirectory = None
    if not lpStartupInfo:
        lpStartupInfo = STARTUPINFOW()
        lpStartupInfo.cb = sizeof(STARTUPINFOW)
        lpStartupInfo.lpReserved = 0
        lpStartupInfo.lpDesktop = 0
        lpStartupInfo.lpTitle = 0
        lpStartupInfo.dwFlags = 0
        lpStartupInfo.cbReserved2 = 0
        lpStartupInfo.lpReserved2 = 0
    lpProcessInformation = PROCESS_INFORMATION()
    lpProcessInformation.hProcess = INVALID_HANDLE_VALUE
    lpProcessInformation.hThread = INVALID_HANDLE_VALUE
    lpProcessInformation.dwProcessId = 0
    lpProcessInformation.dwThreadId = 0
    _CreateProcessWithLogonW(lpUsername, lpDomain, lpPassword, dwLogonFlags, lpApplicationName, lpCommandLine,
                             dwCreationFlags, lpEnvironment, lpCurrentDirectory, byref(lpStartupInfo),
                             byref(lpProcessInformation))
    return lpProcessInformation


CreateProcessWithLogonA = MakeANSIVersion(CreateProcessWithLogonW)
CreateProcessWithLogon = DefaultStringType(CreateProcessWithLogonA, CreateProcessWithLogonW)


def CreateProcessWithTokenW(hToken=None, dwLogonFlags=0, lpApplicationName=None, lpCommandLine=None, dwCreationFlags=0,
                            lpEnvironment=None, lpCurrentDirectory=None, lpStartupInfo=None):
    _CreateProcessWithTokenW = windll.advapi32.CreateProcessWithTokenW
    _CreateProcessWithTokenW.argtypes = [HANDLE, DWORD, LPWSTR, LPWSTR, DWORD, LPVOID, LPWSTR, LPVOID,
                                         LPPROCESS_INFORMATION]
    _CreateProcessWithTokenW.restype = bool
    _CreateProcessWithTokenW.errcheck = RaiseIfZero

    if not hToken:
        hToken = None
    if not lpApplicationName:
        lpApplicationName = None
    if not lpCommandLine:
        lpCommandLine = None
    else:
        lpCommandLine = ctypes.create_unicode_buffer(lpCommandLine, max(MAX_PATH, len(lpCommandLine) + 1))
    if not lpEnvironment:
        lpEnvironment = None
    else:
        lpEnvironment = ctypes.create_unicode_buffer(lpEnvironment)
    if not lpCurrentDirectory:
        lpCurrentDirectory = None
    if not lpStartupInfo:
        lpStartupInfo = STARTUPINFOW()
        lpStartupInfo.cb = sizeof(STARTUPINFOW)
        lpStartupInfo.lpReserved = 0
        lpStartupInfo.lpDesktop = 0
        lpStartupInfo.lpTitle = 0
        lpStartupInfo.dwFlags = 0
        lpStartupInfo.cbReserved2 = 0
        lpStartupInfo.lpReserved2 = 0
    lpProcessInformation = PROCESS_INFORMATION()
    lpProcessInformation.hProcess = INVALID_HANDLE_VALUE
    lpProcessInformation.hThread = INVALID_HANDLE_VALUE
    lpProcessInformation.dwProcessId = 0
    lpProcessInformation.dwThreadId = 0
    _CreateProcessWithTokenW(hToken, dwLogonFlags, lpApplicationName, lpCommandLine, dwCreationFlags, lpEnvironment,
                             lpCurrentDirectory, byref(lpStartupInfo), byref(lpProcessInformation))
    return lpProcessInformation


CreateProcessWithTokenA = MakeANSIVersion(CreateProcessWithTokenW)
CreateProcessWithToken = DefaultStringType(CreateProcessWithTokenA, CreateProcessWithTokenW)


def CreateProcessAsUserA(hToken=None, lpApplicationName=None, lpCommandLine=None, lpProcessAttributes=None,
                         lpThreadAttributes=None, bInheritHANDLEs=False, dwCreationFlags=0, lpEnvironment=None,
                         lpCurrentDirectory=None, lpStartupInfo=None):
    _CreateProcessAsUserA = windll.advapi32.CreateProcessAsUserA
    _CreateProcessAsUserA.argtypes = [HANDLE, LPSTR, LPSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD,
                                      LPVOID, LPSTR, LPVOID, LPPROCESS_INFORMATION]
    _CreateProcessAsUserA.restype = bool
    _CreateProcessAsUserA.errcheck = RaiseIfZero

    if not lpApplicationName:
        lpApplicationName = None
    if not lpCommandLine:
        lpCommandLine = None
    else:
        lpCommandLine = ctypes.create_string_buffer(lpCommandLine.encode('ascii'),
                                                    max(MAX_PATH, len(lpCommandLine) + 1))
    if not lpEnvironment:
        lpEnvironment = None
    else:
        lpEnvironment = ctypes.create_string_buffer(lpEnvironment.encode('ascii'))
    if not lpCurrentDirectory:
        lpCurrentDirectory = None
    if not lpProcessAttributes:
        lpProcessAttributes = None
    else:
        lpProcessAttributes = byref(lpProcessAttributes)
    if not lpThreadAttributes:
        lpThreadAttributes = None
    else:
        lpThreadAttributes = byref(lpThreadAttributes)
    if not lpStartupInfo:
        lpStartupInfo = STARTUPINFO()
        lpStartupInfo.cb = sizeof(STARTUPINFO)
        lpStartupInfo.lpReserved = 0
        lpStartupInfo.lpDesktop = 0
        lpStartupInfo.lpTitle = 0
        lpStartupInfo.dwFlags = 0
        lpStartupInfo.cbReserved2 = 0
        lpStartupInfo.lpReserved2 = 0
    lpProcessInformation = PROCESS_INFORMATION()
    lpProcessInformation.hProcess = INVALID_HANDLE_VALUE
    lpProcessInformation.hThread = INVALID_HANDLE_VALUE
    lpProcessInformation.dwProcessId = 0
    lpProcessInformation.dwThreadId = 0
    _CreateProcessAsUserA(hToken, lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes,
                          bool(bInheritHANDLEs), dwCreationFlags, lpEnvironment, lpCurrentDirectory,
                          byref(lpStartupInfo), byref(lpProcessInformation))
    return lpProcessInformation


def CreateProcessAsUserW(hToken=None, lpApplicationName=None, lpCommandLine=None, lpProcessAttributes=None,
                         lpThreadAttributes=None, bInheritHANDLEs=False, dwCreationFlags=0, lpEnvironment=None,
                         lpCurrentDirectory=None, lpStartupInfo=None):
    _CreateProcessAsUserW = windll.advapi32.CreateProcessAsUserW
    _CreateProcessAsUserW.argtypes = [HANDLE, LPWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD,
                                      LPVOID, LPWSTR, LPVOID, LPPROCESS_INFORMATION]
    _CreateProcessAsUserW.restype = bool
    _CreateProcessAsUserW.errcheck = RaiseIfZero

    if not lpApplicationName:
        lpApplicationName = None
    if not lpCommandLine:
        lpCommandLine = None
    else:
        lpCommandLine = ctypes.create_unicode_buffer(lpCommandLine, max(MAX_PATH, len(lpCommandLine) + 1))
    if not lpEnvironment:
        lpEnvironment = None
    else:
        lpEnvironment = ctypes.create_unicode_buffer(lpEnvironment)
    if not lpCurrentDirectory:
        lpCurrentDirectory = None
    if not lpProcessAttributes:
        lpProcessAttributes = None
    else:
        lpProcessAttributes = byref(lpProcessAttributes)
    if not lpThreadAttributes:
        lpThreadAttributes = None
    else:
        lpThreadAttributes = byref(lpThreadAttributes)
    if not lpStartupInfo:
        lpStartupInfo = STARTUPINFO()
        lpStartupInfo.cb = sizeof(STARTUPINFO)
        lpStartupInfo.lpReserved = 0
        lpStartupInfo.lpDesktop = 0
        lpStartupInfo.lpTitle = 0
        lpStartupInfo.dwFlags = 0
        lpStartupInfo.cbReserved2 = 0
        lpStartupInfo.lpReserved2 = 0
    lpProcessInformation = PROCESS_INFORMATION()
    lpProcessInformation.hProcess = INVALID_HANDLE_VALUE
    lpProcessInformation.hThread = INVALID_HANDLE_VALUE
    lpProcessInformation.dwProcessId = 0
    lpProcessInformation.dwThreadId = 0
    _CreateProcessAsUserW(hToken, lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes,
                          bool(bInheritHANDLEs), dwCreationFlags, lpEnvironment, lpCurrentDirectory,
                          byref(lpStartupInfo), byref(lpProcessInformation))
    return lpProcessInformation


CreateProcessAsUser = GuessStringType(CreateProcessAsUserA, CreateProcessAsUserW)

PWAITCHAINCALLBACK = WINFUNCTYPE(HWCT, DWORD_PTR, DWORD, LPDWORD, PWAITCHAIN_NODE_INFO, LPBOOL)


def OpenThreadWaitChainSession(Flags=0, callback=None):
    _OpenThreadWaitChainSession = windll.advapi32.OpenThreadWaitChainSession
    _OpenThreadWaitChainSession.argtypes = [DWORD, PVOID]
    _OpenThreadWaitChainSession.restype = HWCT
    _OpenThreadWaitChainSession.errcheck = RaiseIfZero

    if callback is not None:
        callback = PWAITCHAINCALLBACK(callback)
    aHANDLE = _OpenThreadWaitChainSession(Flags, callback)
    return ThreadWaitChainSessionHANDLE(aHANDLE)


def GetThreadWaitChain(WctHANDLE, Context=None, Flags=WCTP_GETINFO_ALL_FLAGS, ThreadId=-1,
                       NodeCount=WCT_MAX_NODE_COUNT):
    _GetThreadWaitChain = windll.advapi32.GetThreadWaitChain
    _GetThreadWaitChain.argtypes = [HWCT, LPDWORD, DWORD, DWORD, LPDWORD, PWAITCHAIN_NODE_INFO, LPBOOL]
    _GetThreadWaitChain.restype = bool
    _GetThreadWaitChain.errcheck = RaiseIfZero

    dwNodeCount = DWORD(NodeCount)
    NodeInfoArray = (WAITCHAIN_NODE_INFO * NodeCount)()
    IsCycle = BOOL(0)
    _GetThreadWaitChain(WctHANDLE, Context, Flags, ThreadId, byref(dwNodeCount),
                        ctypes.cast(ctypes.pointer(NodeInfoArray), PWAITCHAIN_NODE_INFO), byref(IsCycle))
    while dwNodeCount.value > NodeCount:
        NodeCount = dwNodeCount.value
        NodeInfoArray = (WAITCHAIN_NODE_INFO * NodeCount)()
        _GetThreadWaitChain(WctHANDLE, Context, Flags, ThreadId, byref(dwNodeCount),
                            ctypes.cast(ctypes.pointer(NodeInfoArray), PWAITCHAIN_NODE_INFO), byref(IsCycle))
    return (
        [WaitChainNodeInfo(NodeInfoArray[index]) for index in xrange(dwNodeCount.value)],
        bool(IsCycle.value)
    )


def CloseThreadWaitChainSession(WctHANDLE):
    _CloseThreadWaitChainSession = windll.advapi32.CloseThreadWaitChainSession
    _CloseThreadWaitChainSession.argtypes = [HWCT]
    _CloseThreadWaitChainSession(WctHANDLE)


def SaferCreateLevel(dwScopeId=SAFER_SCOPEID_USER, dwLevelId=SAFER_LEVELID_NORMALUSER, OpenFlags=0):
    _SaferCreateLevel = windll.advapi32.SaferCreateLevel
    _SaferCreateLevel.argtypes = [DWORD, DWORD, DWORD, POINTER(SAFER_LEVEL_HANDLE), LPVOID]
    _SaferCreateLevel.restype = BOOL
    _SaferCreateLevel.errcheck = RaiseIfZero

    hLevelHANDLE = SAFER_LEVEL_HANDLE(INVALID_HANDLE_VALUE)
    _SaferCreateLevel(dwScopeId, dwLevelId, OpenFlags, byref(hLevelHANDLE), None)
    return SaferLevelHANDLE(hLevelHANDLE.value)


def SaferComputeTokenFromLevel(LevelHANDLE, InAccessToken=None, dwFlags=0):
    _SaferComputeTokenFromLevel = windll.advapi32.SaferComputeTokenFromLevel
    _SaferComputeTokenFromLevel.argtypes = [SAFER_LEVEL_HANDLE, HANDLE, PHANDLE, DWORD, LPDWORD]
    _SaferComputeTokenFromLevel.restype = BOOL
    _SaferComputeTokenFromLevel.errcheck = RaiseIfZero

    OutAccessToken = HANDLE(INVALID_HANDLE_VALUE)
    lpReserved = DWORD(0)
    _SaferComputeTokenFromLevel(LevelHANDLE, InAccessToken, byref(OutAccessToken), dwFlags, byref(lpReserved))
    return TokenHandle(OutAccessToken.value), lpReserved.value


def SaferCloseLevel(hLevelHANDLE):
    _SaferCloseLevel = windll.advapi32.SaferCloseLevel
    _SaferCloseLevel.argtypes = [SAFER_LEVEL_HANDLE]
    _SaferCloseLevel.restype = BOOL
    _SaferCloseLevel.errcheck = RaiseIfZero

    if hasattr(hLevelHANDLE, 'value'):
        _SaferCloseLevel(hLevelHANDLE.value)
    else:
        _SaferCloseLevel(hLevelHANDLE)


def SaferiIsExecutableFileType(szFullPath, bFromShellExecute=False):
    _SaferiIsExecutableFileType = windll.advapi32.SaferiIsExecutableFileType
    _SaferiIsExecutableFileType.argtypes = [LPWSTR, BOOLEAN]
    _SaferiIsExecutableFileType.restype = BOOL
    _SaferiIsExecutableFileType.errcheck = RaiseIfLastError

    SetLastError(ERROR_SUCCESS)
    return bool(_SaferiIsExecutableFileType(unicode(szFullPath), bFromShellExecute))


SaferIsExecutableFileType = SaferiIsExecutableFileType


def RegCloseKey(hKey):
    if hasattr(hKey, 'value'):
        value = hKey.value
    else:
        value = hKey

    if value in (
            HKEY_CLASSES_ROOT,
            HKEY_CURRENT_USER,
            HKEY_LOCAL_MACHINE,
            HKEY_USERS,
            HKEY_PERFORMANCE_DATA,
            HKEY_CURRENT_CONFIG
    ):
        return

    _RegCloseKey = windll.advapi32.RegCloseKey
    _RegCloseKey.argtypes = [HKEY]
    _RegCloseKey.restype = LONG
    _RegCloseKey.errcheck = RaiseIfNotErrorSuccess
    _RegCloseKey(hKey)


def RegConnectRegistryA(lpMachineName=None, hKey=HKEY_LOCAL_MACHINE):
    _RegConnectRegistryA = windll.advapi32.RegConnectRegistryA
    _RegConnectRegistryA.argtypes = [LPSTR, HKEY, PHKEY]
    _RegConnectRegistryA.restype = LONG
    _RegConnectRegistryA.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegConnectRegistryA(lpMachineName, hKey, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


def RegConnectRegistryW(lpMachineName=None, hKey=HKEY_LOCAL_MACHINE):
    _RegConnectRegistryW = windll.advapi32.RegConnectRegistryW
    _RegConnectRegistryW.argtypes = [LPWSTR, HKEY, PHKEY]
    _RegConnectRegistryW.restype = LONG
    _RegConnectRegistryW.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegConnectRegistryW(lpMachineName, hKey, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


RegConnectRegistry = GuessStringType(RegConnectRegistryA, RegConnectRegistryW)


def RegCreateKeyA(hKey=HKEY_LOCAL_MACHINE, lpSubKey=None):
    _RegCreateKeyA = windll.advapi32.RegCreateKeyA
    _RegCreateKeyA.argtypes = [HKEY, LPSTR, PHKEY]
    _RegCreateKeyA.restype = LONG
    _RegCreateKeyA.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegCreateKeyA(hKey, lpSubKey, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


def RegCreateKeyW(hKey=HKEY_LOCAL_MACHINE, lpSubKey=None):
    _RegCreateKeyW = windll.advapi32.RegCreateKeyW
    _RegCreateKeyW.argtypes = [HKEY, LPWSTR, PHKEY]
    _RegCreateKeyW.restype = LONG
    _RegCreateKeyW.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegCreateKeyW(hKey, lpSubKey, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


RegCreateKey = GuessStringType(RegCreateKeyA, RegCreateKeyW)


def RegOpenKeyA(hKey=HKEY_LOCAL_MACHINE, lpSubKey=None):
    _RegOpenKeyA = windll.advapi32.RegOpenKeyA
    _RegOpenKeyA.argtypes = [HKEY, LPSTR, PHKEY]
    _RegOpenKeyA.restype = LONG
    _RegOpenKeyA.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegOpenKeyA(hKey, lpSubKey, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


def RegOpenKeyW(hKey=HKEY_LOCAL_MACHINE, lpSubKey=None):
    _RegOpenKeyW = windll.advapi32.RegOpenKeyW
    _RegOpenKeyW.argtypes = [HKEY, LPWSTR, PHKEY]
    _RegOpenKeyW.restype = LONG
    _RegOpenKeyW.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegOpenKeyW(hKey, lpSubKey, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


RegOpenKey = GuessStringType(RegOpenKeyA, RegOpenKeyW)


def RegOpenKeyExA(hKey=HKEY_LOCAL_MACHINE, lpSubKey=None, samDesired=KEY_ALL_ACCESS):
    _RegOpenKeyExA = windll.advapi32.RegOpenKeyExA
    _RegOpenKeyExA.argtypes = [HKEY, LPSTR, DWORD, REGSAM, PHKEY]
    _RegOpenKeyExA.restype = LONG
    _RegOpenKeyExA.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegOpenKeyExA(hKey, lpSubKey, 0, samDesired, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


def RegOpenKeyExW(hKey=HKEY_LOCAL_MACHINE, lpSubKey=None, samDesired=KEY_ALL_ACCESS):
    _RegOpenKeyExW = windll.advapi32.RegOpenKeyExW
    _RegOpenKeyExW.argtypes = [HKEY, LPWSTR, DWORD, REGSAM, PHKEY]
    _RegOpenKeyExW.restype = LONG
    _RegOpenKeyExW.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegOpenKeyExW(hKey, lpSubKey, 0, samDesired, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


RegOpenKeyEx = GuessStringType(RegOpenKeyExA, RegOpenKeyExW)


def RegOpenCurrentUser(samDesired=KEY_ALL_ACCESS):
    _RegOpenCurrentUser = windll.advapi32.RegOpenCurrentUser
    _RegOpenCurrentUser.argtypes = [REGSAM, PHKEY]
    _RegOpenCurrentUser.restype = LONG
    _RegOpenCurrentUser.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegOpenCurrentUser(samDesired, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


def RegOpenUserClassesRoot(hToken, samDesired=KEY_ALL_ACCESS):
    _RegOpenUserClassesRoot = windll.advapi32.RegOpenUserClassesRoot
    _RegOpenUserClassesRoot.argtypes = [HANDLE, DWORD, REGSAM, PHKEY]
    _RegOpenUserClassesRoot.restype = LONG
    _RegOpenUserClassesRoot.errcheck = RaiseIfNotErrorSuccess

    hkResult = HKEY(INVALID_HANDLE_VALUE)
    _RegOpenUserClassesRoot(hToken, 0, samDesired, byref(hkResult))
    return RegistryKeyHANDLE(hkResult.value)


def RegQueryValueA(hKey, lpSubKey=None):
    _RegQueryValueA = windll.advapi32.RegQueryValueA
    _RegQueryValueA.argtypes = [HKEY, LPSTR, LPVOID, PLONG]
    _RegQueryValueA.restype = LONG
    _RegQueryValueA.errcheck = RaiseIfNotErrorSuccess

    cbValue = LONG(0)
    _RegQueryValueA(hKey, lpSubKey, None, byref(cbValue))
    lpValue = ctypes.create_string_buffer(cbValue.value)
    _RegQueryValueA(hKey, lpSubKey, lpValue, byref(cbValue))
    return lpValue.value


def RegQueryValueW(hKey, lpSubKey=None):
    _RegQueryValueW = windll.advapi32.RegQueryValueW
    _RegQueryValueW.argtypes = [HKEY, LPWSTR, LPVOID, PLONG]
    _RegQueryValueW.restype = LONG
    _RegQueryValueW.errcheck = RaiseIfNotErrorSuccess

    cbValue = LONG(0)
    _RegQueryValueW(hKey, lpSubKey, None, byref(cbValue))
    lpValue = ctypes.create_unicode_buffer(cbValue.value * sizeof(WCHAR))
    _RegQueryValueW(hKey, lpSubKey, lpValue, byref(cbValue))
    return lpValue.value


RegQueryValue = GuessStringType(RegQueryValueA, RegQueryValueW)


def _internal_RegQueryValueEx(ansi, hKey, lpValueName=None, bGetData=True):
    _RegQueryValueEx = _caller_RegQueryValueEx(ansi)

    cbData = DWORD(0)
    dwType = DWORD(-1)
    _RegQueryValueEx(hKey, lpValueName, None, byref(dwType), None, byref(cbData))
    Type = dwType.value

    if not bGetData:
        return cbData.value, Type

    if Type in (REG_DWORD, REG_DWORD_BIG_ENDIAN):
        if cbData.value != 4:
            raise ValueError("REG_DWORD value of size %d" % cbData.value)
        dwData = DWORD(0)
        _RegQueryValueEx(hKey, lpValueName, None, None, byref(dwData), byref(cbData))
        return dwData.value, Type

    if Type == REG_QWORD:
        if cbData.value != 8:
            raise ValueError("REG_QWORD value of size %d" % cbData.value)
        qwData = QWORD(0)
        _RegQueryValueEx(hKey, lpValueName, None, None, byref(qwData), byref(cbData))
        return qwData.value, Type

    if Type in (REG_SZ, REG_EXPAND_SZ):
        if ansi:
            szData = ctypes.create_string_buffer(cbData.value)
        else:
            szData = ctypes.create_unicode_buffer(cbData.value)
        _RegQueryValueEx(hKey, lpValueName, None, None, byref(szData), byref(cbData))
        return szData.value, Type

    if Type == REG_MULTI_SZ:
        if ansi:
            szData = ctypes.create_string_buffer(cbData.value)
        else:
            szData = ctypes.create_unicode_buffer(cbData.value)
        _RegQueryValueEx(hKey, lpValueName, None, None, byref(szData), byref(cbData))
        Data = szData[:]
        if ansi:
            aData = Data.split('\0')
        else:
            aData = Data.split(u'\0')
        aData = [token for token in aData if token]
        return aData, Type

    if Type == REG_LINK:
        szData = ctypes.create_unicode_buffer(cbData.value)
        _RegQueryValueEx(hKey, lpValueName, None, None, byref(szData), byref(cbData))
        return szData.value, Type

    szData = ctypes.create_string_buffer(cbData.value)
    _RegQueryValueEx(hKey, lpValueName, None, None, byref(szData), byref(cbData))
    return szData.raw, Type


def _caller_RegQueryValueEx(ansi):
    if ansi:
        _RegQueryValueEx = windll.advapi32.RegQueryValueExA
        _RegQueryValueEx.argtypes = [HKEY, LPSTR, LPVOID, PDWORD, LPVOID, PDWORD]
    else:
        _RegQueryValueEx = windll.advapi32.RegQueryValueExW
        _RegQueryValueEx.argtypes = [HKEY, LPWSTR, LPVOID, PDWORD, LPVOID, PDWORD]
    _RegQueryValueEx.restype = LONG
    _RegQueryValueEx.errcheck = RaiseIfNotErrorSuccess
    return _RegQueryValueEx


def RegQueryValueExA(hKey, lpValueName=None, bGetData=True):
    return _internal_RegQueryValueEx(True, hKey, lpValueName, bGetData)


def RegQueryValueExW(hKey, lpValueName=None, bGetData=True):
    return _internal_RegQueryValueEx(False, hKey, lpValueName, bGetData)


RegQueryValueEx = GuessStringType(RegQueryValueExA, RegQueryValueExW)


def RegSetValueEx(hKey, lpValueName=None, lpData=None, dwType=None):
    if lpValueName is None:
        if isinstance(lpData, GuessStringType.t_ansi):
            ansi = True
        elif isinstance(lpData, GuessStringType.t_unicode):
            ansi = False
        else:
            ansi = (GuessStringType.t_ansi == GuessStringType.t_default)
    elif isinstance(lpValueName, GuessStringType.t_ansi):
        ansi = True
    elif isinstance(lpValueName, GuessStringType.t_unicode):
        ansi = False
    else:
        raise TypeError("String expected, got %s instead" % type(lpValueName))

    if dwType is None:
        if lpValueName is None:
            dwType = REG_SZ
        elif lpData is None:
            dwType = REG_NONE
        elif isinstance(lpData, GuessStringType.t_ansi):
            dwType = REG_SZ
        elif isinstance(lpData, GuessStringType.t_unicode):
            dwType = REG_SZ
        elif isinstance(lpData, int):
            dwType = REG_DWORD
        elif isinstance(lpData, long):
            dwType = REG_QWORD
        else:
            dwType = REG_BINARY

    if ansi:
        _RegSetValueEx = windll.advapi32.RegSetValueExA
        _RegSetValueEx.argtypes = [HKEY, LPSTR, DWORD, DWORD, LPVOID, DWORD]
    else:
        _RegSetValueEx = windll.advapi32.RegSetValueExW
        _RegSetValueEx.argtypes = [HKEY, LPWSTR, DWORD, DWORD, LPVOID, DWORD]
    _RegSetValueEx.restype = LONG
    _RegSetValueEx.errcheck = RaiseIfNotErrorSuccess

    if lpData is None:
        DataRef = None
        DataSize = 0
    else:
        if dwType in (REG_DWORD, REG_DWORD_BIG_ENDIAN):
            Data = DWORD(lpData)
        elif dwType == REG_QWORD:
            Data = QWORD(lpData)
        elif dwType in (REG_SZ, REG_EXPAND_SZ):
            if ansi:
                Data = ctypes.create_string_buffer(lpData)
            else:
                Data = ctypes.create_unicode_buffer(lpData)
        elif dwType == REG_MULTI_SZ:
            if ansi:
                Data = ctypes.create_string_buffer('\0'.join(lpData) + '\0\0')
            else:
                Data = ctypes.create_unicode_buffer(u'\0'.join(lpData) + u'\0\0')
        elif dwType == REG_LINK:
            Data = ctypes.create_unicode_buffer(lpData)
        else:
            Data = ctypes.create_string_buffer(lpData)
        DataRef = byref(Data)
        DataSize = sizeof(Data)

    _RegSetValueEx(hKey, lpValueName, 0, dwType, DataRef, DataSize)


RegSetValueExA = RegSetValueExW = RegSetValueEx


def RegEnumKeyA(hKey, dwIndex):
    _RegEnumKeyA = windll.advapi32.RegEnumKeyA
    _RegEnumKeyA.argtypes = [HKEY, DWORD, LPSTR, DWORD]
    _RegEnumKeyA.restype = LONG

    cchName = 1024
    while True:
        lpName = ctypes.create_string_buffer(cchName)
        errcode = _RegEnumKeyA(hKey, dwIndex, lpName, cchName)
        if errcode != ERROR_MORE_DATA:
            break
        cchName = cchName + 1024
        if cchName > 65536:
            raise ctypes.WinError(errcode)
    if errcode == ERROR_NO_MORE_ITEMS:
        return None
    if errcode != ERROR_SUCCESS:
        raise ctypes.WinError(errcode)
    return lpName.value


def RegEnumKeyW(hKey, dwIndex):
    _RegEnumKeyW = windll.advapi32.RegEnumKeyW
    _RegEnumKeyW.argtypes = [HKEY, DWORD, LPWSTR, DWORD]
    _RegEnumKeyW.restype = LONG

    cchName = 512
    while True:
        lpName = ctypes.create_unicode_buffer(cchName)
        errcode = _RegEnumKeyW(hKey, dwIndex, lpName, cchName * 2)
        if errcode != ERROR_MORE_DATA:
            break
        cchName = cchName + 512
        if cchName > 32768:
            raise ctypes.WinError(errcode)
    if errcode == ERROR_NO_MORE_ITEMS:
        return None
    if errcode != ERROR_SUCCESS:
        raise ctypes.WinError(errcode)
    return lpName.value


RegEnumKey = DefaultStringType(RegEnumKeyA, RegEnumKeyW)


def _internal_RegEnumValue(ansi, hKey, dwIndex, bGetData=True):
    if ansi:
        _RegEnumValue = windll.advapi32.RegEnumValueA
        _RegEnumValue.argtypes = [HKEY, DWORD, LPSTR, LPDWORD, LPVOID, LPDWORD, LPVOID, LPDWORD]
    else:
        _RegEnumValue = windll.advapi32.RegEnumValueW
        _RegEnumValue.argtypes = [HKEY, DWORD, LPWSTR, LPDWORD, LPVOID, LPDWORD, LPVOID, LPDWORD]
    _RegEnumValue.restype = LONG

    cchValueName = DWORD(1024)
    dwType = DWORD(-1)
    lpcchValueName = byref(cchValueName)
    lpType = byref(dwType)
    if ansi:
        lpValueName = ctypes.create_string_buffer(cchValueName.value)
    else:
        lpValueName = ctypes.create_unicode_buffer(cchValueName.value)
    if bGetData:
        cbData = DWORD(0)
        lpcbData = byref(cbData)
    else:
        lpcbData = None
    lpData = None
    errcode = _RegEnumValue(hKey, dwIndex, lpValueName, lpcchValueName, None, lpType, lpData, lpcbData)

    if errcode == ERROR_MORE_DATA or (bGetData and errcode == ERROR_SUCCESS):
        if ansi:
            cchValueName.value = cchValueName.value + sizeof(CHAR)
            lpValueName = ctypes.create_string_buffer(cchValueName.value)
        else:
            cchValueName.value = cchValueName.value + sizeof(WCHAR)
            lpValueName = ctypes.create_unicode_buffer(cchValueName.value)

        if bGetData:
            Type = dwType.value

            if Type in (REG_DWORD, REG_DWORD_BIG_ENDIAN):
                if cbData.value != sizeof(DWORD):
                    raise ValueError("REG_DWORD value of size %d" % cbData.value)
                Data = DWORD(0)

            elif Type == REG_QWORD:
                if cbData.value != sizeof(QWORD):
                    raise ValueError("REG_QWORD value of size %d" % cbData.value)
                Data = QWORD(0)

            elif Type in (REG_SZ, REG_EXPAND_SZ, REG_MULTI_SZ):
                if ansi:
                    Data = ctypes.create_string_buffer(cbData.value)
                else:
                    Data = ctypes.create_unicode_buffer(cbData.value)

            elif Type == REG_LINK:
                Data = ctypes.create_unicode_buffer(cbData.value)

            else:
                Data = ctypes.create_string_buffer(cbData.value)

            lpData = byref(Data)

        errcode = _RegEnumValue(hKey, dwIndex, lpValueName, lpcchValueName, None, lpType, lpData, lpcbData)

    if errcode == ERROR_NO_MORE_ITEMS:
        return None

    if not bGetData:
        return lpValueName.value, dwType.value

    if Type in (REG_DWORD, REG_DWORD_BIG_ENDIAN, REG_QWORD, REG_SZ, REG_EXPAND_SZ, REG_LINK):
        return lpValueName.value, dwType.value, Data.value

    if Type == REG_MULTI_SZ:
        sData = Data[:]
        del Data
        if ansi:
            aData = sData.split('\0')
        else:
            aData = sData.split(u'\0')
        aData = [token for token in aData if token]
        return lpValueName.value, dwType.value, aData

    return lpValueName.value, dwType.value, Data.raw


def RegEnumValueA(hKey, dwIndex, bGetData=True):
    return _internal_RegEnumValue(True, hKey, dwIndex, bGetData)


def RegEnumValueW(hKey, dwIndex, bGetData=True):
    return _internal_RegEnumValue(False, hKey, dwIndex, bGetData)


RegEnumValue = DefaultStringType(RegEnumValueA, RegEnumValueW)


def RegDeleteValueA(hKeySrc, lpValueName=None):
    _RegDeleteValueA = windll.advapi32.RegDeleteValueA
    _RegDeleteValueA.argtypes = [HKEY, LPSTR]
    _RegDeleteValueA.restype = LONG
    _RegDeleteValueA.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteValueA(hKeySrc, lpValueName)


def RegDeleteValueW(hKeySrc, lpValueName=None):
    _RegDeleteValueW = windll.advapi32.RegDeleteValueW
    _RegDeleteValueW.argtypes = [HKEY, LPWSTR]
    _RegDeleteValueW.restype = LONG
    _RegDeleteValueW.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteValueW(hKeySrc, lpValueName)


RegDeleteValue = GuessStringType(RegDeleteValueA, RegDeleteValueW)


def RegDeleteKeyValueA(hKeySrc, lpSubKey=None, lpValueName=None):
    _RegDeleteKeyValueA = windll.advapi32.RegDeleteKeyValueA
    _RegDeleteKeyValueA.argtypes = [HKEY, LPSTR, LPSTR]
    _RegDeleteKeyValueA.restype = LONG
    _RegDeleteKeyValueA.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteKeyValueA(hKeySrc, lpSubKey, lpValueName)


def RegDeleteKeyValueW(hKeySrc, lpSubKey=None, lpValueName=None):
    _RegDeleteKeyValueW = windll.advapi32.RegDeleteKeyValueW
    _RegDeleteKeyValueW.argtypes = [HKEY, LPWSTR, LPWSTR]
    _RegDeleteKeyValueW.restype = LONG
    _RegDeleteKeyValueW.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteKeyValueW(hKeySrc, lpSubKey, lpValueName)


RegDeleteKeyValue = GuessStringType(RegDeleteKeyValueA, RegDeleteKeyValueW)


def RegDeleteKeyA(hKeySrc, lpSubKey=None):
    _RegDeleteKeyA = windll.advapi32.RegDeleteKeyA
    _RegDeleteKeyA.argtypes = [HKEY, LPSTR]
    _RegDeleteKeyA.restype = LONG
    _RegDeleteKeyA.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteKeyA(hKeySrc, lpSubKey)


def RegDeleteKeyW(hKeySrc, lpSubKey=None):
    _RegDeleteKeyW = windll.advapi32.RegDeleteKeyW
    _RegDeleteKeyW.argtypes = [HKEY, LPWSTR]
    _RegDeleteKeyW.restype = LONG
    _RegDeleteKeyW.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteKeyW(hKeySrc, lpSubKey)


RegDeleteKey = GuessStringType(RegDeleteKeyA, RegDeleteKeyW)


def RegDeleteKeyExA(hKeySrc, lpSubKey=None, samDesired=KEY_WOW64_32KEY):
    _RegDeleteKeyExA = windll.advapi32.RegDeleteKeyExA
    _RegDeleteKeyExA.argtypes = [HKEY, LPSTR, REGSAM, DWORD]
    _RegDeleteKeyExA.restype = LONG
    _RegDeleteKeyExA.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteKeyExA(hKeySrc, lpSubKey, samDesired, 0)


def RegDeleteKeyExW(hKeySrc, lpSubKey=None, samDesired=KEY_WOW64_32KEY):
    _RegDeleteKeyExW = windll.advapi32.RegDeleteKeyExW
    _RegDeleteKeyExW.argtypes = [HKEY, LPWSTR, REGSAM, DWORD]
    _RegDeleteKeyExW.restype = LONG
    _RegDeleteKeyExW.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteKeyExW(hKeySrc, lpSubKey, samDesired, 0)


RegDeleteKeyEx = GuessStringType(RegDeleteKeyExA, RegDeleteKeyExW)


def RegCopyTreeA(hKeySrc, lpSubKey, hKeyDest):
    _RegCopyTreeA = windll.advapi32.RegCopyTreeA
    _RegCopyTreeA.argtypes = [HKEY, LPSTR, HKEY]
    _RegCopyTreeA.restype = LONG
    _RegCopyTreeA.errcheck = RaiseIfNotErrorSuccess
    _RegCopyTreeA(hKeySrc, lpSubKey, hKeyDest)


def RegCopyTreeW(hKeySrc, lpSubKey, hKeyDest):
    _RegCopyTreeW = windll.advapi32.RegCopyTreeW
    _RegCopyTreeW.argtypes = [HKEY, LPWSTR, HKEY]
    _RegCopyTreeW.restype = LONG
    _RegCopyTreeW.errcheck = RaiseIfNotErrorSuccess
    _RegCopyTreeW(hKeySrc, lpSubKey, hKeyDest)


RegCopyTree = GuessStringType(RegCopyTreeA, RegCopyTreeW)


def RegDeleteTreeA(hKey, lpSubKey=None):
    _RegDeleteTreeA = windll.advapi32.RegDeleteTreeA
    _RegDeleteTreeA.argtypes = [HKEY, LPWSTR]
    _RegDeleteTreeA.restype = LONG
    _RegDeleteTreeA.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteTreeA(hKey, lpSubKey)


def RegDeleteTreeW(hKey, lpSubKey=None):
    _RegDeleteTreeW = windll.advapi32.RegDeleteTreeW
    _RegDeleteTreeW.argtypes = [HKEY, LPWSTR]
    _RegDeleteTreeW.restype = LONG
    _RegDeleteTreeW.errcheck = RaiseIfNotErrorSuccess
    _RegDeleteTreeW(hKey, lpSubKey)


RegDeleteTree = GuessStringType(RegDeleteTreeA, RegDeleteTreeW)


def RegFlushKey(hKey):
    _RegFlushKey = windll.advapi32.RegFlushKey
    _RegFlushKey.argtypes = [HKEY]
    _RegFlushKey.restype = LONG
    _RegFlushKey.errcheck = RaiseIfNotErrorSuccess
    _RegFlushKey(hKey)


def CloseServiceHANDLE(hSCObject):
    _CloseServiceHANDLE = windll.advapi32.CloseServiceHANDLE
    _CloseServiceHANDLE.argtypes = [SC_HANDLE]
    _CloseServiceHANDLE.restype = bool
    _CloseServiceHANDLE.errcheck = RaiseIfZero

    if isinstance(hSCObject, HANDLE):

        hSCObject.close()
    else:
        _CloseServiceHANDLE(hSCObject)


def OpenSCManagerA(lpMachineName=None, lpDatabaseName=None, dwDesiredAccess=SC_MANAGER_ALL_ACCESS):
    _OpenSCManagerA = windll.advapi32.OpenSCManagerA
    _OpenSCManagerA.argtypes = [LPSTR, LPSTR, DWORD]
    _OpenSCManagerA.restype = SC_HANDLE
    _OpenSCManagerA.errcheck = RaiseIfZero

    hSCObject = _OpenSCManagerA(lpMachineName, lpDatabaseName, dwDesiredAccess)
    return ServiceControlManagerHANDLE(hSCObject)


def OpenSCManagerW(lpMachineName=None, lpDatabaseName=None, dwDesiredAccess=SC_MANAGER_ALL_ACCESS):
    _OpenSCManagerW = windll.advapi32.OpenSCManagerW
    _OpenSCManagerW.argtypes = [LPWSTR, LPWSTR, DWORD]
    _OpenSCManagerW.restype = SC_HANDLE
    _OpenSCManagerW.errcheck = RaiseIfZero

    hSCObject = _OpenSCManagerA(lpMachineName, lpDatabaseName, dwDesiredAccess)
    return ServiceControlManagerHANDLE(hSCObject)


OpenSCManager = GuessStringType(OpenSCManagerA, OpenSCManagerW)


def OpenServiceA(hSCManager, lpServiceName, dwDesiredAccess=SERVICE_ALL_ACCESS):
    _OpenServiceA = windll.advapi32.OpenServiceA
    _OpenServiceA.argtypes = [SC_HANDLE, LPSTR, DWORD]
    _OpenServiceA.restype = SC_HANDLE
    _OpenServiceA.errcheck = RaiseIfZero
    return ServiceHANDLE(_OpenServiceA(hSCManager, lpServiceName, dwDesiredAccess))


def OpenServiceW(hSCManager, lpServiceName, dwDesiredAccess=SERVICE_ALL_ACCESS):
    _OpenServiceW = windll.advapi32.OpenServiceW
    _OpenServiceW.argtypes = [SC_HANDLE, LPWSTR, DWORD]
    _OpenServiceW.restype = SC_HANDLE
    _OpenServiceW.errcheck = RaiseIfZero
    return ServiceHANDLE(_OpenServiceW(hSCManager, lpServiceName, dwDesiredAccess))


OpenService = GuessStringType(OpenServiceA, OpenServiceW)


def CreateServiceA(hSCManager, lpServiceName,
                   lpDisplayName=None,
                   dwDesiredAccess=SERVICE_ALL_ACCESS,
                   dwServiceType=SERVICE_WIN32_OWN_PROCESS,
                   dwStartType=SERVICE_DEMAND_START,
                   dwErrorControl=SERVICE_ERROR_NORMAL,
                   lpBinaryPathName=None,
                   lpLoadOrderGroup=None,
                   lpDependencies=None,
                   lpServiceStartName=None,
                   lpPassword=None):
    _CreateServiceA = windll.advapi32.CreateServiceA
    _CreateServiceA.argtypes = [SC_HANDLE, LPSTR, LPSTR, DWORD, DWORD, DWORD, DWORD, LPSTR, LPSTR, LPDWORD, LPSTR,
                                LPSTR, LPSTR]
    _CreateServiceA.restype = SC_HANDLE
    _CreateServiceA.errcheck = RaiseIfZero

    dwTagId = DWORD(0)
    hService = _CreateServiceA(hSCManager, lpServiceName, dwDesiredAccess, dwServiceType, dwStartType, dwErrorControl,
                               lpBinaryPathName, lpLoadOrderGroup, byref(dwTagId), lpDependencies, lpServiceStartName,
                               lpPassword)
    return ServiceHANDLE(hService), dwTagId.value


def CreateServiceW(hSCManager, lpServiceName,
                   lpDisplayName=None,
                   dwDesiredAccess=SERVICE_ALL_ACCESS,
                   dwServiceType=SERVICE_WIN32_OWN_PROCESS,
                   dwStartType=SERVICE_DEMAND_START,
                   dwErrorControl=SERVICE_ERROR_NORMAL,
                   lpBinaryPathName=None,
                   lpLoadOrderGroup=None,
                   lpDependencies=None,
                   lpServiceStartName=None,
                   lpPassword=None):
    _CreateServiceW = windll.advapi32.CreateServiceW
    _CreateServiceW.argtypes = [SC_HANDLE, LPWSTR, LPWSTR, DWORD, DWORD, DWORD, DWORD, LPWSTR, LPWSTR, LPDWORD, LPWSTR,
                                LPWSTR, LPWSTR]
    _CreateServiceW.restype = SC_HANDLE
    _CreateServiceW.errcheck = RaiseIfZero

    dwTagId = DWORD(0)
    hService = _CreateServiceW(hSCManager, lpServiceName, dwDesiredAccess, dwServiceType, dwStartType, dwErrorControl,
                               lpBinaryPathName, lpLoadOrderGroup, byref(dwTagId), lpDependencies, lpServiceStartName,
                               lpPassword)
    return ServiceHANDLE(hService), dwTagId.value


CreateService = GuessStringType(CreateServiceA, CreateServiceW)


def DeleteService(hService):
    _DeleteService = windll.advapi32.DeleteService
    _DeleteService.argtypes = [SC_HANDLE]
    _DeleteService.restype = bool
    _DeleteService.errcheck = RaiseIfZero
    _DeleteService(hService)


def GetServiceKeyNameA(hSCManager, lpDisplayName):
    _GetServiceKeyNameA = windll.advapi32.GetServiceKeyNameA
    _GetServiceKeyNameA.argtypes = [SC_HANDLE, LPSTR, LPSTR, LPDWORD]
    _GetServiceKeyNameA.restype = bool

    cchBuffer = DWORD(0)
    _GetServiceKeyNameA(hSCManager, lpDisplayName, None, byref(cchBuffer))
    if cchBuffer.value == 0:
        raise ctypes.WinError()
    lpServiceName = ctypes.create_string_buffer(cchBuffer.value + 1)
    cchBuffer.value = sizeof(lpServiceName)
    success = _GetServiceKeyNameA(hSCManager, lpDisplayName, lpServiceName, byref(cchBuffer))
    if not success:
        raise ctypes.WinError()
    return lpServiceName.value


def GetServiceKeyNameW(hSCManager, lpDisplayName):
    _GetServiceKeyNameW = windll.advapi32.GetServiceKeyNameW
    _GetServiceKeyNameW.argtypes = [SC_HANDLE, LPWSTR, LPWSTR, LPDWORD]
    _GetServiceKeyNameW.restype = bool

    cchBuffer = DWORD(0)
    _GetServiceKeyNameW(hSCManager, lpDisplayName, None, byref(cchBuffer))
    if cchBuffer.value == 0:
        raise ctypes.WinError()
    lpServiceName = ctypes.create_unicode_buffer(cchBuffer.value + 2)
    cchBuffer.value = sizeof(lpServiceName)
    success = _GetServiceKeyNameW(hSCManager, lpDisplayName, lpServiceName, byref(cchBuffer))
    if not success:
        raise ctypes.WinError()
    return lpServiceName.value


GetServiceKeyName = GuessStringType(GetServiceKeyNameA, GetServiceKeyNameW)


def GetServiceDisplayNameA(hSCManager, lpServiceName):
    _GetServiceDisplayNameA = windll.advapi32.GetServiceDisplayNameA
    _GetServiceDisplayNameA.argtypes = [SC_HANDLE, LPSTR, LPSTR, LPDWORD]
    _GetServiceDisplayNameA.restype = bool

    cchBuffer = DWORD(0)
    _GetServiceDisplayNameA(hSCManager, lpServiceName, None, byref(cchBuffer))
    if cchBuffer.value == 0:
        raise ctypes.WinError()
    lpDisplayName = ctypes.create_string_buffer(cchBuffer.value + 1)
    cchBuffer.value = sizeof(lpDisplayName)
    success = _GetServiceDisplayNameA(hSCManager, lpServiceName, lpDisplayName, byref(cchBuffer))
    if not success:
        raise ctypes.WinError()
    return lpDisplayName.value


def GetServiceDisplayNameW(hSCManager, lpServiceName):
    _GetServiceDisplayNameW = windll.advapi32.GetServiceDisplayNameW
    _GetServiceDisplayNameW.argtypes = [SC_HANDLE, LPWSTR, LPWSTR, LPDWORD]
    _GetServiceDisplayNameW.restype = bool

    cchBuffer = DWORD(0)
    _GetServiceDisplayNameW(hSCManager, lpServiceName, None, byref(cchBuffer))
    if cchBuffer.value == 0:
        raise ctypes.WinError()
    lpDisplayName = ctypes.create_unicode_buffer(cchBuffer.value + 2)
    cchBuffer.value = sizeof(lpDisplayName)
    success = _GetServiceDisplayNameW(hSCManager, lpServiceName, lpDisplayName, byref(cchBuffer))
    if not success:
        raise ctypes.WinError()
    return lpDisplayName.value


GetServiceDisplayName = GuessStringType(GetServiceDisplayNameA, GetServiceDisplayNameW)


def StartServiceA(hService, ServiceArgVectors=None):
    _StartServiceA = windll.advapi32.StartServiceA
    _StartServiceA.argtypes = [SC_HANDLE, DWORD, LPVOID]
    _StartServiceA.restype = bool
    _StartServiceA.errcheck = RaiseIfZero

    if ServiceArgVectors:
        dwNumServiceArgs = len(ServiceArgVectors)
        CServiceArgVectors = (LPSTR * dwNumServiceArgs)(*ServiceArgVectors)
        lpServiceArgVectors = ctypes.pointer(CServiceArgVectors)
    else:
        dwNumServiceArgs = 0
        lpServiceArgVectors = None
    _StartServiceA(hService, dwNumServiceArgs, lpServiceArgVectors)


def StartServiceW(hService, ServiceArgVectors=None):
    _StartServiceW = windll.advapi32.StartServiceW
    _StartServiceW.argtypes = [SC_HANDLE, DWORD, LPVOID]
    _StartServiceW.restype = bool
    _StartServiceW.errcheck = RaiseIfZero

    if ServiceArgVectors:
        dwNumServiceArgs = len(ServiceArgVectors)
        CServiceArgVectors = (LPWSTR * dwNumServiceArgs)(*ServiceArgVectors)
        lpServiceArgVectors = ctypes.pointer(CServiceArgVectors)
    else:
        dwNumServiceArgs = 0
        lpServiceArgVectors = None
    _StartServiceW(hService, dwNumServiceArgs, lpServiceArgVectors)


StartService = GuessStringType(StartServiceA, StartServiceW)


def ControlService(hService, dwControl):
    _ControlService = windll.advapi32.ControlService
    _ControlService.argtypes = [SC_HANDLE, DWORD, LPSERVICE_STATUS]
    _ControlService.restype = bool
    _ControlService.errcheck = RaiseIfZero

    rawServiceStatus = SERVICE_STATUS()
    _ControlService(hService, dwControl, byref(rawServiceStatus))
    return ServiceStatus(rawServiceStatus)


def QueryServiceStatus(hService):
    _QueryServiceStatus = windll.advapi32.QueryServiceStatus
    _QueryServiceStatus.argtypes = [SC_HANDLE, LPSERVICE_STATUS]
    _QueryServiceStatus.restype = bool
    _QueryServiceStatus.errcheck = RaiseIfZero

    rawServiceStatus = SERVICE_STATUS()
    _QueryServiceStatus(hService, byref(rawServiceStatus))
    return ServiceStatus(rawServiceStatus)


def QueryServiceStatusEx(hService, InfoLevel=SC_STATUS_PROCESS_INFO):
    if InfoLevel != SC_STATUS_PROCESS_INFO:
        raise NotImplementedError()

    _QueryServiceStatusEx = windll.advapi32.QueryServiceStatusEx
    _QueryServiceStatusEx.argtypes = [SC_HANDLE, SC_STATUS_TYPE, LPVOID, DWORD, LPDWORD]
    _QueryServiceStatusEx.restype = bool
    _QueryServiceStatusEx.errcheck = RaiseIfZero

    lpBuffer = SERVICE_STATUS_PROCESS()
    cbBytesNeeded = DWORD(sizeof(lpBuffer))
    _QueryServiceStatusEx(hService, InfoLevel, byref(lpBuffer), sizeof(lpBuffer), byref(cbBytesNeeded))
    return ServiceStatusProcess(lpBuffer)


def EnumServicesStatusA(hSCManager, dwServiceType=SERVICE_DRIVER | SERVICE_WIN32, dwServiceState=SERVICE_STATE_ALL):
    _EnumServicesStatusA = windll.advapi32.EnumServicesStatusA
    _EnumServicesStatusA.argtypes = [SC_HANDLE, DWORD, DWORD, LPVOID, DWORD, LPDWORD, LPDWORD, LPDWORD]
    _EnumServicesStatusA.restype = bool

    cbBytesNeeded = DWORD(0)
    ServicesReturned = DWORD(0)
    ResumeHANDLE = DWORD(0)

    _EnumServicesStatusA(hSCManager, dwServiceType, dwServiceState, None, 0, byref(cbBytesNeeded),
                         byref(ServicesReturned), byref(ResumeHANDLE))

    Services = []
    success = False
    while GetLastError() == ERROR_MORE_DATA:
        if cbBytesNeeded.value < sizeof(ENUM_SERVICE_STATUSA):
            break
        ServicesBuffer = ctypes.create_string_buffer("", cbBytesNeeded.value)
        success = _EnumServicesStatusA(hSCManager, dwServiceType, dwServiceState, byref(ServicesBuffer),
                                       sizeof(ServicesBuffer), byref(cbBytesNeeded), byref(ServicesReturned),
                                       byref(ResumeHANDLE))
        if sizeof(ServicesBuffer) < (sizeof(ENUM_SERVICE_STATUSA) * ServicesReturned.value):
            raise ctypes.WinError()
        lpServicesArray = ctypes.cast(ctypes.cast(ctypes.pointer(ServicesBuffer), ctypes.c_void_p),
                                      LPENUM_SERVICE_STATUSA)
        for index in xrange(0, ServicesReturned.value):
            Services.append(ServiceStatusEntry(lpServicesArray[index]))
        if success: break
    if not success:
        raise ctypes.WinError()

    return Services


def EnumServicesStatusW(hSCManager, dwServiceType=SERVICE_DRIVER | SERVICE_WIN32, dwServiceState=SERVICE_STATE_ALL):
    _EnumServicesStatusW = windll.advapi32.EnumServicesStatusW
    _EnumServicesStatusW.argtypes = [SC_HANDLE, DWORD, DWORD, LPVOID, DWORD, LPDWORD, LPDWORD, LPDWORD]
    _EnumServicesStatusW.restype = bool

    cbBytesNeeded = DWORD(0)
    ServicesReturned = DWORD(0)
    ResumeHANDLE = DWORD(0)

    _EnumServicesStatusW(hSCManager, dwServiceType, dwServiceState, None, 0, byref(cbBytesNeeded),
                         byref(ServicesReturned), byref(ResumeHANDLE))

    Services = []
    success = False
    while GetLastError() == ERROR_MORE_DATA:
        if cbBytesNeeded.value < sizeof(ENUM_SERVICE_STATUSW):
            break
        ServicesBuffer = ctypes.create_string_buffer("", cbBytesNeeded.value)
        success = _EnumServicesStatusW(hSCManager, dwServiceType, dwServiceState, byref(ServicesBuffer),
                                       sizeof(ServicesBuffer), byref(cbBytesNeeded), byref(ServicesReturned),
                                       byref(ResumeHANDLE))
        if sizeof(ServicesBuffer) < (sizeof(ENUM_SERVICE_STATUSW) * ServicesReturned.value):
            raise ctypes.WinError()
        lpServicesArray = ctypes.cast(ctypes.cast(ctypes.pointer(ServicesBuffer), ctypes.c_void_p),
                                      LPENUM_SERVICE_STATUSW)
        for index in xrange(0, ServicesReturned.value):
            Services.append(ServiceStatusEntry(lpServicesArray[index]))
        if success: break
    if not success:
        raise ctypes.WinError()

    return Services


EnumServicesStatus = DefaultStringType(EnumServicesStatusA, EnumServicesStatusW)


def EnumServicesStatusExA(hSCManager, InfoLevel=SC_ENUM_PROCESS_INFO, dwServiceType=SERVICE_DRIVER | SERVICE_WIN32,
                          dwServiceState=SERVICE_STATE_ALL, pszGroupName=None):
    if InfoLevel != SC_ENUM_PROCESS_INFO:
        raise NotImplementedError()

    _EnumServicesStatusExA = windll.advapi32.EnumServicesStatusExA
    _EnumServicesStatusExA.argtypes = [SC_HANDLE, SC_ENUM_TYPE, DWORD, DWORD, LPVOID, DWORD, LPDWORD, LPDWORD, LPDWORD,
                                       LPSTR]
    _EnumServicesStatusExA.restype = bool

    cbBytesNeeded = DWORD(0)
    ServicesReturned = DWORD(0)
    ResumeHANDLE = DWORD(0)

    _EnumServicesStatusExA(hSCManager, InfoLevel, dwServiceType, dwServiceState, None, 0, byref(cbBytesNeeded),
                           byref(ServicesReturned), byref(ResumeHANDLE), pszGroupName)

    Services = []
    success = False
    while GetLastError() == ERROR_MORE_DATA:
        if cbBytesNeeded.value < sizeof(ENUM_SERVICE_STATUS_PROCESSA):
            break
        ServicesBuffer = ctypes.create_string_buffer("", cbBytesNeeded.value)
        success = _EnumServicesStatusExA(hSCManager, InfoLevel, dwServiceType, dwServiceState, byref(ServicesBuffer),
                                         sizeof(ServicesBuffer), byref(cbBytesNeeded), byref(ServicesReturned),
                                         byref(ResumeHANDLE), pszGroupName)
        if sizeof(ServicesBuffer) < (sizeof(ENUM_SERVICE_STATUS_PROCESSA) * ServicesReturned.value):
            raise ctypes.WinError()
        lpServicesArray = ctypes.cast(ctypes.cast(ctypes.pointer(ServicesBuffer), ctypes.c_void_p),
                                      LPENUM_SERVICE_STATUS_PROCESSA)
        for index in xrange(0, ServicesReturned.value):
            Services.append(ServiceStatusProcessEntry(lpServicesArray[index]))
        if success: break
    if not success:
        raise ctypes.WinError()

    return Services


def EnumServicesStatusExW(hSCManager, InfoLevel=SC_ENUM_PROCESS_INFO, dwServiceType=SERVICE_DRIVER | SERVICE_WIN32,
                          dwServiceState=SERVICE_STATE_ALL, pszGroupName=None):
    _EnumServicesStatusExW = windll.advapi32.EnumServicesStatusExW
    _EnumServicesStatusExW.argtypes = [SC_HANDLE, SC_ENUM_TYPE, DWORD, DWORD, LPVOID, DWORD, LPDWORD, LPDWORD, LPDWORD,
                                       LPWSTR]
    _EnumServicesStatusExW.restype = bool

    if InfoLevel != SC_ENUM_PROCESS_INFO:
        raise NotImplementedError()

    cbBytesNeeded = DWORD(0)
    ServicesReturned = DWORD(0)
    ResumeHANDLE = DWORD(0)

    _EnumServicesStatusExW(hSCManager, InfoLevel, dwServiceType, dwServiceState, None, 0, byref(cbBytesNeeded),
                           byref(ServicesReturned), byref(ResumeHANDLE), pszGroupName)

    Services = []
    success = False
    while GetLastError() == ERROR_MORE_DATA:
        if cbBytesNeeded.value < sizeof(ENUM_SERVICE_STATUS_PROCESSW):
            break
        ServicesBuffer = ctypes.create_string_buffer("", cbBytesNeeded.value)
        success = _EnumServicesStatusExW(hSCManager, InfoLevel, dwServiceType, dwServiceState, byref(ServicesBuffer),
                                         sizeof(ServicesBuffer), byref(cbBytesNeeded), byref(ServicesReturned),
                                         byref(ResumeHANDLE), pszGroupName)
        if sizeof(ServicesBuffer) < (sizeof(ENUM_SERVICE_STATUS_PROCESSW) * ServicesReturned.value):
            raise ctypes.WinError()
        lpServicesArray = ctypes.cast(ctypes.cast(ctypes.pointer(ServicesBuffer), ctypes.c_void_p),
                                      LPENUM_SERVICE_STATUS_PROCESSW)
        for index in xrange(0, ServicesReturned.value):
            Services.append(ServiceStatusProcessEntry(lpServicesArray[index]))
        if success: break
    if not success:
        raise ctypes.WinError()

    return Services


EnumServicesStatusEx = DefaultStringType(EnumServicesStatusExA, EnumServicesStatusExW)


def SetThreadToken(token_handle, thread_handle=None):
    _SetThreadToken = windll.advapi32.SetThreadToken
    _SetThreadToken.argtypes = [PHANDLE, HANDLE]
    _SetThreadToken.restype = bool
    _SetThreadToken.errcheck = RaiseIfZero

    _SetThreadToken(thread_handle, token_handle)


_all = set(vars().keys()).difference(_all)
__all__ = [_x for _x in _all if not _x.startswith('_')]
__all__.sort()
