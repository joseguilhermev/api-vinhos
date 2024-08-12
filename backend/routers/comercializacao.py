from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

router = APIRouter()


@router.get(
    "/{ano}/{item}",
    summary="Buscar dados de comercialização",
    description="Recupera dados sobre a comercialização de um item específico para um determinado ano.",
    response_model=List[Dict[str, str]],
)
async def pegar_dados_comercializacao(ano: int, item: str):
    """
    Busca dados de comercialização para um item específico e ano a partir de uma fonte externa.

    Args:
    - ano (int): O ano dos dados de comercialização.
    - item (str): O item de comercialização para o qual os dados serão buscados.

    Returns:
    - Lista de dicionários contendo os dados de comercialização.
    """
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04"
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
                    "Produto": cells[0].text.strip(),
                    "Quantidade (L.)": cells[1].text.strip(),
                }
            )

    return data
