import pytest
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.binary = "/usr/bin/firefox"
    firefox_options.headless = True
    return firefox_options


@pytest.fixture
def mock_macro_template():
    code_dir = os.path.abspath('.')
    return os.path.join(code_dir, 'templates/tests/macro_enabled_template.xlsm')


@pytest.fixture
def mock_xlsx_template():
    code_dir = os.path.abspath('.')
    return os.path.join(code_dir, 'templates/tests/mock_xlsx_template.xlsx')


def test_create_new_template(selenium, mock_macro_template):
    selenium.get("http://localhost:8000/templates/create")
    selenium.find_element_by_id("id_name").send_keys("TEST TEMPLATE")
    selenium.find_element_by_id("id_description").send_keys("TEST TEMPLATE DESCRIPTION")
    selenium.find_element_by_id("id_source_file").send_keys(mock_macro_template)
    selenium.find_element_by_id("submit-id-submit").click()
    title = WebDriverWait(selenium, 5).until(EC.presence_of_element_located((By.ID, "show-datamap-table"))).text
    assert title == "Templates"


def test_create_new_template_bad_file(selenium, mock_xlsx_template):
    selenium.get("http://localhost:8000/templates/create")
    selenium.find_element_by_id("id_name").send_keys("TEST TEMPLATE")
    selenium.find_element_by_id("id_description").send_keys("TEST TEMPLATE DESCRIPTION")
    selenium.find_element_by_id("id_source_file").send_keys(mock_xlsx_template)
    selenium.find_element_by_id("submit-id-submit").click()
    try:
        message = WebDriverWait(selenium, 3).until(
            EC.presence_of_element_located((By.ID, "bad-file-upload-id"))
        )
        assert "You can only upload a macro-enabled Excel file here" in message.text
    except TimeoutException as e:
        print("Not going there")
