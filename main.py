import urllib.request
from bs4 import BeautifulSoup

# part 1 - https://www.youtube.com/watch?v=WHhaUK8yhXU



# source = urllib.request.urlopen(url)

# soup = BeautifulSoup(source,'html.parser')

# first_paragraph = soup.p.getText()
# print(first_paragraph)

# links = soup.find_all('a')
# for link in links:
#     print(link.get('href'))

# images = soup.find_all('img')
# for image in images:
#     print(image.get('src'))

# part 2 - https://www.youtube.com/watch?v=QEWlYJ3FT6U

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.source = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(self.source,'html.parser')


    def scrapeParagraphs(self):
        tags = self.soup.find_all('p')

        for tag in tags:
            print(tag.getText())
    

    def scrapeLinks(self):
        tags = self.soup.find_all('a')

        for tag in tags:
            print(tag.get('href'))

    
    def scrapeImages(self):
        tags = self.soup.find_all('img')

        for tag in tags:
            print(tag.get('src'))



url = "https://www.investopedia.com/articles/personal-finance/101014/10-characteristics-successful-entrepreneurs.asp"
# WebScraper(url).scrapeImages()
# WebScraper(url).scrapeParagraphs()
WebScraper(url).scrapeLinks()