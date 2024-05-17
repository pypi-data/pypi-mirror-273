from unicrypto.hashlib import md4 as MD4
from pypykatz.dpapi.structures.system import DPAPI_SYSTEM
from pypykatz.commons.common import hexdump


class LSASecret:
    def __init__(self, key_name, raw_secret, history=False):
        self.raw_secret = raw_secret
        self.key_name = key_name
        self.history = history

    @staticmethod
    def process(key_name, raw_secret, history=False, system_hive=None):
        kn = key_name.upper()
        if len(raw_secret) == 0:
            return
        if raw_secret.startswith(b'\x00\x00'):
            return

        if kn.startswith('_SC_'):
            lss = LSASecretService(kn, raw_secret, history, system_hive)
            lss.process_secret()

        elif kn.startswith('DEFAULTPASSWORD'):
            lss = LSASecretDefaultPassword(kn, raw_secret, history)
            lss.process_secret()

        elif kn.startswith('ASPNET_WP_PASSWORD'):
            lss = LSASecretASPNET(kn, raw_secret, history)
            lss.process_secret()

        elif kn.startswith('DPAPI_SYSTEM'):
            lss = LSASecretDPAPI(kn, raw_secret, history)
            lss.process_secret()

        elif kn.startswith('$MACHINE.ACC'):
            lss = LSASecretMachineAccount(kn, raw_secret, history)
            lss.process_secret()

        else:
            lss = LSASecret(kn, raw_secret, history)

        return lss

    def __str__(self):
        return '=== LSASecret %s ===\r\n' % self.key_name + '\r\nHistory: %s' % self.history + '\r\nSecret: \r\n' + hexdump(
            self.raw_secret)

    def to_dict(self):
        t = {'type': 'LSASecret', 'key_name': self.key_name, 'history': self.history, 'raw_secret': self.raw_secret}
        return t


class LSASecretService(LSASecret):
    def __init__(self, key_name, raw_secret, history, system_hive=None):
        LSASecret.__init__(self, key_name, raw_secret, history)
        self.system_hive = system_hive
        self.service = None
        self.username = None
        self.secret = None

    def process_secret(self):
        try:
            self.secret = self.raw_secret.decode('utf-16-le')
        except:
            self.secret = self.raw_secret.hex()
        else:

            self.service = self.key_name
            self.username = 'UNKNOWN'
            if self.system_hive is not None:
                print(self.key_name[4:])
                self.username = self.system_hive.get_service_user(self.key_name[4:])

    def __str__(self):
        return '=== LSA Service User Secret ===\r\nHistory: %s\r\nService name: %s \r\nUsername: %s' % (
            self.history, self.service, self.username) + '\r\n' + hexdump(self.secret)

    def to_dict(self):
        t = {'type': 'LSASecretService', 'key_name': self.key_name, 'history': self.history, 'username': self.username,
             'secret': self.secret, 'service': self.service}
        return t


class LSASecretDefaultPassword(LSASecret):
    def __init__(self, key_name, raw_secret, history):
        LSASecret.__init__(self, key_name, raw_secret, history)
        self.username = None
        self.secret = None

    def process_secret(self):
        try:
            self.secret = self.raw_secret.decode('utf-16-le')
        except:
            pass
        else:

            self.username = 'UNKNOWN'

    def __str__(self):
        return '=== LSA Default Password ===\r\nHistory: %s\r\nUsername: %s\r\nPassword: %s' % (
            self.history, self.username, self.secret)

    def to_dict(self):
        t = {'type': 'LSASecretDefaultPassword', 'key_name': self.key_name, 'history': self.history,
             'username': self.username, 'secret': self.secret}
        return t


class LSASecretASPNET(LSASecret):
    def __init__(self, key_name, raw_secret, history):
        LSASecret.__init__(self, key_name, raw_secret, history)
        self.username = 'ASPNET'
        self.secret = None

    def process_secret(self):
        try:
            self.secret = self.raw_secret.decode('utf-16-le')
        except:
            pass

    def __str__(self):
        return '=== LSA ASPNET Password ===\r\nHistory: %s\r\nUsername: %s\r\nPassword: %s' % (
            self.history, self.username, self.secret)

    def to_dict(self):
        t = {'type': 'LSASecretASPNET', 'key_name': self.key_name, 'history': self.history, 'username': self.username,
             'secret': self.secret}
        return t


class LSASecretMachineAccount(LSASecret):
    def __init__(self, key_name, raw_secret, history):
        LSASecret.__init__(self, key_name, raw_secret, history)
        self.username = None
        self.secret = None
        self.kerberos_password = None

    def process_secret(self):
        ctx = MD4(self.raw_secret)

        self.secret = ctx.digest()

        self.kerberos_password = self.raw_secret.decode('utf-16-le', 'replace').encode('utf-8', 'replace')

    def to_dict(self):
        t = {'type': 'LSASecretMachineAccount', 'key_name': self.key_name, 'history': self.history,
             'username': self.username, 'secret': self.secret, 'kerberos_password': self.kerberos_password}
        return t

    def __str__(self):
        return '=== LSA Machine account password ===\r\nHistory: %s\r\nNT: %s\r\nPassword(hex): %s\r\nKerberos password(hex): %s' % (
            self.history, self.secret.hex(), self.raw_secret.hex(), self.kerberos_password.hex())


class LSASecretDPAPI(LSASecret):
    def __init__(self, key_name, raw_secret, history):
        LSASecret.__init__(self, key_name, raw_secret, history)
        self.machine_key = None
        self.user_key = None

    def process_secret(self):
        ds = DPAPI_SYSTEM.from_bytes(self.raw_secret)
        self.machine_key = ds.machine_key
        self.user_key = ds.user_key

    def to_dict(self):
        t = {'type': 'LSASecretDPAPI', 'key_name': self.key_name, 'history': self.history,
             'machine_key': self.machine_key, 'user_key': self.user_key}
        return t

    def __str__(self):
        return '=== LSA DPAPI secret ===\r\nHistory: %s\r\nMachine key (hex): %s\r\nUser key(hex): %s' % (
            self.history, self.machine_key.hex(), self.user_key.hex())


class LSADCCSecret:
    def __init__(self, version, domain, username, hash_value, iteration=10240, last_write_ts=None):
        self.version = version
        self.domain = domain
        self.username = username
        self.iteration = iteration
        self.hash_value = hash_value
        self.last_write_ts = last_write_ts

    def to_dict(self):
        t = {'version': self.version, 'domain': self.domain, 'username': self.username, 'iteration': self.iteration,
             'hash_value': self.hash_value, 'lastwrite': self.get_lastwrite()}
        return t

    def get_lastwrite(self, default=None):
        if self.last_write_ts is None:
            return default
        return self.last_write_ts.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.to_lopth()

    def to_lopth(self):
        if self.version == 1:
            return "%s/%s:%s:%s" % (self.domain, self.username, self.hash_value.hex(), self.username)
        else:
            return "%s/%s:*%s*$DCC2$%s#%s#%s" % (
                self.domain, self.username, self.get_lastwrite(''), self.iteration, self.username,
                self.hash_value.hex())
