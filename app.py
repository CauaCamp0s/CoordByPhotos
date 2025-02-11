import json
import os
from datetime import datetime

import exifread
import openpyxl
import requests
from openpyxl.styles import Alignment
from PIL.ExifTags import GPSTAGS, TAGS


def dms_to_decimal(dms):
    # Converte uma lista [graus, minutos, segundos] para decimal
    degrees = float(dms.values[0].num) / float(dms.values[0].den)
    minutes = float(dms.values[1].num) / float(dms.values[1].den)
    seconds = float(dms.values[2].num) / float(dms.values[2].den)

    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    return decimal


def get_exif_data(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
    return tags


def extract_metadata(image_path):
    exif_data = get_exif_data(image_path)

    metadata = {
        'Nome do Arquivo': os.path.basename(image_path),
        'Data e Hora': None,
        'Latitude': None,
        'Longitude': None,
        'Endereço': None
    }

    if 'EXIF DateTimeOriginal' in exif_data:
        dt_str = str(exif_data['EXIF DateTimeOriginal'])
        dt_obj = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
        metadata['Data e Hora'] = dt_obj.strftime('%Y-%m-%d %H:%M:%S')

    if 'GPS GPSLatitude' in exif_data and 'GPS GPSLongitude' in exif_data:
        lat_dms = exif_data['GPS GPSLatitude']
        lon_dms = exif_data['GPS GPSLongitude']
        lat_ref = str(exif_data['GPS GPSLatitudeRef'])
        lon_ref = str(exif_data['GPS GPSLongitudeRef'])

        # Converter para decimal e arredondar para 4 casas decimais
        metadata['Latitude'] = round(dms_to_decimal(lat_dms), 4)
        if lat_ref in ['S']:
            metadata['Latitude'] = -metadata['Latitude']

        metadata['Longitude'] = round(dms_to_decimal(lon_dms), 4)
        if lon_ref in ['W']:
            metadata['Longitude'] = -metadata['Longitude']

    return metadata


def obter_endereco(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    headers = {"User-Agent": "MeuBotDeGeocodificacao/1.0"}  # Necessário para usar a API Nominatim
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dados = response.json()
        endereco = dados.get("display_name", "Endereço não encontrado")
        return endereco
    else:
        return "Endereço não encontrado"


def save_to_excel(metadata_list, output_file):
    wb = openpyxl.Workbook()
    ws = wb.active

    # Definir cabeçalhos
    ws.append(['Nome do Arquivo', 'Data e Hora', 'Latitude', 'Longitude', 'Endereço'])

    # Adicionar dados
    for metadata in metadata_list:
        ws.append([metadata['Nome do Arquivo'], metadata['Data e Hora'], metadata['Latitude'], metadata['Longitude'], metadata['Endereço']])

    # Ajustar largura das colunas
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column_letter].width = adjusted_width

    # Centralizar conteúdo
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal='center')

    # Salvar arquivo
    wb.save(output_file)


def main(directory, output_file_json, output_file_excel):
    metadata_list = []

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(directory, filename)
            metadata = extract_metadata(image_path)

            if metadata['Latitude'] and metadata['Longitude']:
                endereco = obter_endereco(metadata['Latitude'], metadata['Longitude'])
                metadata['Endereço'] = endereco
                print(f"Processado: {filename} -> {endereco}")

            metadata_list.append(metadata)

    with open(output_file_json, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=4)

    print(f"Arquivo JSON salvo com sucesso: {output_file_json}")

    save_to_excel(metadata_list, output_file_excel)
    print(f"Arquivo Excel salvo com sucesso: {output_file_excel}")


if __name__ == "__main__":
    directory = r"C:\Users\Cauã Campos\Documents\dev\CoordByPhotos\images"  # Substitua pelo caminho do seu diretório de imagens
    output_file_json = "metadados_fotos.json"
    output_file_excel = "metadados_fotos.xlsx"
    main(directory, output_file_json, output_file_excel)