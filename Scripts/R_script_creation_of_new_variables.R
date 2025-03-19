install.packages("openxlsx")
library(dplyr)
library(openxlsx)

#1. Carregar os dados
caminho_ficheiro <- "C:\\Users\\joama\\OneDrive\\Ambiente de Trabalho\\Big Data\\big data Trabalho\\gdp_pisa_no_NA.csv"
gdp_pisa_no_NA <- read.csv(caminho_ficheiro)

#2. Criar novas colunas com médias de cada disciplina para os 3 anos arredondadas a 3 casas decimais
gdp_pisa_no_NA <- gdp_pisa_no_NA %>%
  mutate(
    Means_Maths = round(rowMeans(select(., Maths_2012, Maths_2015, Maths_2018), na.rm = TRUE), 3),
    Means_Science = round(rowMeans(select(., Science_2012, Science_2015, Science_2018), na.rm = TRUE), 3),
    Means_Reading = round(rowMeans(select(., Reading_2012, Reading_2015, Reading_2018), na.rm = TRUE), 3)
  )


# Criar novas colunas com as médias de cada ano para as 3 disciplinas arredondadas a 3 casas decimais
gdp_pisa_no_NA <- gdp_pisa_no_NA %>%
  mutate(
    Mean_2012 = round(rowMeans(select(., contains("2012") & !contains("GDP"))), 3),
    Mean_2015 = round(rowMeans(select(., contains("2015") & !contains("GDP"))), 3),
    Mean_2018 = round(rowMeans(select(., contains("2018") & !contains("GDP"))), 3)
  )


#3. Guardar o dataset atualizado
write.xlsx(gdp_pisa_no_NA, "DSF.xlsx", rowNames = FALSE)






