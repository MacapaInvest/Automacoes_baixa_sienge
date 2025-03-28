📊 Automacao de Baixas no Sienge

Este projeto é uma aplicação em Streamlit para automatizar o processo de baixas no sistema Sienge. A ferramenta permite carregar um arquivo Excel com os dados das parcelas, realizar as baixas de forma automatizada e gerar um relatório detalhado com o status de cada baixa.

🛠️ Funcionalidades

✅ Upload de Arquivo Excel:

Aceita arquivos no formato .xlsx contendo as colunas:

Cód SPE

Título

Parcela

✅ Processamento Automático:

Identifica o subdomínio a partir do Cód SPE.

Realiza login no ambiente do Sienge.

Executa as baixas com base nas informações fornecidas.

✅ Seleção de Conta Manual:

Quando há múltiplas contas bancárias disponíveis, o sistema permite a seleção manual antes de efetuar a baixa.

✅ Geração de Relatório:

Cria um arquivo Excel com o status de cada baixa ("Baixa realizada" ou "Falha").

Disponibiliza o download do relatório atualizado.

📊 Fluxo do Processo

Carregar Arquivo Excel:

O usuário faz o upload do arquivo com as informações das parcelas.

Configurar Data de Baixa:

A data de baixa é definida automaticamente.

Selecionar Conta Bancária (Se Necessário):

Caso existam múltiplas contas para um Cód SPE, o usuário pode selecionar manualmente.

Executar as Baixas:

O sistema realiza as baixas no Sienge, registrando o status de cada operação.

Baixar Relatório:

Após o processo, um arquivo Excel é gerado com as informações e o status de cada baixa.

📂 Estrutura do Projeto

📦 automacao-baixas-sienge
├── 📄 app.py                 # Código principal do Streamlit
├── 📄 baixas.py              # Função para realizar baixas
├── 📄 login.py               # Função para realizar login no Sienge
├── 📄 data.py                # Função para definir a data de baixa
├── 📄 consulta_conta.py      # Consulta de contas bancárias
└── 📄 lista_spe.py           # Mapeamento de Cód SPE para subdomínios

▶️ Executando o Projeto

📧 Configuração do Outlook e do config.txt

Para garantir o recebimento do código de acesso do Sienge, certifique-se de:

Ter o Outlook Desktop instalado e configurado na máquina.

Atualizar o arquivo config.txt com o subdomínio, e-mail e senha utilizados para o login no Sienge.

Exemplo de entrada no config.txt:

subdominio=seu-subdominio
email=seu-email@exemplo.com
senha=sua-senha

Se o e-mail e a senha estiverem corretos e o Outlook configurado, você poderá validar o código automaticamente ao efetuar o login.

Para garantir o recebimento do código de acesso do Sienge, certifique-se de:

Ter o Outlook Desktop instalado e configurado na máquina.

Atualizar o arquivo config.txt com o e-mail que será utilizado para receber o código de acesso.

Exemplo de entrada no config.txt:

email=seu-email@exemplo.com

Se o e-mail estiver correto e o Outlook configurado, você poderá validar o código automaticamente ao efetuar o login.

Certifique-se de ter o Python 3.10+ instalado em sua máquina.

Clone este repositório:

git clone https://github.com/seu-usuario/automacao-baixas-sienge.git
cd automacao-baixas-sienge

Crie um ambiente virtual (opcional, mas recomendado):

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Instale as dependências:

pip install -r requirements.txt

Execute a aplicação:

streamlit run app.py

📌 Requisitos

Python 3.10+

Streamlit

Pandas

Numpy

openpyxl

🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma Issue ou enviar um Pull Request.

Faça um Fork do repositório.

Crie um branch com sua feature:

git checkout -b minha-feature

Faça commit das suas alterações:

git commit -m 'Adicionar nova feature'

Envie suas alterações:

git push origin minha-feature

📄 Licença

Este projeto está licenciado sob a MIT License.

👨‍💻 Desenvolvido por Igor Costa Felix Santos


