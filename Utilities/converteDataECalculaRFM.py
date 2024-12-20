import pandas as pd

# Load the CSV file
file_path = r'C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\Steps\online_retail_II.csv'
data = pd.read_csv(file_path)

# Converter invoicedate em datetime
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'].str.strip("'"), format='%m/%d/%Y %H:%M')

# converter datetime em milisegundos desde unix epoch
data['InvoiceDate_ms'] = (data['InvoiceDate'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')

# Save the modified dataset to a new CSV file
output_path = r'C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\Steps\online_retail_II_fixed_with_ms.csv'  
data.to_csv(output_path, index=False)

print(f"Modified file saved at: {output_path}")

# Carregar o arquivo CSV
data = pd.read_csv(output_path)

# Converter InvoiceDate para datetime
data['InvoiceDate_ms'] = pd.to_datetime(data['InvoiceDate_ms'], unit='ms')
data['InvoiceDate_ms'] = data['InvoiceDate_ms'].dt.strftime('%Y-%m-%d %H:%M:%S')
data['InvoiceDate_ms'] = pd.to_datetime(data['InvoiceDate_ms'].str.strip("'"), format='%Y-%m-%d %H:%M:%S')

# Ignorar linhas com quantidade negativa
data = data[data['Quantity'] > 0]

# Definir uma data de referência (máxima no conjunto + 1 dia para cálculo RFM)
snapshot_date = data['InvoiceDate_ms'].max() + pd.Timedelta(days=1)

# Calcular Recência (dias desde a última compra)
customer_last_purchase = data.groupby("Customer ID")['InvoiceDate_ms'].transform('max')
data['Recency'] = (snapshot_date - customer_last_purchase).dt.days

# Calcular o valor total para cada linha (Price * Quantity)
data['TotalValue'] = data['Price'] * data['Quantity']

# Identificar cancelamentos (Invoice começa com 'C')
data['IsCancellation'] = data['Invoice'].astype(str).str.startswith('C')

# Filtrar apenas as transações válidas (não canceladas)
valid_transactions = data[~data['IsCancellation']]

# Contar faturas únicas por cliente
customer_frequency = valid_transactions.groupby("Customer ID")['Invoice'].nunique()

# Adicionar ao DataFrame principal
data['Frequency'] = data["Customer ID"].map(customer_frequency)

# Calcular Valor Monetário (soma de TotalValue por cliente)
customer_monetary = data.groupby("Customer ID")['TotalValue'].transform('sum')
data['MonetaryValue'] = customer_monetary

# Guardar o dataset modificado num novo arquivo CSV
output_path = r'C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\Steps\online_retail_II_fixed_with_correctDate_and_RFM.csv'
data.to_csv(output_path, index=False)

print(f"Ficheiro modificado com colunas RFM guardado em: {output_path}")