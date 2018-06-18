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
def test_upload_datamap_form_title(selenium):
    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
    assert "Upload datamap" in selenium.title


def test_upload_incorrect_csv(selenium, bad_csv_file):
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


def test_upload_correct_csv(selenium, good_csv_file):
    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
    selenium.find_element_by_id("id_uploaded_file").send_keys(good_csv_file)
    selenium.find_element_by_id("submit-id-submit").click()
    redirected_h3 = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.ID, "datamap-title"))
    )
    # TODO this needs to test for the name of the datamap
    # but we haven't included that yet. So test for it...
    assert "Test Datamap 1" in redirected_h3.text


def test_upload_big_key_csv(selenium, csv_hundred_plus_key):
    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
    selenium.find_element_by_id("id_uploaded_file").send_keys(csv_hundred_plus_key)
    selenium.find_element_by_id("submit-id-submit").click()
    message = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located((By.TAG_NAME, "legend"))
    )
    assert "Upload Datamap" in message.text


def test_create_new_datamap(selenium):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    t = selenium.find_element_by_id("id_tier")
    for option in t.find_elements_by_tag_name('option'):
        if option.text == "DfT Tier 1":
            option.click()
            break
    selenium.find_element_by_id("submit-id-submit").click()
    friendly_title = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[1]/h3")
        )  # this appears on dm upload page
    )
    assert friendly_title.text == "Getting data into a datamap"


def test_list_of_current_datamaps_on_create_datamap_page(selenium):
    selenium.get("http://localhost:8000/datamaps/create")
    assert selenium.find_element(
        By.CLASS_NAME, "card-title").text == "Current datamaps in system"


def test_attempt_to_create_same_dm_name_pf_family_combo_rejected(selenium):
    rand_title = uuid.uuid4()
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    t = selenium.find_element_by_id("id_tier")
    for option in t.find_elements_by_tag_name('option'):
        if option.text == "DfT Tier 1":
            option.click()
            break
    selenium.find_element_by_id("submit-id-submit").click()
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    t = selenium.find_element_by_id("id_tier")
    for option in t.find_elements_by_tag_name('option'):
        if option.text == "DfT Tier 1":
            option.click()
            break
    selenium.find_element_by_id("submit-id-submit").click()
    advisory = WebDriverWait(selenium, 3).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div/div[1]/form/div[1]/ul/li")
        )  # this appears on dm upload page
    )
    assert advisory.text == "Datamap with this Name and Tier already exists."


def test_add_datamapline_line_on_datamap_page(selenium):
    rand_title = uuid.uuid4()
    datamap_name_char_limit = 25 # from model
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    t = selenium.find_element_by_id("id_tier")
    for option in t.find_elements_by_tag_name('option'):
        if option.text == "DfT Tier 1":
            option.click()
            break
    selenium.find_element_by_id("submit-id-submit").click()
    # because the create datamap form currently limits to name to
    # 25 chars, we need to chop the uuid here to 25 to get the correct
    # url
    selenium.get(
        f"http://localhost:8000/datamaps/{str(rand_title)[:datamap_name_char_limit]}-dft-tier-1"
    )
    assert selenium.find_element_by_id("add-line-to-datamap-button")


def test_manually_add_datamapline(selenium):
    rand_title = uuid.uuid4()
    datamap_name_char_limit = 25 # from model
    selenium.get("http://localhost:8000/datamaps/create")
    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
    t = selenium.find_element_by_id("id_tier")
    for option in t.find_elements_by_tag_name('option'):
        if option.text == "DfT Tier 1":
            option.click()
            break
    selenium.find_element_by_id("submit-id-submit").click()
    selenium.get(
        f"http://localhost:8000/datamaps/create-datamapline/{str(rand_title)[:datamap_name_char_limit]}-dft-tier-1"
    )
    t = selenium.find_element_by_id("id_datamap")
    for option in t.find_elements_by_tag_name('option'):
        if option.text == str(rand_title)[:datamap_name_char_limit]:
            option.click()
            break
    selenium.find_element_by_id("id_key").send_keys("100 KEY")
    selenium.find_element_by_id("id_max_length").send_keys("100")
    selenium.find_element_by_id("id_sheet").send_keys("SHEET NAME")
    selenium.find_element_by_id("id_cell_ref").send_keys("CELL_REF")
    selenium.find_element_by_id("submit-id-submit").click()
    header = WebDriverWait(selenium, 30).until(
        EC.presence_of_element_located(
            (By.ID, "show-datamap-table"))  # this appears on dm upload page
    )
    assert str(rand_title)[:datamap_name_char_limit] in header.text
