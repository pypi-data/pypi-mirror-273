import asyncio
import json

from ffmpeg import Progress
from ffmpeg.asyncio import FFmpeg
from ffmpeg.errors import FFmpegError

from cx_core import DataPackage
from .env import env
from .mission import Mission


class Transcoder:
    def __init__(self, mission: Mission):
        self.task = None
        self.media_info = None
        self.duration = None
        self.mission = mission

    def __enter__(self):
        self.task = env.progress.add_task(description=f'{self.mission.source.name}...')

        ffprobe = FFmpeg(executable='ffprobe').input(self.mission.source, print_format='json', show_format=None)
        media = json.loads(asyncio.run(ffprobe.execute()))
        self.media_info = DataPackage(**media)
        self.duration = float(self.media_info.format.duration)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        env.progress.remove_task(self.task)
        self.task = None
        env.current_ffmpeg = None
        return False

    async def transcode(self):
        for folder in self.mission.iter_target_folders():
            env.progress.update(self.task, description=f'检测目标目录: {folder}')
            if not folder.exists():
                env.print(f'目标目录 {folder} 不存在，自动创建')
                folder.mkdir(parents=True, exist_ok=True)

        ffmpeg = FFmpeg(self.mission.profile.general.ffmpeg)
        env.debug(f'创建 ffmpeg 对象: {self.mission.profile.general.ffmpeg}')

        env.progress.update(self.task, description=f'写入全局参数')
        for k, v in self.mission.general_options.iter_options():
            ffmpeg.option(k, v)
            env.debug(f'写入全局选项： [green]{k}[/green] : [yellow]{v}[/yellow]')

        for input_ in self.mission.inputs:
            env.progress.update(self.task, description=f'为 {input_.filename.name} 写入输入参数')
            ffmpeg.input(input_.filename.absolute(), input_.raw_data)
            env.debug(f'添加输入选项： {input_.raw_data}')

        for output_ in self.mission.outputs:
            env.progress.update(self.task, description=f'为 {output_.filename.name} 写入输出参数')
            ffmpeg.output(output_.filename.absolute(), output_.raw_data)
            env.debug(f'添加输出选项： {output_.raw_data}')

        env.debug(f'全部任务选项输入完毕， ffmpeg 对象构建完成')

        @ffmpeg.on('progress')
        def on_progress(progress: Progress):
            desc = f'{self.mission.source.name}... [yellow]x{round(progress.speed, 2)}[/yellow]'
            curr = progress.time.seconds
            env.progress.update(self.task, description=desc, completed=curr, total=self.duration)

        @ffmpeg.on('stderr')
        def on_stderr(line):
            env.debug(f'[grey]FFMPEG输出：[/grey] {line}')

        @ffmpeg.on('start')
        def on_start(arguments):
            env.debug(f'开始执行任务: {' '.join(arguments)}')

        @ffmpeg.on('completed')
        def on_completed():
            env.debug(f'[green]{self.mission.source.name}[/green] [yellow]执行完毕，顺利退出[/yellow]')

        @ffmpeg.on('terminated')
        def on_terminated():
            env.warning('[purple]FFMPEG 被终止[purple]')
            env.print('尝试移除未完成的目标文件...')
            for t in self.mission.outputs:
                f = t.filename
                f.unlink(missing_ok=True)
                env.debug(f'[red]已删除 {f.absolute()}[/red]')

        env.current_ffmpeg = ffmpeg
        await ffmpeg.execute()
        env.current_ffmpeg = None

    def run(self):
        try:
            asyncio.run(self.transcode())
        except FFmpegError as err:
            env.error(f'ffmpeg执行出错: [red]{err.message}[/red]')
