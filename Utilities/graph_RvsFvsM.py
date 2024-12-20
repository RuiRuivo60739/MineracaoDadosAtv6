import pandas as pd
import plotly.express as px

# Carregar o conjunto de dados
file_path = r'C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\Steps\online_retail_II_cleaned_with_scores_clusters_churnRisk_description.csv'  # Replace with the actual file path
data = pd.read_csv(file_path)

# Calcular o numero de elementos por cluster
rfm_counts = data.groupby(['Recency_score', 'Frequency_score', 'Monetary_score']).size().reset_index(name='contagem_por_cluster')

# Adicionamos a contagem aos dados originais
data = pd.merge(data, rfm_counts, on=['Recency_score', 'Frequency_score', 'Monetary_score'])

# Aplicamos uma escala para os pontos serem mais visiveis
data['contagem_por_cluster_escala'] = data['contagem_por_cluster'] * 30  # Fator de escala

# Criar o plot
fig = px.scatter_3d(
    data,
    x='Recency_score',
    y='Frequency_score',
    z='Monetary_score',
    color='ChurnRisk',  # A cor é baseada no risco de churn
    size='contagem_por_cluster_escala',  # Tamanho dos pontos é baseado na contagem
    size_max=100,  # Maximum marker size
    title='3D Scatter Plot: Contagem de elementos e risco de abandonamento',
    labels={
        'Recency_score': 'Recency Score',
        'Frequency_score': 'Frequency Score',
        'Monetary_score': 'Monetary Score',
        'ChurnRisk': 'Churn Risk',
        'contagem_por_cluster': 'Contagem por Cluster'
    },

    color_continuous_scale='RdYlGn_r'  # Usamos o gradiente vermelho para verde (vermelho -> risco alto, verde -> risco baixo)
)

# Utilizamos marcadores quadrados
fig.update_traces(marker=dict(symbol='square', opacity=0.8))

# Customize the layout
fig.update_layout(scene=dict(
    xaxis_title='Recency Score',
    yaxis_title='Frequency Score',
    zaxis_title='Monetary Score'
))

# Mostrar o plot
fig.show()

# Opcional para gravar como html
# fig.write_html("3D_Cluster_Plot_Count_and_ChurnRisk.html")
