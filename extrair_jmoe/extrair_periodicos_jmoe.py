import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para obter os títulos dos artigos de uma URL específica
def obter_titulos_artigos(ano, volume, numero):
    url = f"https://www.scielo.br/j/jmoea/i/{ano}.v{volume}n{numero}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro ao acessar {url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar todos os títulos dos artigos dentro das tags <strong> com a classe 'd-block mt-2'
    artigos = soup.find_all('strong', class_='d-block mt-2')
    titulos = []
    
    for artigo in artigos:
        titulos.append(artigo.get_text().strip())
    
    return titulos

# Função para obter todos os links das edições da grade
def obter_links_edicoes():
    url = "https://www.scielo.br/j/jmoea/grid"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro ao acessar {url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    # Encontre os links para as edições, filtrando aqueles que seguem o padrão
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith("/j/jmoea/i/"):  # Filtrando os links para as edições
            links.append("https://www.scielo.br" + href)
    
    return links

# Lista para armazenar os dados
dados_periodicos = []

# Obter todos os links das edições
links_edicoes = obter_links_edicoes()

# Iterar sobre os links de edições
for link in links_edicoes:
    # Extrair ano, volume e número da URL
    partes = link.split("/i/")[1].split(".v")
    ano = partes[0]
    volume, numero = partes[1].split("n")
    
    # Obter os títulos dos artigos dessa edição
    titulos = obter_titulos_artigos(ano, volume, numero)
    
    # Adicionar os dados encontrados à lista
    for titulo in titulos:
        dados_periodicos.append({
            "ano": ano,
            "volume": volume,
            "numero": numero,
            "titulo_artigo": titulo
        })

# Converter para DataFrame e salvar em CSV
df_periodicos = pd.DataFrame(dados_periodicos)

# Verificando se há dados antes de salvar
if not df_periodicos.empty:
    df_periodicos.to_csv("periodicos_por_pesquisador.csv", index=False, encoding="utf-8")
    print("Extração concluída! Salvo em 'periodicos_por_pesquisador.csv'")
else:
    print("Nenhum dado foi extraído.")
