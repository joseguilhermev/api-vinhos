from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

router = APIRouter()

# Mapeamento das categorias de uvas para os subtipos do site
category_mapping = {
    "Viníferas": "subopt_01",
    "Americanas e híbridas": "subopt_02",
    "Uvas de mesa": "subopt_03",
    "Sem classificação": "subopt_04",
}


@router.get(
    "/{ano}/{categoria}/{item}",
    summary="Buscar dados de processamento",
    description="Recupera dados de processamento para um item específico, categoria e ano.",
    response_model=List[Dict[str, str]],
)
async def pegar_dados_processamento(ano: int, categoria: str, item: str):
    """
    Busca dados de processamento para uma categoria específica de uvas, item e ano a partir de uma fonte externa.

    Args:
    - ano (int): O ano dos dados de processamento.
    - categoria (str): A categoria das uvas (ex: 'Viníferas', 'Americanas e híbridas', etc.).
    - item (str): O item de processamento para o qual os dados serão buscados.

    Returns:
    - Lista de dicionários contendo os dados de processamento.
    """
    subopcao = category_mapping.get(categoria)
    if not subopcao:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao={subopcao}"
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
    capture = False
    for row in tbody.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            continue

        if "tb_item" in cells[0].get("class", []):
            if cells[0].text.strip().upper() == item.upper():
                capture = True
            else:
                if capture:
                    break
        elif capture and "tb_subitem" in cells[0].get("class", []):
            data.append(
                {
                    "Cultivar": cells[0].text.strip(),
                    "Quantidade (Kg)": cells[1].text.strip(),
                }
            )

    return data
