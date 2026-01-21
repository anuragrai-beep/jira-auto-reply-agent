import json
from datetime import datetime, time
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import jira_auto_reply as sut


def make_env(monkeypatch, **overrides):
    base = {
        "JIRA_BASE_URL": "https://example.atlassian.net",
        "JIRA_EMAIL": "anurag.rai@certifyos.com",
        "JIRA_API_TOKEN": "token",
        "JIRA_ASSIGNEE_ACCOUNT_ID": "712020:abc",
        "PROJECT_KEY": "TS",
        "ASSIGNEE_FALLBACK": "currentUser()",
        "STATUS_FIELD_ID": "customfield_10353",
        "STATUS_TRANSITION_TODO_TO_IN_PROGRESS": "To-Do",
        "STATUS_TRANSITION_IN_PROGRESS_TO_WAITING": "Iprogress",
        "STATUS_TRANSITION_WAITING_TO_IN_PROGRESS": "Wating for clinet",
        "USE_CONFLUENCE_KB": "false",
        "CONFLUENCE_BASE_URL": "https://example.atlassian.net/wiki",
        "CONFLUENCE_SPACE_KEY": "TS",
        "OPENAI_MODEL": "gpt-4o-mini",
        "LAST_RUN_PATH": "last_run.json",
    }
    base.update(overrides)
    for key, value in base.items():
        monkeypatch.setenv(key, value)


def test_parse_time_env(monkeypatch):
    monkeypatch.setenv("WINDOW_START", "06:15")
    assert sut.parse_time_env("WINDOW_START", "05:30") == time(6, 15)


def test_within_reply_window_handles_same_day_window():
    config = SimpleNamespace(window_start=time(5, 30), window_end=time(17, 30))
    assert sut.within_reply_window(config, datetime(2024, 1, 1, 6, 0))
    assert not sut.within_reply_window(config, datetime(2024, 1, 1, 20, 0))


def test_within_reply_window_handles_overnight_window():
    config = SimpleNamespace(window_start=time(22, 0), window_end=time(6, 0))
    assert sut.within_reply_window(config, datetime(2024, 1, 1, 23, 0))
    assert sut.within_reply_window(config, datetime(2024, 1, 2, 5, 30))
    assert not sut.within_reply_window(config, datetime(2024, 1, 2, 12, 0))


def test_load_config_requires_account_id(monkeypatch):
    make_env(monkeypatch)
    config = sut.load_config()
    assert config.jira_assignee_account_id == "712020:abc"


def test_jira_search_issues_builds_jql(monkeypatch):
    make_env(monkeypatch)
    config = sut.load_config()
    last_run = datetime(2024, 1, 2, 3, 4, 5)

    captured = {}

    def fake_get(url, headers, auth, params, timeout):
        captured["url"] = url
        captured["params"] = params
        return SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {"issues": [{"key": "TS-1"}]},
        )

    monkeypatch.setattr(sut.requests, "get", fake_get)
    issues = sut.jira_search_issues(config, last_run)

    assert issues == [{"key": "TS-1"}]
    assert url_ends_with(captured["url"], "/rest/api/3/search/jql")
    assert 'project = "TS"' in captured["params"]["jql"]
    assert 'status = "To-Do"' in captured["params"]["jql"]
    assert "updated >= " in captured["params"]["jql"]


def test_generate_ai_reply_falls_back_without_key(monkeypatch):
    make_env(monkeypatch)
    config = sut.load_config()
    object.__setattr__(config, "openai_api_key", None)
    issue = {"fields": {"summary": "Test ticket"}}
    reply = sut.generate_ai_reply(config, issue)
    assert "Test ticket" in reply


def test_generate_ai_reply_calls_openai(monkeypatch):
    make_env(monkeypatch, OPENAI_API_KEY="key")
    config = sut.load_config()

    def fake_post(url, headers, json, timeout):
        assert url == "https://api.openai.com/v1/chat/completions"
        assert json["model"] == config.openai_model
        return SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {
                "choices": [{"message": {"content": "Thanks for the details!"}}]
            },
        )

    monkeypatch.setattr(sut.requests, "post", fake_post)
    reply = sut.generate_ai_reply(config, {"fields": {"summary": "A"}})
    assert reply == "Thanks for the details!"


def test_jira_transition_issue_uses_transition_id(monkeypatch):
    make_env(monkeypatch)
    config = sut.load_config()

    monkeypatch.setattr(
        sut,
        "jira_list_transitions",
        lambda *_: [{"id": "55", "name": "Iprogress"}],
    )

    captured = {}

    def fake_post(url, headers, auth, json, timeout):
        captured["url"] = url
        captured["json"] = json
        return SimpleNamespace(raise_for_status=lambda: None)

    monkeypatch.setattr(sut.requests, "post", fake_post)
    sut.jira_transition_issue(config, "TS-1", "Iprogress")

    assert url_ends_with(captured["url"], "/rest/api/3/issue/TS-1/transitions")
    assert captured["json"] == {"transition": {"id": "55"}}


def test_process_issues_calls_all_actions(monkeypatch):
    make_env(monkeypatch)
    config = sut.load_config()

    called = {"comment": 0, "assign": 0, "transition": 0}

    monkeypatch.setattr(sut, "generate_ai_reply", lambda *_: "reply")
    monkeypatch.setattr(
        sut, "jira_add_comment", lambda *_: called.__setitem__("comment", 1)
    )
    monkeypatch.setattr(
        sut, "jira_assign_issue", lambda *_: called.__setitem__("assign", 1)
    )
    monkeypatch.setattr(
        sut, "jira_transition_issue", lambda *_: called.__setitem__("transition", 3)
    )

    issues = [{"key": "TS-1"}]
    processed = sut.process_issues(config, issues, config.jira_assignee_account_id)

    assert processed == 1
    assert called["comment"] == 1
    assert called["assign"] == 1
    assert called["transition"] == 3


def url_ends_with(url: str, suffix: str) -> bool:
    return url.rstrip("/").endswith(suffix)
