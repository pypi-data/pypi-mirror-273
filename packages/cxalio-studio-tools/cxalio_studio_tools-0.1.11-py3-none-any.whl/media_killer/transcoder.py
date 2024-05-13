import asyncio
import json
import signal
from pathlib import Path

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg
from ffmpeg.errors import FFmpegError

from cx_core import DataPackage
from .env import env
from functools import cache


def make_target(source: Path, profile=None) -> str:
    if not profile:
        profile = env.profile
    result = profile.output.folder / source.name
    parent_level = profile.output.keep_parent_level
    if parent_level > 0:
        parents = source.absolute().parent.parts
        selected_parts = parents[-1 * parent_level:]
        t_folder = Path(*selected_parts)
        env.debug(
            f'取用 {parent_level} 个上级目录:\n{source.name} -> {t_folder}'
        )
        result = profile.output.folder / t_folder / source.name

    t_suffix = profile.output.suffix
    if not t_suffix.startswith('.'):
        t_suffix = '.' + t_suffix

    result = result.with_suffix(t_suffix)
    return str(result)


def options_to_dict(options: DataPackage) -> dict:
    result = {}
    for k, v in options.items():
        result[k] = "" if v is None else v
    return result


class Transcoder:
    def __init__(self, source: str, profile=None):
        self.task = None
        self.source = Path(source)
        self.profile = profile if profile else env.profile
        self.duration = None

    def __enter__(self):
        self.task = env.progress.add_task(description=f'{self.source.name}...')
        ffprobe = FFmpeg(executable='ffprobe').input(self.source, print_format='json', show_format=None)
        media = json.loads(asyncio.run(ffprobe.execute()))
        media = DataPackage(**media)
        self.duration = float(media.format.duration)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.remove_task(self.task)
        self.task = None
        env.current_ffmpeg = None
        return False

    @property
    @cache
    def target(self):
        return make_target(self.source, self.profile)

    async def transcode(self):
        target = self.target

        parent = Path(target).absolute().parent
        env.debug(f'检测父级目录： {parent}')
        parent.mkdir(parents=True, exist_ok=True)

        env.debug('开始构建 ffmpeg 对象...')
        ffmpeg = FFmpeg()
        for k, v in self.profile.general.options.items():
            ffmpeg.option(k, v)
            env.debug(f'写入全局选项： [green]{k}[/green] : [yellow]{v}[/yellow]')

        if self.profile.general.hardware_accelerate:
            ffmpeg.option('hwaccel', self.profile.general.hardware_accelerate)
            env.debug(f'设置硬件加速：[yellow]{self.profile.general.hardware_accelerate}[/yellow]')

        if self.profile.general.overwrite_existed:
            env.debug(f'启用覆写')
            ffmpeg.option('y')
        else:
            ffmpeg.option('n')

        input_options = options_to_dict(self.profile.input.options)
        ffmpeg.input(self.source, input_options)
        env.debug(f'为 {self.source} 写入输入参数: {input_options}')

        output_options = options_to_dict(self.profile.output.options)
        ffmpeg.output(target, output_options)
        env.debug(f'为 {target} 写入输出参数: {output_options}')

        @ffmpeg.on('progress')
        def on_progress(progress: Progress):
            desc = f'{self.source.name}... [yellow]x{round(progress.speed, 2)}[/yellow]'
            curr = progress.time.seconds
            env.progress.update(self.task, description=desc, completed=curr, total=self.duration)

        @ffmpeg.on('stderr')
        def on_stderr(line):
            env.debug(f'FFMPEG输出：{line}')

        @ffmpeg.on('start')
        def on_start(arguments):
            env.debug(f'开始执行任务: {arguments}')

        @ffmpeg.on('completed')
        def on_completed():
            env.debug(f'{self.source}转完了')

        @ffmpeg.on('terminated')
        def on_terminated():
            env.info('FFMPEG 终止')
            Path(target).unlink(True)
            env.print('尝试移除未完成的目标文件...')

        # env.debug(f'正在执行的参数：{ffmpeg.arguments}')
        env.current_ffmpeg = ffmpeg
        await ffmpeg.execute()
        env.current_ffmpeg = None

    def run(self):
        try:
            asyncio.run(self.transcode())
        except FFmpegError as err:
            env.error(f'当前 FFmpeg 进程被终止: [red]{err.message}')
