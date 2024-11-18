import chardet

# Ruta al archivo
file_path = 'data/heart.csv'

# Leer una muestra del archivo para determinar su codificación
with open(file_path, 'rb') as file:
    raw_data = file.read(10000)  # Leer los primeros 10,000 bytes
    detected_encoding = chardet.detect(raw_data)

print("Encoding detectado:", detected_encoding)
