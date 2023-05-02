import re

# Regular expression for matching money
MONEY_PATTERN = re.compile(
    r'(\$[\d]+(\,\d{3})(\.\d+)?)|(\$[\d]+(\.\d)?)|([\d]+ dollars)|([\d]+ USD)')
