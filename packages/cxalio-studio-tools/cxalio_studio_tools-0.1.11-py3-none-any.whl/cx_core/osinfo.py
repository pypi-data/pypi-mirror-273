import platform
from functools import cache
import os
from pathlib import Path


class OSInfo:
    def __init__(self):
        self.__system = platform.system()

    @property
    def system(self):
        return self.__system

    @property
    def hosts_file(self):
        if self.system == 'Windows':
            windir = Path(os.getenv('windir'))
            return windir / "System32/drivers/etc/hosts"
        return Path("/etc/hosts")

