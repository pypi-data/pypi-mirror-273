import os
from pathlib import Path

DEFAULT_BRANCH = os.environ.get("DEFAULT_BRANCH", "master")
CODEOWNERS_FILE = Path(os.getcwd()) / "codeowners.yml"


CI_SERVER_URL = os.environ["CI_SERVER_URL"]
CI_PROJECT_ID = os.environ["CI_PROJECT_ID"]
CI_MERGE_REQUEST_IID = os.environ["CI_MERGE_REQUEST_IID"]
GITLAB_TOKEN = os.environ["CODE_OWNERS_GITLAB_TOKEN"]


GITLAB_DISCUSSIONS_URL = (
    f"{CI_SERVER_URL}/api/v4/projects/{CI_PROJECT_ID}"
    f"/merge_requests/{CI_MERGE_REQUEST_IID}/discussions"
)
