"""Тесты парсера и фильтра.

Запуск: pytest tests/ -v
Или из корня проекта: pytest
"""
from __future__ import annotations

import sys
from pathlib import Path

# Добавляем src/ в PYTHONPATH
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from src.filter import VACANCY_TAGS, filter_vacancies, is_vacancy
from src.loader import _natural_sort_key, list_html_files
from src.parser import (
    Message,
    _extract_tags,
    _to_utc_iso,
    message_to_csv_row,
    parse_all_messages,
    parse_message,
)


# --- _to_utc_iso ---

def test_to_utc_iso_positive_offset():
    """UTC+3:00 → отнимаем 3 часа."""
    assert _to_utc_iso("21.09.2016 16:35:02 UTC+03:00") == "2016-09-21T13:35:02+00:00"


def test_to_utc_iso_negative_offset():
    """UTC-5:00 → прибавляем 5 часов."""
    assert _to_utc_iso("15.03.2024 02:00:00 UTC-05:00") == "2024-03-15T07:00:00+00:00"


def test_to_utc_iso_invalid():
    assert _to_utc_iso("invalid") is None
    assert _to_utc_iso("") is None
    assert _to_utc_iso(None) is None


# --- _extract_tags ---

def test_extract_tags_basic():
    tags = _extract_tags("Ищем аналитика #vacancy #естьработа #москва")
    assert tags == {"#vacancy", "#естьработа", "#москва"}


def test_extract_tags_lowercase():
    """Регистр не должен иметь значения."""
    tags = _extract_tags("#VACANCY #Vacancy")
    assert tags == {"#vacancy"}  # dedup


def test_extract_tags_skip_anchors():
    """#go_to_message12345 — якорь, не тег."""
    tags = _extract_tags("См. #go_to_message12345 и #vacancy")
    assert tags == {"#vacancy"}


def test_extract_tags_empty():
    assert _extract_tags("") == set()
    assert _extract_tags("Без тегов вообще") == set()


def test_extract_tags_dedup():
    tags = _extract_tags("#vacancy #VACANCY #Vacancy")
    assert tags == {"#vacancy"}


# --- _natural_sort_key ---

def test_natural_sort_key():
    """messages2 < messages10."""
    keys = sorted(
        ["messages.html", "messages2.html", "messages10.html", "messages100.html"],
        key=lambda n: _natural_sort_key(n),
    )
    assert keys == ["messages.html", "messages2.html", "messages10.html", "messages100.html"]


# --- parse_message ---

SAMPLE_BLOCK = """
<div class="message default clearfix" id="message12345">
  <div class="pull_left userpic_wrap">
    <div class="userpic userpic8" style="width: 42px; height: 42px">
      <div class="initials" style="line-height: 42px">АИ</div>
    </div>
  </div>
  <div class="body">
    <div class="pull_right date details" title="21.09.2016 16:35:02 UTC+03:00">16:35</div>
    <div class="from_name">Алексей Иванов</div>
    <div class="text">Ищем аналитика в команду <br><br>Теги: #vacancy #москва<br><a href="https://hh.ru/vacancy/123456">hh.ru/vacancy/123456</a></div>
  </div>
</div>
"""


def test_parse_message_basic():
    m = parse_message(SAMPLE_BLOCK)
    assert m is not None
    assert m.message_id == 12345
    assert m.author == "Алексей Иванов"
    assert m.date == "2016-09-21T13:35:02+00:00"
    assert not m.is_service
    assert "Ищем аналитика" in m.text
    assert "#vacancy" in m.text
    assert "https://hh.ru/vacancy/123456" in m.links
    assert "#vacancy" in m.tags
    assert "#москва" in m.tags
    assert m.is_vacancy()


def test_parse_message_id_with_dash():
    """'message-1' (для service-сообщений) → id=1."""
    block = '<div class="message service" id="message-1"><div class="body details">21 September 2016</div></div>'
    m = parse_message(block)
    assert m is not None
    assert m.message_id == 1
    assert m.is_service


def test_parse_message_service_no_text():
    """Service-сообщение: нет text/author, но message_id парсится."""
    block = """
    <div class="message service" id="message2">
      <div class="body details">Alexey Nikushin changed group title</div>
    </div>
    """
    m = parse_message(block)
    assert m is not None
    assert m.is_service
    assert m.author is None
    assert m.text == ""


def test_parse_message_invalid_returns_none():
    """Блок без класса 'message' → None."""
    block = '<div class="other"><p>not a message</p></div>'
    assert parse_message(block) is None


def test_parse_message_br_normalization():
    """<br> → пробел, множественные <br> не схлопываются."""
    block = """
    <div class="message default clearfix" id="message1">
      <div class="body">
        <div class="pull_right date details" title="01.01.2020 00:00:00 UTC+00:00"></div>
        <div class="from_name">Test</div>
        <div class="text">line one<br>line two<br><br>line four</div>
      </div>
    </div>
    """
    m = parse_message(block)
    assert m is not None
    assert m.text == "line one line two line four"


