from .common.live_reader_ctypes import *
from .common.privileges import enable_debug_privilege
from .common.psapi import *
from .common.version import *
from .common.kernel32 import *
from .common.fileinfo import *
from minidump.streams.SystemInfoStream import PROCESSOR_ARCHITECTURE

from pypykatz import logger
import sys
import copy
import platform
import os
import ntpath
import winreg


class Module:
    def __init__(self):
        self.name = None
        self.baseaddress = None
        self.size = None
        self.endaddress = None
        self.pages = []

        self.versioninfo = None
        self.checksum = None
        self.timestamp = None

    def inrange(self, addr):
        return self.baseaddress <= addr < self.endaddress

    @staticmethod
    def parse(name, module_info, timestamp):
        m = Module()
        m.name = name
        m.baseaddress = module_info.lpBaseOfDll
        m.size = module_info.SizeOfImage
        m.endaddress = m.baseaddress + m.size

        m.timestamp = timestamp

        return m

    def __str__(self):
        return '%s %s %s %s %s' % (
        self.name, hex(self.baseaddress), hex(self.size), hex(self.endaddress), self.timestamp)


class Page:
    def __init__(self):
        self.BaseAddress = None
        self.AllocationBase = None
        self.AllocationProtect = None
        self.RegionSize = None
        self.EndAddress = None

        self.data = None

    @staticmethod
    def parse(page_info):
        p = Page()
        p.BaseAddress = page_info.BaseAddress
        p.AllocationBase = page_info.AllocationBase
        p.AllocationProtect = page_info.AllocationProtect
        p.RegionSize = min(page_info.RegionSize, 100 * 1024 * 1024)
        p.EndAddress = page_info.BaseAddress + page_info.RegionSize
        return p

    def read_data(self, process_handle):
        self.data = ReadProcessMemory(process_handle, self.BaseAddress, self.RegionSize)

    def inrange(self, addr):
        return self.BaseAddress <= addr < self.EndAddress

    def search(self, pattern, process_handle):
        if len(pattern) > self.RegionSize:
            return []
        data = ReadProcessMemory(process_handle, self.BaseAddress, self.RegionSize)
        fl = []
        offset = 0
        while len(data) > len(pattern):
            marker = data.find(pattern)
            if marker == -1:
                return fl
            fl.append(marker + offset + self.BaseAddress)
            data = data[marker + 1:]
            offset += marker + 1

        return fl

    def __str__(self):
        return '0x%08x 0x%08x %s 0x%08x' % (
        self.BaseAddress, self.AllocationBase, self.AllocationProtect, self.RegionSize)


class BufferedLiveReader:
    def __init__(self, reader):
        self.reader = reader
        self.pages = []

        self.current_segment = None
        self.current_position = None

    def _select_segment(self, requested_position):

        for page in self.pages:
            if page.inrange(requested_position):
                self.current_segment = page
                self.current_position = requested_position
                return

        for page in self.reader.pages:
            if page.inrange(requested_position):
                page.read_data(self.reader.process_handle)
                newsegment = copy.deepcopy(page)
                self.pages.append(newsegment)
                self.current_segment = newsegment
                self.current_position = requested_position
                return

        raise Exception('Memory address 0x%08x is not in process memory space' % requested_position)

    def get_reader(self):
        return self.reader

    def seek(self, offset, whence=0):

        if whence == 0:
            t = self.current_segment.BaseAddress + offset
        elif whence == 1:
            t = self.current_position + offset
        elif whence == 2:
            t = self.current_segment.EndAddress - offset
        else:
            raise Exception('Seek function whence value must be between 0-2')

        if not self.current_segment.inrange(t):
            raise Exception('Seek would cross memory segment boundaries (use move)')

        self.current_position = t
        return

    def move(self, address):

        self._select_segment(address)
        return

    def align(self, alignment=None):

        if alignment is None:
            if self.reader.processor_architecture == PROCESSOR_ARCHITECTURE.AMD64:
                alignment = 8
            else:
                alignment = 4
        offset = self.current_position % alignment
        if offset == 0:
            return
        offset_to_aligned = (alignment - offset) % alignment
        self.seek(offset_to_aligned, 1)
        return

    def tell(self):

        return self.current_position

    def peek(self, length):

        t = self.current_position + length
        if not self.current_segment.inrange(t):
            raise Exception('Would read over segment boundaries!')
        return self.current_segment.data[
               self.current_position - self.current_segment.BaseAddress:t - self.current_segment.BaseAddress]

    def read(self, size=-1):

        if size < -1:
            raise Exception('You shouldnt be doing this')
        if size == -1:
            t = self.current_segment.remaining_len(self.current_position)
            if not t:
                return None

            old_new_pos = self.current_position
            self.current_position = self.current_segment.EndAddress
            return self.current_segment.data[old_new_pos - self.current_segment.BaseAddress:]

        t = self.current_position + size
        if not self.current_segment.inrange(t):
            raise Exception('Would read over segment boundaries!')

        old_new_pos = self.current_position
        self.current_position = t
        return self.current_segment.data[
               old_new_pos - self.current_segment.BaseAddress:t - self.current_segment.BaseAddress]

    def read_int(self):

        if self.reader.processor_architecture == PROCESSOR_ARCHITECTURE.AMD64:
            return int.from_bytes(self.read(8), byteorder='little', signed=True)
        else:
            return int.from_bytes(self.read(4), byteorder='little', signed=True)

    def read_uint(self):

        if self.reader.processor_architecture == PROCESSOR_ARCHITECTURE.AMD64:
            return int.from_bytes(self.read(8), byteorder='little', signed=False)
        else:
            return int.from_bytes(self.read(4), byteorder='little', signed=False)

    def find(self, pattern):

        pos = self.current_segment.data.find(pattern)
        if pos == -1:
            return -1
        return pos + self.current_position

    def find_all(self, pattern):

        pos = []
        last_found = -1
        while True:
            last_found = self.current_segment.data.find(pattern, last_found + 1)
            if last_found == -1:
                break
            pos.append(last_found + self.current_segment.start_address)

        return pos

    def find_global(self, pattern):

        pos_s = self.reader.search(pattern)
        if len(pos_s) == 0:
            return -1

        return pos_s[0]

    def find_all_global(self, pattern, allocationprotect=0x04):

        return self.reader.search(pattern, allocationprotect=allocationprotect)

    def get_ptr(self, pos):
        self.move(pos)
        return self.read_uint()

    def get_ptr_with_offset(self, pos):
        if self.reader.processor_architecture == PROCESSOR_ARCHITECTURE.AMD64:
            self.move(pos)
            ptr = int.from_bytes(self.read(4), byteorder='little', signed=True)
            return pos + 4 + ptr
        else:
            self.move(pos)
            return self.read_uint()

    def find_in_module(self, module_name, pattern, find_first=False, reverse_order=False):
        t = self.reader.search_module(module_name, pattern, find_first=find_first, reverse_order=reverse_order)
        return t


