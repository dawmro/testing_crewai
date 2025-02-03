#!/usr/bin/env python
import sys
import warnings
import os
import agentops
from crew import SceneMaker
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

story_path = "input/story.txt"

def read_file(filename):
    with open(filename, "r", encoding='utf-8') as fp:
        file_content = fp.read()
        return file_content

def run():
    """
    Run the crew.
    """
    inputs = {
        'story_text': read_file(story_path),
        'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    }
    agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), skip_auto_end_session=False)
    SceneMaker().crew().kickoff(inputs=inputs)
    agentops.end_session('Success')


if __name__ == "__main__":
    run()