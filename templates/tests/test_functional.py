import pytest
import os
import uuid

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.binary = "/opt/firefox-quantum/firefox"
    firefox_options.headless = True
    return firefox_options


@pytest.fixture
def mock_macro_template():
    code_dir = os.path.abspath('.')
    return os.path.join(code_dir, 'templates/tests/macro_enabled_template.xlsm')


def test_create_new_template(selenium, mock_macro_template):
    selenium.get("http://localhost:8000/templates/create")
    selenium.find_element_by_id("id_name").send_keys("TEST TEMPLATE")
    selenium.find_element_by_id("id_description").send_keys("TEST TEMPLATE DESCRIPTION")
    selenium.find_element_by_id("id_source_file").send_keys(mock_macro_template)
    selenium.find_element_by_id("submit-id-submit").click()
    try:
        WebDriverWait(selenium, 3).until(
            EC.presence_of_element_located((By.ID, "template-title"))
        )
        # we have an id of template-title, so we are on the correct page
        # iterate through them all to find out target
        #
        ts = selenium.find_elements_by_id("template-title")
        for t in ts:
            if t.text == "TEST TEMPLATE":
                assert True
                return
        assert False
    except TimeoutException as e:
        raise e.msg(f"Cannot find a template-title tag.")
