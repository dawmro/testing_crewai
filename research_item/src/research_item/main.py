#!/usr/bin/env python
import sys
import warnings

from crew import ResearchItem

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        "item1": "Apple Watch Ultra 2",
        "item2": "Garmin Fenix 9",
        "goal": "Find the best health wearable for 2024 for training for a marathon",
    }
    ResearchItem().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
