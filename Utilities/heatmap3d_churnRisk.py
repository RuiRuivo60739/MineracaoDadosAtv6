import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import plotly.graph_objects as go

# Ler o ficheiro CSV
file_path = r'C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\Steps\online_retail_II_cleaned_with_scores_clusters_churnRisk_description.csv'


data = pd.read_csv(file_path)

# Preparar os dados
x = data['Recency_score']
y = data['Frequency_score']
z = data['ChurnRisk']


# Criar a grade para interpolação
grid_x, grid_y = np.meshgrid(
    np.linspace(x.min(), x.max(), 100),
    np.linspace(y.min(), y.max(), 100)
)

grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')
grid_rfm = griddata((x, y), z, (grid_x, grid_y), method='cubic')

# Criar gráfico interativo 3D com Plotly
fig = go.Figure(data=[
    go.Surface(
        z=grid_z,
        x=grid_x,
        y=grid_y,
        surfacecolor=grid_rfm,
        colorscale='RdYlGn',
        colorbar=dict(title='RFM Score')
    )
])

fig.update_layout(
    title='Risco de Churn ',
    scene=dict(
        xaxis_title='Recency Score',
        yaxis_title='Frequency Score',
        zaxis_title='Monetary Score'
    )
)

fig.show()
