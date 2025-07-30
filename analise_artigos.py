import pandas as pd

# Carregar o CSV que foi gerado anteriormente
df_periodicos = pd.read_csv("periodicos_por_pesquisador.csv", encoding="utf-8")

# Exibir as primeiras linhas do DataFrame para verificar a estrutura
print("Primeiras linhas do DataFrame:")
print(df_periodicos.head())

# 1. Análise do número de artigos por edição (ano, volume e número)
artigos_por_edicao = df_periodicos.groupby(['ano', 'volume', 'numero']).size().reset_index(name='num_artigos')

# Exibindo a análise de artigos por edição
print("\nNúmero de artigos por edição (ano, volume, número):")
print(artigos_por_edicao)

# 2. Análise do número total de artigos por ano
artigos_por_ano = df_periodicos.groupby('ano').size().reset_index(name='num_artigos_por_ano')

# Exibindo a análise do número total de artigos por ano
print("\nNúmero total de artigos por ano:")
print(artigos_por_ano)

# Salvar os resultados de análise em um novo arquivo CSV (se desejar)
artigos_por_edicao.to_csv("artigos_por_edicao.csv", index=False, encoding="utf-8")
artigos_por_ano.to_csv("artigos_por_ano.csv", index=False, encoding="utf-8")

print("\nAnálises salvas em 'artigos_por_edicao.csv' e 'artigos_por_ano.csv'.")
