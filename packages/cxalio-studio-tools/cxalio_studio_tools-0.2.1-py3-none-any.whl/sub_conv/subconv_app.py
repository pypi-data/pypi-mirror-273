import pkgutil
from argparse import ArgumentParser
from functools import cache

from rich.columns import Columns
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich_argparse import RichHelpFormatter

from cx_core import AbstractApp, DataPackage, LogLevel
from cx_core.folder_expander import FolderExpander
from cx_subtitle import SubtitleFormatter
from cx_subtitle.loader import *
from cx_subtitle.saver import *
from .env import env
from .exceptions import *
from .subtitle_translator import SubtitleTranslator


class SubConvApp(AbstractApp):
    __loader_classes = {
        '.srt': SrtLoader,
        '.txt': TxtLoader,
        '.docx': WordLoader,
        '.ttml': TTMLLoader
    }

    __saver_classes = {
        'srt': SrtSaver,
        'txt': TxtSaver,
        'word': WordSaver,
        'excel': ExcelSaver,
        'csv': CsvSaver
    }

    __suffixes = {
        'txt': '.txt',
        'word': '.docx',
        'excel': '.xlsx',
        'csv': '.csv',
        'srt': '.srt',
        'ttml': '.ttml',
        'rtf': '.rtf'
    }

    APP_VERSION = "0.2.0"
    APP_NAME = "subconv"

    def __init__(self):
        super(SubConvApp, self).__init__()

        _parser = ArgumentParser(prog=SubConvApp.APP_NAME,
                                 description=f'批量提取台词本，支持的格式包括{" ".join(str(x) for x in self.__loader_classes.keys())}',
                                 epilog=f'Version {SubConvApp.APP_VERSION} Designed by xiii_1991',
                                 formatter_class=RichHelpFormatter, exit_on_error=False)

        _parser.add_argument('--format', '-f', dest='format', default='txt',
                             choices=self.__saver_classes.keys(),
                             help='指定输出格式')

        _parser.add_argument('--encoding', '-c', dest='encoding', default='auto',
                             help='设定输出编码')

        _parser.add_argument('-o', '--output-folder', dest='target_folder', default=None,
                             help='指定输出目录')

        _parser.add_argument('-t', '--time', dest='keep_time', action='store_true',
                             help='尽量保留时间信息')

        _parser.add_argument('--bypass-formatter', dest='bypass_formatter', default=False,
                             action='store_true', help='跳过默认的内容检查器，使用原样输出')

        _parser.add_argument('--overwrite', '-y', dest='overwrite_target', default=False,
                             action='store_true', help='强制覆盖已存在的目标文件')

        _parser.add_argument('--translate', dest='translate', action='store_true',
                             help='自动翻译为英文版本（需要网络）')

        _parser.add_argument('--debug', '-d', action='store_true', dest='debug',
                             help='调试模式')

        _parser.add_argument('--pretend', '-p', dest='pretend_mode', action='store_true',
                             help='干转模式，不执行写入操作')

        _parser.add_argument('--full-help', help='显示详细的说明',
                             dest='show_full_help', action='store_true')

        _parser.add_argument('sources', nargs='*',
                             help='需要转换的文件')

        self.parser = _parser
        self.args = None

        self.translator = None
        self.formatter = None

        self.global_task = None
        self.current_task = None

    def __enter__(self):
        env.start()

        _args = self.parser.parse_args()
        self.args = DataPackage(**vars(_args))
        env.log_level = LogLevel.DEBUG if self.args.debug else LogLevel.WARNING

        if not self.args.bypass_formatter:
            env.print(f'启用字幕格式检查器')
            self.formatter = SubtitleFormatter()

        if self.args.translate:
            env.print(f'启用字幕文本翻译器')
            self.translator = SubtitleTranslator()

        self.global_task = env.progress.add_task(description='全局进度', start=False, visible=False)
        self.current_task = env.progress.add_task(description='当前进度', start=False, visible=False)

        env.info('Initialized ...')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.remove_task(self.global_task)
        env.progress.remove_task(self.current_task)
        self.global_task = None
        self.current_task = None
        env.stop()
        return False

    def is_loadable(self, source):
        suffix = Path(source).suffix.lower()
        return suffix in self.__loader_classes

    def make_loader(self, source) -> AbstractSubtitleLoader:
        source = Path(source)
        env.info(f'开始构建 loader <- {source}')
        if not source.is_file():
            raise ValueError('这玩意儿不是文件')
        loader_class = self.__loader_classes.get(source.suffix.lower())
        loader = loader_class(source) if loader_class else None
        return loader

    @staticmethod
    def show_full_help():
        data = pkgutil.get_data('sub_conv', 'help.md').decode('utf-8')
        panel = Panel(Markdown(data), width=80)
        env.console.print(panel)

    @property
    def target_suffix(self):
        suffix = self.__suffixes.get(str(self.args.format).lower())
        return suffix if suffix else '.txt'

    @property
    def target_encoding(self):
        return 'utf-8' if self.args.encoding == 'auto' else self.args.encoding

    @staticmethod
    def print_subtitles(subtitles):
        panels = (
            Panel(Text(x.content, style='blue'),
                  title=Text(str(x.start.timestamp), style='yellow'),
                  subtitle=Text(str(x.end.timestamp), style='green'),
                  title_align='left',
                  subtitle_align='right',
                  expand=True)
            for x in subtitles)
        env.print(Columns(panels, expand=True, equal=True))

    @cache
    def target_path(self, source) -> Path:
        source = Path(source)
        target = source.with_suffix(self.target_suffix)
        if self.args.target_folder:
            target = Path(self.args.target_folder) / target.name
            env.info(f'检测到指定的目标文件夹,已更新目标："{target.absolute()}"')
        return target

    def make_saver(self, source) -> AbstractSubtitleSaver:
        source = Path(source)
        target = self.target_path(source)
        saver_class = self.__saver_classes.get(self.args.format, TxtSaver)
        saver = saver_class(target, keep_time=self.args.keep_time)
        saver.encoding = self.target_encoding
        return saver

    def do_job(self, source):
        env.info(f'开始执行任务{source}')

        source = Path(source)

        if not self.is_loadable(source):
            env.error(f'{source} 的格式无法读取，将跳过任务')
            return

        target_path = self.target_path(source)
        if target_path == source:
            env.error(f'[yellow]{source.name}[/yellow] 源文件和目标文件相同，跳过处理。')
            return

        if target_path.exists() and not self.args.overwrite_target:
            env.error(f'目标文件[red]{source.name}[/red]已存在，跳过处理。')
            return

        with self.make_loader(source) as loader:
            subtitles = [x for x in loader.subtitles()]

        if self.args.debug:
            self.print_subtitles(subtitles)

        if self.args.pretend_mode:
            env.print(f'[yellow]{source.name}[/yellow] 已成功读取，[red]干转模式跳过输出[/red] ...')
            return

        with self.make_saver(source) as saver:
            saver.install_processor(self.translator).install_processor(self.formatter)
            target = saver.target
            env.progress.start_task(self.current_task)
            for sbt in env.progress.track(subtitles, task_id=self.current_task):
                env.progress.update(self.current_task, description=f'[yellow]{sbt.content}[/yellow]', visible=True)
                saver.write(sbt)
                if env.wanna_quit:
                    env.error(f'用户退出，正在终止操作……')
                    break

        env.progress.update(self.current_task, visible=False, total=None)
        if env.wanna_quit:
            target.unlink()
            env.print('[red]移除未完成的目标文件...[/red]')
        else:
            env.print(f'[yellow]{target.name}[/yellow] ... [green]转换完成[/green]')

    def sources(self):
        if not self.args.sources:
            return []
        s = self.args.sources
        expander = FolderExpander()
        expander.suffixes_whitelist = self.__loader_classes.keys()
        yield from expander.expand(*s)

    def run(self):
        env.info(f'解析的参数：', self.args)

        if self.args.show_full_help:
            self.show_full_help()
            return

        if not self.args.sources:
            raise NoSourceError()

        if self.args.bypass_formatter:
            env.print('[red]旁通格式化器[/red] ...')

        env.progress.update(self.global_task, visible=True)
        env.progress.start_task(self.global_task)
        for s in env.progress.track(self.sources(), task_id=self.global_task):
            if env.wanna_quit:
                env.error(f'操作终止')
                break
            source = Path(s)
            env.progress.update(self.global_task, description=f'{source.name}...')
            self.do_job(source)


def run():
    with SubConvApp() as app:
        app.run()
