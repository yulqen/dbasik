import pytest
import uuid

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# https://stackoverflow.com/questions/26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.binary = "/opt/firefox-quantum/firefox"
    firefox_options.headless = True
    return firefox_options


def test_upload_datamap_form_title(selenium):
    selenium.get("http://localhost:8000/uploaddatamap")
    assert "Upload datamap" in selenium.title


def test_upload_datamap_form_items(selenium):
    selenium.get("http://localhost:8000/uploaddatamap")
    assert "Upload datamap" in selenium.title
    assert selenium.find_element_by_id("form-table")
    assert selenium.find_element_by_id("id_target_datamap")
    assert selenium.find_element_by_id("id_uploaded_file")
    assert selenium.find_element_by_id("id_replace_all_entries")
    assert selenium.find_element_by_id("upload-button")


def test_upload_incorrect_csv(selenium, bad_csv_file):
    selenium.get("http://localhost:8000/uploaddatamap")
    selenium.find_element_by_id("id_uploaded_file").send_keys(bad_csv_file)
    selenium.find_element_by_id("upload-button").click()
    try:
        message = WebDriverWait(selenium, 3).until(
            EC.presence_of_element_located((By.ID, "message-test"))
        )
        print("Message found!")
        assert "Incorrect headers in csv file" in message.text
    except TimeoutException:
        print("No... timed out")


def test_upload_correct_csv(selenium, good_csv_file):
    selenium.get("http://localhost:8000/uploaddatamap")
    selenium.find_element_by_id("id_uploaded_file").send_keys(good_csv_file)
    selenium.find_element_by_id("upload-button").click()
    redirected_datamap_page = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.ID, "show-datamap-table"))
    )
    # TODO this needs to test for the name of the datamap
    # but we haven't included that yet. So test for it...
    assert "Datamap:" in redirected_datamap_page.text


def test_upload_big_key_csv(selenium, csv_hundred_plus_key):
    selenium.get("http://localhost:8000/uploaddatamap")
    selenium.find_element_by_id("id_uploaded_file").send_keys(csv_hundred_plus_key)
    selenium.find_element_by_id("upload-button").click()
    message = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located((By.ID, "message-test"))
    )
    assert "Ensure this value has at most 100 characters (it has 106)" in message.text


def test_guidance_text_for_csv_upload(selenium):
    selenium.get("http://localhost:8000/uploaddatamap")
    assert selenium.find_element_by_id("csv-field-advisory")


def test_datamap_create_form_items(selenium):
    selenium.get("http://localhost:8000/createdatamap")
    assert selenium.find_element_by_id("id_name")
    assert selenium.find_element_by_id("id_tier")
    assert selenium.find_element_by_id("submit-new-dm")


def test_create_new_datamap(selenium):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/createdatamap")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    advisory = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located(
            (By.ID, "csv-field-advisory")
        )  # this appears on dm upload page
    )
    assert advisory


def test_list_of_current_datamaps_on_create_datamap_page(selenium):
    selenium.get("http://localhost:8000/createdatamap")
    assert selenium.find_element_by_id("current-datamap-list")


def test_attempt_to_create_same_dm_name_pf_family_combo_rejected(selenium):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/createdatamap")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    selenium.get("http://localhost:8000/createdatamap")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    advisory = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located(
            (By.ID, "datamap-integrity-error")
        )  # this appears on dm upload page
    )
    assert advisory


def test_add_datamapline_line_on_datamap_page(selenium):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/createdatamap")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    selenium.get(f"http://localhost:8000/datamap/{str(rand_title)}")
    assert selenium.find_element_by_id("add-line-to-datamap")
