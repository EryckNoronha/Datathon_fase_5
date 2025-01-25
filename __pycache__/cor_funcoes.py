
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns



#############################################################
#               RETORNA TODOS OS DFS PELO ANO               #
#############################################################

def filter_columns_multiple(df, filters: list):
    """
    Separa as colunas de um DataFrame em múltiplos DataFrames, com base nos padrões especificados.

    Parâmetros:
    - df (pd.DataFrame): O DataFrame a ser filtrado.
    - filters (list): Lista de strings que representam os padrões para separar as colunas.

    Retorna:
    - dict: Um dicionário onde cada chave é um filtro da lista, e o valor é um DataFrame contendo as colunas que correspondem a esse filtro.
    """
    # Inicializa um dicionário para armazenar as colunas correspondentes a cada filtro
    filtered_dfs = {filter_: [] for filter_ in filters}
    
    # Itera pelas colunas do DataFrame uma vez
    for column in df.columns:
        for filter_ in filters:
            # Se o nome da coluna contém o padrão atual, adiciona ao filtro correspondente
            if filter_ in column:
                filtered_dfs[filter_].append(column)
                break  # Garante que uma coluna não seja associada a múltiplos filtros
    
    # Cria DataFrames separados para cada filtro, contendo apenas as colunas relevantes
    result_dfs = {filter_: df[columns] for filter_, columns in filtered_dfs.items()}
    
    return result_dfs


#############################################################
#               FILTRO DE COLUNAS, EXCLUSÃO POR NOMES       #
#############################################################

def filter_columns(df, filters: list):
    """
    Filtra as colunas de um DataFrame do pandas, removendo aquelas
    cujo nome contenha qualquer padrão especificado na lista 'filters'.
    
    Parâmetros:
    - df (pd.DataFrame): O DataFrame a ser filtrado.
    - filters (list): Lista de strings que representam os padrões a serem removidos.
    
    Retorna:
    - pd.DataFrame: Um DataFrame com as colunas filtradas.
    """
    # Inicializa uma lista para indicar quais colunas serão mantidas
    selected_columns = [True] * len(df.columns)  # Todas as colunas começam como "selecionadas"

    # Itera sobre cada coluna do DataFrame
    for index, column in enumerate(df.columns):
        # Verifica se o nome da coluna contém algum dos filtros
        if any(filter in column for filter in filters):
            selected_columns[index] = False  # Marca a coluna como não selecionada (False)
    
    # Retorna apenas as colunas que estão marcadas como True
    return df[df.columns[selected_columns]]

#############################################################
#                    REMOVE LINHAS NaN                      #
#############################################################
def cleaning_dataset(df):
    """
    Limpa um DataFrame removendo linhas que possuem valores ausentes (NaN) de maneira específica.
    
    Passos:
    1. Remove linhas em que **todas** as colunas (exceto 'NOME') têm valores NaN.
    2. Remove linhas que contêm apenas valores NaN em todas as colunas.

    Parâmetros:
    - df (pd.DataFrame): O DataFrame a ser limpo.

    Retorna:
    - pd.DataFrame: O DataFrame limpo.
    """
    # Remove linhas onde todas as colunas, exceto 'NOME', têm valores NaN
    _df = df.dropna(subset=df.columns.difference(['NOME']), how='all')
    
    # Remove linhas que possuem apenas valores NaN (em todas as colunas)
    _df = _df[~_df.isna().all(axis=1)]
    
    return _df


#############################################################
#        COMPARAÇÃO DE AUSENCIA DE ALUNOS EM DFS            #
#############################################################

def calcular_desistentes(df_anterior, df_atual, coluna_nome):
    """
    Retorna uma lista de alunos que estavam no df_anterior, mas não estão no df_atual.
    
    Args:
        df_anterior (pd.DataFrame): DataFrame do período anterior.
        df_atual (pd.DataFrame): DataFrame do período atual.
        coluna_nome (str): Nome da coluna que contém os nomes dos alunos.
    
    Returns:
        list: Lista de nomes dos alunos desistentes.
    """
    # Converte os nomes em sets para facilitar a comparação
    set_anterior = set(df_anterior[coluna_nome])
    set_atual = set(df_atual[coluna_nome])
    
    # Calcula a diferença (alunos que não migraram para o próximo ano)
    desistentes = list(set_anterior - set_atual)
    return desistentes

#############################################################
#              CONVERSÃO COLUNAS E CASAS DECIMAIS           #
#############################################################

def converter_e_arredondar(df, colunas, casas_decimais=2):
    """
    Converte as colunas especificadas de um DataFrame para float e arredonda os valores.

    Parâmetros:
    - df (pd.DataFrame): DataFrame original.
    - colunas (list): Lista com os nomes das colunas a serem convertidas.
    - casas_decimais (int): Número de casas decimais para arredondar (padrão: 2).

    Retorna:
    - pd.DataFrame: DataFrame com as colunas convertidas e arredondadas.
    """
    try:
        # Iterar pelas colunas para conversão
        for coluna in colunas:
            if coluna in df.columns:
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce').round(casas_decimais)
        print(f"Colunas {colunas} foram convertidas para float e arredondadas para {casas_decimais} casas decimais.")
    except Exception as e:
        print(f"Erro ao converter ou arredondar colunas: {e}")
    return df




#-------------------------------GRAFICOS-----------------------------------------------------------------#

