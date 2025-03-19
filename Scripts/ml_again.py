import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

#Carregar os dados
df = pd.read_csv("C:/Users/BioInf_Andre/OneDrive - Universidade do Minho/Documentos/resultado_finalllll.csv")

#Identificar valores NaN
print("Valores NaN antes da imputação:\n", df.isna().sum())

#Normalizar os dados (para KNN não ser afetado por escalas diferentes)
colunas_numericas = df.select_dtypes(include=[np.number]).columns
scaler = StandardScaler()
df_scaled = df.copy()
df_scaled[colunas_numericas] = scaler.fit_transform(df[colunas_numericas])

#Aplicar KNN Imputer (K=5 por padrão)
imputer = KNNImputer(n_neighbors=5)
df_imputed_scaled = df_scaled.copy()
df_imputed_scaled[colunas_numericas] = imputer.fit_transform(df_scaled[colunas_numericas])

#Desnormalizar os dados para voltar à escala original
df_imputed = df.copy()
df_imputed[colunas_numericas] = scaler.inverse_transform(df_imputed_scaled[colunas_numericas])

#Ajustar formatos:
#GDP com 5 casas decimais
#Valores imputados (antes NaN) como inteiros

colunas_gdp = ["GDP_2012", "GDP_2015", "GDP_2018"]
colunas_imputadas = df_imputed.columns[df.isna().any()].tolist()

df_imputed[colunas_gdp] = df_imputed[colunas_gdp].applymap(lambda x: round(x, 5))  # 5 casas decimais para GDP
df_imputed[colunas_imputadas] = df_imputed[colunas_imputadas].applymap(lambda x: int(round(x)))  # Sem casas decimais para imputados

#Verificar se os NaN foram preenchidos
print("\nValores NaN após a imputação:\n", df_imputed.isna().sum())

df_imputed.to_csv("C:/Users/BioInf_Andre/OneDrive - Universidade do Minho/Documentos/gdp_pisa_no_NA.csv", index=False)
print("\n✅ Ficheiro 'dados_imputados.csv' salvo com sucesso!")
