import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, ListedColormap
import matplotlib.colors as mcolors

# Ler o ficheiro CSV
file_path = r'C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\Steps\online_retail_II_cleaned_with_scores_clusters_churnRisk_description.csv'
data = pd.read_csv(file_path)

# Definir os segmentos detalhados
def detailed_segment_customer(recency_score, frequency_score, monetary_score, churn_risk, cluster, churn_risk_description):
    return f"{cluster}\nR: {recency_score}, F: {frequency_score}, M: {monetary_score}\nChurn Risk: {churn_risk}\n{churn_risk_description}"

# Adicionar os segmentos detalhados ao dataset
data['Segmentos de Clientes'] = data.apply(
    lambda row: detailed_segment_customer(
         row['Recency_score'], row['Frequency_score'], row['Monetary_score'], row['ChurnRisk'],row['cluster'], row['ChurnRisk_description']
    ), axis=1
)

# Criar matriz de churn_risk
churn_risk_matrix = data.pivot_table(
    index='Frequency_score',
    columns='Monetary_score',
    values='ChurnRisk',
    aggfunc='mean'
)

# Criar tabela de rótulos detalhados
heatmap_labels = data.pivot_table(
    index='Frequency_score',
    columns='Monetary_score',
    values='Segmentos de Clientes',
    aggfunc=lambda x: x.mode()[0] if not x.empty else None
)

# Normalizar os valores de churn_risk para usar no gradiente de cores
norm = Normalize(vmin=churn_risk_matrix.min().min(), vmax=churn_risk_matrix.max().max())
cmap = plt.cm.RdYlGn_r  # Vermelho (alto risco) -> Verde (baixo risco)

# Configurar o mapa de calor
fig, ax = plt.subplots(figsize=(14, 8))

# Criar os blocos de 1x1 com cores baseadas no churn_risk
for i in range(churn_risk_matrix.shape[0]):
    for j in range(churn_risk_matrix.shape[1]):
        churn_risk_value = churn_risk_matrix.iloc[i, j]
        if pd.notna(churn_risk_value):
            color = cmap(norm(churn_risk_value))
            rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color=color, edgecolor='black')  # Adicionar bordas pretas
            ax.add_patch(rect)


# Configuração dos eixos
ax.set_xticks(np.arange(churn_risk_matrix.shape[1]))
ax.set_xticklabels(churn_risk_matrix.columns, rotation=45)
ax.set_yticks(np.arange(churn_risk_matrix.shape[0]))
ax.set_yticklabels(churn_risk_matrix.index)
ax.set_xlabel('Monetary Score')
ax.set_ylabel('Frequency Score')
ax.set_title('Heatmap de Segmentos de Clientes (gradiente de risco de churn)')

# Adicionar rótulos detalhados nas células
for i in range(heatmap_labels.shape[0]):
    for j in range(heatmap_labels.shape[1]):
        label = heatmap_labels.iloc[i, j]
        if pd.notna(label):  # Apenas para células não vazias
            ax.text(
                j, i, label, ha='center', va='center', fontsize=7, color='black',
                wrap=True, bbox=dict(boxstyle="round,pad=0.3", edgecolor='none', facecolor='white', alpha=0.5)
            )

# Ajustar limites do gráfico
ax.set_xlim(-0.5, churn_risk_matrix.shape[1] - 0.5)
ax.set_ylim(-0.5, churn_risk_matrix.shape[0] - 0.5)

# Adicionar barra de cores
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.02, pad=0.04)
cbar.set_label('Churn Risk (Vermelho=Alto, Verde=Baixo)')

plt.tight_layout()
plt.show()
