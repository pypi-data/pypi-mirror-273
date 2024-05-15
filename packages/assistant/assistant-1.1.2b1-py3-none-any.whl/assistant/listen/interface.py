import threading
import requests

disclamer = """To speak with Assistant, you need to install the listen module.
Run the following command:
```shell
pip install -r stt-listen
```"""

try:
    from listen import mic
except (ModuleNotFoundError, ImportError) as e:
    e.msg = disclamer
    raise e

class ListenInterface:
    asr_host = "localhost"
    asr_port = "5063"
    def __init__(self, asr_host=asr_host, asr_port=asr_port, **kwargs):
        self.asr_host = asr_host
        self.asr_port = asr_port
        # self.asr_stop_event = threading.Event()
        # self.bg_listen_thread = threading.Thread(target=self._listen, args=(self.asr_stop_event,))
        
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def is_asr_server_up(self):
        try:
            r = requests.get(f"http://{self.asr_host}:{self.asr_port}")
            if r.status_code == 200:
                return True
            else:
                raise Exception("ASR Server is not up.")
        except (requests.ConnectionError, Exception) as e:
            return False

    def listen(self):
        source = mic.Microphone()
        source.record()
        query = source.transcribe_until_silence()
        source.stop_record()
        # source.stop_stream()
        # source.destroy()
        source.vad_audio.pa.terminate()
        source.vad_audio.destroy()
        return query
