from langchain.tools import BaseTool
from math import pi
from typing import Union

import os
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from langchain.agents import initialize_agent


class NoteMakingTool(BaseTool):
    name = "NoteMaker"
    description = "Give this tool a message with your note when you need to make or edit an exisiting note. It will overwrite existing note. Your message should be in the following format: <file title> | <your note>"  # noqa: E501

    def _run(self, new_text: str):
        file_name = new_text.split("|")[0]
        with open(f"./alexandria/{file_name}", "w", encoding="utf-8") as f:
            f.write(new_text.split("|")[1])
        return f"Created a note called {file_name}"
    
    def _arun(self, radius: Union[int, float]):
        raise NotImplementedError("This tool does not support async")

class NoteReaderTool(BaseTool):
    name = "NoteReader"
    description = "use this tool when you need to read a note"

    def _run(self, file_name: str):
        with open(f"./alexandria/{file_name}.md", "r", encoding="utf-8") as f:
            text = f.read()
        return text
    
    def _arun(self, radius: Union[int, float]):
        raise NotImplementedError("This tool does not support async")

def get_file_names():
    """
    Returns a list of file names in the "alexandria" folder.
    """
    folder_path = "./alexandria"
    file_names = os.listdir(folder_path)
    file_names.remove('.obsidian')
    return file_names



OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'OPENAI_API_KEY'

# initialize LLM (we use ChatOpenAI because we'll later define a `chat` agent)
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
    model_name='gpt-3.5-turbo'
)
# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)


tools = [NoteMakingTool()]

# initialize agent with tools
agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory
)

notes = get_file_names()

system_message = f""" 
Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with note taking tasks, which is editing and building upon notes based on given articles or blocks of text provided by user, answering simple questions based on created notes, providing in-depth explanations and discussions on a wide range of topics. 
As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. 
Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Assistant has access to note editing, note creation, note reading, and note searching tools. 

Here is a list of notes that exist: {notes}

"""  # noqa: E501

if __name__ == "__main__":

    new_prompt = agent.agent.create_prompt(
        system_message=system_message,
        tools=tools
    )

    agent.agent.llm_chain.prompt = new_prompt

    # existing prompt
    agent("Can you create a note on the topic of 'artificial intelligence'?")