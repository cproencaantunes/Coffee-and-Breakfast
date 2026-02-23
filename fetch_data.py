import requests
import xml.etree.ElementTree as ET
import json

def get_weather():
    # Coordenadas de Lisboa
    url = "https://api.open-meteo.com/v1/forecast?latitude=38.71&longitude=-9.13&current_weather=true"
    try:
        r = requests.get(url)
        return r.json()['current_weather']
    except Exception as e:
        print(f"Erro no clima: {e}")
        return {"temperature": "--", "windspeed": "--"}

def get_news():
    # RSS do jornal Público (Últimas Notícias)
    rss_url = "https://www.publico.pt/rss/ultimas"
    news = []
    try:
        r = requests.get(rss_url, timeout=10)
        root = ET.fromstring(r.content)
        # Pega nos primeiros 5 itens
        for item in root.findall('./channel/item')[:5]:
            title = item.find('title').text
            link = item.find('link').text
            news.append({"title": title, "url": link})
    except Exception as e:
        print(f"Erro nas notícias: {e}")
        news = [{"title": "Ligar robô às notícias...", "url": "#"}]
    return news

# Criar o dicionário de dados
data = {
    "weather": get_weather(),
    "news": get_news()
}

# Guardar no ficheiro data.json que o teu HTML vai ler
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Sucesso: data.json foi atualizado!")
const financeHtml = data.finance.map(f => `
    <li class="border-b border-slate-700 pb-2 last:border-0">
        <a href="${f.url}" target="_blank" class="hover:text-amber-400 transition-colors">• ${f.title}</a>
    </li>
`).join('');
document.getElementById('finance-list').innerHTML = financeHtml;
