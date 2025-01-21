
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#############################################################
#               RETORNA TODOS OS DFS PELO ANO               #
#############################################################

def filter_columns_multiple(df, filters: list):
    # Criar um dicionário para armazenar os dataframes filtrados
    filtered_dfs = {filter_: [] for filter_ in filters}
    
    # Iterar pelas colunas do dataframe apenas uma vez
    for column in df.columns:
        for filter_ in filters:
            if filter_ in column:
                filtered_dfs[filter_].append(column)
                break  # Evitar adicionar a mesma coluna a múltiplos filtros
    
    # Criar dataframes separados para cada filtro
    result_dfs = {filter_: df[columns] for filter_, columns in filtered_dfs.items()}
    
    return result_dfs

