from habr import HabrParse_csv #import module for parsing popular article from habrhabr.ru

if __name__ == '__main__':
    #base url for parsing article
    base_url = 'https://habr.com/ru/top/yearly/'
    
    #function for save to .csv "N"-articles form "base_url", in our case we parse from TOP popular article per year
    HabrParse_csv(base_url, 22)