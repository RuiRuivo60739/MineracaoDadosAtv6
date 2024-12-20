from scipy.io import arff
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the ARFF file
file_path = r"C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\online_retail_II_fixed_clustered.arff"  # Replace with your ARFF file path
data, meta = arff.loadarff(file_path)

# Convert ARFF data to a pandas DataFrame
data_df = pd.DataFrame(data)

# Specify the percentage for the test set
test_size_percentage = 0.2  # 20% for test set

# Split the data into training and test sets
train_set, test_set = train_test_split(data_df, test_size=test_size_percentage, random_state=42)

# Save the splits to separate ARFF files
train_set_file = r"C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\train_set_" + str(
    100 - test_size_percentage * 100) + ".arff"
test_set_file = r"C:\Users\Rui\OneDrive - Universidade de Évora\1º Ano\1º Semestre\Mineração de Dados\Actividades\Atividade 6 - Final\test_set_" + str(
    test_size_percentage * 100) + ".arff"


# Function to save a DataFrame as ARFF
def save_to_arff(dataframe, file_path, relation_name="data"):
    with open(file_path, "w") as f:
        # Write the @relation
        f.write(f"@relation {relation_name}\n\n")

        # Write the @attribute section
        for column in dataframe.columns:
            if dataframe[column].dtype == 'object':
                unique_vals = dataframe[column].dropna().unique()
                unique_vals = ",".join([f"'{val.decode('utf-8')}'" for val in unique_vals])
                f.write(f"@attribute {column} {{{unique_vals}}}\n")
            else:
                f.write(f"@attribute {column} numeric\n")

        # Write the @data section
        f.write("\n@data\n")
        dataframe.to_csv(f, index=False, header=False)


# Save ARFF files
save_to_arff(train_set, train_set_file, relation_name="train_set")
save_to_arff(test_set, test_set_file, relation_name="test_set")

print(f"Data has been split and saved as '{train_set_file}' and '{test_set_file}'.")
