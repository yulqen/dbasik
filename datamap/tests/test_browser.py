import pytest


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.binary = "/opt/firefox-quantum/firefox"
    firefox_options.headless = True
    return firefox_options


def test_basic_driver(selenium):
    selenium.get("https://www.python.org")
    assert "Python" in selenium.title

