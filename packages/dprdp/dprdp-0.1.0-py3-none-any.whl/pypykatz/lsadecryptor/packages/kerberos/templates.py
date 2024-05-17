import io
from minidump.win_datatypes import ULONG64, FILETIME, PCWSTR, SIZE_T, BOOL
from pypykatz.commons.common import KatzSystemArchitecture, WindowsMinBuild, WindowsBuild
from pypykatz.commons.win_datatypes import POINTER, PVOID, ULONG, LIST_ENTRY, \
    DWORD, LSA_UNICODE_STRING, PKERB_EXTERNAL_NAME, KIWI_GENERIC_PRIMARY_CREDENTIAL, \
    LUID, PLSAISO_DATA_BLOB
from pypykatz.lsadecryptor.package_commons import PackageTemplate


class KerberosTemplate(PackageTemplate):
    def __init__(self, sysinfo):
        super().__init__('Kerberos', sysinfo)
        self.signature = None
        self.first_entry_offset = None
        self.kerberos_session_struct = None
        self.kerberos_ticket_struct = None
        self.keys_list_struct = None
        self.hash_password_struct = None
        self.csp_info_struct = None

    @staticmethod
    def get_template(sysinfo):

        template = KerberosTemplate(sysinfo)
        if sysinfo.architecture == KatzSystemArchitecture.X64:
            if WindowsMinBuild.WIN_XP.value <= sysinfo.buildnumber < WindowsMinBuild.WIN_2K3.value:
                template.signature = b'\x48\x3b\xfe\x0f\x84'
                template.first_entry_offset = -4
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_51
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_51
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_5
                template.hash_password_struct = KERB_HASHPASSWORD_5
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_5


            elif WindowsMinBuild.WIN_2K3.value <= sysinfo.buildnumber < WindowsMinBuild.WIN_VISTA.value:
                template.signature = b'\x48\x3b\xfe\x0f\x84'
                template.first_entry_offset = -4
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_52
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_5
                template.hash_password_struct = KERB_HASHPASSWORD_5
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_5

            elif WindowsMinBuild.WIN_VISTA.value <= sysinfo.buildnumber < WindowsMinBuild.WIN_7.value:
                template.signature = b'\x48\x8b\x18\x48\x8d\x0d'
                template.first_entry_offset = 6
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_60
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_60

            elif WindowsMinBuild.WIN_7.value <= sysinfo.buildnumber < WindowsMinBuild.WIN_8.value:
                template.signature = b'\x48\x8b\x18\x48\x8d\x0d'
                template.first_entry_offset = 6
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_6
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_60

            elif WindowsMinBuild.WIN_8.value <= sysinfo.buildnumber < WindowsBuild.WIN_10_1507.value:
                template.signature = b'\x48\x8b\x18\x48\x8d\x0d'
                template.first_entry_offset = 6
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_6
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_62

            elif WindowsBuild.WIN_10_1507.value <= sysinfo.buildnumber < WindowsBuild.WIN_10_1511.value:
                template.signature = b'\x48\x8b\x18\x48\x8d\x0d'
                template.first_entry_offset = 6
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_10
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_6
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_10

            elif WindowsBuild.WIN_10_1511.value <= sysinfo.buildnumber < WindowsBuild.WIN_10_1607.value:
                template.signature = b'\x48\x8b\x18\x48\x8d\x0d'
                template.first_entry_offset = 6
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_10
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_10
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_10


            elif WindowsBuild.WIN_10_1607.value <= sysinfo.buildnumber < WindowsBuild.WIN_11_2022.value:
                template.signature = b'\x48\x8b\x18\x48\x8d\x0d'
                template.first_entry_offset = 6
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_10_1607
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_10_1607
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6_1607
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_10

            elif sysinfo.buildnumber >= WindowsBuild.WIN_11_2022.value:
                template.signature = b'\x48\x8b\x18\x48\x8d\x0d'
                template.first_entry_offset = 6
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_10_1607
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_11
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6_1607
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_10

            else:
                raise Exception('Could not identify template! Architecture: %s sysinfo.buildnumber: %s' % (
                    sysinfo.architecture, sysinfo.buildnumber))


        elif sysinfo.architecture == KatzSystemArchitecture.X86:
            if WindowsMinBuild.WIN_XP.value <= sysinfo.buildnumber < WindowsMinBuild.WIN_2K3.value:
                template.signature = b'\x8B\x7D\x08\x8B\x17\x39\x50'
                template.first_entry_offset = -8
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_51
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_51
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_5
                template.hash_password_struct = KERB_HASHPASSWORD_5
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_5


            elif WindowsMinBuild.WIN_2K3.value <= sysinfo.buildnumber < WindowsMinBuild.WIN_VISTA.value:
                template.signature = b'\x8B\x7D\x08\x8B\x17\x39\x50'
                template.first_entry_offset = -8
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_52
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_5
                template.hash_password_struct = KERB_HASHPASSWORD_5
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_5

            elif WindowsMinBuild.WIN_VISTA.value <= sysinfo.buildnumber < WindowsMinBuild.WIN_7.value:
                template.signature = b'\x53\x8b\x18\x50\x56'
                template.first_entry_offset = -11
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_60
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_60

            elif WindowsMinBuild.WIN_7.value <= sysinfo.buildnumber < WindowsMinBuild.WIN_8.value:
                template.signature = b'\x53\x8b\x18\x50\x56'
                template.first_entry_offset = -11
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_6
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_60

            elif WindowsMinBuild.WIN_8.value <= sysinfo.buildnumber < WindowsBuild.WIN_BLUE.value:
                template.signature = b'\x57\x8b\x38\x50\x68'
                template.first_entry_offset = -14
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_6
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_62

            elif WindowsMinBuild.WIN_BLUE.value <= sysinfo.buildnumber < WindowsBuild.WIN_10_1507.value:
                template.signature = b'\x56\x8b\x30\x50\x57'
                template.first_entry_offset = -15
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_6
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_62




            elif WindowsBuild.WIN_10_1507.value <= sysinfo.buildnumber < WindowsBuild.WIN_10_1511.value:
                template.signature = b'\x56\x8b\x30\x50\x57'
                template.first_entry_offset = -15
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_10_X86
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_6
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_10


            elif WindowsBuild.WIN_10_1511.value <= sysinfo.buildnumber < WindowsBuild.WIN_10_1903.value:
                template.signature = b'\x56\x8b\x30\x50\x57'
                template.first_entry_offset = -15
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_10_1607_X86
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_10_1607
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6_1607
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_10


            elif WindowsBuild.WIN_10_1903.value <= sysinfo.buildnumber:
                template.signature = b'\x56\x8b\x30\x50\x53'
                template.first_entry_offset = -15
                template.kerberos_session_struct = KIWI_KERBEROS_LOGON_SESSION_10_1607_X86
                template.kerberos_ticket_struct = KIWI_KERBEROS_INTERNAL_TICKET_10_1607
                template.keys_list_struct = KIWI_KERBEROS_KEYS_LIST_6
                template.hash_password_struct = KERB_HASHPASSWORD_6_1607
                template.csp_info_struct = KIWI_KERBEROS_CSP_INFOS_10


        else:
            raise Exception('Unknown architecture! %s' % sysinfo.architecture)

        return template


