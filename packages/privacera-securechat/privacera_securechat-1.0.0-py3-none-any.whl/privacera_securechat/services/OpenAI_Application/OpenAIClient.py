import logging
from langchain.llms import OpenAI
from services.langchain_service_intf import LangChainServiceIntf
logger = logging.getLogger(__name__)


class OpenAIClient(LangChainServiceIntf):
    def __init__(self, ai_app_name):
        super().__init__(ai_app_name)
        logger.info("Initializing OPENAI model")
        openai_config = self.config["openai"]
        self.max_input_size = openai_config.get("max_input_size", 4096)
        self.num_outputs = openai_config.get("num_outputs", 512)
        self.temperature = openai_config.get("temperature", 0.1)
        self.openai_model = openai_config.get("model", None)
        if "ask_prompt_suffix" in openai_config:
            self.ask_prompt_suffix = openai_config.get("ask_prompt_suffix")
        if "client_error_msg" in openai_config:
            self.client_error_msg = openai_config.get("client_error_msg")
        logger.info(f"Max Input Size: {self.max_input_size}")
        logger.info(f"Number of Outputs: {self.num_outputs}")
        logger.info(f"Temperature: {self.temperature}")
        logger.info(f"Ask Prompt Suffix: {self.ask_prompt_suffix}")
        logger.info(f"Conversation History K: {self.conversation_history_k}")
        logger.info(f"Open AI Model: {self.openai_model}")
        logger.info(f"Disable Conversation Chain: {self.disable_conversation_chain}")
        openai_params = {"temperature": self.temperature}
        if self.openai_model is not None and self.openai_model != "":
            openai_params["model"] = self.openai_model
        self.langchain_llm = OpenAI(**openai_params)
