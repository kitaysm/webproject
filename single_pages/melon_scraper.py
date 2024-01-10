from bs4 import BeautifulSoup
import requests

def get_melon_chart():
    # headers 변수: 웹 서버에게 이 요청이 웹 브라우저에서 온 것처럼 보이도록 사용자 에이전트 정보를 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    url = "https://www.melon.com/chart/index.htm"

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    lst50 = soup.select(".lst50")
    lst100 = soup.select(".lst100")
    lst = lst50 + lst100

    chart_data = []

    for i in lst:
        picture = i.select_one(".image_typeAll img").get('src')
        title = i.select_one(".ellipsis.rank01 a").text
        singers = [singer.text for singer in i.select(".ellipsis.rank02 > a")]
        album = i.select_one(".ellipsis.rank03 > a").text

        chart_data.append({
            "title": title,
            "artist": ', '.join(singers),  # 여러 가수가 있는 경우를 대비하여 문자열로 결합
            "album": album,
            "picture": picture
        })

    return chart_data

if __name__ == "__main__":
    print(get_melon_chart())