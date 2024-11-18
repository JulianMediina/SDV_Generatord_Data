from sdv.datasets.local import load_csvs
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import Metadata
from sdv.evaluation.single_table import run_diagnostic, evaluate_quality
import seaborn as sns
import matplotlib.pyplot as plt
import os



# assume that my_folder contains a CSV file named 'guests.csv'
datasets = load_csvs(
    folder_name='data/',
    read_csv_parameters={
        'skipinitialspace': True,
        'encoding': 'ascii'
    })

# the data is available under the file name

data = datasets['heart']
print (data)

metadata = Metadata.detect_from_dataframe(
    data=data,
    table_name='heart')
print (metadata)


synthesizer = GaussianCopulaSynthesizer(metadata)
synthesizer.fit(data)
#GENERA #num_rows REGISTROS Y EXPORTA
synthetic_data = synthesizer.sample(num_rows=300,output_file_path='output/dataGAN.csv')
synthesizer.auto_assign_transformers(data)
print (synthesizer.get_transformers())

print (synthetic_data)
print('****************************************************************')
print(type(synthetic_data))


#EVALUAR RESULTADOS
# 1. perform basic validity checks
diagnostic = run_diagnostic(data, synthetic_data, metadata)

# 2. measure the statistical similarity
quality_report = evaluate_quality(data, synthetic_data, metadata)
print(quality_report.get_details(property_name='Column Shapes'))
print('Quality report:', quality_report.get_score())

# 3. plot the data
fig = quality_report.get_visualization(property_name='Column Shapes')
fig.show()


# 4. plot the data
# Crear un directorio para guardar las gráficas

os.makedirs('output/plots', exist_ok=True)

# 1. Histogramas superpuestos
numerical_columns = data.select_dtypes(include=['number']).columns

for column in numerical_columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True, color='blue', label='Original', bins=20, alpha=0.5)
    sns.histplot(synthetic_data[column], kde=True, color='orange', label='Generado', bins=20, alpha=0.5)
    plt.title(f'Distribución Comparativa: {column}')
    plt.xlabel(column)
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(f'output/plots/comparative_histogram_{column}.png')
    plt.close()

# 2. Sumas acumuladas superpuestas
for column in numerical_columns:
    plt.figure(figsize=(10, 6))
    original_cumsum = data[column].cumsum()
    synthetic_cumsum = synthetic_data[column].cumsum()
    plt.plot(original_cumsum, label='Original', color='blue', linestyle='-')
    plt.plot(synthetic_cumsum, label='Generado', color='orange', linestyle='--')
    plt.title(f'Suma Acumulada Comparativa: {column}')
    plt.xlabel('Índice')
    plt.ylabel('Suma acumulada')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(f'output/plots/comparative_cumulative_sum_{column}.png')
    plt.close()

print("Las gráficas comparativas se han generado y guardado en la carpeta 'output/plots'.")
