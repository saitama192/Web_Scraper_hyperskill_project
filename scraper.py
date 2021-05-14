import requests
import os
from bs4 import BeautifulSoup


def search_article(pages, topic, url, base_dir):
    link = url
    dir = base_dir
    for counter in range(pages):
        r = requests.get(link)  # headers={'Accept-Language': 'en-US,en;q=0.5'} #hidden argument
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            res_news = soup.find_all('article')
           # print('Articles on this page '+str(len(res_news)))
            print('page article number')
            for element in res_news:
                s_word = element.find(class_ = 'c-meta__type')
                if s_word.text == topic:
                    print(s_word.text)
                    if element.find('a') != -1:
                        b = element.find('a')
                        c = element.find('h3')
                        print(c.text)
                        file_writer(b.get('href'),c.text, counter+1, dir)

            d = soup.find_all('li', class_ = 'c-pagination__item')
            if d:
                next_page = d[-1]
                lnk_nxt = next_page.find('a').get('href')
                final_lnk = 'https://www.nature.com'+lnk_nxt
                print(final_lnk)
                link = final_lnk

        else:
            return None
        print(counter)



def file_writer(link, article_name, page_no, base_dir):
    url = 'https://www.nature.com/articles/'+link[-18:]
    article_name = article_name.replace(' ', '_')
    article_name = article_name.replace('\n', '')
    article_name = article_name.replace(':', '')
    article_name = article_name.replace('?', '')

    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        article_content = soup.find('div', {'class':'article__body cleared'})
        if article_content is not None:
            check_dir(page_no, base_dir)
            c = (article_content.text.strip()).encode()
            b = open(article_name+'.txt', 'wb')
            b.write(c)
            b.close()
            os.chdir(base_dir)

        elif soup.find('div', {'class': 'Theme-Layer-BodyText--inner'}) is not None:
            article_content = soup.find('div', {'class':'Theme-Layer-BodyText--inner'})
            check_dir(page_no, base_dir)
            c = (article_content.text.strip()).encode()
            b = open(article_name + '.txt', 'wb')
            b.write(c)
            b.close
            os.chdir(base_dir)

        elif soup.find('div', {'class': 'article__copy'}) is not None:
            article_content = soup.find('div', {'class':'article-item__body'})
            check_dir(page_no, base_dir)
            c = (article_content.text.strip()).encode()
            b = open(article_name + '.txt', 'wb')
            b.write(c)
            b.close
            os.chdir(base_dir)


def check_dir(page_no, base_dir):
    b = os.getcwd()
    try:
        os.mkdir('Page_{}'.format(page_no))
            #print('folder created')
        os.chdir(base_dir + '\Page_{}'.format(page_no))
        #print('directory changed')
    except OSError:
        os.chdir(base_dir+'\Page_{}'.format(page_no))
        #print('directory changed')


def check_dir_main(page_no, base_dir):
    c = os.getcwd()
    if base_dir == c:
        for a in range(page_no):
            try:
                os.mkdir('Page_{}'.format(a+1))
            except OSError:
                pass
    else:
        for a in range(page_no):
            try:
                b = 'Page_{}'.format(a+1)
                d = os.path.join(c,b)
                os.mkdir(d)
            except OSError:
                pass


def main():
    n = int(input())
    b = input()
    base_dir = os.getcwd()
    check_dir_main(n, base_dir)
    a = 'https://www.nature.com/nature/articles'
    print(a)
    c = search_article(n, b, a, base_dir)

main()