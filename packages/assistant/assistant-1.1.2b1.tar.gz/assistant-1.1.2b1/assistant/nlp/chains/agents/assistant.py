"""Assistant agent classes"""
from typing import Any, Dict, List, Tuple, Union #, Optional
from langchain_core.agents import AgentAction, AgentFinish #, AgentStep
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import BaseMessage
from langchain.chains.llm import LLMChain
from langchain.agents.agent import LLMSingleActionAgent, AgentOutputParser #, BaseSingleActionAgent
from langchain.callbacks.manager import Callbacks
from assistant.nlp.chains.parsers.json import JsonOutputParser

class AssistantSingleActionAgent(LLMSingleActionAgent):
    """An agent that can perform a single action at any given time."""
    
    llm_chain: LLMChain
    """LLMChain to use for agent."""
    output_parser: AgentOutputParser
    """Output parser to use for agent."""
    stop: List[str]
    """List of strings to stop on."""

    @property
    def input_keys(self) -> List[str]:
        """Return the input keys.

        Returns:
            List of input keys.
        """
        return list(set(self.llm_chain.input_keys) - {"intermediate_steps"})

    def dict(self, **kwargs: Any) -> Dict:
        """Return dictionary representation of agent."""
        _dict = super().dict()
        del _dict["output_parser"]
        return _dict

    def plan(
        self,
        intermediate_steps: List[Tuple[AgentAction, str]],
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with the observations.
            callbacks: Callbacks to run.
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        full_output = self.llm_chain.predict(
            intermediate_steps=intermediate_steps,
            # stop=self.stop,
            callbacks=callbacks,
            **kwargs,
        )
        return self.output_parser.parse(full_output)

    async def aplan(
        self,
        intermediate_steps: List[Tuple[AgentAction, str]],
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            callbacks: Callbacks to run.
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        full_inputs = self.get_full_inputs(intermediate_steps, **kwargs)
        full_output = self.llm_chain.apredict(
            stop=self.stop,
            callbacks=callbacks,
            **full_inputs,
        )
        return self.output_parser.aparse(full_output)

    def tool_run_logging_kwargs(self) -> Dict:
        return {
            "llm_prefix": "",
            "observation_prefix": "" if len(self.stop) == 0 else self.stop[0],
        }
    
    
