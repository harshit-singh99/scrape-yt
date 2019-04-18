from bs4 import BeautifulSoup as bs
import requests
import nltk
import csv
import copy
remove_words = ['http', 'subscribe', 'sponser', 'facebook', 'twitter', 'instagram', 'snapchat', 'follow', 'check out',
                'www', '.org', 'net', '.com']

def scrape(url, tags):
    url = "https://www.youtube.com/watch?v=" + url

    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    desc = soup.find('p', attrs={'id' : 'eow-description'}).getText()
    title = soup.find('span', attrs={'id' : 'eow-title'}).getText().strip()
    list_l = soup.select('a.content-link.spf-link.yt-uix-sessionlink.spf-link')
    list_l = [l['href'][9:] for l in list_l]
    sents = nltk.sent_tokenize(desc)
    sents = [sent for sent in sents if not any(word in sent.lower() for word in remove_words)]
    sents = "".join(sents).replace(',', '')
    if len(sents) > 1000:
        sents = sents[:1000]
    category = soup.find('ul', attrs={'class' : 'content watch-info-tag-list'}).getText().strip()
    if category not in tags:
        return False

    return {'title': title, 'description': sents, 'links': list_l}



def one(url, tags, category):
    urls = copy.deepcopy(url)
    n = 0
    written_urls = []
    while(n < 1700):
        url = urls[0]
        if url in written_urls:
            urls.pop(0)
            continue
        vals = scrape(url, tags)
        written_urls.append(url)
        try:
            writer.writerow([url, vals['title'], vals['description'], category])
            urls.extend(vals['links'])
            n += 1
        except:
            pass



file = open('data.csv', 'w')
writer = csv.writer(file)
writer.writerow(['Video Id', 'Title', 'Description', 'Category'])

urls = [['RcmrbNRK-jY'],
        ['VSqkL31w69k'], 
        ['NFAN6L7xnvY'], 
        ['uuN6zU3ePG0'], 
        ['kxaVxz-cmhA'], 
        ['QLRHsPWQz_Y', 'qYnavutKVN8', 'dhYOPzcsbGM']]
tags = [['People & Blogs', 'Travel & Events'], 
        ['Science & Technology'],
        ['People & Blog', 'Entertainment'],
        ['Science & Technology'], 
        ['Education'],
        ['How-to & Style', 'Entertainment', 'Music']]
categories = ['travel', 'science', 'food', 'manufacturing', 'history', 'art']
for i in range(len(urls)):
    one(urls[i], tags[i], categories[i])

file.close()
