import os
import glob
import time
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import win32com.client
import time
import re
from datetime import datetime
import pytz
import re
import platform

def esperar_codigo_sienge(timeout=300, intervalo=5):
    """
    Aguarda até que um novo e-mail chegue na Caixa de Entrada.
    Exibe o código de verificação presente no corpo do e-mail com o assunto "Código de Verificação do Sienge ID".

    Parâmetros:
        timeout (int): Tempo máximo de espera em segundos (padrão: 120s).
        intervalo (int): Intervalo entre verificações em segundos (padrão: 5s).

    Retorna:
        str: O código de verificação encontrado ou mensagem de erro.
    """
    try:
        # Conectar ao Outlook
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)  # Caixa de Entrada
        print("Conectado ao Outlook e Caixa de Entrada acessada.")
        
        # Armazena o momento de execução da função
        tempo_inicial = time.time()
        
        # Obtém o fuso horário local
        local_tz = pytz.timezone("America/Sao_Paulo")
        tempo_inicial = datetime.fromtimestamp(tempo_inicial, tz=pytz.UTC).astimezone(local_tz)

        # Obtém a quantidade inicial de e-mails
        initial_message_count = len(inbox.Items)
        print(f"Quantidade inicial de e-mails: {initial_message_count}")

        while (time.time() - tempo_inicial.timestamp()) < timeout:
            # Obtém os e-mails mais recentes
            messages = inbox.Items
            messages.Sort("[ReceivedTime]", True)  # Ordena por data decrescente
            print("Verificando os e-mails mais recentes...")

            # Verifica a quantidade final de e-mails
            final_message_count = len(messages)
            print(f"Quantidade final de e-mails: {final_message_count}")
            
            # Se a diferença for maior ou igual a 1, procuro o último e-mail com o assunto desejado
            if final_message_count - initial_message_count >= 1:
                for message in messages:
                    try:
                        if hasattr(message, 'ReceivedTime'):
                            # Verifica se o assunto corresponde ao que procuramos
                            if "Código de Verificação do Sienge ID" in message.Subject:
                                print(f"Assunto do e-mail encontrado: {message.Subject}")
                                
                                # Obtém o corpo do e-mail
                                corpo_email = message.Body
                                
                                # Utiliza expressão regular para capturar o código
                                codigo = re.search(r'(\d{6})', corpo_email)  # Captura seis dígitos
                                
                                if codigo:
                                    print(f"Código de verificação encontrado: {codigo.group(0)}")
                                    return codigo.group(0)  # Retorna o código de verificação
                                else:
                                    print("Código de verificação não encontrado no corpo do e-mail.")
                                    return "Código não encontrado no corpo do e-mail"
                    except AttributeError:
                        # Caso o item não tenha a propriedade 'ReceivedTime', ignora
                        print("Ignorando item que não possui a propriedade 'ReceivedTime'.")

            # Aguarda um tempo antes de tentar novamente
            print("Aguardando novo e-mail...")
            time.sleep(intervalo)  # Espera antes de tentar novamente

        return "Tempo limite atingido. Nenhum e-mail encontrado.", None

    except Exception as e:
        return f"Erro ao acessar o Outlook: {e}", None
    
def preencher_codigo(codigo, navegador):
    """
    Preenche os campos de código com os dígitos fornecidos em cada XPath.
    
    Parâmetros:
        codigo (str): O código de verificação de 6 dígitos.
        driver (WebDriver): O objeto WebDriver do Selenium para controlar o navegador.
    """
    xpaths = [
        "/html/body/div/div/div/div/div/div/div/div[2]/form/div/div[2]/div[1]/div/div[1]/div/input",
        "/html/body/div/div/div/div/div/div/div/div[2]/form/div/div[2]/div[1]/div/div[2]/div/input",
        "/html/body/div/div/div/div/div/div/div/div[2]/form/div/div[2]/div[1]/div/div[3]/div/input",
        "/html/body/div/div/div/div/div/div/div/div[2]/form/div/div[2]/div[1]/div/div[4]/div/input",
        "/html/body/div/div/div/div/div/div/div/div[2]/form/div/div[2]/div[1]/div/div[5]/div/input",
        "/html/body/div/div/div/div/div/div/div/div[2]/form/div/div[2]/div[1]/div/div[6]/div/input"
    ]
    
    # Verifica se o código tem 6 dígitos
    if len(codigo) == 6:
        for i, digit in enumerate(codigo):
            try:
                # Encontrar o campo de input usando o XPath correspondente
                input_element = navegador.find_element(By.XPATH, xpaths[i])
                # Preencher o campo com o dígito correspondente
                input_element.send_keys(digit)
                print(f"Preenchido o campo {i + 1} com o dígito {digit}")
            except Exception as e:
                print(f"Erro ao preencher o campo {i + 1}: {e}")
    else:
        print("Código inválido. Certifique-se de que tem 6 dígitos.")
        