class PKERB_SMARTCARD_CSP_INFO_5(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KERB_SMARTCARD_CSP_INFO_5)


class KERB_SMARTCARD_CSP_INFO_5:
    def __init__(self, reader, size):
        pos = reader.tell()

        self.ContextInformation = PVOID(reader).value
        self.nCardNameOffset = ULONG(reader).value
        self.nReaderNameOffset = ULONG(reader).value
        self.nContainerNameOffset = ULONG(reader).value
        self.nCSPNameOffset = ULONG(reader).value
        diff = reader.tell() - pos
        data = reader.read(size - diff + 4)
        self.bBuffer = io.BytesIO(data)

    @staticmethod
    def read_wcharnull(buffer, tpos):
        pos = buffer.tell()
        buffer.seek(tpos, 0)
        data = b''
        i = 0
        nc = 0
        while i < 255:
            if nc == 3:
                break
            c = buffer.read(1)
            if c == b'\x00':
                nc += 1
            else:
                nc = 0
            data += c
            i += 1
        buffer.seek(pos, 0)
        return data.decode('utf-16-le').replace('\x00', '')

    def get_infos(self):
        t = {'CardName': self.read_wcharnull(self.bBuffer, self.nCardNameOffset),
             'ReaderName': self.read_wcharnull(self.bBuffer, self.nReaderNameOffset),
             'ContainerName': self.read_wcharnull(self.bBuffer, self.nContainerNameOffset),
             'CSPName': self.read_wcharnull(self.bBuffer, self.nCSPNameOffset)}

        return t


class PKERB_SMARTCARD_CSP_INFO(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KERB_SMARTCARD_CSP_INFO)


class KERB_SMARTCARD_CSP_INFO:
    def __init__(self, reader, size):
        pos = reader.tell()

        self.MessageType = DWORD(reader).value
        self.ContextInformation = PVOID(reader).value
        self.SpaceHolderForWow64 = ULONG64(reader).value
        self.flags = DWORD(reader).value
        self.KeySpec = DWORD(reader).value
        self.nCardNameOffset = ULONG(reader).value * 2
        self.nReaderNameOffset = ULONG(reader).value * 2
        self.nContainerNameOffset = ULONG(reader).value * 2
        self.nCSPNameOffset = ULONG(reader).value * 2
        diff = reader.tell() - pos
        data = reader.read(size - diff + 4)
        self.bBuffer = io.BytesIO(data)

    @staticmethod
    def read_wcharnull(buffer, tpos):
        pos = buffer.tell()
        buffer.seek(tpos, 0)
        data = b''
        i = 0
        nc = 0
        while i < 255:
            if nc == 3:
                break
            c = buffer.read(1)
            if c == b'\x00':
                nc += 1
            else:
                nc = 0
            data += c
            i += 1
        buffer.seek(pos, 0)
        return data.decode('utf-16-le').replace('\x00', '')

    def get_infos(self):
        t = {'CardName': self.read_wcharnull(self.bBuffer, self.nCardNameOffset),
             'ReaderName': self.read_wcharnull(self.bBuffer, self.nReaderNameOffset),
             'ContainerName': self.read_wcharnull(self.bBuffer, self.nContainerNameOffset),
             'CSPName': self.read_wcharnull(self.bBuffer, self.nCSPNameOffset)}

        return t


class PKIWI_KERBEROS_CSP_INFOS_5(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_CSP_INFOS_5)


