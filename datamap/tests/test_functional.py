import os
import tempfile

from django.test import LiveServerTestCase, TestCase
import uuid

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.webdriver import WebDriver

# https://stackoverflow.com/questions/26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python
from datamap.models import Datamap
from register.models import Tier


def bad_csv_file():
    tmpdir = tempfile.gettempdir()
    uf = os.path.join(tmpdir, "bad_datamap.csv")
    with open(uf, "w") as f:
        f.write("bad_key,bad_sheet,bad_cell_ref\n")
        f.write("First row col 1,First row col 2,A15\n")
        f.write("Second row col 1,Second row col 2,B15\n")
        f.write("Third row col 1,Third row col 2,C15\n")
        f.write("Fourth row col 1,Fourth row col 2,D15\n")
    return uf


# see https://stackoverflow.com/questions/29378328/django-liveservertestcase-fails-to-load-a-page-when-i-run-multiple-tests#29533884
# about why we are using a mixin here (comment from CoreDumpError at bottom) - without it, can only run one test in class
class DatamapIntegrationTests(LiveServerTestCase, TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tier1 = Tier.objects.create(name="DfT Tier 1")
        cls.datamap1 = Datamap.objects.create(name="Test Datamap 1", slug="test-datamap-1", tier=cls.tier1)
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(3)
        cls.bad_csv_file = bad_csv_file()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        os.remove(cls.bad_csv_file)
        super().tearDownClass()

    def test_upload_datamap_form_title(self):
        self.selenium.get(f"{self.live_server_url}/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
        self.assertTrue("Upload datamap" in self.selenium.title)

    def test_upload_incorrect_csv(self):
        self.selenium.get(f"{self.live_server_url}/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
        self.selenium.find_element_by_id("id_uploaded_file").send_keys(self.bad_csv_file)
        self.selenium.find_element_by_id("submit-id-submit").click()
        message = WebDriverWait(self.selenium, 5).until(EC.presence_of_element_located((By.ID, "message-test")))
        print("Message found!")
        self.assertTrue("This field is required" in message.text)

# def test_upload_correct_csv(selenium, good_csv_file):
#    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
#    selenium.find_element_by_id("id_uploaded_file").send_keys(good_csv_file)
#    selenium.find_element_by_id("submit-id-submit").click()
#    redirected_h3 = WebDriverWait(selenium, 10).until(
#        EC.presence_of_element_located((By.ID, "datamap-title"))
#    )
#    assert "Test Datamap 1" in redirected_h3.text
#
#
# def test_upload_big_key_csv(selenium, csv_hundred_plus_key):
#    selenium.get("http://localhost:8000/datamaps/uploaddatamap/test-datamap-1-dft-tier-1")
#    selenium.find_element_by_id("id_uploaded_file").send_keys(csv_hundred_plus_key)
#    selenium.find_element_by_id("submit-id-submit").click()
#    message = WebDriverWait(selenium, 3).until(
#        EC.presence_of_element_located((By.TAG_NAME, "legend"))
#    )
#    assert "Upload Datamap" in message.text
#
#
# def test_create_new_datamap(selenium):
#    rand_title = uuid.uuid4()
#    selenium.get("http://localhost:8000/datamaps/create")
#    selenium.find_element_by_id("id_name").send_keys(str(rand_title))
#    t = selenium.find_element_by_id("id_tier")
#    for option in t.find_elements_by_tag_name('option'):
#        if option.text == "DfT Tier 1":
#            option.click()
#            break
#    selenium.find_element_by_id("submit-id-submit").click()
#    friendly_title = WebDriverWait(selenium, 3).until(
#        EC.presence_of_element_located(
#            (By.XPATH, "/html/body/div/div/div[1]/h3")
#        )  # this appears on dm upload page
#    )
#    assert friendly_title.text == "Getting data into a datamap"
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
