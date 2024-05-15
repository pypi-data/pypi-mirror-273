import logging
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from core import config
from core import llm_constants

logger = logging.getLogger(__name__)

import privacera_shield.client
import privacera_shield.exception
from core.llm_constants import paig_shield


class LangChainServiceIntf:

    def __init__(self, ai_application_name):
        self.langchain_llm = None
        self.paig_shield = paig_shield
        self.ai_application_name = ai_application_name
        self.config = config.Config
        ai_application_conf = self.config["AI_applications"]
        self.conversation_history_k = ai_application_conf.get("conversation_history_k", 3)
        vector_store_factory_instance = llm_constants.vector_store
        self.vectordb = vector_store_factory_instance.get_application_vectordb_index(self.ai_application_name)
        self.ask_prompt_suffix = self.config.get("ask_prompt_suffix")
        self.client_error_msg: str = self.config.get("client_error_msg")
        self.disable_conversation_chain = ai_application_conf[self.ai_application_name].get(
            "disable_conversation_chain", False)

    def _get_retrievalqa(self):
        try:
            return RetrievalQA.from_chain_type(llm=self.langchain_llm, chain_type='map_reduce',
                                               retriever=self.vectordb.as_retriever(), verbose=True)
        except Exception as e:
            logger.error(f"Exception occurred while getting llm chain with error :: {e}")
            raise e

    def _get_conversational_retrieval_chain(self, conversation_messages=None, temperature=None):
        try:
            memory = ConversationBufferWindowMemory(
                k=self.conversation_history_k,
                memory_key="chat_history",
                return_messages=True)

        except Exception as e:
            logger.error(f"Exception occur while getting conversation buffer window memory with error :: {e}")
            raise e
        if memory and conversation_messages:
            for conversation in conversation_messages:
                if conversation['type'] == "prompt":
                    memory.chat_memory.add_user_message(conversation['content'])
                else:
                    memory.chat_memory.add_ai_message(conversation['content'])

        try:
            qa = ConversationalRetrievalChain.from_llm(self.langchain_llm, memory=memory, verbose=True,
                                                       retriever=self.vectordb.as_retriever())
            return qa
        except Exception as e:
            logger.error(f"Exception occurred while getting qa chain with error :: {e}")
            raise e

    def _get_retrieval_object(self, conversation_messages=None):
        if self.disable_conversation_chain:
            return self._get_retrievalqa()
        else:
            return self._get_conversational_retrieval_chain(conversation_messages)

    def _execute_prompt(self, retrieval_object, prompt):
        if self.disable_conversation_chain:
            result = retrieval_object({"query": prompt})
            return result['result']
        else:
            result = retrieval_object({"question": prompt})
            return result['answer']

    def ask_prompt(self, prompt, conversation_messages=None, temperature=None, user_name=None):
        logger.info(f"Asking prompt :: {prompt} for ai_application_name :: {self.ai_application_name}")
        if not temperature:
            temperature = 0.1
        try:
            if self.ask_prompt_suffix:
                prompt = prompt + self.ask_prompt_suffix

            if self.paig_shield.DISABLE_PAIG_SHIELD_PLUGIN_FLAG:
                retrieval_object = self._get_retrieval_object(conversation_messages)
                reply = self._execute_prompt(retrieval_object, prompt)
                logger.info(f"Reply :: {reply}")
            else:
                logger.info(f"Authorizing for  :: {user_name}")
                ai_app = self.paig_shield.get_paig_config_map(self.ai_application_name)
                kwargs = {
                    "username": user_name
                }
                if ai_app is not None:
                    kwargs['application'] = ai_app
                with privacera_shield.client.create_shield_context(**kwargs):
                    retrieval_object = self._get_retrieval_object(conversation_messages)
                    reply = self._execute_prompt(retrieval_object, prompt)
                    logger.info(f"Reply :: {reply}")
            return reply

        except privacera_shield.exception.AccessControlException as e:
            logger.exception(f"Access Denied, message: {e}")
            return (f"Access Denied")
        except Exception as ex:
            logging.exception(
                f"Exception occurred when asking auth_service to execute_prompt, question= {prompt} with error :: {ex}")
            return self.client_error_msg
