import base64
import requests
from credenciais import obter_credenciais


# Função para consultar contas correntes
def consultar_contas_correntes(subdominio, cod_spe, account_status="ENABLED", limit=100, offset=0):
    """
    Consulta as contas correntes associadas a um 'company_id' (cod_spe) fornecido.
    :param subdominio: O subdomínio a ser utilizado na API (ex: 'sej', 'macapainvest')
    :param cod_spe: O código SPE que será usado como company_id
    :param account_status: Status das contas (padrão é "ENABLED")
    :param limit: Número máximo de resultados a retornar (padrão é 100)
    :param offset: Deslocamento da consulta (padrão é 0)
    :return: Lista de números de contas bancárias
    """
    url = f"https://api.sienge.com.br/{subdominio}/public/api/v1/checking-accounts"
    token = obter_credenciais(subdominio)

    headers = {
        "Authorization": token
    }

    params = {
        "companyId": cod_spe,  # Usando cod_spe diretamente como company_id
        "accountStatus": account_status,
        "limit": limit,
        "offset": offset
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extrair somente os 'accountNumber' com accountType = "Bancária"
            contas_bancarias = [
                conta['accountNumber'] for conta in data.get('results', [])
                if conta.get('accountType', {}).get('description') == "Bancária"
            ]
            
            return contas_bancarias
        else:
            print(f"❌ Erro na requisição. Status code: {response.status_code}")
            print(response.json())
            return []

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return []
