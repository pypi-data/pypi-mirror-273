import enum


class PrivilegeValues(enum.Enum):
    SE_CREATE_TOKEN = 2
    SE_ASSIGNPRIMARYTOKEN = 3
    SE_LOCK_MEMORY = 4
    SE_INCREASE_QUOTA = 5
    SE_UNSOLICITED_INPUT = 6
    SE_TCB = 7
    SE_SECURITY = 8
    SE_TAKE_OWNERSHIP = 9
    SE_LOAD_DRIVER = 10
    SE_SYSTEM_PROFILE = 11
    SE_SYSTEMTIME = 12
    SE_PROF_SINGLE_PROCESS = 13
    SE_INC_BASE_PRIORITY = 14
    SE_CREATE_PAGEFILE = 15
    SE_CREATE_PERMANENT = 16
    SE_BACKUP = 17
    SE_RESTORE = 18
    SE_SHUTDOWN = 19
    SE_DEBUG = 20
    SE_AUDIT = 21
    SE_SYSTEM_ENVIRONMENT = 22
    SE_CHANGE_NOTIFY = 23
    SE_REMOTE_SHUTDOWN = 24
    SE_UNDOCK = 25
    SE_SYNC_AGENT = 26
    SE_ENABLE_DELEGATION = 27
    SE_MANAGE_VOLUME = 28
    SE_IMPERSONATE = 29
    SE_CREATE_GLOBAL = 30
    SE_TRUSTED_CREDMAN_ACCESS = 31
    SE_RELABEL = 32
    SE_INC_WORKING_SET = 33
    SE_TIME_ZONE = 34
    SE_CREATE_SYMBOLIC_LINK = 35


class Privileges(enum.Enum):
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