def carregar_configuracoes_subdominios(caminho_arquivo):
    configuracoes = {}
    
    try:
        # Abrir o arquivo para leitura
        with open(caminho_arquivo, 'r') as file:
            # Ler cada linha do arquivo
            for linha in file:
                # Remover quebras de linha e espaços em branco
                linha = linha.strip()
                
                # Dividir a linha em subdominio, usuario e senha usando o delimitador ";"
                dados = linha.split(';')
                
                if len(dados) == 3:
                    subdominio, usuario, senha = dados
                    # Adicionar ao dicionário com a chave 'subdominio'
                    configuracoes[subdominio] = {'usuario': usuario, 'senha': senha}
        
        return configuracoes
    except Exception as e:
        print(f"Erro ao carregar as configurações: {e}")
        return {}


        
        
def fazerLogin(subdominio, t=5):
    # Caminho do arquivo de configurações
    caminho_arquivo = 'config.txt'
    
    # Carregar configurações do arquivo
    configuracoes_subdominios = carregar_configuracoes_subdominios(caminho_arquivo)

    # Conectar ao Outlook e obter a quantidade inicial de e-mails
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)  # Caixa de Entrada
        initial_message_count = len(inbox.Items)  # Contagem inicial de e-mails
        print(f"Quantidade inicial de e-mails: {initial_message_count}")
    except Exception as e:
        print(f"Erro ao acessar o Outlook: {e}")
        return None  # Se houver erro no Outlook, retorna None

    if subdominio in configuracoes_subdominios:
        usuario = configuracoes_subdominios[subdominio]['usuario']
        senha = configuracoes_subdominios[subdominio]['senha']
    else:
        print(f"Configuração não encontrada para o subdomínio: {subdominio}")
        return None  # Se não encontrar a configuração, retorna None

    # URL do subdomínio
    url_inicial = f'https://{subdominio}.sienge.com.br/'
    navegador = webdriver.Chrome()
    navegador.get(url_inicial)

    # Maximizar a janela
    navegador.maximize_window()

    try:
        # Esperar até que o botão de login seja clicável
        fazerLoginComSiengeId = WebDriverWait(navegador, t).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnEntrarComSiengeID"]'))
        )
        fazerLoginComSiengeId.click()

        # Inserir o e-mail
        campo_email = WebDriverWait(navegador, t).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":r2:"]'))
        )
        campo_email.send_keys(usuario)

        # Clicar no botão de login
        botao = WebDriverWait(navegador, t).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/form/div/div[2]/button'))
        )
        botao.click()

        #time.sleep(2)

        # Inserir a senha
        campo_senha = WebDriverWait(navegador, t).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/form/div/div[1]/div[2]/div/div/input'))
        )
        campo_senha.send_keys(senha)

        # Clicar para confirmar o login
        botao = WebDriverWait(navegador, t).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/form/div/div[2]/button[1]'))
        )
        botao.click()

        #time.sleep(2)

        # Se o subdomínio for 'sej', realizar ações adicionais
        if subdominio == 'sej':
            # Aguarda e extrai o código
            codigo = esperar_codigo_sienge()
            preencher_codigo(codigo, navegador)

            botao = WebDriverWait(navegador, t).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/div/div/div/div[2]/form/div/button'))
            )
            botao.click()
            try:
                # Se o botão não for encontrado, tenta o link abaixo
                link = WebDriverWait(navegador, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="formEsqueceuSenha"]/div[2]/a[1]'))
                )
                link.click()
            except:
                pass
            
            time.sleep(3)

            # Extração de contas pagas
            navegador.get(url_inicial)
            
            
            try:
                # Se o botão não for encontrado, tenta o link abaixo
                link = WebDriverWait(navegador, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="formEsqueceuSenha"]/div[2]/a[1]'))
                )
                link.click()
            except:
                pass
            
            #time.sleep(5)

            # Extração de contas pagas
            navegador.get(url_inicial)
        
        else:
            try:
                # Se o botão não for encontrado, tenta o link abaixo
                link = WebDriverWait(navegador, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="formEsqueceuSenha"]/div[2]/a[1]'))
                )
                link.click()
            except:
                pass
            
            try:
                # Se o botão não for encontrado, tenta o link abaixo
                link = WebDriverWait(navegador, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="formEsqueceuSenha"]/div[2]/a[1]'))
                )
                link.click()
            except:
                pass
            
            
            time.sleep(3)            
        return navegador  # Retorna o navegador após login
    except Exception as e:
        print(f"Erro durante o login: {e}")
        navegador.quit()  # Fecha o navegador em caso de erro
        return None  # Retorna None se o login falhar
