# Otimização do Funil de Conversão e Análise de Teste A/B 🚀

**Observação**: Para rodar este projeto localmente, clone o repositório, crie um arquivo .env na raiz baseado no modelo .env.example e insira suas credenciais locais do MySQL.

## 1. Contexto de Negócio
Este projeto simula o papel de um Analista de Dados atuando como ponte entre o time de Produto/Marketing e as soluções de dados da companhia. 

**O Problema:** O time de produto implementou um novo layout no botão de checkout (Variante B) com o objetivo de aumentar a conversão de vendas. Como analista, meu papel foi estruturar os dados brutos, garantir a integridade das informações, validar estatisticamente o resultado do teste e criar um dashboard de BI para suporte à tomada de decisão.

### KPIs Cadastrados:
* **Taxa de Conversão (CR):** Total de conversões / Total de sessões.
* **Receita Média por Usuário (ARPU):** Faturamento total / Total de usuários únicos.

---

## 2. Arquitetura e Ferramentas
* **Python:** Utilizado para geração de dados sintéticos realistas e tratamento inicial (Bibliotecas: `pandas`, `numpy`).
* **MySQL (v8.0+):** Banco de dados relacional utilizado para armazenamento, modelagem (Star Schema) e consultas avançadas utilizando Joins e CTEs.
* **Power BI:** Para visualização de dados e construção do dashboard de negócios.

## 3. Desenvolvimento do código de Análise
* Criei um pipeline onde o Python serve como uma camada de automação estatística. Ele puxa os dados limpos e agregados via query SQL do MySQL, isola as métricas de conversão e calcula dinamicamente o teste Qui-Quadrado de Independência através da biblioteca SciPy, gerando um veredito de negócio baseado em significância estatística, mitigando o risco de o time tomar decisões com base no achismo
