from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import os

# Load environment variables from .env file
load_dotenv()

# Set the value of the OPENAI_API_KEY variable to the value of the environment variable "OPENAI_API_KEY"  # noqa: E501
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def get_file_names():
    """
    Returns a list of file names in the "alexandria" folder.
    """
    folder_path = "./alexandria"
    file_names = os.listdir(folder_path)
    file_names.remove('.obsidian')
    return file_names

def update_markdown_file(file_name, new_text):
    """
    Overwrites the contents of a markdown file with new text.

    Args:
        file_path (str): The path to the markdown file.
        new_text (str): The new text to write to the file.
    """
    with open(f"./alexandria/{file_name}", "w", encoding="utf-8") as f:
        f.write(new_text)


if __name__ == "__main__":

    # Get the list of file names in the "alexandria" folder
    file_names = get_file_names()
    # Overwrite the first file in the list
    update_markdown_file(file_names[0], "This is a test.")

