import requests
import bs4
import re

# Заголовки нужны, чтобы симитировать поведение браузера
HEADERS = {
    'Cookie': 'hl=ru; fl=ru; _ym_uid=1649308338142175875; _ym_d=1649308338; _ga=GA1.2.2023437693.1649308338; _gid=GA1.2.283701464.1654666886; _ym_isad=2; visited_articles=315264:436638:173063:210450; habr_web_home_feed=/all/',
    'Host': 'habr.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}
base_url = "https://habr.com"
url = base_url + "/ru/all/"

# Список слов для поиска
KEYWORDS = ['Python', 'Java']

if __name__ == '__main__':
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')

    articles = soup.find_all('article')

    for article in articles:
        preview = article.find_all(class_='tm-article-snippet')
        user_info = article.find(class_="tm-article-snippet__meta").find(class_="tm-user-info__username") # text - надо проверять что есть такое поле и оно заполнено
        date_info = article.find(class_="tm-article-snippet__datetime-published").find("time").attrs["title"]
        title = article.find("h2").find("span")
        hubs = article.find_all(class_="tm-article-snippet__hubs-item")
        hubs = set(hub.text.strip() for hub in hubs)
        preview_text = article.find(class_="tm-article-body tm-article-snippet__lead")
        link = base_url + article.find(class_="tm-article-snippet__title-link").attrs["href"]

        if not user_info:
            user_info = ""
        else:
            user_info = user_info.text
        if not title:
            title = ""
        else:
            title = title.text
        if not preview_text:
            preview_text = ""
        else:
            preview_text = preview_text.text


        for elem in KEYWORDS:
            pattern = f'{elem}\S*'
            if re.search(pattern, user_info) \
                    or re.search(pattern, user_info) \
                    or re.search(pattern, date_info) \
                    or re.search(pattern, title) \
                    or re.search(pattern, preview_text):
                print(f"{date_info} - {title} - {link}")
                break
            else:
                for hub in hubs:
                    if re.search(pattern, hub):
                        print(f"{date_info} - {title} - {link}")
                        break
