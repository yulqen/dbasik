import os
import uuid

from django.test import LiveServerTestCase

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

# https://stackoverflow.com/questions/26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python
from datamap.models import Datamap
from datamap.tests.fixtures import (
    csv_incorrect_headers,
    csv_correct_headers,
    csv_containing_hundred_plus_length_key,
)
from register.models import Tier


class DatamapIntegrationTests(LiveServerTestCase):
    """
    Run tests on web pages related to creating Datamap objects in the system.
    """

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        cls.driver.implicitly_wait(10)
        super().setUpClass()

    def setUp(self):
        self.url_to_uploaddatamap = (
            f"{self.live_server_url}/datamaps/uploaddatamap/test-datamap-1-dft-tier-1"
        )
        Datamap.objects.create(
            name="Test Datamap 1",
            slug="test-datamap-1",
            tier=(Tier.objects.create(name="DfT Tier 1")),
        )
        self.csv_incorrect_headers = csv_incorrect_headers()
        self.csv_correct_headers = csv_correct_headers()
        self.csv_single_long_key = csv_containing_hundred_plus_length_key()

    def tearDown(self):
        os.remove(self.csv_incorrect_headers)
        os.remove(self.csv_correct_headers)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_confirm_upload_datamap_in_title_tag(self):
        """
        Given a non-logged-in user with a desire to upload a csv file in order to create datamap
        When he goes to the page in the site where you upload a csv file
        Then he is presented with the correct page
        """
        self.driver.get(f"{self.url_to_uploaddatamap}")
        self.assertTrue("Upload datamap" in self.driver.title)

    def test_uploaded_csv_with_correct_headers_is_processed(self):
        """
        Given a non-logged-in user with a desire to upload a csv file to create a datamap,
        and a csv-file formatted correctly
        When he submits the csv using the form
        Then he is presented with a page associated with the datamap which he has uploaded data to
        """
        self.driver.get(f"{self.url_to_uploaddatamap}")
        self.driver.find_element_by_id("id_uploaded_file").send_keys(
            self.csv_correct_headers
        )
        self.driver.find_element_by_id("submit-id-submit").click()
        redirected_h3 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "datamap-title"))
        )
        self.assertTrue("Test Datamap 1" in redirected_h3.text)

    def test_uploaded_csv_with_wrong_headers_is_flagged(self):
        """
        Given a non-logged-in user with a desire to upload a csv file to create a datamap,
        and a csv-file formatted IN-correctly
        When he submits the csv using the form
        Then he is presented with a warning that this csv file needs to include the correct keys
        """
        self.driver.get(f"{self.url_to_uploaddatamap}")
        self.driver.find_element_by_id("id_uploaded_file").send_keys(
            self.csv_incorrect_headers
        )
        self.driver.find_element_by_id("submit-id-submit").click()
        message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "message-test"))
        )
        self.assertTrue("This field is required" in message.text)

    def test_upload_big_key_csv(self):
        """
        Given a non-logged-in user with a desire to upload a csv file to create a datamap,
        and a csv-file containing a key that is too long
        When he submits the csv using the form
        Then he is presented with a warning that this csv file needs to include the correct length of keys
        """
        self.driver.get(f"{self.url_to_uploaddatamap}")
        self.driver.find_element_by_id("id_uploaded_file").send_keys(
            self.csv_single_long_key
        )
        self.driver.find_element_by_id("submit-id-submit").click()
        message = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, "message-test"))
        )
        self.assertTrue("Field: key Errors: Ensure this value has at most 100 characters" in message.text)

    def test_create_new_datamap(self):
        """
        Given a non-logged-in user with a desire to create a datamap
        When he correctly submits the form to create the datamap
        Then he is presented a new page that invites him to upload a csv file
        """
        rand_title = uuid.uuid4()
        self.driver.get(f"{self.live_server_url}/datamaps/create")
        self.driver.find_element_by_id("id_name").send_keys(str(rand_title))
        t = self.driver.find_element_by_id("id_tier")
        for option in t.find_elements_by_tag_name("option"):
            if option.text == "DfT Tier 1":
                option.click()
                break
        self.driver.find_element_by_id("submit-id-submit").click()
        friendly_title = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/h3"))
        )
        self.assertTrue("Getting data into a datamap" in friendly_title.text)


