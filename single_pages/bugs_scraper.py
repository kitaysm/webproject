from bs4 import BeautifulSoup
import requests

def get_bugs_chart():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    url = "https://music.bugs.co.kr/chart/track/realtime/total?wl_ref=M_contents_03_01"

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    print(html)
    
    chart_data1 = []

    for items in soup.find_all('tr',{'rowtype':'track'}):
        rank = items.find('div',class_='ranking').find('strong').get_text(strip=True)
        img = items.find('a',class_='thumbnail').find('img').get('src')
        title = items.find('p', class_='title').find('a').get('title')
        artist = items.find('p', class_='artist').find('a').get('title')
        album = items.find('a', class_='album').get('title')
        chart_data1.append({
            "rank": rank,
            "img": img,
            "title": title,
            "artist": artist,
            "album": album,
        })
    
    return chart_data1

if __name__ == "__main__":
    print(get_bugs_chart())