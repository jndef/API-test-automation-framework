import os

from dotenv import load_dotenv
load_dotenv()


stages={
    "local":"http://localhost:8000",
    "local_docker":"http://host.docker.internal:8000",
    
}


def get_stage():
    stage_key=os.getenv("STAGE")
    return stages[stage_key]