#
#
# def test_list_of_current_datamaps_on_create_datamap_page(selenium):
#    selenium.get("http://localhost:8000/datamaps/create")
#    assert selenium.find_element(
#        By.CLASS_NAME, "card-title").text == "Current datamaps in system"
#
#
# def test_attempt_to_create_same_dm_name_pf_family_combo_rejected(selenium):
#    rand_title = uuid.uuid4()
#    selenium.get("http://localhost:8000/datamaps/create")
#    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
#    t = selenium.find_element_by_id("id_tier")
#    for option in t.find_elements_by_tag_name('option'):
#        if option.text == "DfT Tier 1":
#            option.click()
#            break
#    selenium.find_element_by_id("submit-id-submit").click()
#    selenium.get("http://localhost:8000/datamaps/create")
#    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
#    t = selenium.find_element_by_id("id_tier")
#    for option in t.find_elements_by_tag_name('option'):
#        if option.text == "DfT Tier 1":
#            option.click()
#            break
#    selenium.find_element_by_id("submit-id-submit").click()
#    advisory = WebDriverWait(selenium, 3).until(
#        EC.presence_of_element_located(
#            (By.XPATH, "/html/body/div/div/div/div[1]/form/div[1]/ul/li")
#        )  # this appears on dm upload page
#    )
#    assert advisory.text == "Datamap with this Name and Tier already exists."
#
#
# def test_add_datamapline_line_on_datamap_page(selenium):
#    rand_title = uuid.uuid4()
#    datamap_name_char_limit = 25 # from model
#    selenium.get("http://localhost:8000/datamaps/create")
#    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
#    t = selenium.find_element_by_id("id_tier")
#    for option in t.find_elements_by_tag_name('option'):
#        if option.text == "DfT Tier 1":
#            option.click()
#            break
#    selenium.find_element_by_id("submit-id-submit").click()
#    # because the create datamap form currently limits to name to
#    # 25 chars, we need to chop the uuid here to 25 to get the correct
#    # url
#    selenium.get(
#        f"http://localhost:8000/datamaps/{str(rand_title)[:datamap_name_char_limit]}-dft-tier-1"
#    )
#    assert selenium.find_element_by_id("add-line-to-datamap-button")
#
#
# def test_manually_add_datamapline(selenium):
#    rand_title = uuid.uuid4()
#    datamap_name_char_limit = 25 # from model
#    selenium.get("http://localhost:8000/datamaps/create")
#    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
#    t = selenium.find_element_by_id("id_tier")
#    for option in t.find_elements_by_tag_name('option'):
#        if option.text == "DfT Tier 1":
#            option.click()
#            break
#    selenium.find_element_by_id("submit-id-submit").click()
#    selenium.get(
#        f"http://localhost:8000/datamaps/create-datamapline/{str(rand_title)[:datamap_name_char_limit]}-dft-tier-1"
#    )
#    t = selenium.find_element_by_id("id_datamap")
#
#    for option in t.find_elements_by_tag_name('option'):
#        if option.text == str(rand_title)[:datamap_name_char_limit]:
#            option.click()
#            break
#    selenium.find_element_by_id("id_key").send_keys("100 KEY")
#    selenium.find_element_by_id("id_max_length").send_keys("100")
#    selenium.find_element_by_id("id_sheet").send_keys("SHEET NAME")
#
#    selenium.find_element_by_id("id_cell_ref").send_keys("CELL_REF")
#    selenium.find_element_by_id("submit-id-submit").click()
#    header = WebDriverWait(selenium, 30).until(
#        EC.presence_of_element_located(
#            (By.ID, "show-datamap-table"))  # this appears on dm upload page
#    )
#    assert str(rand_title)[:datamap_name_char_limit] in header.text
