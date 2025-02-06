#!/usr/bin/env python
import agentops
import os
import sys
import warnings

from crew import SceneMaker

from utils.data_prep import get_projects, create_inputs_array, create_recap

from dotenv import load_dotenv


load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

PROJECTS_DIR = 'input'
SYNOPIS_PATH = os.path.join(PROJECTS_DIR, "synopis.txt")
RESULTS_DIR = 'output'
# example story path: input/Overlord, Advent of the New Gods, Part 1, Volume 1, Chapter 01 - Alone No More/story.txt



def run():
    """
    Run the crew.
    """
    # projects_list = get_projects(PROJECTS_DIR)
    # inputs_array = create_inputs_array(projects_list, PROJECTS_DIR, SYNOPIS_PATH)
    
    # agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), skip_auto_end_session=True)
    # SceneMaker().crew().kickoff_for_each(inputs=inputs_array)
    # agentops.end_session('Success')

    results_list = get_projects(RESULTS_DIR)
    create_recap(results_list, RESULTS_DIR)



if __name__ == "__main__":
    run()