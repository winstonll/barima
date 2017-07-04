import pandas as pd
from newspaper import Article

paragraphcount = 0
linecount = 0

for line in text:
    if line in ('\n', '\r\n'):
        if linecount == 0:
            paragraphcount = paragraphcount + 1
        linecount = linecount + 1
    else:
        linecount = 0