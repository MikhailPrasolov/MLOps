# Глава 9. Получение данных

**Книга:** «Data Science с нуля» — Джоэл Грасс (2-е изд., 2019)
**Файл кода:** `scratch/getting_data.py`

> **Контекст:** глава-практикум по «добыче» данных: текстовые файлы, CSV (включая «грязные» варианты с `,` внутри), HTML через BeautifulSoup, JSON через REST API и стриминг Twitter. Главный месседж — 80% работы дата-сайентиста это **сбор и очистка**, а не моделирование.

## Ключевые концепции

- **`open(path, 'r'/'w')` + `csv.reader`/`csv.DictReader`** — стандартный путь для табличных данных
- **BeautifulSoup** — парсинг HTML: `soup.find('p')`, `soup('p', {'class': 'important'})`, `soup.p.text`
- **Regex** — фильтрация URL/email: `r"^https?://.*\.house\.gov/?$"`
- **REST API** — `requests.get(url).text` → `json.loads()` → `Counter` по полям
- **Streaming (Twitter API)** — `TwythonStreamer` с callback'ами `on_success`/`on_error`
- **Don't roll your own CSV** — никогда не собирайте строки через `",".join(...)`, используйте `csv.writer`

## Код

```python
import csv, json, re
import requests
from bs4 import BeautifulSoup
from collections import Counter

# 1. CSV с произвольным разделителем
with open('stocks.txt') as f:
    reader = csv.DictReader(f, delimiter=':')   # заголовок date:symbol:price
    for row in reader:
        process(row["date"], row["symbol"], float(row["closing_price"]))

# 2. Парсинг HTML
html = requests.get(url).text
soup = BeautifulSoup(html, 'html5lib')
paragraphs_with_ids = [p for p in soup('p') if p.get('id')]
important = soup('p', {'class': 'important'})

# 3. JSON из REST API
repos = json.loads(requests.get("https://api.github.com/users/joelgrus/repos").text)
dates = [parse(repo["created_at"]) for repo in repos]
month_counts = Counter(d.month for d in dates)

# 4. Email-домены
def get_domain(email):
    return email.lower().split("@")[-1]
domain_counts = Counter(get_domain(line.strip())
                        for line in open('email_addresses.txt')
                        if "@" in line)
```

## Связанные главы

- [[ch08-summary]] — предыдущая
- [[ch10-summary]] — следующая (что делать с собранным)
- [[ch22-summary]] — HTML часто содержит граф ссылок
- [[ch24-summary]] — базы данных как альтернатива файлам

## Краткие выводы

1. **`csv.writer` / `csv.DictReader`** — единственный правильный способ работы с CSV
2. **`BeautifulSoup` + `re`** — стандартная связка для скрапинга
3. **`requests.get().text → json.loads()`** — универсальный паттерн REST API

## Где пригодится

| Концепция | Применение |
|-----------|-----------|
| `csv.DictReader` | Чтение выгрузок из банков, ERP, аналитики |
| `BeautifulSoup` | Скрапинг маркетплейсов, вакансий, новостей |
| `requests + json` | Интеграция с любым REST API (GitHub, Slack, etc.) |
| `Counter` по полям | Подсчёт частот меток, доменов, тегов |
| Streaming API | Реал-тайм аналитика Twitter/Telegram/IoT |
