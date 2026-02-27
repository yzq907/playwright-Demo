# tests/test_example.py
import re
from playwright.sync_api import expect

def test_homepage_title(page):
    page.goto("https://www.baidu.com")
    expect(page).to_have_title(re.compile("百度一下"))