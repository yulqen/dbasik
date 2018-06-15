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

# FIXME - problems here. This datamaplines_for_single_datamap
# fixture is likely to be adding to the database locally but it needs to
# add to the vagrant database, because that is what selenium is using
# we should do this by loading a fixture.json file into the database first
# In Pycharm we could use a pre-test command to do it
def test_upload_datamap_form_title(selenium, clean_vagrant_db):
    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
    assert "Upload datamap" in selenium.title


def test_upload_incorrect_csv(selenium, bad_csv_file, clean_vagrant_db):
    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
    selenium.find_element_by_id("id_uploaded_file").send_keys(bad_csv_file)
    selenium.find_element_by_id("submit-id-submit").click()
    try:
        message = WebDriverWait(selenium, 3).until(
            EC.presence_of_element_located((By.ID, "message-test"))
        )
        print("Message found!")
        assert "Incorrect headers in csv file" in message.text
    except TimeoutException:
        print("No... timed out")


def test_upload_correct_csv(selenium, good_csv_file, clean_vagrant_db):
    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
    selenium.find_element_by_id("id_uploaded_file").send_keys(good_csv_file)
    selenium.find_element_by_id("submit-id-submit").click()
    redirected_h3 = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.ID, "datamap-title"))
    )
    # TODO this needs to test for the name of the datamap
    # but we haven't included that yet. So test for it...
    assert "Test Datamap 1" in redirected_h3.text


def test_upload_big_key_csv(selenium, csv_hundred_plus_key, clean_vagrant_db):
    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
    selenium.find_element_by_id("id_uploaded_file").send_keys(csv_hundred_plus_key)
    selenium.find_element_by_id("submit-id-submit").click()
    message = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located((By.ID, "message-test"))
    )
    assert "Ensure this value has at most 100 characters (it has 106)" in message.text


def test_guidance_text_for_csv_upload(selenium, clean_vagrant_db):
    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
    assert selenium.find_element_by_id("csv-field-advisory")


def test_datamap_create_form_items(selenium, clean_vagrant_db):
    selenium.get("http://localhost:8000/datamaps/create")
    assert selenium.find_element_by_id("id_name")
    assert selenium.find_element_by_id("id_tier")
    assert selenium.find_element_by_id("submit-new-dm")


def test_create_new_datamap(selenium, clean_vagrant_db):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    advisory = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located(
            (By.ID, "csv-field-advisory")
        )  # this appears on dm upload page
    )
    assert advisory


def test_list_of_current_datamaps_on_create_datamap_page(selenium, clean_vagrant_db):
    selenium.get("http://localhost:8000/datamaps/create")
    assert selenium.find_element_by_id("current-datamap-list")


def test_attempt_to_create_same_dm_name_pf_family_combo_rejected(selenium, clean_vagrant_db):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    advisory = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located(
            (By.ID, "datamap-integrity-error")
        )  # this appears on dm upload page
    )
    assert advisory


def test_add_datamapline_line_on_datamap_page(selenium, clean_vagrant_db):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    selenium.get(f"http://localhost:8000/datamaps/{str(rand_title)}")
    assert selenium.find_element_by_id("add-line-to-datamap")


def test_manually_add_datamapline(selenium, clean_vagrant_db):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    selenium.find_element_by_id("submit-new-dm").click()
    selenium.get(f"http://localhost:8000/datamaps/create-datamapline/{rand_title}")
    selenium.find_element_by_id("id_key").send_keys("This is an imitation datamapline KEY")
    selenium.find_element_by_id("id_sheet").send_keys("SHEET NAME")
    selenium.find_element_by_id("id_cell_ref").send_keys("CELL_REF")
    selenium.find_element_by_id("submit-new-dml").click()
    header = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located(
            (By.ID, "show-datamap-table")
        )  # this appears on dm upload page
    )
    assert str(rand_title) in header.text

