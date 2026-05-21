import os
from dotenv import load_dotenv
import mysql.connector
import numpy as np
import scipy.stats as stats
import pandas as pd

load_dotenv()

print("Conectando ao banco de dados MySQL...")

# Ajuste os valores abaixo de acordo com as configurações do seu banco de dados MySQL :)
conexao = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME')
)

query_mysql = """
WITH sessoes_limpas AS(
	
    SELECT DISTINCT * FROM sessoes

),

metricas_por_variante AS (

	SELECT
		u.variante_escolhida,
        COUNT(DISTINCT u.id_usuario) AS total_usuarios,
        COUNT(s.id_sessao) AS total_sessoes,
        SUM(s.conversao) AS total_conversoes,
        SUM(s.valor_gasto) AS receita_total
	FROM usuarios u
    LEFT JOIN sessoes_limpas s ON u.id_usuario = s.id_usuario
    GROUP BY u.variante_escolhida

)

SELECT * FROM metricas_por_variante;
"""

print("Executando consulta SQL para obter as métricas por variante...")

df_metricas = pd.read_sql(query_mysql, conexao)
conexao.close()

print("Dados obtidos com sucesso! Aqui estão as métricas por variante:")
print(df_metricas)

# Extração dos valores dinamicamente para o teste A/B :)

dados_a = df_metricas[df_metricas['variante_escolhida'] == 'A'].iloc[0]
dados_b = df_metricas[df_metricas['variante_escolhida'] == 'B'].iloc[0]

sessoes_a = dados_a['total_sessoes']
conversoes_a = dados_a['total_conversoes']
sem_conversao_a = sessoes_a - conversoes_a

sessoes_b = dados_b['total_sessoes']
conversoes_b = dados_b['total_conversoes']
sem_conversao_b = sessoes_b - conversoes_b

# Criando a tabela de contingência para o teste qui-quadrado :)
# O que é o teste qui-quadrado?

#É uma ferramenta estatística usada para verificar se existe uma associação significativa entre duas variáveis categóricas. 
#No contexto de um teste A/B, ele pode ser usado para comparar as taxas de conversão entre as variantes A e B, ajudando a determinar se as diferenças observadas são estatisticamente significativas ou se podem ser atribuídas ao acaso.

tabela_contingencia = np.array([
    [conversoes_a, sem_conversao_a],
    [conversoes_b, sem_conversao_b]])

chi2, p_valor, dof, esperados = stats.chi2_contingency(tabela_contingencia)

taxa_a = (conversoes_a / sessoes_a) * 100
taxa_b = (conversoes_b / sessoes_b) * 100

print("\n------------------------------------")
print("RESULTADOS DO TESTE A/B:")
print("\n------------------------------------")
print(f"Taxa de Conversão Variante A: {taxa_a:.2f}%")
print(f"Taxa de Conversão Variante B: {taxa_b:.2f}%")
print(f"p-valor do teste qui-quadrado: {p_valor:.6f}")
print("\n------------------------------------")



alfa = 0.05
print("\nAnálise de significância:")
if p_valor < alfa:
    print("Estatisticamente significativo! Rejeitamos a hipótese nula. A variante B tem uma taxa de conversão significativamente diferente da variante A.")
else:
    print("Não é estatisticamente significativo. Não rejeitamos a hipótese nula. Não há evidências suficientes para afirmar que a variante B tem uma taxa de conversão diferente da variante A.")