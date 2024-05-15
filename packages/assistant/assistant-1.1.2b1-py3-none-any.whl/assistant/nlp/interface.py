import attr
import requests
import random
import threading

from xonsh.built_ins import XSH

from halo import Halo

from assistant.nlp.chains.session import SessionAssistant
from assistant.nlp.chains.callback_handlers import InputOutputAsyncCallbackHandler
from assistant.nlp.think import let_me_think_about_it, sorry_unable_to_think
try:
    from assistant.listen.interface import ListenInterface
    is_listen_interface = True
except (ModuleNotFoundError, ImportError) as e:
    is_listen_interface = False

try:
    from assistant.say.interface import SayInterface
    is_say_interface = True
except (ModuleNotFoundError, ImportError) as e:
    is_say_interface = False

class ModernHalo(Halo):
    def start(self, text=None):
        """Starts the spinner on a separate thread.
        Parameters
        ----------
        text : None, optional
            Text to be used alongside spinner
        Returns
        -------
        self
        """
        if text is not None:
            self.text = text
        if self._spinner_id is not None:
            return self
        if not (self.enabled and self._check_stream()):
            return self
        self._hide_cursor()

        self._stop_spinner = threading.Event()
        self._spinner_thread = threading.Thread(target=self.render)
        self._spinner_thread.set_daemon = True
        self._render_frame()
        self._spinner_id = self._spinner_thread.name
        self._spinner_thread.start()
        return self


@attr.s(auto_attribs=True, frozen=True)
class PredictReturn:
    success: bool
    unparse: str = None
    error_message: str = None

def get_random_thinking_sentence():
    """
    Returns a random sentence to indicate that the assistant is thinking about a response.
    """
    return random.choice(let_me_think_about_it)

def get_random_sorry_sentence():
    """
    Returns a random sentence to indicate that the assistant is unable to think about a response.
    """
    return random.choice(sorry_unable_to_think)

class AssistantInterface:
    nlp_host = "localhost"
    nlp_port = "5085"
    interface = None

    def __init__(
            self,
            nlp_host=nlp_host, nlp_port=nlp_port,
            verbose=False, callbacks=[], 
            **kwargs
        ):
        self.nlp_host = nlp_host
        self.nlp_port = nlp_port
        self.spinner = ModernHalo(spinner="dots13", text="...", color="cyan")
        self.set_assistant(verbose=verbose, callbacks=callbacks)
        self.is_asr = self.set_asr()
        self.is_tts = self.set_tts()

    def set_assistant(self, verbose=False, callbacks=[]):
        self.session_assistant = SessionAssistant(
            temperature=0.0, max_tokens=1000, verbose=verbose, callbacks=callbacks
        )  # , callbacks=[InputOutputAsyncCallbackHandler()])

    def set_asr(self):
        if not is_listen_interface:
            self.listen_interface = None
            return is_listen_interface
        self.listen_interface = ListenInterface()
        return is_listen_interface
    
    def set_tts(self):
        if not is_say_interface:
            self.say_interface = None
            return is_say_interface
        self.say_interface = SayInterface()
        return is_say_interface

    def is_nlp_server_up(self):
        try:
            r = requests.get(f"http://{self.nlp_host}:{self.nlp_port}")
            if r.status_code == 200:
                return True
            else:
                raise Exception("NLP Server is not up.")
        except (requests.ConnectionError, Exception) as e:
            return False

    def assistant(self, query):
        try:
            if self.is_nlp_server_up():
                self.spinner.text = f"{get_random_thinking_sentence()}..."
                self.spinner.start()
                return self.session_assistant(query)
            else:
                return None
        except requests.exceptions.ConnectionError:
            return None
        finally:
            self.spinner.stop()

    def get_intro(self, prompt_into = "Assistant?"):
        """
        Returns the introduction prompt for the assistant.

        Returns:
        str: The introduction prompt for the assistant.
        """
        
        return (
            self.assistant(prompt_into)
            or get_random_sorry_sentence()
        )
    
    def say(self, sentence: str | list[str]):
        if isinstance(sentence, str):
            sentence = sentence.split("\n")
        if self.is_tts:
            self.say_interface.say(sentence)
