import requests
from bs4 import BeautifulSoup
import pprint


def scrape_hacker_news(pages=1):
    '''Return a list of news server responses, recieves the number of pages where is extracting data'''
    new_hn_res = []
    for i in range(1, pages+1):
        try:
            response = requests.get('https://news.ycombinator.com/?p='+ str(i))
            soup = BeautifulSoup(response.text,'html.parser')
            links = soup.select('.titleline')
            subtext = soup.select('.subtext')
            new_hn_res.append(create_custom_hn(links,subtext))  
        except requests.RequestException as e:
            print(f'error scraping the page {i},:{e}')
            continue
    return new_hn_res
    

def sort_news_by_votes(news):
    '''Return sorted dic by positive votes of users'''
    return sorted(news, key = lambda k:k['points'], reverse = True)


def create_custom_hn(links,container_votes):
    '''Return a unsorted dict with title, link and votes of hacker news posts'''
    new_hn = []
    for idx, item in enumerate(links):
        # link = item.find_all('a')[0].get('href')
        title = item.get_text()
        link = item.a.get('href')
        votes = container_votes[idx].select('.score')
        
        if not len(votes):
            continue

        points = int(votes[0].get_text().replace(" points",''))
        if points > 99:
                new_hn.append({
                    'title':title,
                    'link':link,
                    'points':points,
                })
    return sort_news_by_votes(new_hn)

        
if __name__ == '__main__':
    pages_to_scrape = 3 
    pprint.pprint(scrape_hacker_news(pages_to_scrape))


