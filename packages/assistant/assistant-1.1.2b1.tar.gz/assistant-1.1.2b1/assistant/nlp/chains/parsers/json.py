import json
import re

from langchain.agents import AgentOutputParser
from langchain.agents.conversational_chat.prompt import FORMAT_INSTRUCTIONS
from langchain.output_parsers.json import parse_json_markdown as _parse_jsonmd
from langchain.schema import AgentAction, AgentFinish

from json.decoder import JSONDecodeError


def parse_json(json_string: str) -> dict:
    """
    Parse a JSON dict from a string.

    Args:
        json_string: The string.

    Returns:
        The parsed JSON object as a Python dictionary.
    """
    json_str = json_string

    # Strip whitespace and newlines from the start and end
    json_str = json_str.strip()

    # handle newlines and other special characters inside the returned value
    # json_str = _custom_parser(json_str)

    # Parse the JSON string into a Python dictionary
    parsed = json.loads(json_str)

    return parsed


class JsonOutputParser(AgentOutputParser):
    """Parses JSON output."""
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> AgentAction | AgentFinish:
        _text = self.handle_model_specifics(text)
        # print(_text)
        try:
            # this will work IF the text is a valid JSON with function and parameters
            json_resp = parse_json(_text)
            func, params = json_resp["function"], json_resp["parameters"]
            if func.lower().replace(" ", "_") == "final_answer":
                # this means the agent is finished so we call AgentFinish
                return AgentFinish({"output": params["answer"] or params}, _text)
            # otherwise the agent wants to use an action, so we call AgentAction
            return AgentAction(func, params, _text)
        except KeyError as ke:
            _ke = str(ke).strip()
            if isinstance(json_resp, dict) and _ke != "'function'":
                # LLM did manage to respond a json parsable dict but failed to generate the expected format
                # lets try to handle it any way
                func = json_resp.pop("function", None)
                json_resp.pop("final_answer", None)
                params = json_resp
                
                if func.lower().replace(" ", "_") == "final_answer":
                    # this means the agent is finished so we call AgentFinish
                    return AgentFinish({"output": params["answer"] if isinstance(params, dict) and 'answer' in params else params if isinstance(params, str) else json_resp[func]},
                                       f"KeyError: Missing key: {_ke}\nLLM Response: {_text}")
                # otherwise the agent wants to use an action, so we call AgentAction
                return AgentAction(
                    func, params,
                    f"KeyError: Missing key: {_ke}\nLLM Response: {_text}"
                )
            elif isinstance(json_resp, dict) and _ke == "'function'":
                # LLM did manage to respond a json parsable dict but failed to generate the expected format
                # lets try to handle it any way
                js_keys = list(json_resp.keys())
                func = js_keys[0]
                params = json_resp[func]
                if func.lower().replace(" ", "_") == "final_answer":
                    # this means the agent is finished so we call AgentFinish
                    return AgentFinish({"output": params["answer"] if isinstance(params, dict) and 'answer' in params else params if isinstance(params, str) else json_resp[func] },
                                       f"KeyError: Missing key: {_ke}\nLLM Response: {_text}")
                # otherwise the agent wants to use an action, so we call AgentAction
                return AgentAction(
                    func, params,
                    f"KeyError: Missing key: {_ke}\nLLM Response: {_text}"
                )
        except JSONDecodeError as jsde:
            # LLM failed to respond a json parsable dict
            if not _text.startswith("{"):
                return AgentFinish(
                    {"output": _text},
                    f"JSONDecodeError: Could not parse output: {str(jsde)}\nLLM Response: {_text}",
                )
            return AgentFinish(
                    {"output": ""},
                    f"JSONDecodeError: Could not parse output: {str(jsde)}\nLLM Response: {_text}",
                )

    def handle_model_specifics(self, model_output: str) -> str:
        """
        Remove special tokens from the given output and perform any necessary pre-processing steps.
        """
        model_output = model_output.replace("\n}\n}\n\n", "\n}\n}<|im_end|>\n\n")
        model_output = model_output.split("<|im_end|>")[0]
        model_output = model_output.split("<|im_start|>")[0]
        # model_output = model_output.split("<s>[INST]")[0]
        # model_output = model_output.split("</s>")[0]
        # model_output = model_output.replace(
        #     "```\n\n```", "```</s> | <s>[INST] This hallucination will be discarded [/INST] ```"
        #     ).split(" | ")[0].removesuffix('<s>')
        # model_output = model_output.split("[/INST]")[0].strip()
        # model_output = model_output.split("[INST]")[0].strip()
        # text = text.replace("""</s>""", "")
        # text = text.replace("\n", '')
        # text = text.replace("\t", '')
        # text = text.replace("\r", '')
        # text = text.replace(" ", '')
        # text = text.replace("```json", '')
        model_output = model_output.replace("```", '')
        # model_output = model_output.strip("\n")
        while model_output.endswith("<|im_end|>"):
            model_output = model_output.removesuffix("<|im_end|>")
        return model_output

    @property
    def _type(self) -> str:
        return "conversational_chat"


if __name__ == "__main__":
    # Lets try to parse various forms or output from the llm
    js_text = [
        """{ "function": "final_answer", "answer": "L'écran a été effacé. Je suis prêt à vous aider si vous avez besoin d'aide ou de questions." }""",
        """{ "function": "final_answer", "parameters": {"answer": "L'écran a été effacé. Je suis prêt à vous aider si vous avez besoin d'aide ou de questions."} }""",
        """ {
  "function": "final_answer",
  "parameters": {
    "answer": "Hello! It's good to see you again. I'm here to assist you. What can I help you with today?"
  }
}""",
    """{
    "function": "shell",
    "parameters": {
        "code": "cd $HOME && ls"
    }
}<|im_stop|>""",
        """ {
  "function": "final_answer",
  "answer": "I apologize for the confusion earlier. I understand that you wanted me to change the directory using the 'cd' command instead of listing the files in the parent directory. I have acknowledged your request and will make sure to follow your instructions in the future. Please let me know if you need any further assistance."
}""",
    """{
    "final_answer": "I have executed the 'ls' command in the shell, and the output shows the files and directories present in your current directory. You can observe the list of files and directories yourself."
}<|im_stop|>""",
    """ {
  "final_answer": {
    "answer": "Je suis désolé, je ne peux pas déterminer quelle fonction convient le mieux à cette phrase. Pourriez-vous fournir plus d'informations ou reformuler votre demande?"
  }
}""",
    ]
    output_parser = JsonOutputParser()
    print("\n"*3, end="\n\n" + "=" * 50 + "\n\n",)
    for text in js_text:
        print(
            output_parser.parse(text).to_json(),
            end="\n\n" + "=" * 50 + "\n\n",
        )
