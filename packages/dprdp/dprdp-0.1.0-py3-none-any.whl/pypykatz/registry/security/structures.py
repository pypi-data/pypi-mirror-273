import io

from pypykatz.commons.filetime import filetime_to_dt


class LSA_SECRET_BLOB:
    def __init__(self):
        self.legnth = None
        self.unk = None
        self.secret = None

    @staticmethod
    def from_bytes(data):
        return LSA_SECRET_BLOB.from_buffer(io.BytesIO(data))

    @staticmethod
    def from_buffer(buff):
        sk = LSA_SECRET_BLOB()
        sk.legnth = int.from_bytes(buff.read(4), 'little')
        sk.unk = buff.read(12)
        sk.secret = buff.read(sk.legnth)
        return sk

    def __str__(self):
        t = '== LSA_SECRET_BLOB ==\r\n'
        for k in self.__dict__:
            if isinstance(self.__dict__[k], list):
                for i, item in enumerate(self.__dict__[k]):
                    t += '   %s: %s: %s' % (k, i, str(item))
            else:
                t += '%s: %s \r\n' % (k, str(self.__dict__[k]))
        return t


class LSA_SECRET:
    def __init__(self):
        self.version = None
        self.enc_key_id = None
        self.enc_algo = None
        self.flags = None
        self.data = None

    @staticmethod
    def from_bytes(data):
        return LSA_SECRET.from_buffer(io.BytesIO(data))

    @staticmethod
    def from_buffer(buff):
        sk = LSA_SECRET()
        sk.version = int.from_bytes(buff.read(4), 'little')
        sk.enc_key_id = buff.read(16)
        sk.enc_algo = int.from_bytes(buff.read(4), 'little')
        sk.flags = int.from_bytes(buff.read(4), 'little')
        sk.data = buff.read()

        return sk

    def __str__(self):
        t = '== LSA_SECRET ==\r\n'
        for k in self.__dict__:
            if isinstance(self.__dict__[k], list):
                for i, item in enumerate(self.__dict__[k]):
                    t += '   %s: %s: %s' % (k, i, str(item))
            else:
                t += '%s: %s \r\n' % (k, str(self.__dict__[k]))
        return t


class LSA_SECRET_XP:
    def __init__(self):
        self.legnth = None
        self.version = None
        self.secret = None

    @staticmethod
    def from_bytes(data):
        return LSA_SECRET_XP.from_buffer(io.BytesIO(data))

    @staticmethod
    def from_buffer(buff):
        sk = LSA_SECRET_XP()
        sk.legnth = int.from_bytes(buff.read(4), 'little')
        sk.version = int.from_bytes(buff.read(4), 'little')
        sk.secret = buff.read(sk.legnth)

        return sk

    def __str__(self):
        t = '== LSA_SECRET_XP ==\r\n'
        for k in self.__dict__:
            if isinstance(self.__dict__[k], list):
                for i, item in enumerate(self.__dict__[k]):
                    t += '   %s: %s: %s' % (k, i, str(item))
            else:
                t += '%s: %s \r\n' % (k, str(self.__dict__[k]))
        return t


class NL_RECORD:
    def __init__(self):
        self.UserLength = None
        self.DomainNameLength = None
        self.EffectiveNameLength = None
        self.FullNameLength = None
        self.LogonScriptName = None
        self.ProfilePathLength = None
        self.HomeDirectoryLength = None
        self.HomeDirectoryDriveLength = None
        self.UserId = None
        self.PrimaryGroupId = None
        self.GroupCount = None
        self.logonDomainNameLength = None
        self.unk0 = None
        self.LastWrite = None
        self.Revision = None
        self.SidCount = None
        self.Flags = None
        self.unk1 = None
        self.LogonPackageLength = None
        self.DnsDomainNameLength = None
        self.UPN = None
        self.IV = None
        self.CH = None
        self.EncryptedData = None

    @staticmethod
    def from_bytes(data):
        return NL_RECORD.from_buffer(io.BytesIO(data))

    @staticmethod
    def from_buffer(buff):
        nl = NL_RECORD()
        nl.UserLength = int.from_bytes(buff.read(2), 'little')
        nl.DomainNameLength = int.from_bytes(buff.read(2), 'little')
        nl.EffectiveNameLength = int.from_bytes(buff.read(2), 'little')
        nl.FullNameLength = int.from_bytes(buff.read(2), 'little')
        nl.LogonScriptName = int.from_bytes(buff.read(2), 'little')
        nl.ProfilePathLength = int.from_bytes(buff.read(2), 'little')
        nl.HomeDirectoryLength = int.from_bytes(buff.read(2), 'little')
        nl.HomeDirectoryDriveLength = int.from_bytes(buff.read(2), 'little')
        nl.UserId = int.from_bytes(buff.read(4), 'little')
        nl.PrimaryGroupId = int.from_bytes(buff.read(4), 'little')
        nl.GroupCount = int.from_bytes(buff.read(4), 'little')
        nl.logonDomainNameLength = int.from_bytes(buff.read(2), 'little')
        nl.unk0 = int.from_bytes(buff.read(2), 'little')
        nl.LastWrite = int.from_bytes(buff.read(8), 'little')
        nl.Revision = int.from_bytes(buff.read(4), 'little')
        nl.SidCount = int.from_bytes(buff.read(4), 'little')
        nl.Flags = int.from_bytes(buff.read(4), 'little')
        nl.unk1 = int.from_bytes(buff.read(4), 'little')
        nl.LogonPackageLength = int.from_bytes(buff.read(4), 'little')
        nl.DnsDomainNameLength = int.from_bytes(buff.read(2), 'little')
        nl.UPN = int.from_bytes(buff.read(2), 'little')
        nl.IV = buff.read(16)
        nl.CH = buff.read(16)
        nl.EncryptedData = buff.read()

        try:
            nl.LastWrite = filetime_to_dt(nl.LastWrite)
        except Exception:
            nl.LastWrite = None

        return nl

    def __str__(self):
        t = '== NL_RECORD ==\r\n'
        for k in self.__dict__:
            if isinstance(self.__dict__[k], list):
                for i, item in enumerate(self.__dict__[k]):
                    t += '   %s: %s: %s' % (k, i, str(item))
            else:
                t += '%s: %s \r\n' % (k, str(self.__dict__[k]))
        return t
