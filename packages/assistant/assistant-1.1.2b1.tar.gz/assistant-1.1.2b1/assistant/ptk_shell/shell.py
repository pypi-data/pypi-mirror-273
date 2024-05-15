import os, sys
import time
import xonsh.tools as xt
import subprocess
import threading

from io import StringIO
from contextlib import redirect_stderr, redirect_stdout
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import merge_completers
from prompt_toolkit.shortcuts import clear
from xonsh.events import events
from xonsh.jobs import jobs
from xonsh.ptk_shell.shell import PromptToolkitShell
from xonsh.base_shell import Tee
from xonsh.built_ins import XSH
from assistant import ASSISTANT_PATH
from assistant.nlp.interface import AssistantInterface
from assistant.ptk_shell.completer import AssistantCompleter
from assistant.nlp.chains.callback_handlers import InputOutputAsyncCallbackHandler
from assistant.execer import AssistantExecer
from assistant import codecache
from assistant.procs.specs import AssistantSubprocSpec
from assistant.procs.pipelines import AssistantCommandPipeline
from assistant.nlp.exit import exit_please
from assistant.nlp.clear import clear_please

class AssistantShell(PromptToolkitShell):
    console = Console()
    error_console = Console(stderr=True, style="bold red")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        callbacks = []
        self.is_listening = False
        self.is_speaking = False
        self.is_debug = bool(XSH.env.get("DEBUG", True if os.environ.get("DEBUG", "False").lower() == "true" else False))
        if self.is_debug:
            callbacks.append(InputOutputAsyncCallbackHandler())
        self.kernel_interface = AssistantInterface(verbose=self.is_debug, callbacks=callbacks)
        if self.kernel_interface.is_asr:
            self.asr_stop_event = threading.Event()
            self.bg_listen_thread = threading.Thread(target=self.listen, args=(self.asr_stop_event,))
        if self.kernel_interface.is_tts:
            self.tts_stop_event = threading.Event()
            self.bg_speak_thread = threading.Thread(target=self.speak, kwargs={"stop_event": self.tts_stop_event})
        self.last_seen = None
        # self.pt_completer = merge_completers([self.pt_completer, AssistantCompleter()]) # TODO: fix https://github.com/xonsh/xonsh//issues/4986
        self.pt_completer = None
        self.execer = AssistantExecer()
        self.subproc_spec_cls = AssistantSubprocSpec
        jobs.pipeline_class = AssistantCommandPipeline
        

    def default(self, line, raw_line=None):
        """Implements code execution."""
        line = line if line.endswith("\n") else line + "\n"
        if not self.need_more_lines:  # this is the first line
            if not raw_line:
                self.src_starts_with_space = False
            else:
                self.src_starts_with_space = raw_line[0].isspace()
        src, code = self.push(line)
        if code is None:
            return # Should probably feed src to LM instead

        events.on_precommand.fire(cmd=src)

        env = XSH.env
        hist = XSH.history  # pylint: disable=no-member
        ts1 = None
        enc = env.get("XONSH_ENCODING")
        err = env.get("XONSH_ENCODING_ERRORS")
        tee = Tee(encoding=enc, errors=err)
        ts0 = time.time()
        try:
            with StringIO() as stdout_buf, \
            StringIO() as stderr_buf, \
            redirect_stdout(stdout_buf), \
            redirect_stderr(stderr_buf):
                exc_info = codecache.run_compiled_code(code, self.ctx, None, "single")
                _out = stdout_buf.getvalue() or stderr_buf.getvalue()
            if exc_info != (None, None, None):
                raise exc_info[1]
            ts1 = time.time()
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 0  # returncode for success
        except xt.XonshError as e:
            if str(e.args[0]).strip() != "":
                self.log_error(str(e.args[0]).strip())
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 1  # return code for failure
        except (SystemExit, KeyboardInterrupt) as err:
            raise err
        except BaseException:
            xt.print_exception(exc_info=exc_info)
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 1  # return code for failure
        finally:
            ts1 = ts1 or time.time()
            tee_out = tee.getvalue() or _out
            if hist.last_cmd_rtn == 0:
                if tee_out.strip() != "":
                    self.log_response(Markdown(f"""{tee_out.strip()}"""))
            else:
                # Subbproc command failed check stdout/err to find why.
                t = tee_out.split(": ")
                if all(item in t for item in ['xonsh', 'subprocess mode', 'command not found']):
                    # Xonsh: subprocess mode: did not found command
                    if self.kernel_interface.is_nlp_server_up():
                        # Assistant: LM is up
                        tee_out = self.kernel_interface.assistant(raw_line.strip())
                        if tee_out != "":
                            hist.last_cmd_rtn = 0
                            # self.log_response(Markdown(tee_out.strip()))
                            self.say(tee_out.strip())
                    else:
                        self.log_error(Markdown(f"""{tee_out.strip()}"""))
                else:
                    if self.kernel_interface.is_nlp_server_up():
                        # Assistant: LM is up
                        tee_out = self.kernel_interface.assistant(raw_line.strip())
                        if tee_out and tee_out != "":
                            hist.last_cmd_rtn = 0
                            self.log_response(Markdown(tee_out.strip()))
                            self.say(tee_out.strip())
                    else:
                        self.log_error(Markdown(f"""{tee_out.strip()}"""))
            self._append_history(
                inp=src,
                ts=[ts0, ts1],
                spc=self.src_starts_with_space,
                tee_out=tee_out,
                cwd=self.precwd,
            )
            self.accumulated_inputs += src
            if (
                tee_out
                and env.get("XONSH_APPEND_NEWLINE")
                and not tee_out.endswith(os.linesep)
            ):
                print(os.linesep, end="")
            tee.close()
            self._fix_cwd()
        if XSH.exit:  # pylint: disable=no-member
            self.set_last_seen()
            if self.kernel_interface.is_asr and self.is_listening:
                self.stop_listening()
            return True

    def is_line_which_builtin(self, line) -> bool:
        llss = line.lower().strip().split( )
        builtin_names = ['assistant', 'listen', 'say', 'which', 'pwd', 'exit', 'clear']
        return True if llss[0] == "which" and llss[1] in builtin_names else False

    def cmdloop(self, intro=None):
        """Enters a loop that reads and execute input from user."""
        if intro:
            # self.log_response(Markdown(intro))
            self.say(intro)
        auto_suggest = AutoSuggestFromHistory()
        while not XSH.exit:
            try:
                line = self.singleline(auto_suggest=auto_suggest)
                if not line:
                    self.emptyline()
                elif line.lower() in exit_please:
                    XSH.exit = True
                elif line.lower() in clear_please:
                    clear()
                elif self.is_line_which_builtin(line):
                    self.log_response(Markdown(f"Using builtin function."))
                else:
                    raw_line = line
                    line = self.precmd(line)
                    self.default(line, raw_line)
            except SystemExit:
                self.reset_buffer()
            except KeyboardInterrupt:
                self.reset_buffer()
                self.log_error(Markdown("# KeyboardInterrupt\n[Ctrl] + [C]: cannot be used to exit a shell.\n\nTry to ask nicely with exit or be rude: [Ctrl] + [D]"))
                continue
            except EOFError:
                if XSH.env.get("IGNOREEOF"):
                    print('Use "exit" to leave the shell.', file=sys.stderr)
                else:
                    break
            except (xt.XonshError, xt.XonshCalledProcessError) as xe:
                if XSH.env.get("DEBUG",
                               True if os.environ.get("DEBUG", "False").lower() == "true" \
                                   else False
                                ):
                    raise xe
                else:
                    self.handle_xonsh_error(xe, raw_line)
            except NameError as ne:
                # Handle the NameError, you can use your LLM here to answer the query.
                if XSH.env.get("DEBUG", True if os.environ.get("DEBUG", "False").lower() == "true" else False):
                    raise ne
                else:
                    self.handle_name_error(ne, raw_line)
            except SyntaxError as se:
                # Handle the SyntaxError, you can use your LLM here to provide guidance.
                if XSH.env.get("DEBUG", True if os.environ.get("DEBUG", "False").lower() == "true" else False):
                    raise se
                else:
                    self.handle_syntax_error(se, raw_line)
            except Exception as e:
                # Handle other exceptions as needed.
                if XSH.env.get("DEBUG", True if os.environ.get("DEBUG", "False").lower() == "true" else False):
                    raise e
                else:
                    _e = f"""{type(e).__name__}: {str(e)}"""
                    self.handle_other_exceptions(_e, raw_line)

    def set_last_seen(self):
        last_seen_file = os.path.join(ASSISTANT_PATH, "history", ".last_seen")
        try:
            os.mkdir(os.path.join(ASSISTANT_PATH, "history"))
        except FileExistsError:
            pass
        with open(last_seen_file, "w") as f:
            f.write(subprocess.check_output(["date"]).decode("utf-8").strip())
    
    def log_query(self, query):
        self.console.print(query, style="italic blue", justify="left")

    def log_response(self, response):
        self.console.print(response, style="bold white", justify="left")
    
    def speak(self, sentence: str | list[str], stop_event: threading.Event):
        is_tts = self.kernel_interface.is_tts
        if isinstance(sentence, str):
            sentence = sentence.split("\n")
        
        for sentence in sentence:
            self.log_response(Markdown(sentence))
            if is_tts and not stop_event.is_set():
                # self.kernel_interface.spinner.info("Speaking...")
                self.is_speaking = True
                self.kernel_interface.say(sentence)
                self.is_speaking = False
                # self.kernel_interface.spinner.info("Stopped speaking.")
    
    def say(self, response: str | list[str]):
        if isinstance(response, str):
            response = response.split("\n")
        if not self.kernel_interface.is_tts:
            self.log_response(Markdown("\n".join(response)))
            return
        # self.bg_speak_thread.daemon = True
        # self.bg_speak_thread = threading.Thread(target=self.speak, kwargs={"sentence": response, "stop_event": self.tts_stop_event})
        # self.bg_speak_thread.start()
        # self.bg_speak_thread.join()
        is_tts = self.kernel_interface.is_tts
        
        for sentence in response:
            self.log_response(Markdown(sentence))
            if is_tts:
                # self.kernel_interface.spinner.info("Speaking...")
                self.is_speaking = True
                self.kernel_interface.say(sentence)
                self.is_speaking = False
                # self.kernel_interface.spinner.info("Stopped speaking.")
        
    
    def stop_speaking(self):
        self.tts_stop_event.set()
        self.is_speaking = False
        try:
            self.bg_speak_thread.join(1)
            self.tts_stop_event = threading.Event()
            self.bg_speak_thread = threading.Thread(target=self.speak, kwargs={"stop_event": self.tts_stop_event})
        except Exception:
            pass
        # self.kernel_interface.spinner.info("Stopped speaking.")
        return self.is_speaking
    
    def log_error(self, error):
        self.error_console.print(error, style="bold red", justify="left")

    def handle_xonsh_error(self, error, raw_line):
        # Handle the NameError here using your LLM or any other logic.
        self.log_error(Markdown(f"# Xonsh\nYou said '{raw_line}' but {error}"))

    def handle_name_error(self, error, raw_line):
        # Handle the NameError here using your LLM or any other logic.
        self.log_error(Markdown(f"# NameError\nYou said '{raw_line}' but {error}"))

    def handle_syntax_error(self, error, raw_line):
        # Handle the SyntaxError here using your LLM or provide guidance.
        self.log_error(Markdown(f"# SyntaxError\nYou said '{raw_line}' but {error}"))

    def handle_other_exceptions(self, error, raw_line):
        # Handle other exceptions as needed using your logic.
        self.log_error(Markdown(f"# Exception\nYou said '{raw_line}' but assistant raised {error}.\nPlease excuse this inconvenience. You can try to running Assistant using DEBUG=True for more information about this error."))

    def listen(self, stop_event):
        while not stop_event.is_set():
            if self.kernel_interface.listen_interface.is_asr_server_up():
                self.kernel_interface.spinner.info("Listening...")
                # It will take time to get the query
                query = self.kernel_interface.listen_interface.listen()
                # Therefor we shall assert stop_event isn't set to proceed
                self.kernel_interface.spinner.info("Stopped listening.")
                if stop_event.is_set():
                    break
                if query:
                    self.log_query(query)
                    answer = self.kernel_interface.assistant(query)
                    if answer:
                        self.say(answer)
                    else:
                        self.log_error(Markdown("Assistant failed to reply."))
                else:
                    self.log_error(Markdown("Nothing heard."))
            else:
                self.log_error(Markdown("ASR Server is not up."))
            if stop_event.is_set():
                break
    
    def start_listening(self):
        """Start listening for user input.
        
        Returns:
        bool: True if the listen server is up, False otherwise.
        """
        if not self.kernel_interface.is_asr:
            self.log_error(Markdown("#Connection Error\nCould not reach the ASR Server."))
            return False
        self.kernel_interface.spinner.info("Listening continuously...")
        # try:
        #     self.bg_listen_thread.join(1)
        # except Exception:
        #     pass
        # self.asr_stop_event = threading.Event()
        # self.bg_listen_thread = threading.Thread(target=self.listen, args=(self.asr_stop_event,))
        # self.bg_listen_thread.daemon = True
        # self.bg_listen_thread.start()
        should_exit = False
        try:
            while not should_exit:
                self.is_listening = True
                self.kernel_interface.spinner.info("Listening...")
                query = self.kernel_interface.listen_interface.listen()
                self.is_listening = False
                self.kernel_interface.spinner.info("Stopped listening.")
                if query and len(query.split()) > 1:
                    self.log_query(query)
                    time.sleep(0.1) # just to make sure the query is logged before the spinner starts
                    answer = self.kernel_interface.assistant(query)
                    if answer:
                        self.say(answer)
                    else:
                        self.log_error(Markdown("Assistant failed to reply."))
                else:
                    self.log_error(Markdown("Nothing heard."))
        except (KeyboardInterrupt, EOFError) as end:
            should_exit = True
            self.log_error(Markdown("Stopped listening."))
            raise end
        except Exception as e:
            should_exit = True
            self.log_error(Markdown("Assistant failed to reply."))
            if XSH.env.get("DEBUG", True if os.environ.get("DEBUG", "False").lower() == "true" else False):
                raise e
        
        self.is_listening = False
        self.kernel_interface.spinner.info("Stopped listening.")
        return self.is_listening
    
    def stop_listening(self):
        self.asr_stop_event.set()
        try:
            self.bg_listen_thread.join(1)
            self.asr_stop_event = threading.Event()
            self.bg_listen_thread = threading.Thread(target=self.listen, args=(self.asr_stop_event,))
        except Exception:
            pass
        self.is_listening = False
        self.kernel_interface.spinner.info("Stopped listening.")
        return self.is_listening