"""Implements a simple echo command for xonsh."""

from rich.markdown import Markdown
from xonsh.built_ins import XSH
from xonsh.tools import unthreadable

def echo(args, stdin, stdout, stderr, env):
    """A simple echo command."""
    opts = _echo_parse_args(args)
    if opts is None:
        return
    if opts['help']:
        print(ECHO_HELP, file=stdout)
        return 0
    ender = opts['end']
    args = map(str, args)
    if opts['escapes']:
        args = map(lambda x: x.encode().decode('unicode_escape'), args)
    print(*args, end=ender, file=stdout)
    return 0, None


def _echo_parse_args(args):
    out = {'escapes': False, 'end': '\n', 'help': False}
    if '-e' in args:
        args.remove('-e')
        out['escapes'] = True
    if '-E' in args:
        args.remove('-E')
        out['escapes'] = False
    if '-n' in args:
        args.remove('-n')
        out['end'] = ''
    if '-h' in args or '--help' in args:
        out['help'] = True
    return out


ECHO_HELP = """Usage: echo [OPTIONS]... [STRING]...
Echo the STRING(s) to standard output.
  -n             do not include the trailing newline
  -e             enable interpretation of backslash escapes
  -E             disable interpretation of backslash escapes (default)
  -h  --help     display this message and exit
This version of echo was written in Python for the xonsh project: http://xon.sh
Based on echo from GNU coreutils: http://www.gnu.org/software/coreutils/"""

"""A pwd implementation for xonsh."""
import os


def pwd(args, stdin, stdout, stderr, env):
    """A pwd implementation"""
    e = env['PWD']
    if '-h' in args or '--help' in args:
        print(PWD_HELP, file=stdout)
        return 0
    if '-P' in args:
        e = os.path.realpath(e)
    print(e, file=stdout)
    return 0, None


PWD_HELP = """Usage: pwd [OPTION]...
Print the full filename of the current working directory.
  -P, --physical   avoid all symlinks
      --help       display this help and exit
This version of pwd was written in Python for the xonsh project: http://xon.sh
Based on pwd from GNU coreutils: http://www.gnu.org/software/coreutils/"""


def assistant_fn(args, stdin=None):
    print("Yes?")

# @unthreadable
def listen_fn(args, stdin=None):
    """Listen for assistant: listen only one sentence by default
    You can type listen to listen for one sentence.
    To listen continuously, type listen start (or stop to stop).
    """
    if args is None:
        args = []
    if args:
        if args[0] == "-h" or args[0] == "--help":
            print("# Help for the `listen` command")
            print("""```text
Usage: `listen [OPTIONS]... [INT]...`
Listen for one sentence by default.
You can type listen to listen for one sentence.
To listen continuously, type `listen start` (or `stop` to stop).
You can also specify the number of sentences to listen for.
```
""")
            return 0
        
        if not XSH.shell.shell.kernel_interface.is_asr:
            print("# Module Not Found Error")
            print("To speak with Assistant, you need to install the listen module.\n")
            print("Run the following command:\n```shell\npip install -r stt-listen\n```")
            return 0
        
        if not XSH.shell.shell.kernel_interface.listen_interface.is_asr_server_up():
            print("# Connection Error")
            print("""Could not reach the Automatic Speech Recognition Server.
                  
Please make sure it is up and running and that it is listening on the right port on localhost.
    
To start the server, run the following command (outside of Assistant in a separate process):

```shell
uvicorn listen.Wav2Vec.as_service:app --port 5063
```
""")
            return 0
        
        try:
            if args[0] == "start":
                try:
                    XSH.shell.shell.start_listening()
                except (KeyboardInterrupt, EOFError):
                    XSH.shell.shell.stop_listening()
                    return 0
                # print("# You can speak now")
                # print("Type `listen stop` to stop.")
                return 0
            elif args[0] == "stop":
                XSH.shell.shell.stop_listening()
                print("# Stopped listening")
                return 0
            else:
                n = int(args[0])
                print(f"Listening for {n} sentences...")
                return 0
        except ValueError:
            print("Usage: `listen [OPTIONS]... [INT]...`")
            return 0
    else:
        shell = XSH.shell.shell
        if not shell.kernel_interface.is_asr:
            print("# Module Not Found Error")
            print("To speak with Assistant, you need to install the listen module.\n")
            print("Run the following command:\n```shell\npip install -r stt-listen\n```")
            return 0
        if not shell.kernel_interface.listen_interface.is_asr_server_up():
            print("# Connection Error")
            print("""Could not reach the Automatic Speech Recognition Server.
                  
Please make sure it is up and running and that it is listening on the right port on localhost.
    
To start the server, run the following command (outside of Assistant in a separate process):

```shell
uvicorn listen.Wav2Vec.as_service:app --port 5063
```
""")
            return 0
        shell.kernel_interface.spinner.text = "Listening..."
        shell.kernel_interface.spinner.start()
        query = shell.kernel_interface.listen_interface.listen()
        shell.kernel_interface.spinner.stop()
        shell.kernel_interface.spinner.info("Stopped listening.")
        if query:
            shell.log_query(Markdown(f"> {query}"))
            answer = shell.kernel_interface.session_assistant(query)
            if answer:
                # shell.log_answer(Markdown(answer))
                shell.say(answer)
            else:
                # shell.log_error(Markdown("Assistant failed to reply."))
                print("Assistant failed to reply.")
        else:
            # shell.log_error(Markdown(f"# Nothing heard\nTranscript: '{query}'"))
            print(f"# Nothing heard\nTranscript: '{query}'")
    return 0

def say_fn(args, stdin=None):
    """say something"""
    if args is None:
        args = []
    if args:
        if args[0] == "-h" or args[0] == "--help":
            print("# Help for the `say` command")
            print("""```text
Usage: `say [OPTIONS]... [STRING]...`
Say something.

Options:

stop: stop speaking
```
""")
            return 0
        elif args[0] == "stop":
            XSH.shell.shell.stop_speaking()
            print("stop")
            return 0
        else:
            XSH.shell.shell.say(" ".join(args))
            return 0
    else:
        print("Usage: `say [OPTIONS]... [STRING]...`")
        return 1