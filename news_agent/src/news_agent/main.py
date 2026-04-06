#!/usr/bin/env python
import os
import sys
import warnings
from datetime import date, datetime, timedelta
from news_agent.crew import NewsAgent
from datetime import date
import pytz
from datetime import datetime

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    import pytz
    from datetime import datetime, timedelta
    
    ist = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist).date()
    yesterday = today - timedelta(days=1)
    
    # Load yesterday's digest if it exists
    previous_news = ""
    digest_path = f"digests/Digest_{yesterday.strftime('%d_%m_%y')}.md"
    if os.path.exists(digest_path):
        with open(digest_path, 'r') as f:
            previous_news = f.read()

    inputs = {
        'current_date': str(today),
        'previous_news': previous_news if previous_news else "No previous digest available."
    }
    try:
        NewsAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'current_date': str(date.today()),
    }
    try:
        NewsAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        NewsAgent().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    import pytz
    from datetime import datetime
    ist = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist).date()
    inputs = {
        'current_date': str(today),
    }
    try:
        NewsAgent().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import pytz
    from datetime import datetime
    import json
    ist = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist).date()
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")
    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")
    inputs = {
        "crewai_trigger_payload": trigger_payload,
        'current_date': str(today),
    }
    try:
        result = NewsAgent().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")