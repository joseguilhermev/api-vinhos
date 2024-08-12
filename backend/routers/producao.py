from fastapi import APIRouter, HTTPException, Query
import requests
from bs4 import BeautifulSoup

router = APIRouter()


@router.get(
    "/{ano}/{item}",
    summary="Buscar dados de produção",
    description="Recupera dados sobre um item específico dos dados de produção para um determinado ano.",
)
async def pegar_dados_producao(ano: int, item: str):
    """
    Busca dados de produção para um item e ano específicos a partir de uma fonte externa.

    Args:
    - ano (int): O ano dos dados de produção.
    - item (str): O item de produção para o qual os dados serão buscados.

    Returns:
    - Lista de dicionários contendo os dados de produção.
    """
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02"
    with requests.Session() as session:
        response = session.get(url)
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

            td_class = cells[0].get("class", [])
            if "tb_item" in td_class:
                if cells[0].text.strip().upper() == item.upper():
                    capture = True
                else:
                    if capture:
                        break
            elif capture and "tb_subitem" in td_class:
                data.append(
                    {
                        "Produto": cells[0].text.strip(),
                        "Quantidade (L.)": cells[1].text.strip(),
                    }
                )

        return data
