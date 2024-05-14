import os
import time
import datetime as dt
import logging
import shutil
from tempfile import mkdtemp
import pandas as pd
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotVisibleException,
    StaleElementReferenceException
)
from ducttape.webui_datasource import WebUIDataSource
from ducttape.exceptions import ReportNotFound, ReportNotReady, RequestError
from ducttape.utils import (
    get_most_recent_file_in_dir,
    DriverBuilder,
    LoggingMixin
)
from .calpads_config import EXTRACT_COLUMNS

class Calpads(WebUIDataSource, LoggingMixin):
    """Class for interacting with the web ui of CALPADS"""

    def __init__(self, username, password, wait_time, hostname, temp_folder_path, headless=False):
        super().__init__(username, password, wait_time, hostname, temp_folder_path, headless)
        self.uri_scheme = 'https://'
        self.base_url = self.uri_scheme + self.hostname
        stream_hdlr = logging.StreamHandler()
        log_fmt = '%(asctime)s CALPADS: %(message)s'
        stream_hdlr.setFormatter(logging.Formatter(fmt=log_fmt))
        self.log.addHandler(stream_hdlr)
        self.log.setLevel(logging.INFO)

    def _login(self):
        """Logs into CALPADS"""
        self.driver.get(self.base_url)
        try:
            WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary')))
        except TimeoutException:
            self.log.info("Was unable to reach the login page. Check the browser: {}".format(self.driver.title))
            raise RequestError("Unable to reach login page. CALPADS might be down.")
        except NoSuchElementException:
            self.log.info("Was unable to reach the login page. Check the browser: {}".format(self.driver.title))
            raise RequestError("Unable to reach login page. CALPADS might be down.")
        user = self.driver.find_element(By.ID, "Username")
        user.send_keys(self.username)
        pw = self.driver.find_element(By.ID, "Password")
        pw.send_keys(self.password)
        agreement = self.driver.find_element(By.ID, "AgreementConfirmed")
        self.driver.execute_script("arguments[0].click();", agreement)
        btn = self.driver.find_element(By.CLASS_NAME, 'btn-primary') 
        btn.click()
        try:
            WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.ID, 'org-select')))
        except TimeoutException:
            self.log.info('Something went wrong with the login. Checking to see if there was an expected error message.')
            try:
                #TODO: Use id, tag-name, or class for the alert if I remember the next time it happens
                alert = WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/form/div[1]')))
                if 'alert' in alert.get_attribute('class'):
                    self.log.info("Found an expected alert during login: '{}'".format(self.driver.find_element(By.XPATH, '/html/body/div[3]/div/form/div[1]/div/ul/li').text))
                    raise RequestError("Found an expected error during login")
                else:
                    self.log.info('There was an unexpected message during login. See driver.')
                    raise RequestError("Found an unexpected error during login. See driver.")
            except TimeoutException:
                self.log.info('There was an unexpected error during login. See driver.')
                raise RequestError("Found an unexpected error during login. See driver.")

        return True

    def download_url_report(self, report_url, temp_folder_name):
        """CALPADS does not have stateful reports"""
        raise NotImplementedError("CALPADS does not have stateful reports.")

    def _select_lea(self, lea_code):
         """
         Factored out common process for switching to a different LEA in the dropdown
         
         Args:
         lea_code (str): string of the seven digit number found next to your LEA name in the org select menu. For most LEAs,
         this is the CD part of the County-District-School (CDS) code. For independently reporting charters, it's the S.
         """
         select = Select(self.driver.find_element(By.ID, 'org-select'))
         for opt in select.options:
             if lea_code in opt.text:
                 opt.click()
                 break
         #Wait for site to re-load if it registered a change in LEA
         WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.ID, 'org-select')))

    def _rename_a_calpads_download(self, folder_path, new_file_text):
        """Gets most recent file in the object's calpads folder and renames it with new_file_text with timestamp appended"""

        recent_file = get_most_recent_file_in_dir(folder_path)
        file_ext = os.path.splitext(recent_file)[1]
        new_file = folder_path + "/" + str(new_file_text) + " " + str(dt.datetime.now().strftime('%Y-%m-%d %H_%M_%S')) + file_ext
        os.rename(recent_file, new_file)

    def get_current_language_data(self, ssid, second_chance=False):
        """
        Search for SSID's latest language data and return the table as a dataframe.

        Get the current language data in CALPADS for the provided SSID. Helpful when
        updating the student information system when receiving a new student.
        Returns a dataframe. When using in a Jupyter notebook, use display() instead of
        print() for checking the language data values in a prettier format.

        Args:
            ssid: CALPADS state student identifier. Can be either a string or integer format.
            second_chance: used during recursion to try again if the wrong table is found.

        Returns:
            language_data (DataFrame): The SELA language information on a CALPADS student profile or raise ReportNotFound exception if it fails
        """
        self.driver = DriverBuilder().get_driver(headless=self.headless)
        self._login()

        ssid_search = self.driver.find_element(By.ID, 'inputSSID')
        ssid_search.send_keys(ssid)

        ssid_btn = self.driver.find_element(By.ID, 'btnSearchSSIDLeftNav')
        ssid_btn.click()
        #Wait for SELA Grid to be clickable
        elem = WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="StudentDetailsPanelBar"]/li[4]/a')))
        elem.click() #open up the SELA Grid
        try:
            WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.ID, 'SELAGrid')))
        except TimeoutException:
            #Maybe the click didn't work the first time, try clicking again
            self.driver.find_element(By.XPATH, '//*[@id="StudentDetailsPanelBar"]/li[4]/a').click()
            WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.ID, 'SELAGrid')))
        
        try:
            WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SELAGrid"]/table/tbody'))) #waiting for the table to load
        except TimeoutException:
            #If the table body is never in the DOM, but the table header exists, it could just mean the SSID doesn't have data.
            if self.driver.find_element(By.XPATH, '//*[@id="SELAGrid"]/table'): #If the header of the table exists...
                lang_data = pd.read_html(self.driver.page_source)[1]
                try:
                    assert all(lang_data.columns == ['Unnamed: 0', 'Reporting LEA', 'Acquisition Code', 'Status Date', 'Primary Language Code',
                                            'Correction Reason Code','Effective Start Date'])
                except AssertionError:
                    self.log.info('Found a table, but it was the wrong one it seems. Trying again')
                    self.get_current_language_data(ssid, True)
                except ValueError: #the assert comparison fails if the array lengths aren't the same
                    self.log.info('Found a table, but it was the wrong one it seems. Trying again')
                    self.get_current_language_data(ssid, True)
                else:
                    #Passed the validations/checks, return the dataframe
                    self.log.info("Student {} does not appear to have any language data. Once confirmed, student should get tested.".format(ssid))
                    self.driver.quit()
                    return lang_data
            else:
                self.log.info('Something unexpected happened when trying to load the SELA table for {}'.format(ssid))
                self.driver.quit() #TODO: Should the driver always close at this point?
                raise ReportNotFound #TODO: A more explicit/accurate error might be helpful
        
        #If the table body *is* found in the DOM, do the following:
        lang_data = pd.read_html(self.driver.page_source)[1] #TODO: Index error happened? Might be going too fast?
        if not second_chance:
            try:
                assert all(lang_data.columns == ['Unnamed: 0', 'Reporting LEA', 'Acquisition Code', 'Status Date', 'Primary Language Code',
                                            'Correction Reason Code','Effective Start Date'])
            except AssertionError:
                self.log.info('Found a table, but it was the wrong one it seems. Trying again')
                self.get_current_language_data(ssid, True)
            except ValueError: #the assert comparison fails if the array lengths aren't the same
                self.log.info('Found a table, but it was the wrong one it seems. Trying again')
                self.get_current_language_data(ssid, True)
            else:
                if len(lang_data) != 0:
                    self.log.info(
                        'Found the latest language data for {}: Status: {}, Status Date: {}, Primary Lang: {}.'.format(
                            ssid, lang_data['Acquisition Code'][0], lang_data['Status Date'][0], lang_data['Primary Language Code'][0]
                            )
                        )
                    self.driver.quit()
                    return lang_data
                else:
                    self.log.info('Student {} does not appear to have any language data. Once confirmed, student should get tested.'.format(ssid))
                self.driver.quit()
                return lang_data
        else: #Sometimes the wrong tab is clicked and the wrong table is indexed at 1. #TODO: Add a max_attempts to get it right feature - this issue seems dependent on loading issues
            try:
                assert all(lang_data.columns == ['Unnamed: 0', 'Reporting LEA', 'Acquisition Code', 'Status Date', 'Primary Language Code',
                                            'Correction Reason Code','Effective Start Date'])
            except AssertionError:
                self.log.info('Found the wrong table again. Closing the driver.')
                self.driver.quit()
                raise ReportNotFound #TODO: A more explicit/accurate error might be helpful
            else:
                if len(lang_data) != 0:
                    self.log.info(
                        'Found the latest language data for {}: Status: {}, Status Date: {}, Primary Lang: {}.'.format(
                            ssid, lang_data['Acquisition Code'][0], lang_data['Status Date'][0], lang_data['Primary Language Code'][0]
                            )
                        )
                    self.driver.quit()
                    return lang_data
                else:
                    self.log.info('Student {} does not appear to have any language data. Once confirmed, student should get tested.'.format(ssid))
                self.driver.quit()
                return lang_data
    
    def request_extract(self, lea_code, extract_name, by_date_range=False, start_date=None, end_date=None,
                        active_students=False, academic_year=None, adjusted_enroll=False,
                        active_staff=True, employment_start_date=None, employment_end_date=None, effective_start_date=None,
                        effective_end_date=None):
        """
        Request an extract with the extract_name from CALPADS.
        
        For Direct Certification Extract, pass in extract_name='DirectCertification'. For SSID Request Extract, pass in 'SSID'.
        For the others, use their abbreviated acronym, e.g. SENR, SELA, etc.
        
        Args:
            lea_code (str): string of the seven digit number found next to your LEA name in the org select menu. For most LEAs,
                this is the CD part of the County-District-School (CDS) code. For independently reporting charters, it's the S.
            extract_name (str): generally the four letter acronym of the extract. e.g. SENR, SELA, etc.
                For Direct Certification Extract, pass in extract_name='DirectCertification'. 
                For SSID Request Extract, pass in 'SSID'.
                Spelling matters, capitalization does not. Raises ReportNotFound if report name is unrecognized/not supported.
            by_date_range (bool, optional): some extracts can be requested with a date range parameter. Set to True to use date range.
                If True, start_date and end_date are required.
            start_date (str, optional): when by_date_range is set to True, this is used as the start date parameter. Format: MM/DD/YYYY.
            end_date (str, optional): when by_date_range is set to True, this is used as the end date parameter. Format: MM/DD/YYYY.
            active_students (bool, optional): When requesting SPRG, True checks off Active Student in the form. 
                When True, extract pulls only student programs with a NULL exit date for the program at the time of the request.
                Defaults to False.
            academic_year (str, optional): String in the format YYYY-YYZZ. E.g. 2019-2020. Required only for some extracts.
            adjusted_enroll (bool, optional): Adjusted cumulative enrollment for CENR extract. 
                When True, pulls students with enrollments dates that fall in the typical school year.
                When False, it pulls students with enrollments from July to June (7/1/YYYY - 6/30/YYZZ). 
                Defaults to False.
            active_staff (bool, optional): For SDEM - only extract SDEM records of active staff. Default to True. If False, must provide employment
                date range.
            employment_start_date (str, optional): For SDEM - used to filter Staff members from the extract. Format: MM/DD/YYYY.
            employment_end_date (str, optional): For SDEM - used to filter Staff members from the extract. Format: MM/DD/YYYY.
            effective_start_date (str, optional): For SDEM, the effective start date of the SDEM record - used to filter Staff members from
                the extract. Format: MM/DD/YYYY.
            effective_end_date (str, optional): For SDEM, the effective end date of the SDEM record - used to filter Staff members from
                the extract. Format: MM/DD/YYYY.

        Returns:
            boolean: True if extract request was successful, False if it was not successful.
        """
        #already changed to appropriate LEA
        extract_name = extract_name.upper()
        academic_year_only_extracts = ['CRSC', 'CRSE', 'SASS', 'SCSC', 'STAS',
                                        'SCTE', 'SCSE', 'SDIS']

        #Some validations of required Args
        if extract_name in academic_year_only_extracts or (extract_name == 'CENR' and not by_date_range):
            assert academic_year, "For {} Extract, academic_year is required. Format YYYY-YYYY".format(extract_name)
        if by_date_range and extract_name != 'SDEM' and extract_name not in academic_year_only_extracts:
            assert start_date and end_date, "If by_date_range is True, start_date and end_date are required."
        if not active_staff and extract_name == 'SDEM':
            assert employment_start_date and employment_end_date, "If not using active staff, employment start date and end date are required."

        #set up driver
        self.driver = DriverBuilder().get_driver(headless=self.headless)
        self._login()
        self._select_lea(lea_code)

        #navigate to extract page
        if extract_name == 'SSID':
            self.driver.get('https://www.calpads.org/Extract/SSIDExtract')
        elif extract_name == 'DIRECTCERTIFICATION':
            self.driver.get('https://www.calpads.org/Extract/DirectCertificationExtract')
        else:
            self.driver.get('https://www.calpads.org/Extract/ODSExtract?RecordType={}'.format(extract_name))
        
        #confirm that we made it to a valid request extract page
        try:
            #Check that we made it to a page with a "Request File" button
            if extract_name != 'SPRG':
                WebDriverWait(self.driver, self.wait_time).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'btn-primary'), 'Request File'))
            else:
                #Currently, SPRG page has a btn-secondary class. Could change later and break the code. ¯\_(ツ)_/¯ 
                WebDriverWait(self.driver, self.wait_time).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'btn-secondary'), 'Request File'))
        except TimeoutException:
            self.log.info("The requested extract, {}, is not a supported extract name.".format(extract_name))
            self.driver.quit()
            raise ReportNotFound
        
        #Select the schools (generally move all) TODO: Consider supporting selective school selection
        if by_date_range and extract_name not in  ['SDEM', 'DIRECTCERTIFICATION'] and extract_name not in academic_year_only_extracts:
            self.driver.find_element(By.XPATH, "//*[contains(text(), 'Date Range')]").click()
        
        if extract_name == 'DIRECTCERTIFICATION':
            self.__move_all_for_extract_request(extract_name, academic_year_only_extracts, by_date_range=False)
        elif extract_name != 'SDEM':
            self.__move_all_for_extract_request(extract_name, academic_year_only_extracts, by_date_range=by_date_range)


        #Need specific method handlers for the extracts. Dispatch to form handlers
        form_handlers = {
            'SSID': lambda: self.__fill_ssid_request_extract(lea_code, academic_year_only_extracts,
                                                            by_date_range, start_date, end_date),
            'DIRECTCERTIFICATION': lambda: self.__fill_dc_request_extract(),
            'SENR': lambda: self.__fill_senr_request_extract(by_date_range,start_date,end_date),
            'SELA': lambda: self.__fill_sela_request_extract(by_date_range, start_date, end_date),
            'SPRG': lambda: self.__fill_sprg_request_extract(active_students, by_date_range, start_date, end_date),
            'CENR': lambda: self.__fill_cenr_request_extract(academic_year, adjusted_enroll, by_date_range,
                                                            start_date, end_date),
            'SINF': lambda: self.__fill_sinf_request_extract(by_date_range, start_date, end_date),
            'CRSC': lambda: self.__fill_crsc_request_extract(academic_year),
            'CRSE': lambda: self.__fill_crse_request_extract(academic_year),
            'SASS': lambda: self.__fill_sass_request_extract(academic_year),
            'SDEM': lambda: self.__fill_sdem_request_extract(active_staff, employment_start_date, employment_end_date,
                                                            effective_start_date, effective_end_date),
            'STAS': lambda: self.__fill_stas_request_extract(academic_year),
            'SCTE': lambda: self.__fill_scte_request_extract(academic_year),
            'SCSC': lambda: self.__fill_scsc_request_extract(academic_year),
            'SCSE': lambda: self.__fill_scse_request_extract(academic_year),
            'SDIS': lambda: self.__fill_sdis_request_extract(academic_year),
            'SPED': lambda: self.__fill_sped_request_extract(by_date_range, start_date, end_date),
            'SSRV': lambda: self.__fill_ssrv_request_extract(by_date_range, start_date, end_date)
        }
        #Call the handler
        form_handlers[extract_name]()

        #Click request button
        reqs = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Request File')]")
        for r in reqs:
            #Some pages have multiple Request File buttons in the DOM depending on the options and permissions of the user
            if r.is_displayed():
                req = r
        req.click()
        try:
            WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, 'alert-success')))
        except TimeoutException:
            self.log.info("The extract request was unsuccessful.")
            self.driver.quit()
            return False
        
        self.log.info("{} {} Extract Request made successfully. Please check back later for download".format(lea_code, extract_name))
        self.driver.get("https://www.calpads.org")
        self.driver.quit()

        return True

    def __move_all_for_extract_request(self, extract_name, year_only_list, by_date_range=False):
        """Refactored method to click move all in request extract forms"""
        #Defaults to the first moveall button which is generally what we want. TODO: Consider supporting other extract request methods. e.g. date range, etc.
        time.sleep(2) #TODO: Don't think there's something explicit to wait for here, the execution seems to be going too fast causes errors on SCSC
        if by_date_range and extract_name not in year_only_list:
            select_xpath = "//div[contains(@id, 'DateRange')]//select[@id='bootstrap-duallistbox-nonselected-list_School']"
        else:
            select_xpath = "//*[@id='bootstrap-duallistbox-nonselected-list_School']"
        select = Select(self.driver.find_element(By.XPATH, select_xpath)) #TODO: GENERALIZE FOR ALL EXTRACTS
        static_options = len(select.options)
        n = 0
        #Going to click moveall multiple times, but I think the time.sleep() above actually solves the need for this.
        while n < static_options:
            if by_date_range and extract_name not in year_only_list: #For when you are using DateRange #TODO: Confirm behavior for all extracts.
                moveall = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'DateRange')]//button[contains(@title, 'Move all')]")[-1]
                moveall.click()
            else: 
                moveall = self.driver.find_elements(By.CLASS_NAME, 'moveall')[0]
                moveall.click()
            n += 1
        assert Select(self.driver.find_element(By.XPATH, select_xpath)).options.__len__() == 0, "Failed to select all of the school options"
        #TODO: Confirm that we don't need to wait for anything here.

    def _fill_typical_date_range_form(self, start_date, end_date, extract_name=None):
        """Fills in the typical date range form"""
        if not extract_name:
            start_date_xpath = "//div[contains(@id, 'DateRange')]//input[contains(@id, 'StartDate')]"
            end_date_xpath = "//div[contains(@id, 'DateRange')]//input[contains(@id, 'EndDate')]"
        elif extract_name in ['SPED', 'SSRV']:
            start_date_xpath = "//div[contains(@id,'NonSelpa')]//input[contains(@id, 'StartDate')]"
            end_date_xpath = "//div[contains(@id,'NonSelpa')]//input[contains(@id, 'EndDate')]"
        try:
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, start_date_xpath)))
        except TimeoutException:
            self.log.info("The extract request was unsuccessful.")
            self.driver.quit()
            return False
        self.driver.find_element(By.XPATH, start_date_xpath).send_keys(start_date)
        self.driver.find_element(By.XPATH, end_date_xpath).send_keys(end_date)

    def __fill_ssid_request_extract(self, lea_code, year_only_list, by_date_range, start_date, end_date):
        """Messiest extract request handler. Assumes that a recent SENR file has been fully Posted for the SSID extract to be current."""
        #We're going back to FileSubmission because we need the job ID for the latest file upload.
        self.driver.get('https://www.calpads.org/FileSubmission')
        try:
            WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="FileSubmissionSearchResults"]/table')))
            jid = self.driver.find_element(By.XPATH, '//*[@id="FileSubmissionSearchResults"]/table/tbody/tr[1]/td[2]').text            
        except NoSuchElementException:
            self.driver.get('https://www.calpads.org/FileSubmission/')
            self.driver.refresh()
            WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="FileSubmissionSearchResults"]/table')))
        finally:
            jid = self.driver.find_element(By.XPATH, '//*[@id="FileSubmissionSearchResults"]/table/tbody/tr[1]/td[2]').text
        #make sure the first row is what is expected
        assert self.driver.find_element(By.XPATH, '//*[@id="FileSubmissionSearchResults"]/table/tbody/tr[1]/td[6]').text == 'SSID-Enrollment',  "Found a job ID, but it doesn't look like it's for an SSID extract."

        #navigate to extract page
        self.driver.get('https://www.calpads.org/Extract/SSIDExtract')

        if not by_date_range:
            jobid_option_xpath = '//*[@id="SelectedJobIDssidExtractbyJob"]/option'
            select_id = 'SelectedJobIDssidExtractbyJob'
            grade_level_xpath = '//*[@id="GradeLevel"]'
        else:
            self.driver.find_element(By.XPATH, "//*[contains(text(), 'Date Range')]").click()
            jobid_option_xpath = '//*[@id="SelectedJobIDssidExtractbyDate"]/option'
            select_id = 'SelectedJobIDssidExtractbyDate'
            grade_level_xpath = '//div[@id="DateRange"]//select[@id="GradeLevel"]'
            self._fill_typical_date_range_form(start_date, end_date)

        try:
            #TODO: More dynamic jobid selection? Or always assume the latest upload/import?
            jobid_option = WebDriverWait(self.driver, self.wait_time).until(EC.element_located_selection_state_to_be((By.XPATH,jobid_option_xpath), True))
        except TimeoutException:
            self.log.info('Job ID failed to automatically populate for SSID Extract for {}. Did you post the file you uploaded yet?'.format(lea_code))
            raise ReportNotReady
        else:
            WebDriverWait(self.driver, self.wait_time).until(EC.element_located_selection_state_to_be((By.XPATH,jobid_option_xpath), True))
            select = Select(self.driver.find_element(By.ID, select_id))
            #Find the element that's been pre-selected
        for opt in select.all_selected_options: #TODO: this returned stale element once for some reason...
            self.driver.execute_script("arguments[0].removeAttribute('selected')", opt)
            #TODO: Confirm if this needs a wait, sometimes throws errors here            
        for opt in select.options:
            if opt.get_attribute('value') == jid:
                self.driver.execute_script("arguments[0].setAttribute('selected', 'selected')", opt)
            else:
                continue
        
        self.__move_all_for_extract_request('SSID', year_only_list, by_date_range)
        #Defaulting to all grades TODO: Maybe support specific grades? Doubt it'd be useful.
        all_grades = Select(self.driver.find_element(By.XPATH, grade_level_xpath))
        all_grades.select_by_visible_text('All')
        
    def __fill_sprg_request_extract(self, active_students, by_date_range, start_date, end_date):
        """Handler for SPRG Extract Request form. Mostly just for selecting all programs in the required field.
        Args:
        active_students (bool): when True, extract only pulls students without an exit date in the program. i.e. have NULL exit dates.
        """
        #Check off Active Students
        if not by_date_range:
            if active_students:
                elem = self.driver.find_element(By.ID, 'ActiveStudentsprgAcdmcYear')
                elem.click()
                #TODO: Confirm no need to wait
            
            select = Select(self.driver.find_element(By.ID, 'EducationProgramCodesprgAcdmcYear'))
        else:
            try:
                WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.ID, 'EnrollmentStartDate')))
            except TimeoutException:
                self.log.info("The extract request was unsuccessful.")
                self.driver.quit()
                return False
            
            if active_students:
                elem = self.driver.find_element(By.ID, 'ActiveStudentsprgDateRange')
                elem.click()
                #TODO: Confirm no need to wait
            
            self.driver.find_element(By.ID, "EnrollmentStartDate").send_keys(start_date)
            self.driver.find_element(By.ID, "EnrollmentEndDate").send_keys(end_date)
            
            select = Select(self.driver.find_element(By.ID, 'EducationProgramCodesprgDateRange'))

        #Select programs - defaulting to All TODO: Support specific programs.
        select.select_by_value("All")
        #TODO: Confirm no need to wait

    def __fill_dc_request_extract(self):
        """Handler for Direct Certification Extract request form. Currently only supports default values at loading."""
        pass
    
    def __fill_sinf_request_extract(self, by_date_range, start_date, end_date):
        """Handler for SINF Extract request form. Currently only supports default values at loading."""
        if by_date_range:
            self._fill_typical_date_range_form(start_date, end_date)
    
    def __fill_sela_request_extract(self, by_date_range, start_date, end_date):
        """Handler for SELA Extract request form. Currently only supports default values at loading."""
        if by_date_range:
            self._fill_typical_date_range_form(start_date, end_date)
    
    def __fill_senr_request_extract(self, by_date_range,start_date,end_date):
        """Handler for SENR Extract request form. Currently only supports default values at loading."""
        if by_date_range:
            self._fill_typical_date_range_form(start_date, end_date)

    def __fill_crsc_request_extract(self, academic_year):
        """Handler for CRSC Extract request form."""
        if academic_year:
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)
    
    def __fill_crse_request_extract(self, academic_year):
        """Handler for CRSE Extract request form."""
        if academic_year:
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)
    
    def __fill_sass_request_extract(self, academic_year):
        """Handler for SASS Extract request form."""
        if academic_year:
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)
    
    def __fill_stas_request_extract(self, academic_year):
        """Handler for STAS Extract request form."""
        if academic_year:
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)
    
    def __fill_scte_request_extract(self, academic_year):
        """Handler for SCTE Extract request form."""
        if academic_year:
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)
    
    def __fill_scsc_request_extract(self, academic_year):
        """Handler for SCSC Extract request form."""
        if academic_year:
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)

    def __fill_scse_request_extract(self, academic_year):
        """Handler for SCSE Extract request form."""
        if academic_year:
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)
    
    def __fill_sdis_request_extract(self, academic_year):
        """Handler for SDIS Extract request form."""
        if academic_year:
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)
    
    def __fill_sdem_request_extract(self, active_staff, employment_start_date, employment_end_date, effective_start_date, effective_end_date):
        """Handler for SDEM Extract request form."""
        if active_staff:
            self.driver.find_element(By.ID, 'ActiveStaff').click()
        else:
            #Must provide employment date range if not selecting active staff
            assert (employment_start_date is not None) and (employment_end_date is not None), "If active_staff is not True, employment start and end date must be provided."
        if employment_start_date:
            self.driver.find_element(By.ID, 'EmploymentStartDate').send_keys(employment_start_date)
        if employment_end_date:
            self.driver.find_element(By.ID, 'EmploymentEndDate').send_keys(employment_end_date)
        if effective_start_date:
            self.driver.find_element(By.ID, 'EffectiveStartDate').send_keys(effective_start_date)
        if effective_end_date:
            self.driver.find_element(By.ID, 'EffectiveEndDate').send_keys(effective_end_date)

    def __fill_cenr_request_extract(self, academic_year, adjusted_enroll, by_date_range, start_date, end_date):
        """Handler for CENR Extract request form.
        Args:
            adjusted_enroll (bool): Adjusted cumulative enrollment. When True, pulls students with enrollments dates that fall in the typical school year.
                When False, it pulls students with enrollments from July to June (7/1/YYYY - 6/30/YYYZ)
            academic_year (str): a string in the format, YYYY-YYYY, e.g. 2018-2019.
        """
        if not by_date_range:
            #Academic year
            year = self.driver.find_element(By.NAME, 'AcademicYear_input')
            year.clear()
            year.send_keys(academic_year)
            all_grades = Select(self.driver.find_element(By.ID, 'GradeLevel'))
        else:
            self._fill_typical_date_range_form(start_date, end_date)
            all_grades = Select(self.driver.find_element(By.XPATH, "//div[contains(@id, 'DateRange')]//select[@id='GradeLevel']"))

        #Defaulting to all grades TODO: Maybe support specific grades? Doubt it'd be useful.
        all_grades.select_by_visible_text('All')

    def __fill_sped_request_extract(self, by_date_range, start_date, end_date):
        if by_date_range:
            self._fill_typical_date_range_form(start_date, end_date, extract_name='SPED')

    def __fill_ssrv_request_extract(self, by_date_range, start_date, end_date):
        if by_date_range:
            self._fill_typical_date_range_form(start_date, end_date, extract_name='SSRV')

    def download_extract(self, lea_code, extract_name, temp_folder_name=None, 
                            max_attempts=10, pandas_kwargs=None):
        """
        Request an extract with the extract_name from CALPADS.
        
        For Direct Certification Extract, pass in extract_name='DirectCertification'. For SSID Request Extract, pass in 'SSID'.
        For the others, use their abbreviated acronym, e.g. SENR, SELA, etc.
        
        Args:
            lea_code (str): string of the seven digit number found next to your LEA name in the org select menu. For most LEAs,
                this is the CD part of the County-District-School (CDS) code. For independently reporting charters, it's the S.
            extract_name (str): generally the four letter acronym of the extract. e.g. SENR, SELA, etc.
                For Direct Certification Extract, pass in extract_name='DirectCertification'. 
                For SSID Request Extract, pass in 'SSID'.
                Spelling matters, capitalization does not. Raises ReportNotFound if report name is unrecognized/not supported.
            temp_folder_name (str): the name for a sub-directory in which the files from the browser will be stored. If this directory does not exist,
                it will be created. The parent directory will be the temp_folder_path used when instantiating Calpads object. If None, a temporary directory
                will be created and deleted as part of cleanup.
            max_attempts (int): the max number of times to try checking for the download. There's a 1 minute wait between each attempt.
            pandas_kwargs (dict): additional arguments to pass to Pandas read_csv

        Returns:
            DataFrame: A Pandas DataFrame of the extract
        """
        extract_name = extract_name.upper()

        if temp_folder_name:
            extract_download_folder_path = self.temp_folder_path + '/' + temp_folder_name
            os.makedirs(extract_download_folder_path, exist_ok=True)
        else:
            extract_download_folder_path = mkdtemp()

        if not pandas_kwargs:
            pandas_kwargs = {}

        self.driver = DriverBuilder().get_driver(download_location=extract_download_folder_path, headless=self.headless)
        self._login()
        self._select_lea(lea_code)

        self.driver.get("https://www.calpads.org/Extract")
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.ID, 'org-select')))
        
        attempt = 0
        success = False
        today_ymd = dt.datetime.now().strftime('%Y-%m-%d')
        #TODO: Extract Type text changes often it seems. File Name split by underscore and get the first item in index might be more reliable?
        expected_extract_types = {
            'SENR': "SSID Enrollment ODS Download",
            'SINF': "Student Information ODS Download",
            'SPRG': "Student Program ODS Download",
            'SELA': "Student English Language Acquisition Status ODS Download",
            'DIRECTCERTIFICATION': 'Direct Certification',
            'SSID': 'SSID Extract',
            'CENR': 'Cumulative Enrollment ODS Download',
            'SASS': 'Staff Assignment ODS Download',
            'SDEM': 'Staff Demographics ODS Download',
            'STAS': 'Student Absence ODS Download',
            'SDIS': 'Student Discipline ODS Download',
            'CRSE': 'Course Section Enrollment ODS Download',
            'CRSC': 'Course Section Completion ODS Download',
            'SCSE': 'Student Course Section Enrollment ODS Download',
            'SCSC': 'Student Course Section Completion ODS Download',
            'SCTE': 'Student Career Technical Education ODS Download',
            'SPED': 'Special Ed ODS Download',
            'SSRV': 'Student Services ODS Download' 
            }
        if not expected_extract_types.get(extract_name, None):
            raise ReportNotFound("{} extract not found".format(extract_name))
        while attempt < max_attempts and not success:
            try:
                WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ExtractRequestGrid"]/table/tbody/tr[1]/td[3]')))
            except TimeoutException:
                raise Exception('The extract table took too long to load. Adjust the wait_time variable.')
            else:
                extract_type = self.driver.find_element(By.XPATH, '//*[@id="ExtractRequestGrid"]/table/tbody/tr[1]/td[3]').text
                extract_status = self.driver.find_element(By.XPATH, '//*[@id="ExtractRequestGrid"]/table/tbody/tr[1]/td[5]').text #expecting Complete
                date_requested = dt.datetime.strptime(self.driver.find_element(By.XPATH, '//*[@id="ExtractRequestGrid"]/table/tbody/tr[1]/td[7]').text,
                                                "%m/%d/%Y %I:%M %p").date().strftime('%Y-%m-%d') #parse the text datetime on CALPADS, extract the date, format it to match today variable formatting
            
            if extract_type == expected_extract_types[extract_name] and extract_status == "Complete" and date_requested == today_ymd: 
                current_file_num = list(os.walk(extract_download_folder_path))[0][2]
                dlbutton = self.driver.find_element(By.XPATH, '//*[@id="ExtractRequestGrid"]/table/tbody/tr[1]/td[1]/a') #Select first download button
                dlbutton.click()
                wait_for_new_file_in_folder(extract_download_folder_path, current_file_num)
                success = True
            else:
                attempt += 1
                self.log.info("The download doesn't seem ready during attempt #{} for LEA {}".format(attempt, lea_code))
                time.sleep(60) #We do want a full minute wait
                self.driver.refresh()
                WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.ID, 'org-select')))
        
        if not success:
            self.driver.quit()
            self.log.info("All download attempts failed for {}. Cancelling {} extract download. Make sure you've requested the extract today.".format(lea_code, extract_name))
            raise ReportNotFound
        
        #Set a default variable for names:
        if 'names' not in pandas_kwargs.keys():
            #If no column names are passed into pandas, use the default file layout names.
            kwargs_copy = pandas_kwargs.copy()
            kwargs_copy['names'] = EXTRACT_COLUMNS[extract_name]
            if not kwargs_copy.get('header'):
                kwargs_copy['header'] = None
        extract_df = pd.read_csv(get_most_recent_file_in_dir(extract_download_folder_path), sep='^', **kwargs_copy)
        self.log.info("{} {} Extract downloaded.".format(lea_code, extract_name))
        self.driver.quit()

        #Download won't have an easily recognizable name. Rename.
        #TODO: Unless one memorizes the LEA codes, should consider optionally supporting a text substitution of the lea_code via a dictionary.
        self._rename_a_calpads_download(extract_download_folder_path, new_file_text=lea_code + " " + extract_name + " Extract")

        if not temp_folder_name:
            shutil.rmtree(extract_download_folder_path)

        return extract_df

    def __get_report_link(self, report_code, is_snapshot=True):   
        if report_code == '8.1eoy3' and is_snapshot:
            #TODO: Might add another variable and if-condition to re-use for ODS as well as Snapshot
            return 'https://www.calpads.org/Report/Snapshot/8_1_StudentProfileList_EOY3_'
        else:
            for i in self.driver.find_elements(By.CLASS_NAME, 'num-wrap-in'):
                if report_code == i.text:
                    return i.find_element(By.XPATH, './../../a').get_attribute('href')
            raise ReportNotFound('{} report code cannot be found on the webpage'.format(report_code))

    def __wait_for_view_report_clickable(self, max_attempts, wait_time=60):
        """Check for the delay before webpage allows another change in value for the report request"""
        attempts = 0
        loaded = False
        while not loaded and attempts < max_attempts:
            try:
                view_report = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable((By.ID, 'ReportViewer1_ctl08_ctl00')))
            except TimeoutException:
                self.log.info('The Report button has not loaded after {} seconds. Attempt: {}'.format(wait_time, attempts+1))
                attempts += 1
            except StaleElementReferenceException:
                #Couldn't tell you why this error gets raised, but here we are
                self.log.info('The Report button has not loaded after {} seconds. Attempt: {}'.format(wait_time, attempts+1))
                attempts += 1
            else:
                return view_report
        if not loaded:
            self.log.info('Max number of attempts waiting for View Report to be clickable reached and all failed.')
            return False

    def __wait_for_download_dropdown(self,lea_code,report_code, max_attempts):
        """Check for the download dropdown for reports to be visible before clicking download"""
        dropdown = False
        attempts = 0
        #CSV download button cannot be clicked until the menu is visible
        #TODO: Use the Async_Wait element visibility as the marker of a completed download? //*[@id="ReportViewer1_AsyncWait_Wait"]
        #No, Yusuph, you cannot wait for its staleness. It does not disappear from the DOM, only gets hidden/display: none.
        while not dropdown and attempts < max_attempts:
            try:
                #The dropdown button to make the dropdown appear
                dropdown_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'ReportViewer1_ctl09_ctl04_ctl00')))
            except TimeoutException:
                #This runs every time the report toolbar takes too long to be visible/clickable
                self.log.info('The report toolbar failed to load for {}'.format(lea_code))
            else:
                #This will run only when the report toolbar is visible
                dropdown_btn.click()
            try:
                #Is the dropdown menu visible?
                WebDriverWait(self.driver, 3).until(EC.visibility_of(self.driver.find_element(By.ID, 'ReportViewer1_ctl09_ctl04_ctl00_Menu')))
            except TimeoutException:
                #The dropdown menu is not visible
                self.log.info('Download Attempt {} failed. Waiting 1 minute.'.format(attempts+1))
                attempts += 1
                time.sleep(60)
            except StaleElementReferenceException:
                #Some quasi random and rare cases where the report is ready for download upon visiting the page without
                #clicking View Report appears to cause a race condition such that upon trying to find the Menu button
                #it flags it as being stale. Just keep swimming and try again.
                #The dropdown menu is not visible
                self.log.info('Download Attempt {} failed. Waiting 1 minute.'.format(attempts+1))
                attempts += 1
                time.sleep(60)
            except NoSuchElementException:
                #Occasionally it seems the report toolbar is potentially not loaded? Let's check if we need to click View Report again
                if self.__wait_for_view_report_clickable(1, 2):
                    view_report = self.driver.find_element(By.ID, 'ReportViewer1_ctl08_ctl00')
                    view_report.click()
                self.log.info('Download Attempt {} failed. Waiting 10 seconds.'.format(attempts+1))
                attempts += 1
                time.sleep(10)
            else:
                dropdown = True
        
        if not dropdown:
            self.log.info('Reached the max download attempts {}. The {} report failed to load for LEA: {}.'.format(max_attempts, report_code, lea_code))
            raise ReportNotReady
        else:
            self.log.info('Opened the {} report download dropdown for LEA: {}'.format(report_code, lea_code))
            return True
    
    def __check_login_request(self):
        """Check if the report page requested another login before loading"""
        #TODO: Confirm behavior of 'log in again' logic
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'Password')))
        except TimeoutException:
            self.log.info("The web page did not request another login. Checking if the report page is up.")
        except NoSuchElementException:
            self.log.info('The web page did not request another login. Checking if the report page is up.')
        else:
            user = self.driver.find_element(By.ID, "Username")
            user.send_keys(self.username)
            pw = self.driver.find_element(By.ID, "Password")
            pw.send_keys(self.password)
            agreement = self.driver.find_element(By.ID, "AgreementConfirmed")
            self.driver.execute_script("arguments[0].click();", agreement)
            btn = self.driver.find_element(By.CLASS_NAME, 'btn-primary')
            btn.click() #TODO: Review code and add similar try/except/else situations

    def _download_report_on_page(self, lea_code, report_code, dl_folder=None, dl_type='csv', max_attempts=10,
                                pandas_kwargs=None):
        """Downloads the report on the page.
        If download_report exceeds max download dropdown attempts after clicking view report,
        use for one-off download of the report available on the page when it finishes loading.
        """
        #TODO: Consider data structure to keep track of LEAs that have had a particular report downloaded and when
        try:
            #In case it's not in the report iframe context
            self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//*[@id="reports"]/div/div/div/iframe'))
        except NoSuchElementException:
            pass
        if self.__wait_for_download_dropdown(lea_code, report_code, max_attempts):
            #TODO: CHANGE FOLDER TO BE TEMP/SPECIFIED FOLDER PATTERN
            current_file_num = list(os.walk(dl_folder))[0][2]
            dl_options = self.driver.find_element(By.ID, 'ReportViewer1_ctl09_ctl04_ctl00_Menu')
            for dl_btn in dl_options.find_elements(By.TAG_NAME, 'a'):
                if dl_type.lower() in dl_btn.get_property('innerHTML').lower():
                    dl_btn.click()
            #script occasionally skips this function call for some reason
            if wait_for_new_file_in_folder(dl_folder, current_file_num):
                pass
            else:
                self.log.info("Download may have taken too long. Ending program.")
                #TODO: Write a better exception?
                raise Exception("Download may have taken too long. Ending program.")
            #TODO: Denote ODS vs. Snapshot in new file name
            self._rename_a_calpads_download(folder_path=dl_folder, new_file_text="{} {} ".format(lea_code, report_code) )
            self.log.info('{} Report successfully downloaded for {}.'.format(report_code, lea_code))
            self.driver.switch_to.default_content()
            
            if dl_type == 'csv':
                report_df = pd.read_csv(get_most_recent_file_in_dir(dl_folder), sep=',', **pandas_kwargs)
            elif dl_type == 'excel':
                report_df = pd.read_excel(get_most_recent_file_in_dir(dl_folder), **pandas_kwargs)
            else:
                report_df = None
            #TODO: Denote Snapshot vs. ODS download in logging
            self.log.info("{} {} downloaded.".format(lea_code, report_code))
            self.driver.quit()

            #Download won't have an easily recognizable name. Rename.
            #TODO: Unless one memorizes the LEA codes, should consider optionally supporting a text substitution of the lea_code via a dictionary.
            self._rename_a_calpads_download(dl_folder, new_file_text=lea_code + " " + report_code)

            return report_df
        else:
            return False
    
    def _parse_report_form(self, lea_code, max_attempts, dry_run, **kwargs):
        """Parse and when it's not a dry run, fill in the form."""

        all_form_elements = self.driver.find_elements(By.XPATH, "//*[@data-parametername]")
        params_dict = dict.fromkeys([i.get_attribute('data-parametername') for i in all_form_elements])
        for i in all_form_elements:
            tag_combos = []
            key = i.get_attribute('data-parametername')
            for j in i.find_elements(By.XPATH, './/*'):
                tag_combos.append(j.tag_name) #Find all the tags that are under the parameter div (i.e. where the form field is located)
                if j.tag_name == 'span' and 'calendar' in j.get_attribute('class'):
                    tag_combos = tag_combos[:-2] #If it's a calendar date input, remove the last two tags so it's treated like a textbox
            params_dict[key] = [tuple(tag_combos)]

        for k, v in params_dict.items():
            if v[0][0] == 'select':
                select = Select(self.driver.find_element(By.XPATH, "//*[@data-parametername='{}']//select".format(k)))
                v.append(('select', tuple(i.text for i in select.options)))
                                
            elif v[0][-1] == 'input':
                v.append(('textbox', 'plain text'))

            elif v[0][-1] == 'label':
                v.append(('textbox_defaultnull', 'plain text'))

            else:
                form_input_div = self.driver.find_element(By.XPATH, "//*[@data-parametername='{}']".format(k))
                div_id = form_input_div.get_attribute('id') + '_divDropDown'
                #More reliable to use execute script to avoid "other element would get the click error"
                self.driver.execute_script('arguments[0].click();', form_input_div.find_element(By.XPATH, './/input')) #Reveal the options
                div_for_input = self.driver.find_element(By.XPATH, '//div[@id="{}"]'.format(div_id))
                all_input_labels = div_for_input.find_elements(By.XPATH, './/input[@type != "hidden"]/following-sibling::label')
                all_input_labels_txt = [i.text for i in all_input_labels]
                dict_opts = dict.fromkeys(all_input_labels_txt, (True, False))
                v.append(('dropdown', dict_opts))
        
        if kwargs and not dry_run:
            self._fill_report_form(lea_code, params_dict, max_attempts, **kwargs)

        return params_dict

    def _fill_report_form(self, lea_code, params_dict, max_attempts, **kwargs):

        #If provided_args is not None and not dry_run -- do stuff for selects only; use dict.get(key) check
        for a, b in kwargs.items():
            if params_dict.get(a): #ensure the key is expected, if unexpected it will do nothing.
                if params_dict[a][1][0] == 'select':
                    select = Select(self.driver.find_element(By.XPATH, "//*[@data-parametername='{}']//select".format(a)))
                    select.select_by_visible_text(b)
                    if not self.__wait_for_view_report_clickable(max_attempts):
                        self.log.info('A requested form value change failed to occur. Discontinuing report download for LEA: {}'.format(lea_code))
                        return False
                
                elif params_dict[a][1][0] == 'textbox':
                    form_input_div = self.driver.find_element(By.XPATH, "//*[@data-parametername='{}']".format(a))
                    form_input_div.find_element(By.XPATH, './/input').send_keys(b)
                    if not self.__wait_for_view_report_clickable(max_attempts):
                        self.log.info('A requested form value change failed to occur. Discontinuing report download for LEA: {}'.format(lea_code))
                        return False
                
                elif params_dict[a][1][0] == 'textbox_defaultnull':
                    form_input_div = self.driver.find_element(By.XPATH, "//*[@data-parametername='{}']".format(a))
                    form_input_div.find_element(By.XPATH, ".//label/preceding-sibling::input").click() #Uncheck the NULL value
                    form_input_div.find_element(By.XPATH, './/input').send_keys(b) #Send value to the first input
                    if not self.__wait_for_view_report_clickable(max_attempts):
                        self.log.info('A requested form value change failed to occur. Discontinuing report download for LEA: {}'.format(lea_code))
                        return False
                else:
                    #Expecting the rest to be dropdowns only
                    form_input_div = self.driver.find_element(By.XPATH, "//*[@data-parametername='{}']".format(a))
                    div_id = form_input_div.get_attribute('id') + '_divDropDown'
                    self.driver.execute_script('arguments[0].click();', form_input_div.find_element(By.XPATH, './/input')) #Reveal the options
                    div_for_input = self.driver.find_element(By.XPATH, '//div[@id="{}"]'.format(div_id))
                    all_inputs = div_for_input.find_elements(By.XPATH, './/input[@type != "hidden"]')
                    all_inputs[0].click() #Click the select all to clear all options
                    if all_inputs[0].get_attribute('checked'):
                        #A few reports start off as unchecked, confirm that the "Select All" option is in expected state
                        all_inputs[0].click()
                    time.sleep(1) #TODO: WebDriverWait
                    for j, x in b.items():
                        elem_idx = [i for i in params_dict[a][1][1].keys()].index(j)
                        if x: #Double checking that the user sent True/truthy value
                            self.driver.execute_script('arguments[0].click();', all_inputs[elem_idx])
                            if not self.__wait_for_view_report_clickable(max_attempts):
                                self.log.info('A requested form value change failed to occur. Discontinuing report download for LEA: {}'.format(lea_code))
                                return False #TODO: pass in max_attempts variable

    def download_snapshot_report(self, lea_code, report_code, dl_type='csv', max_attempts=10, temp_folder_name=None,
                                dry_run=False, pandas_kwargs=None, **kwargs):
        """Download a CALPADS snapshot report in a specified format. 
        
        Args:
            lea_code (str): The 7 digit identifier for your LEA passed in as a string.
            report_code (str): Currently supports all known reports. Expected format is a string e.g. '8.1', '1.17', and '1.18'.
                For reports that have letters in them, for example the 8.1 EOY3, expected input is '8.1eoy3' OR '8.1EOY3'. 
                No spaces, all one word.
            dl_type (str): The format in which you want the download for the report. 
                Currently supports: csv, excel, and pdf.
            max_attempts (int): how often to keep trying to check if view report is clickable or if the download dropdown is visible.
                Each additional attempt is a 1 minute wait time.
            temp_folder_name (str): the name for a sub-directory in which the files from the browser will be stored. 
            If this directory does not exist, it will be created. The parent directory will be the temp_folder_path passed in
            when instantiating the Calpads object. If None, a temporary directory will be created and deleted as part of cleanup.
            dry_run (bool): when False, it downloads the report. When True, it doesn't download the report and instead returns
                a dict wih the form fields and their expected inputs.
            pandas_kwargs (dict): keywords to pass into Pandas read method, read_csv for dl_type='csv' or
                read_excel for dl_type='excel'
            **kwargs: keyword arguments for report inputs/fields. Valid keywords are dynamically assessed per report. 
                To know the options and expected formatting for each report, set dry_run=True and a dict will be returned instead.
        
        Returns:
            bool: True for a successful download of report, else False.
            dict: when dry_run=True, it returns a dict of the form fields and their expected inputs for report manipulation
        """
        report_code = report_code.lower()

        if temp_folder_name:
            report_download_folder_path = self.temp_folder_path + '/' + temp_folder_name
            os.makedirs(report_download_folder_path, exist_ok=True)
        else:
            report_download_folder_path = mkdtemp()

        if not pandas_kwargs:
            pandas_kwargs = {}
        
        #Set defaults for the form input if none provided
        if not kwargs:
            kwargs = {'Status': 'Revised Uncertified'}
        elif kwargs and not kwargs.get('Status'):
            kwargs.update({'Status': 'Revised Uncertified'})

        self.driver = DriverBuilder().get_driver(download_location=report_download_folder_path, headless=self.headless)
        self._login()
        self._select_lea(lea_code)

        #Report link lookup
        self.driver.get('https://www.calpads.org/Report/Snapshot')
        self.driver.get(self.__get_report_link(report_code))
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//*[@id="reports"]//iframe'))

        self.__check_login_request()

        self.__wait_for_view_report_clickable(max_attempts)

        parsed_params_dict = self._parse_report_form(lea_code, max_attempts, dry_run, **kwargs)

        if dry_run:
            self.driver.quit()
            return parsed_params_dict
        
        if self.__wait_for_view_report_clickable(max_attempts):
            view_report = self.driver.find_element(By.ID, 'ReportViewer1_ctl08_ctl00') #Have to find the element again to avoid StaleElementReference error
            view_report.click()
            #Some reports require two clicks of View Report for no apparent reason
            if report_code in ['3.2', '3.3', '8.1eoy3', '1.21'] and self.__wait_for_view_report_clickable(1):
                view_report = self.driver.find_element(By.ID, 'ReportViewer1_ctl08_ctl00')
                view_report.click()

        result = self._download_report_on_page(max_attempts=max_attempts, lea_code=lea_code, report_code=report_code, 
                                                dl_folder=report_download_folder_path, dl_type=dl_type, pandas_kwargs=pandas_kwargs)
        
        #clean up
        if not temp_folder_name:
            shutil.rmtree(report_download_folder_path)
        #TODO: result = None when the option is PDF which might be confusing/unexpected for users. Not sure what a better alternative would be.
        return result
    
    def download_ods_report(self, lea_code, report_code, dl_type='csv', max_attempts=10, temp_folder_name=None, 
                            dry_run=False, pandas_kwargs=None, **kwargs):
        """Download a CALPADS ODS report in a specified format. 
        
        Args:
            lea_code (str): The 7 digit identifier for your LEA passed in as a string.
            report_code (str): Currently supports all known reports. Expected format is a string e.g. '8.1', '1.17', and '1.18'.
                For reports that have letters in them, for example the 8.1 EOY3, expected input is '8.1eoy3' OR '8.1EOY3'. 
                No spaces, all one word.
            dl_type (str): The format in which you want the download for the report. 
                Currently supports: csv, excel, and pdf.
            max_attempts (int): how often to keep trying to check if view report is clickable or if the download dropdown is visible.
                Each additional attempt is a 1 minute wait time.
            temp_folder_name (str): the name for a sub-directory in which the files from the browser will be stored. 
            If this directory does not exist, it will be created. The parent directory will be the temp_folder_path passed in
            when instantiating the Calpads object. If None, a temporary directory will be created and deleted as part of cleanup.
            dry_run (bool): when False, it downloads the report. When True, it doesn't download the report and instead returns
                a dict wih the form fields and their expected inputs.
            pandas_kwargs (dict): keywords to pass into Pandas read method, read_csv for dl_type='csv' or
                read_excel for dl_type='excel'
            **kwargs: keyword arguments for report inputs/fields. Valid keywords are dynamically assessed per report. 
                To know the options and expected formatting for each report, set dry_run=True and a dict will be returned instead.
        
        Returns:
            bool: True for a successful download of report, else False.
            dict: when dry_run=True, it returns a dict of the form fields and their expected inputs for report manipulation
        """
        
        report_code = report_code.lower()

        if temp_folder_name:
            report_download_folder_path = self.temp_folder_path + '/' + temp_folder_name
            os.makedirs(report_download_folder_path, exist_ok=True)
        else:
            report_download_folder_path = mkdtemp()
        
        if not pandas_kwargs:
            pandas_kwargs = {}

        self.driver = DriverBuilder().get_driver(download_location=report_download_folder_path, headless=self.headless)
        self._login()
        self._select_lea(lea_code)

        #Report link lookup
        self.driver.get('https://www.calpads.org/Report/ODS')
        self.driver.get(self.__get_report_link(report_code, is_snapshot=False))
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//*[@id="reports"]//iframe'))

        self.__check_login_request()

        self.__wait_for_view_report_clickable(max_attempts)

        parsed_params_dict = self._parse_report_form(lea_code, max_attempts, dry_run, **kwargs)

        if dry_run:
            self.driver.quit()
            return parsed_params_dict
        
        if self.__wait_for_view_report_clickable(max_attempts):
            view_report = self.driver.find_element(By.ID, 'ReportViewer1_ctl08_ctl00') #Have to find the element again to avoid StaleElementReference error
            view_report.click()
            #Some reports require two clicks of View Report for no apparent reason
            if (report_code in ['1.2', '1.3', '1.5', '12.1', '3.2', '3.3', '3.6', '5.1', '10.1', '11.1', '9.2'] 
                    and self.__wait_for_view_report_clickable(1, 2)):
                view_report = self.driver.find_element(By.ID, 'ReportViewer1_ctl08_ctl00')
                view_report.click()

        result = self._download_report_on_page(lea_code=lea_code, report_code=report_code, dl_folder=report_download_folder_path, 
                                                dl_type=dl_type, max_attempts=max_attempts, pandas_kwargs=pandas_kwargs)
        
        #clean up
        if not temp_folder_name:
            shutil.rmtree(report_download_folder_path)
        
        return result



def wait_for_new_file_in_folder(folder_path, num_files_original, max_attempts=20000):
    """ Waits until a new file shows up in a folder.
    """
    file_added = False
    attempts = 0
    #TODO Wait based on time passed, not number of loops?
    while True and attempts < max_attempts:
        for root, folders, files in os.walk(folder_path):
            # break 'for' loop if files found
            if len(files) > len(num_files_original):
                    file_added = True
                    break
            else:
                continue
        # break 'while' loop if files found
        if file_added:
            # wait for download to complete fully after it's been added - hopefully 3 seconds is enough.
            time.sleep(3)
            return True
        attempts +=1
    return False
