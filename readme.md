# Metadados de Fotos com Geocodificação
Este script Python permite a extração de metadados de arquivos de imagem (JPG, JPEG, PNG), incluindo informações de geolocalização, e realiza a geocodificação para obter o endereço correspondente. Os resultados podem ser salvos em dois formatos: JSON e Excel.

## Funcionalidades
**Extração de Metadados**: Extrai metadados EXIF de imagens, como data e hora de captura, além das coordenadas geográficas (latitude e longitude).

**Geocodificação**: Utiliza a API Nominatim do OpenStreetMap para converter as coordenadas de latitude e longitude em endereços legíveis.

**Saída em JSON**: Salva os metadados e endereços em um arquivo JSON formatado.

**Saída em Excel**: Salva os metadados e endereços em um arquivo Excel, com ajuste automático de largura das colunas e formatação adequada.

## Pré-requisitos
Python 3 ou superior.

Bibliotecas Python necessárias:
- exifread – Para leitura de metadados EXIF.
- Pillow – Para manipulação de imagens.
- requests – Para realizar chamadas HTTP à API Nominatim.
- openpyxl – Para salvar os resultados em um arquivo Excel.

## Instalação
### Passo 1: Clone o repositório
```bash
git clone https://github.com/seu-nome-de-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### Passo 2: Instale as dependências
Recomenda-se criar um ambiente virtual para isolar as dependências do projeto:
```bash
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scriptsctivate`
```

Instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

## Como Usar
Configure o script:
No script Python (metadados.py), ajuste o diretório onde suas imagens estão localizadas e os nomes dos arquivos de saída para JSON e Excel:
```python
directory = r"C:\caminho\para\suas\imagens"  # Substitua pelo caminho correto
output_file_json = "metadados_fotos.json"
output_file_excel = "metadados_fotos.xlsx"
```

Execute o script:
```bash
python metadados.py
```

### Resultados:
O script irá processar as imagens, extrair os metadados e salvar os resultados nos arquivos metadados_fotos.json e metadados_fotos.xlsx.

## Observações
**Limites de Requisição da API Nominatim**: A API Nominatim possui um limite de requisições por segundo. Caso você tenha muitas imagens para processar, é recomendável adicionar um atraso entre as requisições para evitar bloqueios. Exemplo:
```python
import time
time.sleep(1)  # Adiciona um atraso de 1 segundo entre as requisições
```

**Requisitos de Metadados EXIF**: Certifique-se de que suas imagens contenham metadados EXIF com informações de latitude e longitude para que o código funcione corretamente. Caso contrário, as coordenadas não serão extraídas e a geocodificação não será possível.

## Estrutura do Projeto
```plaintext
nome-do-repositorio/
├── metadados.py            # Script principal
├── requirements.txt        # Lista de dependências
├── metadados_fotos.json    # Saída em JSON (gerado após execução)
├── metadados_fotos.xlsx    # Saída em Excel (gerado após execução)
└── README.md               # Este arquivo
```

## Contribuições
Contribuições são sempre bem-vindas! Sinta-se à vontade para:
- Abrir issues para reportar bugs ou sugerir melhorias.
- Enviar pull requests para adicionar novas funcionalidades ou corrigir problemas.

## Licença

Este projeto está licenciado sob a Licença Creative Commons (CC BY-NC 4.0). Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
