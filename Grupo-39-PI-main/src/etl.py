import pandas as pd

def carregar_dados_samu():
    # Carrega a base oficial do SAMU que está na pasta data
    caminho = 'data/samuppc.csv'
    df = pd.read_csv(caminho)
    
    # Exemplo de limpeza: remover colunas que não usaremos
    # (Isso será aprofundado na Etapa 2)
    df_limpo = df[['no_municipio', 'sg_uf', 'no_regiao_brasil', 'vl_indicador_calculado_mun', 'dt_competencia']]
    
    return df_limpo

if __name__ == "__main__":
    dados = carregar_dados_samu()
    print("Dados do SAMU carregados com sucesso!")
    print(dados.head())
