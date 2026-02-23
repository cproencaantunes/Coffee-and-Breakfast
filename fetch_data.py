import requests
import xml.etree.ElementTree as ET
import json

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=38.71&longitude=-9.13&current_weather=true"
    try:
        r = requests.get(url)
        return r.json()['current_weather']
    except Exception as e:
        print(f"Erro no clima: {e}")
        return {"temperature": "--", "windspeed": "--"}

def get_news():
    rss_url = "https://www.publico.pt/rss/ultimas"
    news = []
    try:
        r = requests.get(rss_url, timeout=10)
        root = ET.fromstring(r.content)
        for item in root.findall('./channel/item')[:5]:
            news.append({"title": item.find('title').text, "url": item.find('link').text})
    except Exception as e:
        print(f"Erro no Público: {e}")
    return news

def get_finance():
    # API pública do TipRanks para notícias recentes
    url = "https://www.tipranks.com/api/news/posts?limit=5"
    headers = {"User-Agent": "Mozilla/5.0"}
    finance = []
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            posts = r.json().get('posts', [])
            for p in posts:
                finance.append({
                    "title": p['title'],
                    "url": f"https://www.tipranks.com/news/{p['slug']}"
                })
    except Exception as e:
        print(f"Erro no TipRanks: {e}")
    return finance

# Criar o dicionário de dados consolidado
data = {
    "weather": get_weather(),
    "news": get_news(),
    "finance": get_finance() # Adicionado TipRanks
}

# Guardar no data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Sucesso: data.json atualizado com Clima, Público e TipRanks!")
