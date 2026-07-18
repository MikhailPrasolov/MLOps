"""Парсинг одного HTML-блока сообщения Telegram.

Структура (стандартный экспорт Telegram Web):
```html
<div class="message default clearfix" id="message12345">
  <div class="pull_left userpic_wrap">...</div>
  <div class="body">
    <div class="pull_right date details" title="21.09.2016 16:35:02 UTC+03:00">16:35</div>
    <div class="from_name">Иван Петров</div>
    <div class="text">Ищем аналитика <br><br>Теги: #vacancy #естьработа <br><a href="https://hh.ru/vacancy/123">hh</a></div>
    <div class="reply_to details">...</div>  <!-- опционально -->
    <div class="reactions">...</div>          <!-- опционально -->
  </div>
</div>
```
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from bs4 import BeautifulSoup, Tag


@dataclass
class Message:
    """Одно распарсенное сообщение."""
    date: Optional[str]          # ISO 8601 UTC, e.g. "2016-09-21T13:35:02+00:00"
    message_id: Optional[int]     # int из id="message12345"
    author: Optional[str]         # from_name (для service-сообщений = None)
    text: str                     # чистый видимый текст, <br> → пробел
    links: list[str] = field(default_factory=list)
    # tags хранится как set для O(1) пересечения в is_vacancy()
    tags: set[str] = field(default_factory=set)
    is_service: bool = False     # True для service-message (смена названия и т.п.)

    def is_vacancy(self) -> bool:
        """Эвристика: сообщение — вакансия, если есть любой из этих тегов."""
        vacancy_tags = {"#vacancy", "#вакансия", "#vacancies", "#вакансиям"}
        return bool(self.tags & vacancy_tags)


def _to_utc_iso(date_str: str) -> Optional[str]:
    """Парсит "21.09.2016 16:35:02 UTC+03:00" → ISO 8601 UTC.

    >>> _to_utc_iso("21.09.2016 16:35:02 UTC+03:00")
    '2016-09-21T13:35:02+00:00'
    >>> _to_utc_iso("invalid") is None
    True
    """
    if not date_str:
        return None
    m = re.match(
        r"(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}):(\d{2}):(\d{2})\s+UTC([+-])(\d{1,2}):?(\d{2})?",
        date_str.strip(),
    )
    if not m:
        return None
    day, mon, year, hh, mm, ss, sign, off_h, off_m = m.groups()
    off_m = off_m or "00"
    offset_minutes = int(off_h) * 60 + int(off_m)
    if sign == "-":
        offset_minutes = -offset_minutes
    tz = timezone(timedelta(minutes=offset_minutes))
    try:
        local = datetime(
            int(year), int(mon), int(day),
            int(hh), int(mm), int(ss),
            tzinfo=tz,
        )
        utc = local.astimezone(timezone.utc)
        return utc.isoformat()
    except (ValueError, OverflowError):
        return None


_HASHTAG_RE = re.compile(r"#[\w_]+", re.UNICODE)


def _extract_tags(text: str) -> set[str]:
    """Извлекает хештеги из текста, lowercase, без дублей.

    Пропускает якоря типа #go_to_message12345 — это не теги, а внутриссылки.

    Возвращает set для O(1) проверок в is_vacancy(). Порядок теряется
    (множество в Python неупорядочено) — для вывода в CSV используется
    sorted().

    >>> sorted(_extract_tags("Ищем #vacancy #естьработа #москва"))
    ['#вакансия', '#москва', '#естьработа']
    """
    if not text:
        return set()
    out = set()
    for tag in _HASHTAG_RE.findall(text):
        low = tag.lower()
        if re.match(r"^#go_to_message\d+$", low):
            continue
        out.add(low)
    return out


def _clean_text(text_tag: Tag) -> tuple[str, list[str]]:
    """Превращает <div class="text"> в чистый текст + список URL.

    - <br> → пробел (двойной <br><br> → двойной пробел, как в исходнике)
    - <a href="X">видимый_текст</a> → берём href как URL, видимый текст остаётся
    - Прочие теги (b, i, code, emoji): только видимый текст

    Возвращает (text, links).
    """
    # Копируем, чтобы не мутировать DOM
    tag = BeautifulSoup(str(text_tag), "html.parser").find()
    if tag is None:
        return "", []

    links: list[str] = []
    seen_links: set[str] = set()

    # Сначала собираем ссылки из <a href="...">
    for a in tag.find_all("a"):
        href = a.get("href")
        if href and href not in seen_links:
            seen_links.add(href)
            links.append(href)

    # <br> → пробел
    for br in tag.find_all("br"):
        br.replace_with(" ")

    # Получаем текст (get_text склеит всё, что не убрали)
    text = tag.get_text(separator="", strip=False)

    # Схлопываем пробелы в одном месте, но сохраняем перенос слов
    # Стратегия: \n удаляем (мы заменили <br> на пробел), множественные пробелы → один,
    # но trim по краям
    text = re.sub(r"[ \t]+", " ", text)
    text = text.strip()

    return text, links


def _parse_message_id(div_id: str | None) -> Optional[int]:
    """'message12345' → 12345. 'message-1' (service) → -1."""
    if not div_id:
        return None
    m = re.match(r"^message-?(\d+)$", div_id)
    return int(m.group(1)) if m else None


def parse_message(html_block: str) -> Optional[Message]:
    """Парсит ОДИН `<div class="message ...">` блок (включая обёртку).

    Возвращает None если блок не является message-блоком.
    """
    soup = BeautifulSoup(html_block, "html.parser")
    msg = soup.find("div", class_=re.compile(r"^message(\s|$)"))
    if not msg:
        return None

    # service-сообщения (смена названия, конвертация supergroup) — без автора/текста
    is_service = bool(msg.get("class") and "service" in (msg.get("class") or []))

    # id
    msg_id = _parse_message_id(msg.get("id"))

    # date
    date_div = msg.find("div", class_="pull_right")
    date_title = date_div.get("title") if date_div else None
    date_iso = _to_utc_iso(date_title) if date_title else None

    # author
    from_div = msg.find("div", class_="from_name")
    author = from_div.get_text(strip=True) if from_div else None

    # text + links
    text_div = msg.find("div", class_="text")
    if text_div:
        text, links = _clean_text(text_div)
    else:
        text, links = "", []

    tags = _extract_tags(text)

    return Message(
        date=date_iso,
        message_id=msg_id,
        author=author,
        text=text,
        links=links,
        tags=tags,
        is_service=is_service,
    )


def parse_all_messages(html_text: str) -> list[Message]:
    """Парсит все `<div class="message ...">` блоки в HTML-странице.

    Возвращает только default-сообщения (с автором и текстом).
    Service-сообщения и мусор пропускаются.
    """
    soup = BeautifulSoup(html_text, "html.parser")
    out: list[Message] = []
    for div in soup.find_all("div", class_=re.compile(r"^message(\s|$)")):
        # Берём только div.message default — service и joined — отдельно
        classes = div.get("class") or []
        if "default" not in classes:
            continue
        # Используем parent, чтобы передать ВЕСЬ блок с детьми
        parsed = parse_message(str(div))
        if parsed is not None and not parsed.is_service:
            out.append(parsed)
    return out


def message_to_csv_row(m: Message, source_file: str) -> dict:
    """Превращает Message в плоский dict для pandas.to_csv.

    tags — sorted для детерминированного вывода (set → list).
    """
    return {
        "date": m.date or "",
        "message_id": m.message_id if m.message_id is not None else "",
        "author": m.author or "",
        "text": m.text,
        "links": ";".join(m.links),
        "tags": ";".join(sorted(m.tags)),
        "source_file": source_file,
    }