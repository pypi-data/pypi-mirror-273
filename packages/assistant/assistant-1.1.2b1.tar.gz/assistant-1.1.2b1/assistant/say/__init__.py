import json
import websockets
import asyncio
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydub")

from pydub import AudioSegment
from pydub.playback import play

from assistant import I18N

try:
    from say.TTS import utils as tts_utils
    from say.TTS.as_client import tts
    # from num2words import num2words
except (ModuleNotFoundError, ImportError) as e:
    print(e)
    print("For Assistant to speak, you need to install the say module.")
    print("Run the following command:\n```shell\npip install -r tts-say\n```")
    sys.exit(1)

TTS_CONFIG = tts_utils.get_config_or_default()
is_allowed_to_speak = tts_utils.is_allowed_to_speak(TTS_CONFIG)
if not is_allowed_to_speak:
    print("System has not user autorization to speak.")


class TTS:
    def __init__(self, host=None, port=None, language=None, speaker_idx=None, style_wav=None):
        self.config = tts_utils.get_config_or_default()
        self.host = self.config.get("host", host)
        self.port = self.config.get("port", port)
        self.language = self.config.get("language", language)
        self.speaker_idx = self.config.get("speaker_idx", speaker_idx)
        self.style_wav = self.config.get("style_wav", style_wav)
        self.queue = asyncio.Queue(1)
        self.wait = True

    @property
    def is_allowed_to_speak(self):
        if self.config is None:
            self.config = tts_utils.get_config_or_default()
        return tts_utils.is_allowed_to_speak(self.config)

    def split_sentences(self, text: str, split_char="|"):
        text = text.strip("\n")
        text = text.replace(",", f",{split_char}")
        text = text.replace(".", f".{split_char}")
        text = text.replace("!", f"!{split_char}")
        text = text.replace("?", f"?{split_char}")
        text = text.replace(":", f":{split_char}")
        text = text.replace(";", f";{split_char}")
        text = text.replace("\n", f"{split_char}")
        return text.split(split_char)
    
    def say(self, text: list[str] | str):
        if isinstance(text, str):
            text = text.split("\n")            
        if not self.is_allowed_to_speak:
            print('\n'.join(text))
            return
        try:
            for t in text:
                asyncio.run(tts(self.split_sentences(t), language="fr-fr" if I18N == "fr" else I18N.lower(), style_wav=f"{self.config['tts']['speaker_wav']}", save_output=False))
            # asyncio.run(tts(text, language="fr-fr" if I18N == "fr" else I18N.lower(), voice_name="freeman", preset='fast', save_output=False))
        # asyncio.run(self.asay(text))
        # asyncio.run(self.apronounce())
        except Exception:
            # print(e)
            return
    
    def pronounce(self):
        asyncio.run(self.apronounce())

    async def apronounce(self):
        while True:
            wav = await self.queue.get()
            if wav:
                play(wav)
            self.queue.task_done()
    
    async def asay(self, text: list[str]):
        while self.wait:
            await asyncio.sleep(0.1)
        self.wait = True
        async with websockets.connect(f"ws://{self.host}:{self.port}/api/v1/tts") as ws:
            try:
                j = {
                    'text': text,
                    'speaker_idx': self.speaker_idx,
                    'style_wav': self.style_wav,
                    'language': self.language
                    }
                await ws.send(json.dumps(j).encode('utf-8', 'ignore'))
                wav = await ws.recv()
                _wav = AudioSegment(data=wav, sample_width=2, frame_rate=16000, channels=1)
                await self.queue.put(_wav)
            except ConnectionRefusedError as e:
                pass
            except Exception as e:
                raise e
            finally:
                self.wait = False
                await ws.close()
