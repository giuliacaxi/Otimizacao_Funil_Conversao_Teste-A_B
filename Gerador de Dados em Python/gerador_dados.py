import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

num_usuarios = 5000
num_sessoes = 15000

print("Gerando dados de usuários...")

# Gerar a tabela de usuários

canais = ['Google Ads', 'Meta Ads', 'Orgânico', 'Email Marketing']
variantes = ['A','B']

usuarios_id = np.arange(1, num_usuarios + 1)
idades = np.random.randint(18, 65, size=num_usuarios)
generos = np.random.choice(['Masculino', 'Feminino', 'Outro'], size=num_usuarios, p=[0.48, 0.48, 0.04])
canais_escolhidos = np.random.choice(canais, size=num_usuarios, p=[0.4,0.3,0.2,0.1])
variantes_escolhidas = np.random.choice(variantes, size=num_usuarios, p=[0.5, 0.5])

df_usuarios = pd.DataFrame({
    'id_usuario': usuarios_id,
    'idade': idades,
    'genero': generos,
    'canal_escolhido': canais_escolhidos,
    'variante_escolhida': variantes_escolhidas
})
print("Gerando dados das sessões de navegação...")

# Gerar tabela: fato_sessoes

sessoes_id = np.arange(1, num_sessoes + 1)
usuarios_sessoes = np.random.choice(usuarios_id, size=num_sessoes)

# Criação de datas aleatórias para as sessões

data_inicio = datetime(2026, 2, 1)
datas_sessoes = [data_inicio + timedelta(days = int(np.random.randint(0, 30)),
                                         hours = int(np.random.randint(0, 24)),
                                         minutes = int(np.random.randint(0,60)))
                 for _ in range(num_sessoes)]

df_sessoes = pd.DataFrame({
    'id_sessao': sessoes_id,
    'id_usuario': usuarios_sessoes,
    'data_acesso': datas_sessoes
})

#Mapeamento da variante do usuário para a sessão para aplicar as probabilidades do Teste A/B

df_temp = df_sessoes.merge(df_usuarios[['id_usuario', 'variante_escolhida']], on = 'id_usuario', how = 'left')

conversoes = []
valores_gastos = []

for variante in df_temp['variante_escolhida']:
    if variante == 'A':
        taxa_conversao = 0.11
    else:
        taxa_conversao = 0.14
    
    conversao = np.random.choice([0,1], p=[1 - taxa_conversao, taxa_conversao])
    conversoes.append(conversao)
    
    if conversao == 1:
        valores_gastos.append(round(np.random.uniform(50.0, 350.0), 2))
    else:
        valores_gastos.append(0.0)

df_sessoes['conversao'] = conversoes
df_sessoes['valor_gasto'] = valores_gastos


print("Inserindo inconsistências propositais nos dados para simular situações reais...")

duplicadas = df_sessoes.sample(n=15, random_state=42)
df_sessoes = pd.concat([df_sessoes, duplicadas], ignore_index=True)

print("Salvando arquivos CSV...")

df_usuarios.to_csv('usuarios.csv', index=False)
df_sessoes.to_csv('sessoes.csv', index=False)

print("Dados gerados e salvos com sucesso!")

