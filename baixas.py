import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from seleniumcomandos import clicar_elemento, escrever_elemento, encontrar_elemento,verificar_iframe
import pandas as pd


def efetuar_baixas(navegador, data_baixa, cod_spe, titulo, parcela,conta,url_baixas, max_tentativas=2):

    sucesso = False
    tentativas = 0

    while tentativas < max_tentativas and not sucesso:
        navegador.get(url_baixas)
        time.sleep(5)  # Pequeno delay para carregar a página

        # XPaths dos campos no sistema
        xpath_data = '//*[@id="filter.dtBaixa"]'
        xpath_cod_spe = '//*[@id="filter.contaCorrente.empresa.cdEmpresaView"]'
        xpath_titulo = '//*[@id="filter.titulo"]'
        xpath_parcela = '//*[@id="filter.parcela"]'
        xpath_conta = '//*[@id="entity.contaCorrente.contaCorrentePK.nuConta"]'
        xpath_botao_confirmar = '//*[@id="holderConteudo2"]/form/p/span[1]/span/input'
        xpath_botao_selecionar = '//*[@id="row[0].flSelecao_0"]'
        xpath_botao_salvar = '//*[@id="botaoSalvar"]'
        xpath_alerta_erro = "//div[contains(@class, 'spwAlertaAviso')]//p[contains(text(), 'Não há registros para os parâmetros informados.')]"
        xpath_alerta_sucesso = "//div[contains(@class, 'spwAlertaSucesso')]//p[contains(text(), 'Baixa (s) efetuada (s) com sucesso.')]"

        # Inserindo os valores no sistema
        escrever_elemento(navegador, xpath_data, data_baixa)
        escrever_elemento(navegador, xpath_cod_spe, cod_spe)
        escrever_elemento(navegador, xpath_titulo, titulo)
        escrever_elemento(navegador, xpath_parcela, parcela)
        
        if conta and str(conta).strip().lower() != 'nan':  
            escrever_elemento(navegador, xpath_conta, conta)
            if verificar_iframe(navegador, "spjGenericSearch.do?spwProxySearchURL=", conta):
                print("Iframe correto detectado! Prosseguindo...")
            else:
                print("Iframe não encontrado ou incorreto.")
        

        clicar_elemento(navegador, xpath_botao_confirmar)
        time.sleep(2)  # Pequeno delay para verificar o alerta

        try:
            # Verifica se há um alerta de erro (não há registros)
            erro = encontrar_elemento(navegador, xpath_alerta_erro, tempo_espera=2)
            if erro:
                print(f"Não há registros para Cód SPE {cod_spe}.")
                return 'Erro: Não há registros'  # Retorna erro se não houver registros
        except TimeoutException:
            pass  # Se o erro não for encontrado, continua para o próximo bloco

        try:
            # Se não houver erro, prossegue com a baixa
            print(f"Prosseguindo com a baixa para Cód SPE {cod_spe}.")
            # Clica para selecionar e salvar a baixa
            clicar_elemento(navegador, xpath_botao_selecionar)
            clicar_elemento(navegador, xpath_botao_salvar)
            time.sleep(5)  # Espera um pouco para o alerta de sucesso aparecer

            # Verifica se a baixa foi efetuada com sucesso
            sucesso = encontrar_elemento(navegador, xpath_alerta_sucesso, tempo_espera=3)
            if sucesso:
                print(f"Baixa realizada com sucesso para Cód SPE {cod_spe}!")
                return 'Sucesso'
            else:
                print(f"Alerta de sucesso não encontrado para Cód SPE {cod_spe}. Tentando novamente...")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Erro ao tentar realizar a baixa para Cód SPE {cod_spe}: {e}")

        tentativas += 1
        if tentativas < max_tentativas:
            print(f"Tentativa {tentativas} falhou. Recarregando a página para tentar novamente...")
            time.sleep(5)  # Delay antes de tentar novamente

    print(f"Falha ao efetuar a baixa para Cód SPE {cod_spe} após {max_tentativas} tentativas.")
    return 'Erro: Máximo de tentativas atingido'
