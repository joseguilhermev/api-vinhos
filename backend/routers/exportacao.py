from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

router = APIRouter()

# Mapeamento das categorias de produtos para as subopções correspondentes no site
category_mapping = {
    "Vinhos de mesa": "subopt_01",
    "Espumantes": "subopt_02",
    "Uvas frescas": "subopt_03",
    "Suco de uva": "subopt_04",
}


@router.get(
    "/{ano}/{categoria}",
    summary="Buscar dados de exportação",
    description="Recupera dados de exportação para uma categoria específica e ano.",
    response_model=List[Dict[str, str]],
)
async def pegar_dados_exportacao(ano: int, categoria: str):
    """
    Busca dados de exportação para uma categoria específica e ano a partir de uma fonte externa.

    Args:
    - ano (int): O ano dos dados de exportação.
    - categoria (str): A categoria de produtos para a qual os dados serão buscados (ex: 'Vinhos de mesa', 'Suco de uva').

    Returns:
    - Lista de dicionários contendo os dados de exportação detalhados por país, quantidade e valor.
    """
    subopcao = category_mapping.get(categoria)
    if not subopcao:
        raise HTTPException(status_code=404, detail="Subcategoria não encontrada")

    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao={subopcao}"
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
