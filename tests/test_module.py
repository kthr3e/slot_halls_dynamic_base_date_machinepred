import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, timedelta
from slot_halls_dynamic_base_date_machinepred import generate_event_dates_priority, parse_posts


def test_generate_event_dates_priority_basic():
    base_date = datetime(2024, 6, 15)
    result = generate_event_dates_priority(base_date)
    assert result, "Result should not be empty"
    # check range
    assert min(result.keys()) >= base_date - timedelta(days=364)
    assert max(result.keys()) <= base_date
    # check base date rule
    assert result.get(base_date) == '日付'
    values = set(result.values())
    assert 'Xのつく日' in values
    assert '曜日' in values
    assert any(v.startswith('第') and v.endswith('曜日') for v in values)


def test_parse_posts():
    html = '''
    <div class="ichiran_post">
        <div class="ichiran_title"><a href="https://example.com/post1">Title</a></div>
        <div class="ichiran_result">平均差枚：+1,200</div>
        <div class="ichiran_result2">info1<br>info2</div>
        <div class="hall_header"><span class="hall_name"><a>Hall A</a></span></div>
    </div>
    <div class="ichiran_post">
        <div class="ichiran_title"><a href="https://example.com/post2">Title2</a></div>
        <div class="ichiran_result">平均差枚：+100</div>
        <div class="hall_header"><span class="hall_name"><a>Hall B</a></span></div>
    </div>
    '''
    records = parse_posts(html)
    assert len(records) == 1
    rec = records[0]
    assert rec['hall'] == 'Hall A'
    assert rec['url'] == 'https://example.com/post1'
    assert rec['avg_diff'] == 1200
    assert rec['details'] == ['info1', 'info2']
