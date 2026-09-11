import os

from dotenv import load_dotenv
load_dotenv()


stages={
    "local":"http://localhost:8000",
    "local_docker":"http://host.docker.internal:8000",
    
}


def get_stage() -> str:
    """Global setup for test stage. Puts value of the variable from env file """
    stage_key=os.getenv("STAGE", stages["local"])
    return stages[stage_key]


