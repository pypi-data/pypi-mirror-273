import subprocess  # nosec

import requests
import yaml

from code_owners import config


def load_codeowners() -> dict:
    with open(config.CODEOWNERS_FILE) as file:
        return yaml.safe_load(file)


def get_changed_paths() -> list[str]:
    subprocess.run(["git", "fetch", "origin", "master:master"])  # nosec
    git_diff = subprocess.run(  # nosec
        ["git", "diff", "--name-only", config.DEFAULT_BRANCH], stdout=subprocess.PIPE
    )
    return git_diff.stdout.decode().splitlines()


def match_any_path(sub_paths: list[str], base_paths: list[str]) -> bool:
    if "." in base_paths:
        return True

    matched_paths = (
        sub_path
        for sub_path in sub_paths
        for base_path in base_paths
        if sub_path.startswith(base_path)
    )
    try:
        next(matched_paths)
    except StopIteration:
        return False
    return True


def discussion_exists(content: str) -> bool:
    url = config.GITLAB_DISCUSSIONS_URL
    headers = {"PRIVATE-TOKEN": config.GITLAB_TOKEN}
    resp = requests.get(url, headers=headers, timeout=(3, 30))
    resp.raise_for_status()
    discussions = resp.json()
    filtered_discussions = (
        discussion
        for discussion in discussions
        if discussion["notes"][0]["body"] == content
    )
    try:
        next(filtered_discussions)
    except StopIteration:
        return False
    return True


def notify_owners(owners: str, section_name: str) -> None:
    owners_string = ", ".join(owners)
    content = f'Section "{section_name}" requires codeowner approval: {owners_string}'
    if discussion_exists(content):
        return

    url = config.GITLAB_DISCUSSIONS_URL
    headers = {"PRIVATE-TOKEN": config.GITLAB_TOKEN}
    resp = requests.post(url, headers=headers, json={"body": content}, timeout=(3, 30))
    resp.raise_for_status()


def main() -> None:
    codeowners = load_codeowners()
    changed_paths = get_changed_paths()
    if not changed_paths:
        print("No changes, checking codeowners stopped")
        return

    for section in codeowners["sections"]:
        if match_any_path(changed_paths, section["paths"]):
            notify_owners(section["owners"], section["name"])
    return


if __name__ == "__main__":
    main()
