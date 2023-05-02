# Python robot

RPA Challenge - Fresh News

This web scraper atomatice the following process of extracting data from the New York Times site.

1.Open the site by following the link
2.Enter a phrase in the search field
3.On the result page, apply the following filters:
    select a news category or section (from none to any number of sections, from config.py and/or Robocorp Cloud Work Item)
    choose the latest news
4.Get the values: title, date, and description.
5.Store in an excel file:
    title
    date
    description (if available)
    picture filename
    count of search phrases in the title and description
    True or False, depending on whether the title or description contains any amount of money
    Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
6.Download the news picture and specify the file name in the excel file
Follow the steps 4-6 for all news that fall within the required time period


This web scraper robot is implemented in Python instead of Robot Framework syntax, using the `rpaframework` set of libraries. According to tutorial and instructions on [Robocorp's documentation site](https://robocorp.com/docs/development-guide/python/python-robot).


Robocorp Cloud Work Item payload example:
payload = {
    "search_phrase": "Elon Musk Tesla California",
    "sections": "['Business', 'Technology']",
    "number_of_months": 1
}