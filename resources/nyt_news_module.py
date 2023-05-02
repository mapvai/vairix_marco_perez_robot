# nyt_news_module.py
import re
from .regex_patterns import MONEY_PATTERN


excel_news_columns = ['Date', 'Title', 'Description', 'Picture Name',
                      'Count of search phrases', 'Contains any amount of money']


def construct_news(date, title, description, picture_url):
    return NYTNews(date, title, description, picture_url)


def set_picture_name_to_news(news, picture_name):
    news.set_picture_name(picture_name)


def get_picture_url_from_news(news):
    return news.get_picture_url()


def get_excel_table_from_news(news_list, phrase):
    excel_news_list = []
    excel_news_list.append(excel_news_columns)
    excel_news_list += [[news.get_date(), news.get_title(), news.get_description(), 
                         news.get_picture_name(), news.get_count_search_phrases(phrase), 
                         news.contains_money()] for news in news_list]
    return excel_news_list


class NYTNews:

    def __init__(self, date, title, description, picture_url):
        self.date = date
        self.title = title
        self.description = description
        self.picture_url = picture_url
        self.picture_name = ''

    def set_picture_name(self, picture_name):
        self.picture_name = picture_name

    def get_date(self):
        return self.date
    
    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_picture_url(self):
        return self.picture_url

    def get_picture_name(self):
        return self.picture_name

    def get_count_search_phrases(self, phrase):
        text = self.title + self.description
        text = text.replace('\'', '')
        count = text.count(phrase)
        # in case it is neeed to count the amout of occurences for earch word uncomment the following two lines
        # search_tokens = text.split
        # count = sum([text.count(token) for token in search_tokens])
        return count

    def contains_money(self):
        text = self.title + self.description
        text = text.replace('\'', '')
        match = MONEY_PATTERN.search(text)
        return 'True' if match else 'False'

    def __repr__(self):
        return f'Date: {self.date}, Title: {self.title}, Description: {self.description}, Picture Name: {self.picture_name}, Picture url: {self.picture_url}'
