'''
在Windows和Linux上讲远程盘和本地盘路径互相转换
'''
import locale
import platform
import re
import socket
import subprocess
from pathlib import Path

from bidict import bidict

encoding = locale.getpreferredencoding()


def query_domain(domain: str):
    return socket.gethostbyname(domain)

class NetpathResolver:
    def __init__(self):
        self.system = platform.system().lower()

        """
        servers 的键是通用表示, 所以是str, 值是本地实际路径, 所以是Path, 例: 
        {'//10.10.47.90/connectome': PosixPath('/mnt/90-connectome'),}
        """
        self.servers: bidict[str, Path] = {
            'linux': NetpathResolver.get_linux_mount,
            'windows': NetpathResolver.get_windows_mount,
        }[self.system]()
        queryed_servers = bidict()
        for k, v in self.servers.items():
            queryed_servers[self.domain_to_ip(k)] = v

        self.servers = queryed_servers
        self.hostname = socket.gethostname()
        if self.hostname == 'nhp-server-1':
            # 说明在 inner-data 本机，所以选择 sdf 
            self.servers['//10.20.34.150/inner-data'] = Path('/data/sdf')

    def __getitem__(self, item):
        return self.servers[item]

    def domain_to_ip(self, p: str):
        host_match = re.findall(r'//(.+?)/', p)
        if not host_match:
            return p
        host = host_match[0]
        ip = query_domain(host)
        return p.replace(f'//{host}/', f'//{ip}/')

    @staticmethod
    def get_linux_mount():
        p = subprocess.run("mount", capture_output=True)
        lines = p.stdout.decode(encoding).splitlines()

        res = bidict()
        for line in lines:
            if not line.startswith('//'):
                continue
            e = line.split(" ")
            res[e[0]] = Path(e[2])
        return res

    @staticmethod
    def get_windows_mount():
        p = subprocess.run("net use", capture_output=True)
        lines = p.stdout.decode(encoding).replace('\\', '/')
        lines = re.sub(' +', ' ', lines).splitlines()

        res = bidict()
        for line in lines:
            if not line.startswith('OK'):
                continue
            e = line.split(" ")
            res[e[2]] = Path(e[1] + '/')
        return res

    def _path_transform(self, p: str, dic: dict):
        for prefix, remote_path in dic.items():
            prefix = str(prefix).replace('\\', '/')
            remote_path = str(remote_path).replace('\\', '/')

            if p.startswith(prefix):
                tail = p.replace(prefix, '')
                while tail.startswith('/'):
                    tail = tail[1:]
                p = str(Path(remote_path) / tail).replace('\\', '/')
                break
        return p

    def local_to_unc(self, p: str) -> Path:
        p = str(p).replace('\\', '/')
        return self._path_transform(self.domain_to_ip(p), dict(self.servers.inverse))

    def unc_to_local(self, p: str) -> Path:
        p = str(p).replace('\\', '/')
        return Path(self._path_transform(self.domain_to_ip(p), dict(self.servers)))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.servers})'


class NHPNpR(NetpathResolver):
    @property
    def connectome(self):
        return self.servers["//10.10.47.90/connectome"]

    @property
    def inner_data(self):
        return self.servers["//10.20.34.150/inner-data"]

    @property
    def final_ntp(self) -> Path:
        return self.connectome / 'finalNTP'

    @property
    def final_ntp_91_106(self) -> Path:
        return self.connectome / 'finalNTP-layer4-parcellation91-106'

    @property
    def cla_project(self) -> Path:
        return self.servers['//10.10.47.97/rawData7/Macaque']


nnpr = NHPNpR()

if __name__ == '__main__':
    print(nnpr.final_ntp)
    print(nnpr)
    for i in [
        "/mnt/97-macaque/download-from-bgi", 
        '//10.10.47.97/rawData7/Macaque/download-from-bgi',
        r'\\97-rawdata7.nhp.lan\rawData7\Macaque\download-from-bgi',
        r'M:\Human\download-from-bgi',
        r'//10.20.34.150/inner-data'
    ]:
        t = nnpr.local_to_unc(i)
        print(f'{i}\tto\t{t}')
        tt = nnpr.unc_to_local(str(t))
        print(f'{t}\tto\t{tt}')
