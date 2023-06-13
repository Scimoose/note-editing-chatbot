from langchain.tools import BaseTool
from math import pi
from typing import Union

import os
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from langchain.agents import initialize_agent


class CircumferenceTool(BaseTool):
    name = "Circumference calculator"
    description = "use this tool when you need to calculate a circumference using the radius of a circle"

    def _run(self, radius: Union[int, float]):
        return float(radius)*2.0*pi
    
    def _arun(self, radius: Union[int, float]):
        raise NotImplementedError("This tool does not support async")


class NoteMakingTool(BaseTool):
    name = "NoteMaker"
    description = "use this tool when you need to make a note"

    def _run(self, new_text: str):
        file_name = new_text.split(" ")[0]
        with open(f"./alexandria/{file_name}.md", "w", encoding="utf-8") as f:
            f.write(new_text)
    
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


tools = [CircumferenceTool(), NoteMakingTool()]

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

system_message = """ 


"""

if __name__ == "__main__":

    new_prompt = agent.agent.create_prompt(
        system_message=system_message,
        tools=tools
    )

    agent.agent.llm_chain.prompt = new_prompt

    notes = get_file_names()
    # existing prompt
    print(agent.agent.llm_chain.prompt.messages[0].prompt.template)