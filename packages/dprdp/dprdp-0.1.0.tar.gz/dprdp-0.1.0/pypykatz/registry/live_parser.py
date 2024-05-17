import platform

if platform.system() != 'Windows':
    raise Exception('This will ONLY work on Windows systems!')

import json

from pypykatz.commons.readers.registry.live.reader import LiveRegistryHive
from pypykatz.registry.sam.sam import *
from pypykatz.registry.security.security import *
from pypykatz.registry.system.system import *
from pypykatz.registry.software.software import *

from pypykatz.commons.winapi.processmanipulator import ProcessManipulator
from pypykatz.commons.common import UniversalEncoder


class LiveRegistry:

    def __init__(self):
        self.sam_hive = None
        self.security_hive = None
        self.system_hive = None
        self.software_hive = None

        self.system = None
        self.sam = None
        self.security = None
        self.software = None

    def get_secrets(self):

        pm = ProcessManipulator()
        try:

            pm.assign_token_thread_sid()
        except Exception as e:
            logger.error('Failed to obtain SYSTEM prvis. On-the-fly parsing is not possible.')
            raise e
        else:
            self.system = SYSTEM(self.system_hive)
            bootkey = self.system.get_bootkey()

            if self.sam_hive:
                self.sam = SAM(self.sam_hive, bootkey)
                self.sam.get_secrets()

            if self.security_hive:
                self.security = SECURITY(self.security_hive, bootkey)
                self.security.get_secrets()

            if self.software_hive:
                try:
                    self.software = SOFTWARE(self.software_hive, bootkey)
                    self.software.get_default_logon()
                except Exception as e:
                    logger.warning('Failed to parse SOFTWARE hive. Reason: %s' % str(e))
            self.cleanup()

    def cleanup(self):
        for hive in [self.system_hive, self.security_hive, self.sam_hive]:
            try:
                hive.close()
            except:
                pass

    def to_file(self, file_path, json_format=False):
        with open(file_path, 'a', newline='') as f:
            if not json_format:
                f.write(str(self))
            else:
                f.write(self.to_json())

    def to_json(self):
        return json.dumps(self.to_dict(), cls=UniversalEncoder, indent=4, sort_keys=True)

    def to_dict(self):
        t = {'SYSTEM': self.system.to_dict()}
        if self.sam:
            t['SAM'] = self.sam.to_dict()
        if self.security:
            t['SECURITY'] = self.security.to_dict()
        if self.software:
            t['SOFTWARE'] = self.software.to_dict()
        return t

    def __str__(self):
        t = str(self.system)
        if self.sam:
            t += str(self.sam)
        if self.security:
            t += str(self.security)
        return t

    @staticmethod
    def go_live():
        lr = LiveRegistry()
        lr.sam_hive = LiveRegistryHive('SAM')
        lr.system_hive = LiveRegistryHive('SYSTEM')
        lr.security_hive = LiveRegistryHive('SECURITY')
        lr.software_hive = LiveRegistryHive('SOFTWARE')

        lr.get_secrets()
        return lr
