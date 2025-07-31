import requests
from bs4 import BeautifulSoup
import pandas as pd

# Carregar o CSV com os artigos (substitua o caminho do arquivo conforme necessário)
df_artigos = pd.read_csv('periodicos_por_pesquisador.csv')

# Função para extrair os autores e palavras-chave a partir do título do artigo
def obter_autores_e_palavras_chave(titulo, ano, volume, numero):
    url = f"https://www.scielo.br/j/jmoea/i/{ano}.v{volume}n{numero}/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erro ao acessar {url} para o artigo {titulo}")
        return [], []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar o artigo específico pela correspondência do título
    artigo = soup.find('strong', string=titulo)
    
    if not artigo:
        print(f"Artigo {titulo} não encontrado na página.")
        return [], []

    # Encontrar todos os autores do artigo
    autores_tags = artigo.find_all_next('a', href=True)
    autores = [autor.get_text(strip=True) for autor in autores_tags]
    
    # Encontrar as palavras-chave (geralmente estão em uma lista específica ou dentro de uma classe)
    palavras_chave_tags = soup.find_all('a', class_='palavra-chave')
    palavras_chave = [palavra.get_text(strip=True) for palavra in palavras_chave_tags]
    
    return autores, palavras_chave

# Lista para armazenar os dados atualizados com os autores e palavras-chave
dados_com_autores_palavras_chave = []

# Iterar sobre cada artigo no CSV
for index, row in df_artigos.iterrows():
    titulo = row['titulo_artigo']
    ano = row['ano']
    volume = row['volume']
    numero = row['numero']
    
    # Obter os autores e palavras-chave para cada artigo
    autores, palavras_chave = obter_autores_e_palavras_chave(titulo, ano, volume, numero)
    
    # Adicionar os dados no formato desejado (com os autores e palavras-chave)
    dados_com_autores_palavras_chave.append({
        "ano": ano,
        "volume": volume,
        "numero": numero,
        "titulo_artigo": titulo,
        "autores": ", ".join(autores),  # Adiciona os autores separados por vírgula
        "palavras_chave": ", ".join(palavras_chave)  # Adiciona as palavras-chave separadas por vírgula
    })

# Criar um DataFrame com os dados
df_autores_palavras_chave = pd.DataFrame(dados_com_autores_palavras_chave)

# Salvar em um novo CSV com as colunas 'autores' e 'palavras_chave'
df_autores_palavras_chave.to_csv('artigos_com_autores_palavras_chave.csv', index=False, encoding='utf-8')

print("Autoria e palavras-chave extraídas e salvas em 'artigos_com_autores_palavras_chave.csv'")
