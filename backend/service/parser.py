from curl_cffi import requests
from bs4 import BeautifulSoup
from backend.models.achv_model import Achv

url = "https://psnprofiles.com/guide/26347-where-the-seeds-fall-trophy-guide"


def get_html(url) -> str:
    response = requests.get(url=url, impersonate="chrome", timeout=(1, 10))
    response.raise_for_status()

    return response.text


def get_html_from_response(response):
    html = BeautifulSoup(response, "html.parser")
    return html


def get_achv_from_html(html):
    achievements = []
    section = html.find_all("div", class_="box section-holder")

    for id, sec in enumerate(section, start=1):
        if not sec.find("table", class_="zebra"):
            continue
        else:
            sibling = sec.find_next_sibling("div")
            title_parent = sec.find("a", class_="title")
            title_text = title_parent.get_text(strip=True)
            guide_div = sibling.select_one("div.guide")
            achievements.append(
                Achv(
                    id=id,
                    title=title_text,
                    tag=[
                        tag.get_text(strip=True).upper()
                        for tag in sibling.select("div#tags span.tag")
                    ],
                    description=title_parent.find_next_sibling(
                        "br"
                    ).next_sibling.strip(),
                    guide=(
                        " ".join(
                            guide_div.get_text(separator=" ", strip=True)
                            .replace("\u200b", "")
                            .split()
                        )
                        if guide_div
                        else ""
                    ),
                    unlocked=False,
                )
            )

    return achievements


if __name__ == "__main__":
    raw_html = open(
        "/home/valen/Rastreador-de-logros-para-juegos/backend/tests/unit_tests/fixtures/sample_guide.html",
        encoding="utf-8",
    ).read()
    soup = get_html_from_response(raw_html)
    achvs = get_achv_from_html(soup)

    print(f"Total encontrados: {len(achvs)}")
    for a in achvs[:3]:
        print(a)
