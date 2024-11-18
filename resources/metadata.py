"""
Script para generar metadatos detallados de cada columna en `heart.csv`.

Descripción:
Este script crea metadatos personalizados para cada columna del archivo `heart.csv`, clasificando las columnas en categorías relevantes:
- Variables categóricas
- Variables numéricas continuas

Guarda los metadatos en un archivo JSON para su reutilización.

Requisitos:
- Instalar pandas:
    pip install pandas
- Instalar SDV:
    pip install sdv
"""

import pandas as pd
from sdv.metadata import Metadata

# Cargar datos desde el archivo CSV
file_path = 'heart.csv'  # Cambia esta ruta según la ubicación de tu archivo
data = pd.read_csv(file_path)

# Detectar metadatos automáticamente
metadata = Metadata.detect_from_dataframe(data=data, table_name='heart_data')

# Definir los metadatos manualmente para cada columna
categorical_columns = ['sex', 'cp', 'fbs', 'restecg', 'exng', 'slp', 'caa', 'thall', 'output']
numerical_columns = ['age', 'trtbps', 'chol', 'thalachh', 'oldpeak']

# Actualizar los tipos de datos categóricos en los metadatos
for column in categorical_columns:
    metadata.update_column(column_name=column, sdtype='categorical')

# Actualizar los tipos de datos numéricos continuos
for column in numerical_columns:
    metadata.update_column(column_name=column, sdtype='numerical')

# Validar los metadatos
try:
    metadata.validate()
    print("Metadatos validados correctamente.")
except Exception as e:
    print("Error durante la validación de metadatos:", e)

# Guardar los metadatos en un archivo JSON
output_json_path = 'heart_metadata_detailed.json'
metadata.save_to_json(filepath=output_json_path)
print(f"Metadatos guardados en {output_json_path}")

# Inspeccionar los metadatos generados
print("Metadatos detallados:")
print(metadata.to_dict())
