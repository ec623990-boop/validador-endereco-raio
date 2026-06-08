# Validador de Endereços por Raio Geográfico

Ferramenta em Python que valida se colaboradores/candidatos residem dentro de um raio configurável em relação a pontos de interesse (terminais, filiais, etc.), usando geocodificação automática de endereços.

---

## O que o script faz

1. **Lê dois arquivos Excel:**
   - `pontos.xlsx` — lista de pontos de referência com latitude e longitude
   - `colaboradores.xlsx` — lista de colaboradores com endereço residencial

2. **Geocodifica automaticamente** cada endereço usando o serviço OpenStreetMap (Nominatim)

3. **Calcula a distância** (em metros) entre o endereço do colaborador e cada ponto de referência

4. **Identifica o ponto mais próximo** e verifica se está dentro do raio configurado

5. **Gera um arquivo Excel** `colaboradores_validados.xlsx` com o resultado de cada colaborador

---

## Pré-requisitos

- Python 3.8 ou superior
- pip

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/validador-endereco.git
cd validador-endereco

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## Estrutura dos arquivos Excel

### `pontos.xlsx`

| Coluna    | Descrição                        |
|-----------|----------------------------------|
| Ponto     | Nome do ponto de referência      |
| Latitude  | Latitude decimal (ex: -23.5505)  |
| Longitude | Longitude decimal (ex: -46.6333) |

### `colaboradores.xlsx`

| Coluna    | Descrição                                              |
|-----------|--------------------------------------------------------|
| Residência | Endereço completo do colaborador (rua, número, cidade) |
| *(outros)* | Qualquer outra coluna será mantida no arquivo de saída |

> **Atenção:** O nome da coluna deve ser exatamente `Residência` (com acento).

Veja exemplos de estrutura em [`pontos_exemplo.xlsx.md`](pontos_exemplo.xlsx.md).

---

## Como usar

1. Coloque os arquivos `pontos.xlsx` e `colaboradores.xlsx` na **mesma pasta** que o script

2. (Opcional) Ajuste o raio em metros no topo do script:

```python
RAIO_METROS = 1500  # padrão: 1500m
```

3. Execute:

```bash
python validar.py
```

4. O script exibirá os primeiros 5 endereços carregados para confirmar que está lendo o arquivo correto. Pressione **ENTER** para iniciar.

5. Ao final, será gerado o arquivo `colaboradores_validados.xlsx` na mesma pasta.

---

## Arquivo de saída

O arquivo `colaboradores_validados.xlsx` contém todas as colunas originais mais:

| Coluna nova          | Descrição                                    |
|----------------------|----------------------------------------------|
| Latitude             | Latitude geocodificada do endereço           |
| Longitude            | Longitude geocodificada do endereço          |
| Ponto Mais Próximo   | Nome do ponto de referência mais próximo     |
| Distância (m)        | Distância em metros até o ponto mais próximo |
| Status Raio 1500m    | `ATENDE` ou `NÃO ATENDE`                    |

---

## Configuração

No topo do arquivo `validar.py` você encontra as configurações principais:

```python
RAIO_METROS = 1500           # Raio de validação em metros
ARQUIVO_PONTOS = 'pontos.xlsx'          # Planilha com os pontos de referência
ARQUIVO_COLAB = 'colaboradores.xlsx'    # Planilha com os colaboradores
ARQUIVO_SAIDA = 'colaboradores_validados.xlsx'  # Arquivo de saída
```

---

## Possíveis erros

| Situação                     | O que aparece no arquivo de saída        |
|------------------------------|------------------------------------------|
| Endereço não encontrado      | `ENDEREÇO NÃO LOCALIZADO` / `NÃO ATENDE` |
| Erro inesperado no endereço  | `ERRO` / `NÃO ATENDE`                   |

Se muitos endereços não forem localizados, verifique se estão completos (rua, número, cidade, estado).

---

## Dependências

| Biblioteca | Uso                                      |
|------------|------------------------------------------|
| pandas     | Leitura e escrita de arquivos Excel      |
| openpyxl   | Motor de leitura/escrita `.xlsx`         |
| geopy      | Geocodificação e cálculo de distâncias   |

---

## Observações importantes

- O script faz uma pausa de **1 segundo** entre cada endereço para respeitar o limite do serviço Nominatim (OpenStreetMap). Não remova esse delay.
- Para grandes volumes (centenas de endereços), considere rodar o script fora do horário comercial.
- Os arquivos `colaboradores.xlsx` e `colaboradores_validados.xlsx` estão no `.gitignore` para proteger dados pessoais.

---

## Licença

MIT — use, modifique e distribua à vontade.
