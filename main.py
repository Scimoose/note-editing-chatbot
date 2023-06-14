import os
from utils.agent import Agent
from utils.markdown_operations import NoteMakingTool, NoteReaderTool


def get_file_names():
    """
    Returns a list of file names in the "alexandria" folder.
    """
    folder_path = "./alexandria"
    file_names = os.listdir(folder_path)
    file_names.remove('.obsidian')
    return file_names

notes = get_file_names()

with open(os.path.join('prompts', 'system_prompt.txt'), 'r') as f:
    system_message = f.read().format(notes=notes)

tools = [NoteMakingTool(), NoteReaderTool()]

if __name__ == "__main__":

    # initialize agent with tools
    agent = Agent(tools).get_agent()

    new_prompt = agent.agent.create_prompt(
        system_message=system_message,
        tools=tools
    )

    print(system_message)

    agent.agent.llm_chain.prompt = new_prompt

    # existing prompt
    agent("Can you edit the Artificial intelligence note and add 2 sentences about LLMs?")