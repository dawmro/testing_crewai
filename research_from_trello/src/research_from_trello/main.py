#!/usr/bin/env python
import sys
import warnings
import os
import agentops 
from crew import ResearchFromTrello

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), skip_auto_end_session=True)
    ResearchFromTrello().crew().kickoff()
    agentops.end_session('Success')


if __name__ == "__main__":
    run()

