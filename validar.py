import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# ==================================================
# CONFIGURAÇÃO
# ==================================================

RAIO_METROS = 1500

ARQUIVO_PONTOS = 'pontos.xlsx'
ARQUIVO_COLAB = 'colaboradores.xlsx'
ARQUIVO_SAIDA = 'colaboradores_validados.xlsx'

geolocator = Nominatim(user_agent="validador_endereco_v1")

# ==================================================
# LEITURA DOS ARQUIVOS
# ==================================================

import os

print('Lendo planilhas...')
print(f'Pasta atual: {os.getcwd()}')
print(f'Arquivo lido: {os.path.abspath(ARQUIVO_COLAB)}\n')

try:
    pontos = pd.read_excel(ARQUIVO_PONTOS)
    colaboradores = pd.read_excel(ARQUIVO_COLAB)
except Exception as erro:
    print(f'Erro ao ler arquivos: {erro}')
    exit()

# CONFIRMAÇÃO DOS DADOS CARREGADOS
print('=' * 50)
print(f'Total de candidatos encontrados: {len(colaboradores)}')
print('Primeiros 5 endereços carregados:')
for i, row in colaboradores.head(5).iterrows():
    print(f'  {i+1}. {str(row["Residência"]).strip()}')
print('=' * 50)
print('\nSe os endereços acima são os NOVOS, pressione ENTER para continuar.')
print('Se são os ANTIGOS, feche o colaboradores.xlsx no Excel e rode novamente.')
input('Pressione ENTER para iniciar...\n')

# ==================================================
# LISTAS RESULTADO
# ==================================================

lista_lat = []
lista_lon = []
lista_ponto = []
lista_distancia = []
lista_status = []

total = len(colaboradores)
print(f'Total de candidatos: {total}')
print('Iniciando validação...\n')

# ==================================================
# LOOP COLABORADORES
# ==================================================

for index, colaborador in colaboradores.iterrows():

    try:

        endereco = str(colaborador['Residência']).strip()

        print(f'[{index + 1}/{total}] {endereco}')

        # ==========================================
        # BUSCAR LATITUDE/LONGITUDE
        # ==========================================

        try:
            location = geolocator.geocode(endereco, timeout=10)
        except GeocoderTimedOut:
            location = None

        if not location:
            lista_lat.append('')
            lista_lon.append('')
            lista_ponto.append('ENDEREÇO NÃO LOCALIZADO')
            lista_distancia.append('')
            lista_status.append('NÃO ATENDE')
            print('  → Não localizado\n')
            time.sleep(1)
            continue

        lat_colab = location.latitude
        lon_colab = location.longitude

        lista_lat.append(lat_colab)
        lista_lon.append(lon_colab)

        # ==========================================
        # ENCONTRAR PONTO MAIS PRÓXIMO
        # ==========================================

        menor_distancia = 999999999
        melhor_ponto = ''

        for _, ponto in pontos.iterrows():
            lat_ponto = ponto['Latitude']
            lon_ponto = ponto['Longitude']
            distancia = geodesic(
                (lat_colab, lon_colab),
                (lat_ponto, lon_ponto)
            ).meters
            if distancia < menor_distancia:
                menor_distancia = distancia
                melhor_ponto = ponto['Ponto']

        lista_ponto.append(melhor_ponto)
        lista_distancia.append(round(menor_distancia, 2))

        if menor_distancia <= RAIO_METROS:
            lista_status.append('ATENDE')
        else:
            lista_status.append('NÃO ATENDE')

        print(f'  → {melhor_ponto} | {round(menor_distancia, 2)}m | {lista_status[-1]}\n')

        time.sleep(1)

    except Exception as erro:
        print(f'  → Erro: {erro}\n')
        lista_lat.append('')
        lista_lon.append('')
        lista_ponto.append('ERRO')
        lista_distancia.append('')
        lista_status.append('NÃO ATENDE')
        time.sleep(1)

# ==================================================
# ADICIONAR COLUNAS E SALVAR CÓPIA
# ==================================================

colaboradores['Latitude']           = lista_lat
colaboradores['Longitude']          = lista_lon
colaboradores['Ponto Mais Próximo'] = lista_ponto
colaboradores['Distância (m)']      = lista_distancia
colaboradores['Status Raio 1500m']  = lista_status

try:
    colaboradores.to_excel(ARQUIVO_SAIDA, index=False)

    atende     = lista_status.count('ATENDE')
    nao_atende = lista_status.count('NÃO ATENDE')

    print('\n===================================')
    print('CONCLUÍDO!')
    print('===================================')
    print(f'Total     : {total}')
    print(f'ATENDE    : {atende}')
    print(f'NÃO ATENDE: {nao_atende}')
    print(f'\nArquivo gerado: {ARQUIVO_SAIDA}')

except Exception as erro:
    print(f'Erro ao salvar: {erro}')
