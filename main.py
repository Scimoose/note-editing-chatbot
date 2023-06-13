from dotenv import load_dotenv
import os
import markdown_operations as md

# Load environment variables from .env file
load_dotenv()

# Set the value of the OPENAI_API_KEY variable to the value of the environment variable "OPENAI_API_KEY"  # noqa: E501
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

if __name__ == "__main__":

    # Get the list of file names in the "alexandria" folder
    file_names = md.get_file_names()
    print(f"File names: {file_names}")
