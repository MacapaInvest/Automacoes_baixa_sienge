from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def clicar_elemento(navegador, xpath, tempo_espera=10):
    """
    Clica em um elemento identificado pelo XPath.
    
    Parâmetros:
        navegador: Instância do WebDriver.
        xpath: O XPath do elemento a ser clicado.
        tempo_espera: Tempo máximo de espera para encontrar o elemento (padrão: 10 segundos).
    """
    try:
        # Espera até o elemento estar clicável
        elemento = WebDriverWait(navegador, tempo_espera).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elemento.click()
        time.sleep(0.5)  # Tempo pequeno de espera após clicar
    except TimeoutException:
        print(f"Timeout: O elemento com XPath '{xpath}' não ficou clicável dentro do tempo esperado.")
        raise  # Levanta a exceção para ser tratada em outro lugar
    except NoSuchElementException:
        print(f"Erro: O elemento com XPath '{xpath}' não foi encontrado na página.")
        raise  # Levanta a exceção para ser tratada em outro lugar
    except Exception as e:
        print(f"Erro inesperado ao clicar no elemento com XPath '{xpath}': {e}")
        raise  # Levanta a exceção para ser tratada em outro lugar

def escrever_elemento(navegador, xpath, texto, tempo_espera=10):
    """
    Escreve um texto em um campo identificado pelo XPath e pressiona TAB no final.
    
    Parâmetros:
        navegador: Instância do WebDriver.
        xpath: O XPath do elemento onde o texto será inserido.
        texto: O texto a ser inserido no campo.
        tempo_espera: Tempo máximo de espera para encontrar o elemento (padrão: 10 segundos).
    """
    try:
        # Espera até o campo estar visível e presente
        elemento = WebDriverWait(navegador, tempo_espera).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        elemento.clear()  # Limpa o campo antes de inserir o texto
        elemento.send_keys(texto)  # Insere o texto
        elemento.send_keys(Keys.TAB)  # Pressiona TAB
        time.sleep(0.5)  # Tempo pequeno após digitar
    except TimeoutException:
        print(f"Timeout: O campo com XPath '{xpath}' não ficou visível dentro do tempo esperado.")
        raise  # Levanta a exceção para ser tratada em outro lugar
    except NoSuchElementException:
        print(f"Erro: O campo com XPath '{xpath}' não foi encontrado na página.")
        raise  # Levanta a exceção para ser tratada em outro lugar
    except Exception as e:
        print(f"Erro inesperado ao escrever no elemento com XPath '{xpath}': {e}")
        raise  # Levanta a exceção para ser tratada em outro lugar

def encontrar_elemento(navegador, xpath, tempo_espera=10):
    """
    Função para localizar um elemento na página, utilizando XPath.
    
    Parâmetros:
        navegador (WebDriver): Objeto do Selenium WebDriver.
        xpath (str): XPath do elemento a ser encontrado.
        tempo_espera (int, opcional): Tempo máximo de espera para o elemento ser encontrado (padrão é 10 segundos).
    
    Retorna:
        WebElement: O elemento encontrado na página.
    
    Levanta:
        Exception: Caso o elemento não seja encontrado dentro do tempo limite.
    """
    try:
        # Espera até que o elemento esteja presente ou visível na página
        elemento = WebDriverWait(navegador, tempo_espera).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        print(f"Elemento encontrado: {xpath}")
        time.sleep(0.5)  # Tempo pequeno após encontrar o elemento
        return elemento
    
    except TimeoutException:
        print(f"Timeout: O elemento com XPath '{xpath}' não foi encontrado dentro do tempo esperado.")
        raise  # Levanta a exceção para ser tratada adequadamente
    except NoSuchElementException:
        print(f"Erro: O elemento com XPath '{xpath}' não foi encontrado na página.")
        raise  # Levanta a exceção para ser tratada adequadamente
    except Exception as e:
        print(f"Erro inesperado ao encontrar o elemento com XPath '{xpath}': {e}")
        raise  # Levanta a exceção para ser tratada adequadamente
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def verificar_iframe(navegador, parte_url_iframe, conta):
    """
    Verifica se o iframe com a URL correta está presente, muda o foco para ele,
    encontra a linha onde 'conta' está presente, clica no input correspondente,
    em seguida no botão 'Selecionar' e volta para a página principal.
    
    :param navegador: O driver do Selenium.
    :param parte_url_iframe: Parte da URL que identifica o iframe.
    :param conta: O valor da conta a ser localizado.
    :return: True se encontrar, clicar e voltar o foco, False caso contrário.
    """
    try:
        # Localiza todos os iframes na página
        iframes = navegador.find_elements(By.TAG_NAME, "iframe")
        
        for iframe in iframes:
            # Verifica se o 'src' do iframe contém a URL desejada
            if parte_url_iframe in iframe.get_attribute('src'):
                navegador.switch_to.frame(iframe)
                print("Iframe encontrado. Foco alterado.")
                
                try:
                    # Localiza todas as células com o atributo desejado
                    colunas_conta = navegador.find_elements(By.XPATH, "//td[@property='contaCorrentePK.nuConta']")
                    
                    # Itera sobre as células para encontrar o índice onde o valor bate
                    for indice, coluna in enumerate(colunas_conta):
                        print(f"Índice {indice} - Conta: {coluna.text}")
                        
                        if coluna.text.strip() == conta:
                            print(f"Conta {conta} encontrada no índice {indice}.")
                            
                            # Localiza todos os inputs tipo radio (supondo que estão na mesma ordem das células)
                            radios = navegador.find_elements(By.XPATH, "//input[@type='radio' and @name='rowSelect']")
                            
                            if indice < len(radios):
                                # Clica no input correspondente
                                radios[indice].click()
                                print(f"Selecionado input no índice {indice}.")
                                
                                # Clica no botão "Selecionar"
                                botao_selecionar = navegador.find_element(By.ID, "pbSelecionar")
                                botao_selecionar.click()
                                print("Botão 'Selecionar' clicado.")
                                
                                # Volta o foco para a página principal
                                navegador.switch_to.default_content()
                                print("Foco retornado para a página principal.")
                                
                                return True
                            else:
                                print("Índice fora do alcance dos inputs.")
                                return False
                    
                    print(f"Conta {conta} não encontrada na tabela.")
                    navegador.switch_to.default_content()  # Garante que o foco volte para a página principal
                    return False
                
                except NoSuchElementException:
                    print("Tabela ou elementos não encontrados dentro do iframe.")
                    navegador.switch_to.default_content()
                    return False
        
        print("Iframe não encontrado ou incorreto.")
        return False

    except NoSuchElementException as e:
        print(f"Erro ao procurar iframes: {e}")
        return False
