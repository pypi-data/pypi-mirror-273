from abc import ABC, abstractmethod
from pypykatz import logger
from pypykatz.commons.common import hexdump
from pypykatz.alsadecryptor.win_datatypes import RTL_AVL_TABLE


class Logger:
    def __init__(self, module_name, package_name, sysinfo):
        self.package_name = package_name
        self.module_name = module_name
        self.sysinfo = sysinfo
        self.logger = logger

    def get_level(self):
        return self.logger.getEffectiveLevel()

    def log(self, msg, loglevel=1):
        first = True
        for line in msg.split('\n'):
            if first:
                self.logger.log(loglevel, '[%s] [%s] %s' % (self.package_name, self.module_name, line))
                first = False
            else:
                self.logger.log(loglevel, '[%s] [%s]    %s' % (self.package_name, self.module_name, line))


class PackageTemplate:
    def __init__(self, package_name, sysinfo=None):
        self.logger = Logger('template', package_name, sysinfo)
        self.package_name = package_name
        self.sysinfo = sysinfo

    def log(self, msg, loglevel=6):
        self.logger.log(loglevel, '%s' % msg)

    def log_template(self, struct_var_name, struct_template_obj, loglevel=6):
        self.logger.log('Selecting template for %s: %s' % (struct_var_name, struct_template_obj.__name__), loglevel)

    @staticmethod
    @abstractmethod
    def get_template(sysinfo):
        pass


class PackageDecryptor:
    def __init__(self, package_name, lsa_decryptor, sysinfo, reader):
        self.logger = Logger('decryptor', package_name, sysinfo)
        self.package_name = package_name
        self.lsa_decryptor = lsa_decryptor
        self.sysinfo = sysinfo
        self.reader = reader

    def log(self, msg, loglevel=6):
        self.logger.log('%s' % msg, loglevel)

    async def find_signature(self, module_name, signature):

        self.log('Searching for key struct signature')
        fl = await self.reader.find_in_module(module_name, self.decryptor_template.signature, find_first=True)
        if len(fl) == 0:
            raise Exception('Signature was not found in module %s Signature: %s' % (
                module_name, self.decryptor_template.signature.hex()))
        return fl[0]

    async def log_ptr(self, ptr, name, datasize=None):

        level = self.logger.get_level()
        if level > 6 or level == 0:
            return

        if not datasize:
            if level == 5:
                datasize = 0x10
            if level == 4:
                datasize = 0x20
            if level == 3:
                datasize = 0x50
            if level == 2:
                datasize = 0x100
            if level == 1:
                datasize = 0x200

        pos = self.reader.tell()
        try:
            await self.reader.move(ptr)
            data = await self.reader.peek(datasize)
            await self.reader.move(pos)
            self.log('%s: %s\n%s' % (name, hex(ptr), hexdump(data, start=ptr)))
        except Exception as e:
            self.log('%s: Logging failed for position %s' % (name, hex(ptr)))

    def decrypt_password(self, enc_password, bytes_expected=False, trim_zeroes=True, segment_size=128):

        dec_password = None
        temp = self.lsa_decryptor.decrypt(enc_password, segment_size=segment_size)
        if temp and len(temp) > 0:
            if not bytes_expected:
                try:
                    dec_password = temp.decode('utf-16-le')
                except:
                    try:
                        dec_password = temp.decode('utf-8')
                    except:
                        try:
                            dec_password = temp.decode('ascii')
                        except:
                            dec_password = temp.hex()
                else:
                    if trim_zeroes:
                        dec_password = dec_password.rstrip('\x00')
            else:
                dec_password = temp

        return dec_password, temp

    async def walk_avl(self, node_ptr, result_ptr_list):

        node = await node_ptr.read(self.reader, override_finaltype=RTL_AVL_TABLE)
        if node is None:
            self.log('AVL walker found empty tree')
            return
        if node.OrderedPointer.value != 0:
            result_ptr_list.append(node.OrderedPointer.value)
            if node.BalancedRoot.LeftChild.value != 0:
                await self.walk_avl(node.BalancedRoot.LeftChild, result_ptr_list)
            if node.BalancedRoot.RightChild.value != 0:
                await self.walk_avl(node.BalancedRoot.RightChild, result_ptr_list)

    async def walk_list(self, entry_ptr, callback, max_walk=255, override_ptr=None):

        entries_seen = {entry_ptr.location: 1}
        max_walk = max_walk
        await self.log_ptr(entry_ptr.value,
                           'List entry -%s-' % entry_ptr.finaltype.__name__ if not override_ptr else override_ptr.__name__)
        while True:
            if override_ptr:
                entry = await entry_ptr.read(self.reader, override_ptr)
            else:
                entry = await entry_ptr.read(self.reader)

            if not entry:
                break

            await callback(entry)

            max_walk -= 1
            self.log('%s next ptr: %x' % (
                entry.Flink.finaltype.__name__ if not override_ptr else override_ptr.__name__, entry.Flink.value))
            self.log('%s seen: %s' % (entry.Flink.finaltype.__name__ if not override_ptr else override_ptr.__name__,
                                      entry.Flink.value not in entries_seen))
            self.log('%s max_walk: %d' % (
                entry.Flink.finaltype.__name__ if not override_ptr else override_ptr.__name__, max_walk))
            if entry.Flink.value != 0 and entry.Flink.value not in entries_seen and max_walk != 0:
                entries_seen[entry.Flink.value] = 1
                await self.log_ptr(entry.Flink.value,
                                   'Next list entry -%s-' % entry.Flink.finaltype.__name__ if not override_ptr else override_ptr.__name__)
                entry_ptr = entry.Flink
            else:
                break
