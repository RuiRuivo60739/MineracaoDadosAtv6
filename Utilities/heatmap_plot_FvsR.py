import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, ListedColormap
import matplotlib.colors as mcolors

# Ler o ficheiro CSV
file_path = r'C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\Steps\online_retail_II_cleaned_with_scores_clusters_churnRisk_description.csv'
data = pd.read_csv(file_path)

# Definir os segmentos detalhados
def detailed_segment_customer(recency_score, frequency_score, monetary_score, churn_risk, churn_risk_description,cluster):

    return f"{cluster}\nR: {recency_score}, F: {frequency_score}, M: {monetary_score}\nChurn Risk: {churn_risk}\n{churn_risk_description}"

# Aplicar a função com múltiplos argumentos
data['Segmentos de Clientes'] = data.apply(
    lambda row: detailed_segment_customer(
        row['Recency_score'], row['Frequency_score'], row['Monetary_score'], row['ChurnRisk'], row['ChurnRisk_description'], row['cluster']
    ), axis=1
)

# Calcular o valor médio de RFM_score_sum por cluster e normalizá-lo
cluster_means = data.groupby('cluster')[['Recency_score', 'Frequency_score', 'Monetary_score']].mean().mean(axis=1)
normalized_cluster_means = (cluster_means - cluster_means.min()) / (cluster_means.max() - cluster_means.min())

# Criar um mapeamento de cores por cluster com base no gradiente
cmap = plt.cm.RdYlGn
cluster_colors = {cluster: cmap(value) for cluster, value in normalized_cluster_means.items()}

# Criar matriz de clusters
cluster_matrix = data.pivot_table(
    index='Frequency_score',
    columns='Recency_score',
    values='cluster',
    aggfunc=lambda x: x.mode()[0] if not x.empty else None
)

# Criar tabela de rótulos detalhados
heatmap_labels = data.pivot_table(
    index='Frequency_score',
    columns='Recency_score',
    values='Segmentos de Clientes',
    aggfunc=lambda x: x.mode()[0] if not x.empty else None
)

# Converter os clusters para cores
color_matrix = cluster_matrix.applymap(lambda x: mcolors.to_hex(cluster_colors[x]) if pd.notna(x) else "#FFFFFF")

# Configurar o mapa de calor com separadores de zonas de cluster
fig, ax = plt.subplots(figsize=(14, 8))
for i in range(color_matrix.shape[0]):
    for j in range(color_matrix.shape[1]):
        color = color_matrix.iloc[i, j]
        rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color=color, edgecolor='black')  # Adicionar bordas pretas
        ax.add_patch(rect)

# Adicionar linhas que separam as zonas de cluster corretamente
for i in range(color_matrix.shape[0]):
    for j in range(color_matrix.shape[1]):
        # Verificar transição horizontal entre clusters
        if j < color_matrix.shape[1] - 1 and cluster_matrix.iloc[i, j] != cluster_matrix.iloc[i, j + 1]:
            ax.plot([j + 0.5, j + 0.5], [i - 0.5, i + 0.5], color='black', linewidth=1.5)
        # Verificar transição vertical entre clusters
        if i < color_matrix.shape[0] - 1 and cluster_matrix.iloc[i, j] != cluster_matrix.iloc[i + 1, j]:
            ax.plot([j - 0.5, j + 0.5], [i + 0.5, i + 0.5], color='black', linewidth=1.5)

# Configuração dos eixos
ax.set_xticks(np.arange(cluster_matrix.shape[1]))
ax.set_xticklabels(cluster_matrix.columns, rotation=45)
ax.set_yticks(np.arange(cluster_matrix.shape[0]))
ax.set_yticklabels(cluster_matrix.index)
ax.set_xlabel('Recency Score')
ax.set_ylabel('Frequency Score')
ax.set_title('Heatmap de Segmentos de Clientes')

# Adicionar rótulos detalhados nas células
for i in range(heatmap_labels.shape[0]):
    for j in range(heatmap_labels.shape[1]):
        label = heatmap_labels.iloc[i, j]
        if pd.notna(label):  # Apenas para células não vazias
            ax.text(
                j, i, label, ha='center', va='center', fontsize=7, color='black',
                wrap=True, bbox=dict(boxstyle="round,pad=0.3", edgecolor='none', facecolor='white', alpha=0.5)
            )

# Ajustar limites do gráfico para garantir que os rótulos fiquem dentro
ax.set_xlim(-0.5, color_matrix.shape[1] - 0.5)
ax.set_ylim(-0.5, color_matrix.shape[0] - 0.5)

# Adicionar barra de cores
sm = plt.cm.ScalarMappable(cmap=cmap, norm=Normalize(vmin=0, vmax=1))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.02, pad=0.04)
cbar.set_label('Gradiente baseado na pontuação RFM normalizada')

plt.tight_layout()
plt.show()
