import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Função para carregar e preparar os dados
def carregar_dados(arquivo):
    print(f"Carregando dados do arquivo {arquivo}...")
    try:
        df = pd.read_csv("C:/Users/BioInf_Andre/OneDrive - Universidade do Minho/Documentos/pisa_2006-2018.csv")
        print(f"Dataset carregado com sucesso. Formato: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para converter valores NA para NaN do pandas
def tratar_na_valores(df):
    print("Convertendo valores 'NA' para NaN...")
    df_processado = df.copy()
    # Converte strings 'NA' para valores NaN do pandas
    df_processado.replace('NA', np.nan, inplace=True)
    # Converte as colunas Score e Rank para números
    df_processado['Score'] = pd.to_numeric(df_processado['Score'], errors='coerce')
    df_processado['Rank'] = pd.to_numeric(df_processado['Rank'], errors='coerce')
    
    # Verifica quantos valores NA existem
    na_count = df_processado['Score'].isna().sum()
    total = len(df_processado)
    print(f"Total de valores NA em Score: {na_count} de {total} ({na_count/total*100:.2f}%)")
    
    return df_processado

# Função para preparar os dados para o modelo
def preparar_dados_modelo(df):
    print("Preparando dados para o modelo...")
    # Cria cópias das colunas categóricas para codificação
    df_modelo = df.copy()
    
    # Codifica variáveis categóricas
    encoders = {}
    for coluna in ['Subject', 'Country']:
        encoders[coluna] = LabelEncoder()
        df_modelo[f'{coluna}_encoded'] = encoders[coluna].fit_transform(df_modelo[coluna])
    
    return df_modelo, encoders

# Função para treinar o modelo de machine learning
def treinar_modelo(df_modelo):
    print("Treinando modelo de RandomForest...")
    
    # Filtra apenas as linhas com Score não-nulo para treinar o modelo
    mask_treino = df_modelo['Score'].notna()
    
    # Verifica se há dados suficientes para treinar
    if mask_treino.sum() < 10:
        print("Erro: Dados insuficientes para treinar o modelo")
        return None
    
    # Seleciona features e target apenas das linhas com Score não-nulo
    X_treino = df_modelo.loc[mask_treino, ['Year', 'Subject_encoded', 'Country_encoded']]
    y_treino = df_modelo.loc[mask_treino, 'Score']
    
    print(f"Treinando com {len(X_treino)} amostras")
    
    # Treina o modelo RandomForest
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_treino, y_treino)
    
    # Faz uma validação simples (usando os mesmos dados por simplicidade)
    y_pred = modelo.predict(X_treino)
    rmse = np.sqrt(mean_squared_error(y_treino, y_pred))
    print(f"RMSE do modelo nos dados de treino: {rmse:.2f}")
    
    return modelo

# Função para preencher os valores ausentes
def preencher_valores_ausentes(df_original, df_modelo, modelo):
    print("Preenchendo valores ausentes...")
    df_preenchido = df_original.copy()
    
    # Identifica linhas com Score NA
    mask_na = df_modelo['Score'].isna()
    na_count = mask_na.sum()
    
    if na_count == 0:
        print("Não há valores ausentes para preencher.")
        return df_preenchido
    
    print(f"Preenchendo {na_count} valores ausentes...")
    
    # Prepara os dados para predição
    X_pred = df_modelo.loc[mask_na, ['Year', 'Subject_encoded', 'Country_encoded']]
    
    # Prediz os valores ausentes
    scores_preditos = modelo.predict(X_pred)
    
    # Arredonda os scores para inteiros
    scores_preditos = np.round(scores_preditos).astype(int)
    
    # Cria uma lista dos índices originais
    indices_na = df_modelo.index[mask_na].tolist()
    
    # Preenche os valores ausentes no DataFrame original
    for i, idx in enumerate(indices_na):
        df_preenchido.at[idx, 'Score'] = scores_preditos[i]
    
    return df_preenchido

# Função principal
def main():
    # Nome do arquivo de entrada e saída
    arquivo_entrada = 'pisa_dataset.csv'
    arquivo_saida = 'pisa_dataset_preenchido.csv'
    
    try:
        # Carrega os dados
        df_original = carregar_dados(arquivo_entrada)
        if df_original is None:
            return
        
        # Trata valores NA
        df_processado = tratar_na_valores(df_original)
        
        # Prepara os dados para o modelo
        df_modelo, encoders = preparar_dados_modelo(df_processado)
        
        # Treina o modelo
        modelo = treinar_modelo(df_modelo)
        if modelo is None:
            return
        
        # Preenche os valores ausentes
        df_preenchido = preencher_valores_ausentes(df_original, df_modelo, modelo)
        
        # Salva o resultado em um novo arquivo
        df_preenchido.to_csv("C:/Users/BioInf_Andre/OneDrive - Universidade do Minho/Documentos/pisa_imputed.csv", index=False)
        print(f"Dataset com valores preenchidos salvo como '{arquivo_saida}'")
        
        # Mostra estatísticas
        total_linhas = len(df_original)
        na_originais = df_processado['Score'].isna().sum()
        print(f"\nEstatísticas:")
        print(f"Total de linhas no dataset: {total_linhas}")
        print(f"Valores NA no score original: {na_originais} ({na_originais/total_linhas*100:.2f}%)")
        print(f"Valores preenchidos pelo modelo: {na_originais}")
        
    except Exception as e:
        print(f"Erro ao processar o dataset: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()