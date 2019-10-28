import requests, lxml, csv
from bs4 import BeautifulSoup

#get content from the page
def get_page(url):
    headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}
    session = requests.session()
    
    request = session.get(url, headers=headers)
    
    if request.ok:
        return request.text
    print(request.status_code)

#parse necessery fields
def parse_data(soup, post_count):
    content_body = soup.find("div", class_='posts_list')

    post_title=[i.text for i in content_body.find_all("a", class_="post__title_link")]
    text_tiser = [i.text for i in content_body.find_all("div", class_="post__body post__body_crop ")]
    data_publish = [i.text for i in content_body.find_all("span", class_="post__time")]
    name_author = [i.text for i in content_body.find_all("span", class_="user-info__nickname user-info__nickname_small")]
    #post_url=[i.get("href") for i in content_body.find_all("a", class_="post__title_link")]

    data = []
    for num in range(post_count):
        data.append(
            {'Заголовок поста': post_title[num],
            'Краткое описание поста': text_tiser[num],
            'Дата публикации': data_publish[num],
            'Имя автора поста': name_author[num]})

    return data

#get count page of pagination
def get_total_pages(soup):
    last_page = soup.find("a", class_="toggle-menu__item-link toggle-menu__item-link_pagination toggle-menu__item-link_bordered").get('href')
    
    return int(last_page.split('/page')[-1][:-1])

#save data to csv
def write_csv(dict):
    with open('habr.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=dict[0])
        writer.writerows(dict)

#main function of this module
def HabrParse_csv(base_url, post_count):
    page_num = post_count // 20 + 2 if post_count > 20 else  2 #counting page for parse
    
    for i in range(1, page_num):
        url = base_url + "page" + str(i)
        html = get_page(url)
        soup = BeautifulSoup(html, 'lxml')
        
        #if that not last page then parse all article, else parse last "20-post_count" articles
        data = parse_data(soup, 20) if post_count >= 20 else parse_data(soup, post_count) 

        #save result to .csv
        write_csv(data)
        post_count -= 20
