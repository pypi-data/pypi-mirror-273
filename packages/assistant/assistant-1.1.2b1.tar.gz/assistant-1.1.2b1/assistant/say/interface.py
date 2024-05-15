from assistant.say import TTS

class SayInterface:
    tts_host = "localhost"
    tts_port = "5067"
    
    def __init__(self):
        self.engine = TTS(host=self.tts_host, port=self.tts_port)
    
    def say(self, text: str | list[str]):
        if isinstance(text, str):
            text = text.split("\n")
        try:
            self.engine.say(text)
        except ConnectionRefusedError:
            pass # No need to make a fuss about it