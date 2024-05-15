class ProfileNoFoundError(FileNotFoundError):
    def __init__(self, target=None):
        super(ProfileNoFoundError, self).__init__()
        self._tgt = target

    def __str__(self):
        if self._tgt:
            return f'ffmpeg 配置文件 "{self._tgt}" 未找到，程序无法执行'
        return '未指定配置文件，程序无法运行'