class KIWI_KERBEROS_CSP_INFOS_5:
    def __init__(self, reader):
        self.PinCode = LSA_UNICODE_STRING(reader)
        self.unk0 = PVOID(reader)
        self.unk1 = PVOID(reader)
        self.CertificateInfos = PVOID(reader)
        self.unkData = PVOID(reader)
        self.Flags = DWORD(reader).value
        self.CspDataLength = DWORD(reader).value
        self.CspData = KERB_SMARTCARD_CSP_INFO_5(reader, size=self.CspDataLength)


class PKIWI_KERBEROS_CSP_INFOS_60(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_CSP_INFOS_60)


class KIWI_KERBEROS_CSP_INFOS_60:
    def __init__(self, reader):
        self.PinCode = LSA_UNICODE_STRING(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.CertificateInfos = PVOID(reader).value
        self.unkData = PVOID(reader).value
        self.Flags = DWORD(reader).value
        self.unkFlags = DWORD(reader).value
        self.CspDataLength = DWORD(reader).value
        self.CspData = KERB_SMARTCARD_CSP_INFO(reader, size=self.CspDataLength)


class PKIWI_KERBEROS_CSP_INFOS_62(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_CSP_INFOS_62)


class KIWI_KERBEROS_CSP_INFOS_62:
    def __init__(self, reader):
        self.PinCode = LSA_UNICODE_STRING(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.CertificateInfos = PVOID(reader).value
        self.unk2 = PVOID(reader).value
        self.unkData = PVOID(reader).value
        self.Flags = DWORD(reader).value
        self.unkFlags = DWORD(reader).value
        self.CspDataLength = DWORD(reader).value
        self.CspData = KERB_SMARTCARD_CSP_INFO(reader, size=self.CspDataLength)


class PKIWI_KERBEROS_CSP_INFOS_10(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_CSP_INFOS_10)


class KIWI_KERBEROS_CSP_INFOS_10:
    def __init__(self, reader):
        self.PinCode = LSA_UNICODE_STRING(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.CertificateInfos = PVOID(reader).value
        self.unk2 = PVOID(reader).value
        self.unkData = PVOID(reader).value
        self.Flags = DWORD(reader).value
        self.unkFlags = DWORD(reader).value
        self.unk3 = PVOID(reader).value
        self.CspDataLength = DWORD(reader).value
        self.CspData = KERB_SMARTCARD_CSP_INFO(reader, size=self.CspDataLength)


class PKIWI_KERBEROS_LOGON_SESSION_51(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_LOGON_SESSION_51)


class KIWI_KERBEROS_LOGON_SESSION_51:
    def __init__(self, reader):
        self.UsageCount = ULONG(reader).value
        self.unk0 = LIST_ENTRY(reader)
        self.unk1 = LIST_ENTRY(reader)
        self.unk2 = PVOID(reader).value
        self.unk3 = ULONG(reader).value
        self.unk4 = ULONG(reader).value
        self.unk5 = PVOID(reader).value
        self.unk6 = PVOID(reader).value
        self.unk7 = PVOID(reader).value
        self.LocallyUniqueIdentifier = LUID(reader).value
        reader.align(8)

        self.unk8 = FILETIME(reader).value
        self.unk9 = PVOID(reader).value
        self.unk10 = ULONG(reader).value
        self.unk11 = ULONG(reader).value
        self.unk12 = PVOID(reader).value
        self.unk13 = PVOID(reader).value
        self.unk14 = PVOID(reader).value
        self.credentials = KIWI_GENERIC_PRIMARY_CREDENTIAL(reader)
        self.unk15 = ULONG(reader).value
        self.unk16 = ULONG(reader).value
        self.unk17 = ULONG(reader).value
        self.unk18 = ULONG(reader).value
        self.unk19 = PVOID(reader).value
        self.unk20 = PVOID(reader).value
        self.unk21 = PVOID(reader).value
        self.unk22 = PVOID(reader).value
        self.pKeyList = PVOID(reader)
        self.unk24 = PVOID(reader).value
        self.Tickets_1 = LIST_ENTRY(reader)
        self.Tickets_2 = LIST_ENTRY(reader)
        self.Tickets_3 = LIST_ENTRY(reader)
        self.SmartcardInfos = PVOID(reader)


class PKIWI_KERBEROS_LOGON_SESSION(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_LOGON_SESSION)


class KIWI_KERBEROS_LOGON_SESSION:
    def __init__(self, reader):
        self.UsageCount = ULONG(reader).value
        reader.align()
        self.unk0 = LIST_ENTRY(reader)
        self.unk1 = PVOID(reader).value
        self.unk2 = ULONG(reader).value
        self.unk3 = ULONG(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.unk6 = PVOID(reader).value
        self.LocallyUniqueIdentifier = LUID(reader).value

        reader.align(8)
        self.unk7 = FILETIME(reader).value
        self.unk8 = PVOID(reader).value
        self.unk9 = ULONG(reader).value
        self.unk10 = ULONG(reader).value
        self.unk11 = PVOID(reader).value
        self.unk12 = PVOID(reader).value
        self.unk13 = PVOID(reader).value
        self.credentials = KIWI_GENERIC_PRIMARY_CREDENTIAL(reader)
        self.unk14 = ULONG(reader).value
        self.unk15 = ULONG(reader).value
        self.unk16 = ULONG(reader).value
        self.unk17 = ULONG(reader).value
        self.unk18 = PVOID(reader).value
        self.unk19 = PVOID(reader).value
        self.unk20 = PVOID(reader).value
        self.unk21 = PVOID(reader).value
        self.pKeyList = PVOID(reader)
        self.unk23 = PVOID(reader).value
        reader.align()
        self.Tickets_1 = LIST_ENTRY(reader)
        self.unk24 = FILETIME(reader).value
        self.Tickets_2 = LIST_ENTRY(reader)
        self.unk25 = FILETIME(reader).value
        self.Tickets_3 = LIST_ENTRY(reader)
        self.unk26 = FILETIME(reader).value
        self.SmartcardInfos = PVOID(reader)


class PKIWI_KERBEROS_10_PRIMARY_CREDENTIAL(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_10_PRIMARY_CREDENTIAL)


class KIWI_KERBEROS_10_PRIMARY_CREDENTIAL:
    def __init__(self, reader):
        self.UserName = LSA_UNICODE_STRING(reader)
        self.Domaine = LSA_UNICODE_STRING(reader)
        self.unk0 = PVOID(reader).value
        self.Password = LSA_UNICODE_STRING(reader)


class PKIWI_KERBEROS_LOGON_SESSION_10(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_LOGON_SESSION_10)


class KIWI_KERBEROS_LOGON_SESSION_10_X86:
    def __init__(self, reader):
        self.UsageCount = ULONG(reader).value
        reader.align()
        self.unk0 = LIST_ENTRY(reader)
        self.unk1 = PVOID(reader).value
        self.unk1b = ULONG(reader).value
        reader.align()
        self.unk2 = FILETIME(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.unk6 = PVOID(reader).value
        self.LocallyUniqueIdentifier = LUID(reader).value

        reader.align()
        self.unk7 = FILETIME(reader).value
        self.unk8 = PVOID(reader).value
        self.unk8b = ULONG(reader).value
        reader.align()
        self.unk9 = FILETIME(reader).value
        self.unk11 = PVOID(reader).value
        self.unk12 = PVOID(reader).value
        self.unk13 = PVOID(reader).value
        reader.align(8)

        self.credentials = KIWI_KERBEROS_10_PRIMARY_CREDENTIAL(reader)
        self.unk14 = ULONG(reader).value
        self.unk15 = ULONG(reader).value
        self.unk16 = ULONG(reader).value
        self.unk17 = ULONG(reader).value

        reader.align(8)
        self.unk19 = PVOID(reader).value
        self.unk20 = PVOID(reader).value
        self.unk21 = PVOID(reader).value
        self.unk22 = PVOID(reader).value
        self.unk23 = PVOID(reader).value
        self.unk24 = PVOID(reader).value
        self.unk25 = PVOID(reader).value

        self.pKeyList = PVOID(reader)
        self.unk26 = PVOID(reader).value

        reader.align()

        self.Tickets_1 = LIST_ENTRY(reader)
        self.unk27 = FILETIME(reader).value
        self.Tickets_2 = LIST_ENTRY(reader)
        self.unk28 = FILETIME(reader).value
        self.Tickets_3 = LIST_ENTRY(reader)
        self.unk29 = FILETIME(reader).value
        self.SmartcardInfos = PVOID(reader)


class KIWI_KERBEROS_LOGON_SESSION_10:
    def __init__(self, reader):
        self.UsageCount = ULONG(reader).value
        reader.align()
        self.unk0 = LIST_ENTRY(reader)
        self.unk1 = PVOID(reader).value
        self.unk1b = ULONG(reader).value
        reader.align()
        self.unk2 = FILETIME(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.unk6 = PVOID(reader).value
        self.LocallyUniqueIdentifier = LUID(reader).value
        self.unk7 = FILETIME(reader).value
        self.unk8 = PVOID(reader).value
        self.unk8b = ULONG(reader).value
        reader.align()
        self.unk9 = FILETIME(reader).value
        self.unk11 = PVOID(reader).value
        self.unk12 = PVOID(reader).value
        self.unk13 = PVOID(reader).value
        self.credentials = KIWI_KERBEROS_10_PRIMARY_CREDENTIAL(reader)
        self.unk14 = ULONG(reader).value
        self.unk15 = ULONG(reader).value
        self.unk16 = ULONG(reader).value
        self.unk17 = ULONG(reader).value

        self.unk19 = PVOID(reader).value
        self.unk20 = PVOID(reader).value
        self.unk21 = PVOID(reader).value
        self.unk22 = PVOID(reader).value
        self.unk23 = PVOID(reader).value
        self.unk24 = PVOID(reader).value
        self.unk25 = PVOID(reader).value
        self.pKeyList = PVOID(reader)
        self.unk26 = PVOID(reader).value
        self.Tickets_1 = LIST_ENTRY(reader)
        self.unk27 = FILETIME(reader).value
        self.Tickets_2 = LIST_ENTRY(reader)
        self.unk28 = FILETIME(reader).value
        self.Tickets_3 = LIST_ENTRY(reader)
        self.unk29 = FILETIME(reader).value
        self.SmartcardInfos = PVOID(reader)


class PKIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607_ISO(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607_ISO)


class KIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607_ISO:
    def __init__(self, reader):
        self.StructSize = DWORD(reader).value
        reader.align()
        self.isoBlob = PLSAISO_DATA_BLOB(reader)


class PKIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607)


class KIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607:
    def __init__(self, reader):
        self.UserName = LSA_UNICODE_STRING(reader)
        self.Domaine = LSA_UNICODE_STRING(reader)
        self.unkFunction = PVOID(reader).value
        self.type = DWORD(reader).value
        reader.align()
        self.Password = LSA_UNICODE_STRING(reader)
        self.IsoPassword = KIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607_ISO(reader)


class PKIWI_KERBEROS_LOGON_SESSION_10_1607(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_LOGON_SESSION_10_1607)


class KIWI_KERBEROS_LOGON_SESSION_10_1607:
    def __init__(self, reader):
        self.UsageCount = ULONG(reader).value
        reader.align()
        self.unk0 = LIST_ENTRY(reader)
        self.unk1 = PVOID(reader).value
        self.unk1b = ULONG(reader).value
        reader.align()
        self.unk2 = FILETIME(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.unk6 = PVOID(reader).value
        self.LocallyUniqueIdentifier = LUID(reader).value
        self.unk7 = FILETIME(reader).value
        self.unk8 = PVOID(reader).value
        self.unk8b = ULONG(reader).value
        reader.align()
        self.unk9 = FILETIME(reader).value
        self.unk11 = PVOID(reader).value
        self.unk12 = PVOID(reader).value
        self.unk13 = PVOID(reader).value
        reader.align(8)
        self.credentials = KIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607(reader)
        self.unk14 = ULONG(reader).value
        self.unk15 = ULONG(reader).value
        self.unk16 = ULONG(reader).value
        self.unk17 = ULONG(reader).value
        self.unk18 = PVOID(reader).value
        self.unk19 = PVOID(reader).value
        self.unk20 = PVOID(reader).value
        self.unk21 = PVOID(reader).value
        self.unk22 = PVOID(reader).value
        self.unk23 = PVOID(reader).value

        reader.align()

        self.pKeyList = PVOID(reader)
        self.unk26 = PVOID(reader).value
        self.Tickets_1 = LIST_ENTRY(reader)
        self.unk27 = FILETIME(reader).value
        self.Tickets_2 = LIST_ENTRY(reader)
        self.unk28 = FILETIME(reader).value
        self.Tickets_3 = LIST_ENTRY(reader)
        self.unk29 = FILETIME(reader).value
        self.SmartcardInfos = PVOID(reader)


class KIWI_KERBEROS_LOGON_SESSION_10_1607_X86:
    def __init__(self, reader):
        self.UsageCount = ULONG(reader).value
        reader.align()
        self.unk0 = LIST_ENTRY(reader)
        self.unk1 = PVOID(reader).value
        self.unk1b = ULONG(reader).value
        reader.align()
        self.unk2 = FILETIME(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.unk6 = PVOID(reader).value
        self.LocallyUniqueIdentifier = LUID(reader).value

        self.unk7 = FILETIME(reader).value
        self.unk8 = PVOID(reader).value
        self.unk8b = ULONG(reader).value
        reader.align()
        self.unk9 = FILETIME(reader).value
        self.unk11 = PVOID(reader).value
        self.unk12 = PVOID(reader).value
        self.unk13 = PVOID(reader).value
        self.unkAlign = ULONG(reader).value

        self.credentials = KIWI_KERBEROS_10_PRIMARY_CREDENTIAL_1607(reader)
        self.unk14 = ULONG(reader).value
        self.unk15 = ULONG(reader).value
        self.unk16 = ULONG(reader).value
        self.unk17 = ULONG(reader).value
        self.unk18 = PVOID(reader).value
        self.unk19 = PVOID(reader).value
        self.unk20 = PVOID(reader).value
        self.unk21 = PVOID(reader).value
        self.unk22 = PVOID(reader).value
        self.unk23 = PVOID(reader).value

        reader.align()

        self.pKeyList = PVOID(reader)
        self.unk26 = PVOID(reader).value

        self.Tickets_1 = LIST_ENTRY(reader)
        self.unk27 = FILETIME(reader).value
        self.Tickets_2 = LIST_ENTRY(reader)
        self.unk28 = FILETIME(reader).value
        self.Tickets_3 = LIST_ENTRY(reader)
        self.unk29 = FILETIME(reader).value
        self.SmartcardInfos = PVOID(reader)


class PKIWI_KERBEROS_INTERNAL_TICKET_51(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_INTERNAL_TICKET_51)


class KIWI_KERBEROS_INTERNAL_TICKET_51:
    def __init__(self, reader):
        self.Flink = PKIWI_KERBEROS_INTERNAL_TICKET_51(reader)
        self.Blink = PKIWI_KERBEROS_INTERNAL_TICKET_51(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.ServiceName = PKERB_EXTERNAL_NAME(reader)
        self.TargetName = PKERB_EXTERNAL_NAME(reader)
        self.DomainName = LSA_UNICODE_STRING(reader)
        self.TargetDomainName = LSA_UNICODE_STRING(reader)
        self.Description = LSA_UNICODE_STRING(reader)
        self.AltTargetDomainName = LSA_UNICODE_STRING(reader)
        self.ClientName = PKERB_EXTERNAL_NAME(reader)
        self.TicketFlags = int.from_bytes(reader.read(4), byteorder='big', signed=False)
        self.unk2 = ULONG(reader).value
        self.KeyType = ULONG(reader).value
        self.Key = KIWI_KERBEROS_BUFFER(reader)
        self.unk3 = PVOID(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.unk6 = PVOID(reader).value
        self.unk7 = PVOID(reader).value
        self.unk8 = PVOID(reader).value
        self.StartTime = FILETIME(reader).value
        self.EndTime = FILETIME(reader).value
        self.RenewUntil = FILETIME(reader).value
        self.unk9 = ULONG(reader).value
        self.unk10 = ULONG(reader).value
        self.domain = PCWSTR(reader).value
        self.unk11 = ULONG(reader).value
        self.strangeNames = PVOID(reader).value
        self.unk12 = ULONG(reader).value
        self.TicketEncType = ULONG(reader).value
        self.TicketKvno = ULONG(reader).value
        self.Ticket = KIWI_KERBEROS_BUFFER(reader)


class PKIWI_KERBEROS_INTERNAL_TICKET_52(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_INTERNAL_TICKET_52)


class KIWI_KERBEROS_INTERNAL_TICKET_52:
    def __init__(self, reader):
        self.Flink = PKIWI_KERBEROS_INTERNAL_TICKET_52(reader)
        self.Blink = PKIWI_KERBEROS_INTERNAL_TICKET_52(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.ServiceName = PKERB_EXTERNAL_NAME(reader)
        self.TargetName = PKERB_EXTERNAL_NAME(reader)
        self.DomainName = LSA_UNICODE_STRING(reader)
        self.TargetDomainName = LSA_UNICODE_STRING(reader)
        self.Description = LSA_UNICODE_STRING(reader)
        self.AltTargetDomainName = LSA_UNICODE_STRING(reader)
        self.ClientName = PKERB_EXTERNAL_NAME(reader)
        self.name0 = PVOID(reader).value
        self.TicketFlags = int.from_bytes(reader.read(4), byteorder='big', signed=False)
        self.unk2 = ULONG(reader).value
        self.KeyType = ULONG(reader).value
        self.Key = KIWI_KERBEROS_BUFFER(reader)
        self.unk3 = PVOID(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.StartTime = FILETIME(reader).value
        self.EndTime = FILETIME(reader).value
        self.RenewUntil = FILETIME(reader).value
        self.unk6 = ULONG(reader).value
        self.unk7 = ULONG(reader).value
        self.domain = PCWSTR(reader).value
        self.unk8 = ULONG(reader).value
        self.strangeNames = PVOID(reader).value
        self.unk9 = ULONG(reader).value
        self.TicketEncType = ULONG(reader).value
        self.TicketKvno = ULONG(reader).value
        self.Ticket = KIWI_KERBEROS_BUFFER(reader)


class PKIWI_KERBEROS_INTERNAL_TICKET_60(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_INTERNAL_TICKET_60)


class KIWI_KERBEROS_INTERNAL_TICKET_60:
    def __init__(self, reader):
        self.Flink = PKIWI_KERBEROS_INTERNAL_TICKET_60(reader)
        self.Blink = PKIWI_KERBEROS_INTERNAL_TICKET_60(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.ServiceName = PKERB_EXTERNAL_NAME(reader)
        self.TargetName = PKERB_EXTERNAL_NAME(reader)
        self.DomainName = LSA_UNICODE_STRING(reader)
        self.TargetDomainName = LSA_UNICODE_STRING(reader)
        self.Description = LSA_UNICODE_STRING(reader)
        self.AltTargetDomainName = LSA_UNICODE_STRING(reader)

        self.ClientName = PKERB_EXTERNAL_NAME(reader)
        self.name0 = PVOID(reader).value
        self.TicketFlags = int.from_bytes(reader.read(4), byteorder='big', signed=False)
        self.unk2 = ULONG(reader).value
        self.KeyType = ULONG(reader).value
        self.Key = KIWI_KERBEROS_BUFFER(reader)
        self.unk3 = PVOID(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.StartTime = FILETIME(reader).value
        self.EndTime = FILETIME(reader).value
        self.RenewUntil = FILETIME(reader).value
        self.unk6 = ULONG(reader).value
        self.unk7 = ULONG(reader).value
        self.domain = PCWSTR(reader).value
        self.unk8 = ULONG(reader).value
        self.strangeNames = PVOID(reader).value
        self.unk9 = ULONG(reader).value
        self.TicketEncType = ULONG(reader).value
        self.TicketKvno = ULONG(reader).value
        self.Ticket = KIWI_KERBEROS_BUFFER(reader)


class PKIWI_KERBEROS_INTERNAL_TICKET_6(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_INTERNAL_TICKET_6)


class KIWI_KERBEROS_INTERNAL_TICKET_6:
    def __init__(self, reader):
        self.Flink = PKIWI_KERBEROS_INTERNAL_TICKET_6(reader)
        self.Blink = PKIWI_KERBEROS_INTERNAL_TICKET_6(reader)

        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.ServiceName = PKERB_EXTERNAL_NAME(reader)
        self.TargetName = PKERB_EXTERNAL_NAME(reader)
        self.DomainName = LSA_UNICODE_STRING(reader)
        self.TargetDomainName = LSA_UNICODE_STRING(reader)
        self.Description = LSA_UNICODE_STRING(reader)
        self.AltTargetDomainName = LSA_UNICODE_STRING(reader)
        self.KDCServer = LSA_UNICODE_STRING(reader)
        self.ClientName = PKERB_EXTERNAL_NAME(reader)
        self.name0 = PVOID(reader).value
        self.TicketFlags = int.from_bytes(reader.read(4), byteorder='big', signed=False)
        self.unk2 = ULONG(reader).value
        self.KeyType = ULONG(reader).value
        reader.align()
        self.Key = KIWI_KERBEROS_BUFFER(reader)
        self.unk3 = PVOID(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.StartTime = FILETIME(reader).value
        self.EndTime = FILETIME(reader).value
        self.RenewUntil = FILETIME(reader).value
        self.unk6 = ULONG(reader).value
        self.unk7 = ULONG(reader).value
        self.domain = PCWSTR(reader).value
        self.unk8 = ULONG(reader).value
        reader.align()
        self.strangeNames = PVOID(reader).value
        self.unk9 = ULONG(reader).value
        self.TicketEncType = ULONG(reader).value
        self.TicketKvno = ULONG(reader).value
        reader.align()
        self.Ticket = KIWI_KERBEROS_BUFFER(reader)


class PKIWI_KERBEROS_INTERNAL_TICKET_10(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_INTERNAL_TICKET_10)


class KIWI_KERBEROS_INTERNAL_TICKET_10:
    def __init__(self, reader):
        self.Flink = PKIWI_KERBEROS_INTERNAL_TICKET_10(reader)
        self.Blink = PKIWI_KERBEROS_INTERNAL_TICKET_10(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.ServiceName = PKERB_EXTERNAL_NAME(reader)
        self.TargetName = PKERB_EXTERNAL_NAME(reader)
        self.DomainName = LSA_UNICODE_STRING(reader)
        self.TargetDomainName = LSA_UNICODE_STRING(reader)
        self.Description = LSA_UNICODE_STRING(reader)
        self.AltTargetDomainName = LSA_UNICODE_STRING(reader)
        self.KDCServer = LSA_UNICODE_STRING
        self.unk10586_d = LSA_UNICODE_STRING
        self.ClientName = PKERB_EXTERNAL_NAME(reader)
        self.name0 = PVOID(reader).value
        self.TicketFlags = int.from_bytes(reader.read(4), byteorder='big', signed=False)
        self.unk2 = ULONG(reader).value
        self.KeyType = ULONG(reader).value
        reader.align()
        self.Key = KIWI_KERBEROS_BUFFER(reader)
        self.unk3 = PVOID(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        reader.align(8)
        self.StartTime = FILETIME(reader).value
        self.EndTime = FILETIME(reader).value
        self.RenewUntil = FILETIME(reader).value
        self.unk6 = ULONG(reader).value
        self.unk7 = ULONG(reader).value
        self.domain = PCWSTR(reader).value
        self.unk8 = ULONG(reader).value
        reader.align()
        self.strangeNames = PVOID(reader).value
        self.unk9 = ULONG(reader).value
        self.TicketEncType = ULONG(reader).value
        self.TicketKvno = ULONG(reader).value
        reader.align()
        self.Ticket = KIWI_KERBEROS_BUFFER(reader)


class PKIWI_KERBEROS_INTERNAL_TICKET_11(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_INTERNAL_TICKET_11)


class KIWI_KERBEROS_INTERNAL_TICKET_11:
    def __init__(self, reader):
        self.Flink = PKIWI_KERBEROS_INTERNAL_TICKET_11(reader)
        self.Blink = PKIWI_KERBEROS_INTERNAL_TICKET_11(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.ServiceName = PKERB_EXTERNAL_NAME(reader)
        self.TargetName = PKERB_EXTERNAL_NAME(reader)
        self.DomainName = LSA_UNICODE_STRING(reader)
        self.TargetDomainName = LSA_UNICODE_STRING(reader)
        self.Description = LSA_UNICODE_STRING(reader)
        self.AltTargetDomainName = LSA_UNICODE_STRING(reader)
        self.KDCServer = LSA_UNICODE_STRING(reader)
        self.unk10586_d = LSA_UNICODE_STRING(reader)
        self.ClientName = PKERB_EXTERNAL_NAME(reader)
        self.name0 = PVOID(reader).value
        self.TicketFlags = int.from_bytes(reader.read(4), byteorder='big', signed=False)
        self.unk2 = ULONG(reader).value
        self.unk14393_0 = PVOID(reader).value
        self.unk2x = ULONG(reader).value
        self.KeyType = ULONG(reader).value
        self.Key = KIWI_KERBEROS_BUFFER(reader)
        self.unk14393_1 = PVOID(reader).value
        self.unk3 = PVOID(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.StartTime = FILETIME(reader).value
        self.EndTime = FILETIME(reader).value
        self.RenewUntil = FILETIME(reader).value
        self.unk6 = ULONG(reader).value
        self.unk7 = ULONG(reader).value
        self.domain = PCWSTR(reader).value
        self.unk8 = ULONG(reader).value
        reader.align()
        self.strangeNames = PVOID(reader).value
        self.unk9 = ULONG(reader).value
        self.TicketEncType = ULONG(reader).value
        self.TicketKvno = ULONG(reader).value
        reader.align()
        self.Ticket = KIWI_KERBEROS_BUFFER(reader)


class PKIWI_KERBEROS_INTERNAL_TICKET_10_1607(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_INTERNAL_TICKET_10_1607)


class KIWI_KERBEROS_INTERNAL_TICKET_10_1607:
    def __init__(self, reader):
        self.Flink = PKIWI_KERBEROS_INTERNAL_TICKET_10_1607(reader)
        self.Blink = PKIWI_KERBEROS_INTERNAL_TICKET_10_1607(reader)
        self.unk0 = PVOID(reader).value
        self.unk1 = PVOID(reader).value
        self.ServiceName = PKERB_EXTERNAL_NAME(reader)
        self.TargetName = PKERB_EXTERNAL_NAME(reader)
        self.DomainName = LSA_UNICODE_STRING(reader)
        self.TargetDomainName = LSA_UNICODE_STRING(reader)
        self.Description = LSA_UNICODE_STRING(reader)
        self.AltTargetDomainName = LSA_UNICODE_STRING(reader)
        self.KDCServer = LSA_UNICODE_STRING(reader)
        self.unk10586_d = LSA_UNICODE_STRING(reader)
        self.ClientName = PKERB_EXTERNAL_NAME(reader)
        self.name0 = PVOID(reader).value
        self.TicketFlags = int.from_bytes(reader.read(4), byteorder='big', signed=False)
        self.unk2 = ULONG(reader).value
        self.unk14393_0 = PVOID(reader).value
        self.KeyType = ULONG(reader).value
        reader.align()
        self.Key = KIWI_KERBEROS_BUFFER(reader)
        self.unk14393_1 = PVOID(reader).value
        self.unk3 = PVOID(reader).value
        self.unk4 = PVOID(reader).value
        self.unk5 = PVOID(reader).value
        self.StartTime = FILETIME(reader).value
        self.EndTime = FILETIME(reader).value
        self.RenewUntil = FILETIME(reader).value
        self.unk6 = ULONG(reader).value
        self.unk7 = ULONG(reader).value
        self.domain = PCWSTR(reader).value
        self.unk8 = ULONG(reader).value
        reader.align()
        self.strangeNames = PVOID(reader).value
        self.unk9 = ULONG(reader).value
        self.TicketEncType = ULONG(reader).value
        self.TicketKvno = ULONG(reader).value
        reader.align()
        self.Ticket = KIWI_KERBEROS_BUFFER(reader)


class PKERB_HASHPASSWORD_GENERIC(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KERB_HASHPASSWORD_GENERIC)


class KERB_HASHPASSWORD_GENERIC:
    def __init__(self, reader):
        self.Type = DWORD(reader).value
        reader.align()
        self.Size = SIZE_T(reader).value
        self.Checksump = PVOID(reader)


class PKERB_HASHPASSWORD_5(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KERB_HASHPASSWORD_5)


class KERB_HASHPASSWORD_5:
    def __init__(self, reader):
        self.salt = LSA_UNICODE_STRING(reader)
        self.generic = KERB_HASHPASSWORD_GENERIC(reader)


class PKERB_HASHPASSWORD_6(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KERB_HASHPASSWORD_6)


class KERB_HASHPASSWORD_6:
    def __init__(self, reader):
        self.salt = LSA_UNICODE_STRING(reader)
        self.stringToKey = PVOID(reader)
        self.generic = KERB_HASHPASSWORD_GENERIC(reader)


class PKERB_HASHPASSWORD_6_1607(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KERB_HASHPASSWORD_6_1607)


class KERB_HASHPASSWORD_6_1607:
    def __init__(self, reader):
        self.salt = LSA_UNICODE_STRING(reader)
        self.stringToKey = PVOID(reader).value
        self.unk0 = PVOID(reader).value
        self.generic = KERB_HASHPASSWORD_GENERIC(reader)


class PKIWI_KERBEROS_KEYS_LIST_5(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_KEYS_LIST_5)


class KIWI_KERBEROS_KEYS_LIST_5:
    def __init__(self, reader):
        self.unk0 = DWORD(reader).value
        self.cbItem = DWORD(reader).value
        self.unk1 = PVOID(reader).value
        self.unk2 = PVOID(reader).value

        self.KeyEntries_start = reader.tell()
        self.KeyEntries = []

    def read(self, reader, keyentries_type):
        reader.move(self.KeyEntries_start)
        for _ in range(self.cbItem):
            self.KeyEntries.append(keyentries_type(reader))


class PKIWI_KERBEROS_KEYS_LIST_6(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_KEYS_LIST_6)


class KIWI_KERBEROS_KEYS_LIST_6:
    def __init__(self, reader):
        self.unk0 = DWORD(reader).value
        self.cbItem = DWORD(reader).value
        self.unk1 = PVOID(reader).value
        self.unk2 = PVOID(reader).value
        self.unk3 = PVOID(reader).value
        self.unk4 = PVOID(reader).value
        self.KeyEntries_start = reader.tell()
        self.KeyEntries = []

    def read(self, reader, keyentries_type):
        reader.move(self.KeyEntries_start)
        for _ in range(self.cbItem):
            self.KeyEntries.append(keyentries_type(reader))


class PKIWI_KERBEROS_ENUM_DATA_TICKET(POINTER):
    def __init__(self, reader):
        super().__init__(reader, KIWI_KERBEROS_ENUM_DATA_TICKET)


class KIWI_KERBEROS_ENUM_DATA_TICKET:
    def __init__(self, reader):
        self.isTicketExport = BOOL(reader).value
        self.isFullTicket = BOOL(reader).value


class KIWI_KERBEROS_BUFFER:
    def __init__(self, reader):
        self.Length = ULONG(reader).value
        reader.align()
        self.Value = PVOID(reader)

        self.Data = None

    def read(self, reader):
        self.Data = self.Value.read_raw(reader, self.Length)
        return self.Data
