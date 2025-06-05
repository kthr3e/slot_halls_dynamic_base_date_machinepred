from datetime import datetime, timedelta
from calendar import monthrange
import re
from bs4 import BeautifulSoup


def generate_event_dates_priority(base_date: datetime) -> dict:
    """Generate prioritized event dates for one year preceding base_date."""
    end = base_date
    start = end - timedelta(days=364)
    day = base_date.day
    digit = day % 10
    weekday = base_date.weekday()

    month_wdays = [d for d in range(1, monthrange(base_date.year, base_date.month)[1] + 1)
                   if datetime(base_date.year, base_date.month, d).weekday() == weekday]
    occurrence = month_wdays.index(day) + 1 if day in month_wdays else None

    prioritized = {}
    m = start.replace(day=1)
    while m <= end:
        y, mo = m.year, m.month
        dim = monthrange(y, mo)[1]
        wdays = [d for d in range(1, dim + 1)
                 if datetime(y, mo, d).weekday() == weekday]

        for d in range(1, dim + 1):
            dt = datetime(y, mo, d)
            if not (start <= dt <= end):
                continue

            if dt.day == day:
                rule = '日付'
            elif occurrence and len(wdays) >= occurrence and dt.day == wdays[occurrence - 1]:
                rule = f'第{occurrence}曜日'
            elif dt.day % 10 == digit:
                rule = 'Xのつく日'
            elif dt.weekday() == weekday:
                rule = '曜日'
            else:
                rule = None

            if rule and dt not in prioritized:
                prioritized[dt] = rule

        m = (m.replace(day=28) + timedelta(days=4)).replace(day=1)
    return prioritized


def parse_posts(html: str):
    """Parse posts HTML and return list of record dictionaries."""
    soup = BeautifulSoup(html, 'html.parser')
    records = []
    for post in soup.select('div.ichiran_post'):
        title_tag = post.select_one('div.ichiran_title a')
        url = title_tag['href'] if title_tag and title_tag.has_attr('href') else None

        result = post.select_one('div.ichiran_result')
        m = re.search(r'平均差枚：\+?([0-9,]+)', result.text) if result else None
        if not m:
            continue
        val = int(m.group(1).replace(',', ''))
        if val < 300:
            continue

        details = []
        result2 = post.select_one('div.ichiran_result2')
        if result2:
            details = [line.strip() for line in result2.get_text(separator="\n").split("\n") if line.strip()]

        hall_tag = post.select_one('div.hall_header span.hall_name a')
        hall = hall_tag.text.strip() if hall_tag else None

        records.append({
            'hall': hall,
            'url': url,
            'avg_diff': val,
            'details': details,
        })
    return records
