# 🚑 Projeto Integrador: eficiência e cobertura do SAMU 192

Este projeto faz parte da disciplina **Projeto Integrador: Desenvolvimento Low Code em Ciência de Dados** do curso de Análise e Desenvolvimento de Sistemas (Senac EAD). O foco desta análise é transformar dados brutos do Serviço de Atendimento Móvel de Urgência (SAMU).

---

## 👥 Integrantes do grupo

* **João Marcos Ribeiro**
* **Cecília Luiza de Moraes da Rosa**
* **Victor Hugo Silva Reis**
* **Victor Hugo Ferreira de Andrade**
* **Fernando Oliveira Marques**
* **Jonatas Viana Rodrigues**
* **Ruan Pereira**



## 📌 Relevância social
O SAMU 192 é um componente fundamental da Rede de Atenção às Urgências no Brasil. Analisar seus indicadores de desempenho é vital para identificar gargalos no atendimento público, avaliar a cobertura regional e propor melhorias que podem, em última instância, salvar mais vidas através da otimização do tempo de resposta.


## 🎯 Objetivos da análise
* Avaliar o percentual de cobertura do SAMU por região e estado.
* Identificar municípios com indicadores de desempenho abaixo da média nacional.
* Monitorar a evolução dos atendimentos ao longo do tempo.
* Criar um dashboard interativo que facilite a visualização da eficiência do serviço para gestores públicos.



## 🗂 Base de dados
Os dados foram extraídos do **Portal de dados abertos do Ministério da Saúde**.
* **Arquivo utilizado:** `samuppc.csv`
* **Principais colunas:** Município, UF, Região, Indicador Calculado e Data de Competência.



## 🛠 Estrutura do repositório
Conforme as diretrizes da disciplina, o projeto está organizado da seguinte forma:

* 📂 **/data**: Contém a base de dados original (`samuppc.csv`) e futuramente a base tratada.
* 📂 **/src**: Contém o script `etl.py` para limpeza e transformação dos dados.
* 📂 **/app**: Contém o arquivo `dashboard.py` para a interface visual em Streamlit.



## 🔄 Planejamento de tarefas

### 1. Tratamento e limpeza (ETL)
* Responsáveis: Cecília Rosa e João Marcos
* Filtragem de dados por competência (ano/mês).
* Padronização de nomes de municípios e estados.

### 2. Análise exploratória
* Responsáveis: Victor Hugo Reis e Victor Hugo Andrade
* Comparação de indicadores entre as regiões do Brasil.
* Identificação de tendências de crescimento do serviço.

### 3. Desenvolvimento do dashboard
* Responsáveis: Fernando Marques, Jonatas Rodrigues e Ruan Pereira
* Criação de mapas de calor e gráficos de desempenho por UF.
* Implementação de filtros por região de saúde.


## 🚀 Tecnologias utilizadas
* **Python / Pandas**: Processamento de dados.
* **Streamlit**: Criação da aplicação visual (Low Code).
* **GitHub**: Gestão de código e documentação.