class LiveReader:
    def __init__(self, process_handle=None, process_name='lsass.exe', process_pid=None):
        self.processor_architecture = None
        self.process_name = process_name
        self.process_handle = process_handle
        self.process_pid = process_pid
        self.current_position = None
        self.BuildNumber = None
        self.modules = []
        self.pages = []

        self.msv_dll_timestamp = None

        self.sanity_check()
        self.setup()

    def sanity_check(self):

        is_python_64 = sys.maxsize > 2 ** 32
        is_windows = platform.system() == 'Windows'
        is_windows_64 = platform.machine().endswith('64')
        if is_windows == False:
            raise Exception('This will only run on Windows')

        if is_windows_64 != is_python_64:
            raise Exception('Python interpreter must be the same architecure of the OS you are running it on.')

    def setup(self):
        logger.log(1, 'Enabling debug privilege')
        enable_debug_privilege()
        logger.log(1, 'Getting generic system info')
        sysinfo = GetSystemInfo()
        self.processor_architecture = PROCESSOR_ARCHITECTURE(sysinfo.id.w.wProcessorArchitecture)

        logger.log(1, 'Getting build number')

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\')
        buildnumber, t = winreg.QueryValueEx(key, 'CurrentBuildNumber')
        self.BuildNumber = int(buildnumber)

        if self.process_handle is None:
            if self.process_pid is None:
                if self.process_name is None:
                    raise Exception('Process name or PID or opened handle must be provided')

                logger.log(1, 'Searching for lsass.exe')
                self.process_pid = pid_for_name(self.process_name)
                logger.log(1, '%s found at PID %d' % (self.process_name, self.process_pid))
                logger.log(1, 'Checking Lsass.exe protection status')

            logger.log(1, 'Opening %s' % self.process_name)
            self.process_handle = OpenProcess(PROCESS_ALL_ACCESS, False, self.process_pid)
            if self.process_handle is None:
                raise Exception('Failed to open lsass.exe Reason: %s' % ctypes.WinError())
        else:
            logger.debug('Using pre-defined handle')
        logger.log(1, 'Enumerating modules')
        module_handles = EnumProcessModules(self.process_handle)
        for module_handle in module_handles:

            module_file_path = GetModuleFileNameExW(self.process_handle, module_handle)
            logger.log(1, module_file_path)
            timestamp = 0
            if ntpath.basename(module_file_path).lower() == 'msv1_0.dll':
                timestamp = int(os.stat(module_file_path).st_ctime)
                self.msv_dll_timestamp = timestamp
            modinfo = GetModuleInformation(self.process_handle, module_handle)
            self.modules.append(Module.parse(module_file_path, modinfo, timestamp))

        logger.log(1, 'Found %d modules' % len(self.modules))

        current_address = sysinfo.lpMinimumApplicationAddress
        while current_address < sysinfo.lpMaximumApplicationAddress:
            page_info = VirtualQueryEx(self.process_handle, current_address)
            self.pages.append(Page.parse(page_info))

            current_address += page_info.RegionSize

        logger.log(1, 'Found %d pages' % len(self.pages))

        for page in self.pages:
            for mod in self.modules:
                if mod.inrange(page.BaseAddress) == True:
                    mod.pages.append(page)

    def get_handler(self):
        return self.process_handle

    def get_memory(self, allocationprotect=0x04):
        t = []
        for page in self.pages:
            if page.AllocationProtect & allocationprotect:
                t.append(page)
        return t

    def get_buffered_reader(self):
        return BufferedLiveReader(self)

    def get_module_by_name(self, module_name):
        for mod in self.modules:
            if mod.name.lower().find(module_name.lower()) != -1:
                return mod
        return None

    def search_module(self, module_name, pattern, find_first=False, reverse_order=False):
        mod = self.get_module_by_name(module_name)
        if mod is None:
            raise Exception('Could not find module! %s' % module_name)
        needles = []
        for page in mod.pages:
            needles += page.search(pattern, self.process_handle)
            if len(needles) > 0 and find_first is True:
                return needles

        return needles

    def search(self, pattern, allocationprotect=0x04):
        t = []
        for page in self.pages:
            if page.AllocationProtect & allocationprotect:
                t += page.search(pattern, self.process_handle)
        return t


if __name__ == '__main__':
    logger.basicConfig(level=1)
    lr = LiveReader()
    blr = lr.get_buffered_reader()

    blr.move(0x1000)
