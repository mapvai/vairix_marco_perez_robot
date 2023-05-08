from RPA.Browser.Selenium import Selenium, ElementNotFound
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from threading import Thread, current_thread
from queue import Queue
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
import datetime
import time
import ast
import os
import resources.nyt_news_module as news_module
from locators.nyt_locators import *
from config import *
from resources.logger import logger

browser = Selenium()
http = HTTP()

WAIT_FOR_ELEMENT_TIME = 0.2
MAX_ATTEMPTS = 5
NUM_THREADS = 10


def extract_latest_news_from_ny_times_and_save_in_excel():
    variables = get_search_configuration_from_work_item_or_environment()
    start_date = get_start_date_formatted(variables['number_of_months'])
    end_date = get_end_date_formatted()
    open_the_ny_times_site(variables['search_phrase'], start_date, end_date)
    select_sections(variables['sections'])
    load_all_available_news()
    all_news_list = scrape_all_news()
    browser.close_browser()
    download_pictures_and_save_pictures_name(all_news_list)
    news_to_excel_list = news_module.get_excel_table_from_news(
        all_news_list, variables['search_phrase'])
    export_all_news_as_excel(news_to_excel_list, SHEET_NAME, EXCEL_FILE_NAME)


def get_search_configuration_from_work_item_or_environment():
    variables = None
    try:
        library = WorkItems()
        library.get_input_work_item()
        variables = library.get_work_item_variables()
    except:
        logger.info(
            'No work item present, getting search data from config file')

    if variables:
        try:
            mapped_vars = {
                'search_phrase': variables['search_phrase'],
                'sections': ast.literal_eval(variables['sections']),
                'number_of_months': variables['number_of_months']
            }
        except Exception as e:
            logger.error(f"Json specified in Work Item payload have invalid format: {e} with {variables}")
            raise e

        return mapped_vars
    else:
        variables = {
            'search_phrase': LOCAL_SEARCH_PHRASE,
            'sections': LOCAL_SECTIONS,
            'number_of_months': LOCAL_NUMBER_OF_MONTHS
        }
        return variables


def get_start_date_formatted(number_of_months):
    current_date = datetime.datetime.now()
    number_of_months = 1 if number_of_months == 0 else number_of_months
    number_of_days = number_of_months * 30
    start_date = current_date - datetime.timedelta(days=number_of_days)
    return start_date.strftime('%Y%m%d')


def get_end_date_formatted():
    end_date = datetime.datetime.now().strftime('%Y%m%d')
    return end_date


def open_the_ny_times_site(query, start_date, end_date):
    url = NYT_URL.format(query=query, startDate=start_date, endDate=end_date)
    browser.open_available_browser(url)


def select_sections(sections):
    if len(sections) > 0:
        browser.click_button(SECTION_SELECTOR)
        for section in sections:
            try:
                section_checkbox_xpath = SECTION_CHECKBOX_LOCATOR.format(
                    section=section)
                browser.click_element(section_checkbox_xpath)
            except:
                logger.critical(f'Section {section} was not found')
        browser.click_button(SECTION_SELECTOR)


def load_all_available_news():
    attempt = 0
    while attempt <= MAX_ATTEMPTS:
        try:
            browser.click_element(SHOW_MORE_BUTTON_LOCATOR)
            attempt = 0
        except (ElementNotFound, StaleElementReferenceException, NoSuchElementException) as e:
            attempt += 1
            time.sleep(WAIT_FOR_ELEMENT_TIME)
        except Exception as e:
            logger.warning('Error attempting to click on SHOW_MORE_BUTTON', e)
            raise e


def scrape_all_news():
    all_news_list = []
    news_counter = len(browser.get_webelements(ALL_NEWS_RESULTS_LOCATOR))
    for i in range(1, news_counter+1):
        DateRelativeLocatorXpath = DATE_RELATIVE_LOCATOR.format(i=i)
        date = get_text_retry(DateRelativeLocatorXpath)
        TitleRelativeLocatorXpath = TITLE_RELATIVE_LOCATOR.format(i=i)
        title = get_text_retry(TitleRelativeLocatorXpath)
        DescriptionRelativeLocatorXpath = DESCRIPTION_RELATIVE_LOCATOR.format(i=i)
        description = get_text_retry(DescriptionRelativeLocatorXpath)
        ImageRelativeLocatorXpath = IMAGE_RELATIVE_LOCATOR.format(i=i)
        picture_url = get_element_attribute_retry(ImageRelativeLocatorXpath, 'src')
        news = news_module.construct_news(date, title, description, picture_url)
        all_news_list.append(news)
    return all_news_list


def get_text_retry(xpath):
    attempt = 0
    text = None
    while attempt <= MAX_ATTEMPTS:
        try:
            text = browser.get_text(xpath)
            break
        except (ElementNotFound, StaleElementReferenceException, NoSuchElementException) as e:
            attempt += 1
            time.sleep(WAIT_FOR_ELEMENT_TIME)
        except Exception as e:
            logger.error('Error getting text', e)
            raise e
    return text


def get_element_attribute_retry(xpath, attribute):
    attempt = 0
    text = None
    while attempt <= MAX_ATTEMPTS:
        try:
            text = browser.get_element_attribute(xpath, attribute)
            break
        except (ElementNotFound, StaleElementReferenceException, NoSuchElementException) as e:
            attempt += 1
            time.sleep(WAIT_FOR_ELEMENT_TIME)
        except Exception as e:
            logger.error('Error getting element attribute', e)
            raise e
    return text


def download_pictures_and_save_pictures_name(news_list):
    q = Queue()
    
    for i in range(NUM_THREADS):
        thread = Thread(target=download_pictures_and_save_pictures_name_worker, args=(q,))
        thread.daemon = True
        thread.start()

    for news in news_list:
        q.put(news)

    q.join()
        

def download_pictures_and_save_pictures_name_worker(q):
    while True:
        news = q.get()

        picture_url = news_module.get_picture_url_from_news(news)
        picture_name = get_picture_name()
        picture_path = os.path.join(OUTPUT_DIR, picture_name)
        response = http.download(picture_url, picture_path)
        if response.status_code == 200:
            news_module.set_picture_name_to_news(news, picture_name)
        else:
            news_module.set_picture_name_to_news(news, 'Picture fails to download')
            logger.error('Picture fails to download', news, response)
        q.task_done()

def get_picture_name():
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    picture_name = str(int(datetime.datetime.strptime(
        now, "%Y-%m-%d-%H-%M-%S-%f").timestamp()*1000)) + '_' + current_thread().name.split('-')[-1] + ".jpg"
    return picture_name


def export_all_news_as_excel(news_list, worksheet_name, file_name):
    excel = Files()
    excel.create_workbook(sheet_name=worksheet_name)
    excel.append_rows_to_worksheet(content=news_list)
    file_path = os.path.join(OUTPUT_DIR, file_name)
    excel.save_workbook(file_path)


# Define a main() function that calls the other functions in order:
def main():
    extract_latest_news_from_ny_times_and_save_in_excel()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
