SECTION_SELECTOR='xpath://div[@data-testid="section"]//button[@data-testid="search-multiselect-button"]'
SECTION_CHECKBOX_LOCATOR='xpath://div[@data-testid="section"]//li[.//span[text()="{section}"]]//label//input[@type="checkbox"]'
SHOW_MORE_BUTTON_LOCATOR='xpath://button[@data-testid="search-show-more-button"]'
ALL_NEWS_RESULTS_LOCATOR='xpath://ol[@data-testid="search-results"]//li[@data-testid="search-bodega-result"]'

# Relative locators
DATE_RELATIVE_LOCATOR = f'{ALL_NEWS_RESULTS_LOCATOR}['+'{i}]//div//span'
TITLE_RELATIVE_LOCATOR = f'{ALL_NEWS_RESULTS_LOCATOR}['+'{i}]//div//div//a//h4'
DESCRIPTION_RELATIVE_LOCATOR = f'{ALL_NEWS_RESULTS_LOCATOR}['+'{i}]//div//div//a//p[1]'
IMAGE_RELATIVE_LOCATOR = f'{ALL_NEWS_RESULTS_LOCATOR}['+'{i}]//div//figure//div//img'