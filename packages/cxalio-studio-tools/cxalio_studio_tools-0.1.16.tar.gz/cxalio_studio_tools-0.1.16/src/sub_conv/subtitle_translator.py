import time

from translators.server import TranslatorError

from cx_subtitle import Subtitle, SubtitleProcessor
import translators
from .env import env


class SubtitleTranslator(SubtitleProcessor):
    def __init__(self, target_lang='en'):
        super(SubtitleTranslator, self).__init__()
        env.debug('初始化翻译器')
        self.target_lang = target_lang
        self.ts = translators
        # _ = self.ts.preaccelerate_and_speedtest()

    def __call__(self, s):
        translated_content = s.content
        for i in range(12):
            if env.wanna_quit:
                break
            try:
                translated_content = str(self.ts.translate_text(s.content, to_language=self.target_lang))
                env.debug(f'翻译文本 "{s.content}" 为 "{translated_content}" ')
                break
            except KeyboardInterrupt:
                env.error(f'用户终止服务')
                break
            except Exception as e:
                env.error(f'ERROR {i}: [red]{e}[/red]')
                time.sleep(2)
        if translated_content == s.content:
            env.debug(f'翻译失败，将保持原样: [yellow]{translated_content}[/yellow]')
        return s.with_content(translated_content)
