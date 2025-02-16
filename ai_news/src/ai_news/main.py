#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from crew import AiNews

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs_array = [
        {
        'topic': 'Bitcoin Mining costs',
        'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        },
        {
        'topic': 'Gold Mining costs',
        'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        },
        {
        'topic': 'Coal Mining costs',
        'date': datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        }
    ]
    AiNews().crew().kickoff_for_each(inputs=inputs_array)


    
run()
