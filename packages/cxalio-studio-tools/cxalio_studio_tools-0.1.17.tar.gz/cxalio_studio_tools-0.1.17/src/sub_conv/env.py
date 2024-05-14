from rich.console import Console
import signal
from cx_core import AbstractEnv, AppLogger


class Env(AbstractEnv):
    def __init__(self):
        super(Env, self).__init__()
        self.console = Console()
        self._logger = AppLogger(console=self.console)
        self.wanna_quit = False


env = Env()


def signal_handler(sig, frame):
    if sig != signal.SIGINT:
        return
    env.info('接收到 SIGINT')
    env.print("收到终止信号，准备退出...")
    env.wanna_quit = True


signal.signal(signal.SIGINT, signal_handler)
