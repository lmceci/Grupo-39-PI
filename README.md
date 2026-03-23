# Grupo-39-PI
# 📊 Projeto de Análise de Dados: Impacto da COVID-19 no Brasil

Este projeto faz parte da disciplina **Projeto Integrador: Desenvolvimento Low Code em Ciência de Dados** do curso de Análise e Desenvolvimento de Sistemas (Senac EAD). O objetivo é realizar o processo completo de ETL (Extração, Transformação e Carga) e criar um dashboard interativo para visualização dos impactos da pandemia no território nacional.


## 👥 Integrantes do Grupo
* **João Marcos Ribeiro**
* **Cecília Luiza de Moraes da Rosa**
* **Victor Hugo Silva Reis**
* **Victor Hugo Ferreira de Andrade**
* **Fernando Oliveira Marques**
* **Jonatas Viana Rodrigues**
* **Ruan Pereira**


## 📌 Tema e Contexto
Análise detalhada da evolução temporal, distribuição geográfica e taxas de letalidade da COVID-19 no Brasil. O projeto visa transformar dados brutos governamentais em insights visuais que facilitem a compreensão da crise sanitária.


## 🎯 Objetivos da Análise
* Identificar os estados com maior volume de casos e óbitos.
* Analisar os períodos de pico (ondas) da pandemia.
* Calcular e monitorar a taxa de mortalidade em tempo real.
* Proporcionar uma ferramenta interativa para comparação entre diferentes regiões e períodos.


## 🗂 Base de Dados
Utilizamos registros oficiais de casos e mortes por COVID-19 no Brasil.
* **Fonte sugerida:** [Brasil.io](https://brasil.io/dataset/covid19/caso_full/) ou Painel Coronavírus (Ministério da Saúde).
* **Dados principais:** Datas, Estados (UF), Casos Confirmados, Óbitos Acumulados e População Estimada.


## 🛠 Estrutura do Repositório
Seguindo as diretrizes da disciplina, o projeto está organizado da seguinte forma:

* 📂 **/data**: Contém os arquivos de dados brutos (`base_original.csv`) e os dados após o tratamento (`base_tratada.csv`).
* 📂 **/src**: Contém os scripts Python responsáveis pelo processo de limpeza e transformação (ETL).
* 📂 **/app**: Contém o código-fonte do dashboard interativo desenvolvido em Streamlit.


## 🔄 Planejamento de Tarefas

### 1. Tratamento e Limpeza (ETL)
**Responsáveis:** João Marcos e Cecília Rosa
* Padronização de formatos de data.
* Tratamento de valores nulos e inconsistentes.
* Criação de métricas (Taxa de Mortalidade = Óbitos / Casos).

### 2. Análise Exploratória
**Responsáveis:** Victor Hugo Reis e Fernando Marques
* Identificação de padrões sazonais.
* Ranking de criticidade por estado.

### 3. Desenvolvimento do Dashboard
**Responsáveis:** Jonatas Viana, Victor Hugo Andrade e Ruan Pereira
* Criação de visualizações (Linhas, Barras e KPIs).
* Implementação de filtros de usuário (UF e Data).


## 🚀 Tecnologias Utilizadas
* **Python**: Linguagem base.
* **Pandas**: Manipulação e tratamento de dados.
* **Streamlit**: Framework para criação do dashboard interativo.
* **GitHub**: Controle de versão e documentação.