#############################################################
#               GRAFICO DE BARRAS - CONTAGEM                #
#############################################################
def plot_exact_counter(size, text, x, y, df) -> None:
    """
    Gera um gráfico de barras com contagens específicas, incluindo os valores exatos de cada barra.

    Parâmetros:
    - size (tuple): Define o tamanho da figura no formato (largura, altura).
    - x (str): O rótulo do eixo X.
    - y (pd.Series): Os valores de contagem (índice para rótulos das categorias e valores para as contagens).
    - df (pd.DataFrame): O DataFrame contendo os dados (não utilizado na lógica atual, mas pode ser incluído para extensibilidade).

    Retorna:
    - None: Apenas exibe o gráfico.
    """
    # Define o tamanho do gráfico
    plt.figure(figsize=size)
    
    # Cria um gráfico de barras
    barplot = plt.bar(y.index, y.values)
    
    # Define o rótulo do eixo X
    plt.xlabel(x)
    
    # Define o rótulo do eixo Y como 'Count'
    plt.ylabel('Count')

    # Adiciona os valores exatos no topo de cada barra
    for index, value in enumerate(y.values):
        plt.text(index, value, round(value, 2), color='black', ha="center")

    # Adiciona o título ao gráfico
    plt.title(f'{text}')
    
    # Exibe o gráfico
    plt.show()

#############################################################
#                      MATRIZ DE CORRELAÇÃO                 #
#############################################################

def analyse_corr(df):
    """
    Analisa e exibe a matriz de correlação de um DataFrame utilizando um mapa de calor.

    Passos:
    1. Converte todas as colunas possíveis do DataFrame para valores numéricos.
    2. Calcula a matriz de correlação entre as colunas numéricas.
    3. Exibe um mapa de calor da matriz de correlação.

    Parâmetros:
    - df (pd.DataFrame): O DataFrame a ser analisado.

    Retorna:
    - None: Apenas exibe o mapa de calor.
    """
    # Converte todas as colunas para valores numéricos (coercendo erros para NaN)
    df = df.apply(pd.to_numeric, errors='coerce')

    # Calcula a matriz de correlação
    corr_matrix = df.corr()

    # Configura o tamanho da figura
    plt.figure(figsize=(10, 8))

    # Cria o mapa de calor da matriz de correlação
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)

    # Exibe o gráfico
    plt.show()


#############################################################
#           BARRAS COMPARATIVAS DE METRICAS                 #
#############################################################

def comparar_colunas_por_metrica(df_alunos_3_anos, dfs_somente_anos, anos):
    """
    Cria um único gráfico de barras agrupadas comparando todas as colunas correspondentes à mesma métrica
    de diferentes anos entre os DataFrames `df_alunos_3_anos` e `dfs_somente_anos`.

    Args:
        df_alunos_3_anos (pd.DataFrame): DataFrame contendo os dados acumulados de todos os anos.
        dfs_somente_anos (dict): Dicionário com os DataFrames de cada ano (exemplo: {'2020': df_somente_2020}).
        anos (list): Lista de anos a serem comparados.
    """
    # Identificar as métricas comuns (prefixos das colunas, ignorando o ano)
    colunas_prefixos = ['ALTO_AVALIACAO', 'ENGAJAMENTO', 'PISICOSSOCIAL', 'APRENDIZAGEM']
    
    # Lista de cores para variar a cada gráfico
    cores = ['blue', 'green', 'red', 'orange']
    
    for idx, prefixo in enumerate(colunas_prefixos):
        # Listas para armazenar os valores médios por ano
        medias_somente = []
        medias_alunos = []
        labels_anos = []
        
        for ano in anos:
            coluna = f"{prefixo}_{ano}"
            
            # Pega o DataFrame do respectivo ano
            df_somente = dfs_somente_anos.get(ano)
            
            if df_somente is not None and coluna in df_somente.columns and coluna in df_alunos_3_anos.columns:
                # Calcular a média para o DataFrame de alunos somente daquele ano
                media_somente = df_somente[coluna].mean()
                medias_somente.append(media_somente)
                
                # Calcular a média para o DataFrame acumulado (df_alunos_3_anos)
                media_alunos = df_alunos_3_anos[coluna].mean()
                medias_alunos.append(media_alunos)
                
                labels_anos.append(ano)
            else:
                print(f"Coluna {coluna} não encontrada em algum dos DataFrames.")
        
        # Criar o gráfico agrupado
        x = np.arange(len(labels_anos))  # Posições no eixo X
        largura = 0.25  # Reduzir a largura das barras para deixá-las mais finas
        
        plt.figure(figsize=(12, 8))  # Aumentar o tamanho da figura para acomodar as barras finas
        
        # Barras para df_somente_{ano}
        plt.bar(x - largura/2, medias_somente, largura, label='Somente Alunos', color=cores[idx % len(cores)])  # Cor dinâmica
        
        # Barras para df_alunos_3_anos
        plt.bar(x + largura/2, medias_alunos, largura, label='Alunos 3 Anos', color=cores[(idx + 1) % len(cores)])  # Cor dinâmica
        
        # Configurações do gráfico
        plt.xticks(x, [f"{prefixo}_{ano}" for ano in labels_anos], rotation=45, ha='right')
        plt.ylabel('Média')
        plt.title(f'Comparação da Métrica: {prefixo}')
        plt.legend()
        plt.tight_layout()
        
        # Exibir o gráfico
        plt.show()