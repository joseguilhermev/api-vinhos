from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup

router = APIRouter()

# Mapeamento das categorias para as subopções correspondentes do site
category_mapping = {
    "Vinhos de mesa": "subopt_01",
    "Espumantes": "subopt_02",
    "Uvas frescas": "subopt_03",
    "Uvas passas": "subopt_04",
    "Suco de uva": "subopt_05",
}


@router.get(
    "/{ano}/{categoria}",
    summary="Buscar dados de importação",
    description="Recupera dados de importação para uma categoria específica e ano.",
)
async def pegar_dados_importacao(ano: int, categoria: str):
    """
    Busca dados de importação para uma categoria específica e ano a partir de uma fonte externa.

    Args:
    - ano (int): O ano dos dados de importação.
    - categoria (str): A categoria de produtos para a qual os dados serão buscados (ex: 'Vinhos de mesa', 'Espumantes').

    Returns:
    - Lista de dicionários contendo os dados de importação detalhados por país, quantidade e valor.
    """
    subopcao = category_mapping.get(categoria)
    if not subopcao:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")

    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao={subopcao}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Recurso não encontrado"
        )

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        raise HTTPException(status_code=404, detail="Dados não encontrados")

    tbody = table.find("tbody")
    if not tbody:
        raise HTTPException(status_code=404, detail="Corpo de dados não encontrado")

    data = []
    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if not cells or len(cells) < 3:
            continue

        data.append(
            {
                "Países": cells[0].text.strip(),
                "Quantidade (Kg)": cells[1].text.strip(),
                "Valor (US$)": cells[2].text.strip(),
            }
        )

    return data