def test_parse_message_multiple_links():
    block = """
    <div class="message default clearfix" id="message1">
      <div class="body">
        <div class="pull_right date details" title="01.01.2020 00:00:00 UTC+00:00"></div>
        <div class="from_name">Test</div>
        <div class="text">ссылки: <a href="https://hh.ru/v1">hh</a> и <a href="https://t.me/c/123">telegram</a></div>
      </div>
    </div>
    """
    m = parse_message(block)
    assert m is not None
    assert "https://hh.ru/v1" in m.links
    assert "https://t.me/c/123" in m.links
    assert len(m.links) == 2


def test_parse_message_dedup_links():
    """Дублирующиеся ссылки сохраняются только один раз."""
    block = """
    <div class="message default clearfix" id="message1">
      <div class="body">
        <div class="pull_right date details" title="01.01.2020 00:00:00 UTC+00:00"></div>
        <div class="from_name">Test</div>
        <div class="text"><a href="https://hh.ru/v1">a</a> <a href="https://hh.ru/v1">b</a></div>
      </div>
    </div>
    """
    m = parse_message(block)
    assert m.links == ["https://hh.ru/v1"]


# --- parse_all_messages ---

PAGE_HTML = """
<html><body>
  <div class="history">
    <div class="message service" id="message-1"><div class="body details">date</div></div>
    <div class="message default clearfix" id="message1">
      <div class="body">
        <div class="pull_right date details" title="01.01.2020 00:00:00 UTC+00:00"></div>
        <div class="from_name">Author 1</div>
        <div class="text">Вакансия 1 #vacancy</div>
      </div>
    </div>
    <div class="message default clearfix joined" id="message2">
      <div class="body">
        <div class="pull_right date details" title="01.01.2020 00:01:00 UTC+00:00"></div>
        <div class="text">Продолжение вакансии #vacancy</div>
      </div>
    </div>
    <div class="message default clearfix" id="message3">
      <div class="body">
        <div class="pull_right date details" title="01.01.2020 00:02:00 UTC+00:00"></div>
        <div class="from_name">Author 2</div>
        <div class="text">Не вакансия, просто привет</div>
      </div>
    </div>
  </div>
</body></html>
"""


def test_parse_all_messages_skips_service():
    msgs = parse_all_messages(PAGE_HTML)
    # Должны получить все default-сообщения, включая 'joined'
    assert len(msgs) == 3
    assert all(not m.is_service for m in msgs)


def test_parse_all_messages_includes_joined():
    """joined-сообщения (без from_name, продолжение) тоже парсятся."""
    msgs = parse_all_messages(PAGE_HTML)
    joined = [m for m in msgs if m.message_id == 2]
    assert len(joined) == 1
    assert joined[0].author is None  # joined не имеет from_name
    assert "Продолжение" in joined[0].text


# --- filter.is_vacancy / filter_vacancies ---

def test_is_vacancy_by_russian_tag():
    m = Message(date=None, message_id=1, author="X", text="t", tags={"#вакансия"})
    assert is_vacancy(m)


def test_is_vacancy_by_english_tag():
    m = Message(date=None, message_id=1, author="X", text="t", tags={"#vacancy"})
    assert is_vacancy(m)


def test_is_vacancy_by_historical_tag():
    m = Message(date=None, message_id=1, author="X", text="t", tags={"#естьработа"})
    assert is_vacancy(m)


def test_not_vacancy_by_irrelevant_tag():
    m = Message(date=None, message_id=1, author="X", text="t", tags={"#москва", "#sql"})
    assert not is_vacancy(m)


def test_filter_vacancies():
    msgs = [
        Message(date=None, message_id=1, author="A", text="t", tags={"#vacancy"}),
        Message(date=None, message_id=2, author="B", text="t", tags={"#москва"}),
        Message(date=None, message_id=3, author="C", text="t", tags={"#вакансия", "#sql"}),
    ]
    result = filter_vacancies(msgs)
    assert len(result) == 2
    assert {m.message_id for m in result} == {1, 3}


# --- message_to_csv_row ---

def test_csv_row_basic():
    m = Message(
        date="2016-09-21T13:35:02+00:00",
        message_id=12345,
        author="Алексей Иванов",
        text="Ищем аналитика",
        links=["https://hh.ru/v1", "https://t.me/c/1"],
        tags={"#vacancy", "#москва"},
    )
    row = message_to_csv_row(m, "messages42.html")
    # tags — sorted для детерминированного вывода
    assert row["date"] == "2016-09-21T13:35:02+00:00"
    assert row["message_id"] == 12345
    assert row["author"] == "Алексей Иванов"
    assert row["text"] == "Ищем аналитика"
    assert row["links"] == "https://hh.ru/v1;https://t.me/c/1"
    assert row["tags"] == "#vacancy;#москва"  # sorted alphabetically
    assert row["source_file"] == "messages42.html"


def test_csv_row_handles_none_values():
    """None-поля становятся пустыми строками (для CSV)."""
    m = Message(
        date=None, message_id=None, author=None, text="",
        links=[], tags=set(),
    )
    row = message_to_csv_row(m, "messages1.html")
    assert row["date"] == ""
    assert row["message_id"] == ""
    assert row["author"] == ""
    assert row["text"] == ""
    assert row["links"] == ""
    assert row["tags"] == ""