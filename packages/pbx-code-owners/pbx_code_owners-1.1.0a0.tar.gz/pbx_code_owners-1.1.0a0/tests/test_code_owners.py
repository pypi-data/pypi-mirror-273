from unittest.mock import ANY, MagicMock, patch

from parameterized import parameterized

from code_owners.parser import discussion_exists, main, notify_owners


@parameterized.expand(
    [
        (["french_owner"], "peugeot"),
        (["polish_owner"], "peugeot_too"),
        (["polish_owner_too", "greg"], "bmw"),
    ]
)
@patch("code_owners.parser.requests.post")
@patch("code_owners.config.GITLAB_DISCUSSIONS_URL", "https://gitlab.test")
@patch("code_owners.config.GITLAB_TOKEN", "secret_token")
def test_notify(owners: str, section_name: str, post_mock: MagicMock):
    with patch("code_owners.parser.discussion_exists", return_value=False):
        notify_owners(owners, section_name)
    expected_message = (
        f'Section "{section_name}" requires codeowner approval: {", ".join(owners)}'
    )
    post_mock.assert_called_once_with(
        "https://gitlab.test",
        headers={"PRIVATE-TOKEN": "secret_token"},
        json={"body": expected_message},
        timeout=ANY,
    )


@parameterized.expand(
    [
        ("LGTM! :>", True),
        ("CTZG", False),
        ("Dzieen bobry", False),
        ("Dzieen bobry *beaver_emoji*", True),
    ]
)
def test_discussion_exists(searched_content: str, expeted_existence: bool):
    mocked_reply = [
        {
            "id": "105a81c457103110851c7906d6b4424876ec1482",
            "notes": [{"body": "Hi, have a nice day! :>"}],
        },
        {
            "id": "9472da155271a85072741b27b9364860abc4add1",
            "notes": [{"body": "Dzieen bobry *beaver_emoji*"}],
        },
        {
            "id": "b4374de03ff500a8a790fe4c993e1c890a821589",
            "notes": [{"body": "LGTM! :>"}],
        },
        {
            "id": "6c10c938ddc3471c9075072d47d1d8d5938a0aee",
            "notes": [{"body": 'Section "beer" requires @bald_man approval'}],
        },
    ]

    with patch("code_owners.parser.requests.get") as get_mock:
        get_mock.return_value.json.return_value = mocked_reply
        assert discussion_exists(searched_content) == expeted_existence


def test_code_owners_match():
    code_owners = {
        "sections": [
            {"name": "Code owners", "owners": ["@user_owner"], "paths": ["."]},
            {"name": "tests", "owners": ["@user_a"], "paths": ["tests/"]},
            {"name": "config", "owners": ["@user_b"], "paths": ["config/config.py"]},
            {
                "name": "compose",
                "owners": ["@user_c", "@user_d"],
                "paths": ["docker/compose.yaml"],
            },
            {"name": "dependencies", "owners": ["@user_a"], "paths": ["requirements/"]},
        ]
    }
    changed_paths = [
        "path/to/file.py",
        "urls.py",
        "tests/tests.py",
        "config/config-dev.py",
        "docker/compose.yaml",
        "requirements/requirements.txt",
    ]

    with patch(
        "code_owners.parser.get_changed_paths", return_value=changed_paths
    ), patch("code_owners.parser.load_codeowners", return_value=code_owners), patch(
        "code_owners.parser.notify_owners"
    ) as notify_owners_mock:
        main()

    assert notify_owners_mock.call_count == 4
    for owner, section in (
        (["@user_owner"], "Code owners"),
        (["@user_a"], "tests"),
        (["@user_c", "@user_d"], "compose"),
        (["@user_a"], "dependencies"),
    ):
        notify_owners_mock.assert_any_call(owner, section)
