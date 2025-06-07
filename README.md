Aluna: Luana Patricia Gomes da Silva
# Site Educacional Interativo com Python e Gemini

Este projeto visa desenvolver uma aplicação web interativa utilizando o framework Flask para criar um site informativo sobre os fundamentos da programação em Python, incluindo uma funcionalidade de perguntas e respostas integrada com a API do Gemini e um dicionário interativo de termos de programação com persistência em arquivo de texto.

## Índice

* [Estrutura do Site](#estrutura-do-site)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Integração com a API do Gemini](#integração-com-a-api-do-gemini)
* [Como Executar Localmente](#como-executar-localmente)
* [Principais Partes do Código Python](#principais-partes-do-código-python)

---

## Estrutura do Site

O site é organizado nas seguintes seções principais:

* **Página Inicial (`/`):**
    * Renderizada por `index.html`.
    * **Conteúdo:** Apresenta uma introdução ao site, destacando os recursos de aprendizado sobre fundamentos de Python e a funcionalidade de interação com a IA. Contém links rápidos para as principais seções.
* **Dicionário de Termos (`/dicionario`):**
    * Renderizada por `dicionario.html`.
    * **Conteúdo:** Exibe uma lista de termos técnicos de programação com suas definições. Permite aos usuários adicionar novos termos, alterar definições existentes e deletar termos. Os dados são persistidos no arquivo `dicionario.txt`.
* **Fundamentos da Programação (Menu Dropdown):**
    * Esta seção do menu agrupa links diretos para páginas que detalham conceitos chave da programação em Python:
        * **Estruturas de Seleção (`/selecao`):**
            * Renderizada por `selecao.html`.
            * **Conteúdo:** Explica o uso de `if`, `elif`, e `else` em Python, com exemplos de sintaxe e casos de uso.
        * **Estruturas de Repetição (`/repeticao`):**
            * Renderizada por `repeticao.html`.
            * **Conteúdo:** Detalha os loops `for` e `while`, e as instruções `break` e `continue`.
        * **Vetores e Matrizes (`/vetores-matrizes`):**
            * Renderizada por `vetores_matrizes.html`.
            * **Conteúdo:** Demonstra como listas Python podem ser usadas para representar vetores (listas unidimensionais) e matrizes (listas de listas).
        * **Funções e Procedimentos (`/funcoes`):**
            * Renderizada por `funcoes.html`.
            * **Conteúdo:** Cobre a definição de funções, uso de parâmetros, argumentos posicionais e nomeados, `*args`, `**kwargs`, docstrings e escopo de variáveis.
        * **Tratamento de Exceções (`/excecoes`):**
            * Renderizada por `excecoes.html`.
            * **Conteúdo:** Explica o tratamento de erros usando `try`, `except`, `else`, `finally`, e a instrução `raise`.
* **Pergunte à IA (`/ia`):**
    * Renderizada por `ia.html`.
    * **Conteúdo:** Oferece uma interface onde o usuário pode digitar uma pergunta. A pergunta é enviada ao modelo de IA Google Gemini, e a resposta gerada é exibida na página.
* **Equipe (`/equipe`):**
    * Renderizada por `equipe.html`.
    * **Conteúdo:** Apresenta informações sobre a desenvolvedora do projeto, Luana Patrícia Gomes da Silva.

---

## Tecnologias Utilizadas

* **Linguagem de Programação Principal:** Python
* **Framework Web:** Flask 3.1.1
* **Frontend:**
    * HTML5
    * CSS3 (arquivo `static/css/style.css` e estilos inline)
    * JavaScript (arquivos `static/js/script.js`, `static/js/pergunte_ia.js`; JavaScript inline em `dicionario.html`)
    * Bootstrap 5.3.3 (via CDN)
    * Bootstrap Icons 1.11.3 (via CDN)
* **API de Inteligência Artificial:** Google Gemini API
    * Biblioteca cliente Python: `google-generativeai==0.8.5` (configurado em `app.py` para usar o modelo "gemini-1.5-pro")
* **Gerenciamento de Variáveis de Ambiente:** `python-dotenv==1.1.0`
* **Servidor WSGI (Desenvolvimento):** Werkzeug 3.1.3 (dependência do Flask)
* **Motor de Template:** Jinja2 3.1.6 (dependência do Flask)
* **Armazenamento de Dados (Dicionário):** Arquivo de texto simples (`dicionario.txt`)
* **Outras bibliotecas Python relevantes (de `requirements.txt`):**
    * `click==8.2.1`
    * `itsdangerous==2.2.0`
    * `MarkupSafe==3.0.2`
    * `google-api-core==2.25.0rc1`
    * `google-auth==2.40.2`
    * `protobuf==5.29.5`
* **Controle de Versão:** Git e GitHub (implícito)

---

## Integração com a API do Gemini

A integração com a API Google Gemini é implementada da seguinte forma no arquivo `app.py`:

1.  **Configuração da Chave da API:**
    * A chave da API do Google Gemini é carregada de uma variável de ambiente chamada `GOOGLE_API_KEY`.
    * Isso é feito utilizando a biblioteca `python-dotenv` para carregar o arquivo `.env` e `os.getenv()` para ler a variável.
    * Uma verificação garante que a chave da API está definida, caso contrário, um erro é levantado.
2.  **Inicialização do Cliente:**
    * A biblioteca `google.generativeai` (importada como `genai`) é configurada com a chave da API usando `genai.configure(api_key=gemini_api_key)`.
3.  **Inicialização do Modelo:**
    * Uma instância do modelo generativo é criada com `model = genai.GenerativeModel("gemini-1.5-pro")`.
    * Há um bloco `try-except` para capturar possíveis erros durante a inicialização do modelo (por exemplo, chave inválida ou problemas de conexão). Se ocorrer um erro, `model` é definido como `None`.
4.  **Processamento de Requisições na Rota `/ia`:**
    * Esta rota aceita métodos GET (para exibir a página) e POST (para enviar uma pergunta).
    * Quando um formulário é submetido (POST), a pergunta do usuário (`user_input`) é obtida.
    * Verifica-se se o modelo foi inicializado corretamente e se o usuário de fato digitou uma pergunta.
    * A pergunta é enviada ao modelo Gemini através de `response = model.generate_content(user_input)`.
    * A resposta de texto é extraída de `response.text`.
    * Qualquer exceção durante a chamada à API é capturada, e uma mensagem de erro é preparada.
5.  **Exibição da Resposta:**
    * A resposta da IA (`ai_response`) ou a mensagem de erro (`error`) são passadas para o template `ia.html` para serem exibidas ao usuário.

---

## Como Executar Localmente

Siga os passos abaixo para executar a aplicação em seu ambiente local:

**Pré-requisitos:**

* Python 3.x instalado
* Pip (gerenciador de pacotes Python)
* Git (para clonar o repositório)
* Uma chave de API do Google Gemini. Você pode obter uma no [Google AI Studio](https://aistudio.google.com/app/apikey).

**Passos:**

1.  **Clone o repositório (se estiver no GitHub):**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO_GIT>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```
    Se não estiver usando Git, apenas certifique-se de ter todos os arquivos do projeto em uma pasta local.

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    Navegue até a pasta raiz do projeto (onde o arquivo `requirements.txt` está localizado) e execute:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    * Crie um arquivo chamado `.env` na raiz do projeto (na mesma pasta que `app.py`).
    * Adicione sua chave da API do Google Gemini ao arquivo `.env` da seguinte forma:
        ```env
        GOOGLE_API_KEY="SUA_CHAVE_API_AQUI"
        ```
    * (Opcional) Você também pode adicionar configurações do Flask ao `.env` se desejar, embora `app.py` já configure `debug=True` ao executar diretamente:
        ```env
        FLASK_APP="app.py"
        FLASK_DEBUG=True
        ```

5.  **Execute a aplicação Flask:**
    Você pode executar a aplicação de duas formas:
    * Usando o comando `flask`:
        ```bash
        # Se você definiu FLASK_APP e FLASK_DEBUG no .env ou exportou como variáveis de ambiente:
        flask run
        ```
    * Executando o script `app.py` diretamente (ele contém `app.run(debug=True)`):
        ```bash
        python app.py
        ```

6.  **Acesse a aplicação:**
    Abra seu navegador e acesse: `http://127.0.0.1:5000/` (ou a porta que o Flask indicar no terminal).

---

## Principais Partes do Código Python

* **`app.py`:**
    * **Descrição:** Este é o arquivo principal da aplicação Flask. Ele configura o servidor, define as rotas (URLs) do site, gerencia a lógica de cada rota, integra-se com a API Gemini e renderiza os templates HTML.
    * **Funcionalidades Chave:**
        * Inicialização do aplicativo Flask.
        * Configuração e inicialização do cliente da API Google Gemini, incluindo carregamento da chave da API a partir de variáveis de ambiente.
        * Definição de rotas usando o decorador `@app.route()`:
            * `/`: Rota para a página inicial (`index.html`).
            * `/ia`: Rota para a página de interação com a IA, lidando com a submissão de perguntas do usuário e a exibição das respostas do Gemini.
            * `/equipe`: Rota para a página "Equipe", que exibe dados estáticos sobre os membros.
            * `/selecao`, `/repeticao`, `/vetores-matrizes`, `/funcoes`, `/excecoes`: Rotas que servem páginas HTML com conteúdo educacional sobre fundamentos de Python. A rota `/fundamentos` existe, mas não possui uma página HTML própria; ela é conceitualmente o agrupamento dessas sub-páginas.
            * `/dicionario`: Rota para visualizar os termos do dicionário.
            * `/adicionar`, `/alterar`, `/deletar`: Rotas POST para manipular os dados do dicionário (adicionar, alterar e deletar termos), utilizando as funções de `dicionarios_utils.py`.
        * O arquivo também contém uma seção `if __name__ == '__main__':` que inicia o servidor de desenvolvimento Flask com `app.run(debug=True)`. A parte do código com `input()` após `app.run()` nesta seção provavelmente não será alcançada enquanto o servidor Flask estiver em execução, pois `app.run()` bloqueia a execução até que o servidor seja parado.

* **`dicionarios_utils.py`:**
    * **Descrição:** Módulo utilitário responsável pela lógica de persistência (leitura e escrita) dos termos do dicionário em um arquivo de texto (`dicionario.txt`).
    * **Constantes:**
        * `CAMINHO_ARQUIVO`: Define o nome do arquivo (`dicionario.txt`) onde os termos são armazenados.
    * **Funções Principais:**
        * `carregar_termos()`: Lê o arquivo `dicionario.txt`, analisa cada linha (esperando o formato `termo::definicao`), e retorna um dicionário Python. Trata casos onde o arquivo não existe (criando um vazio) ou linhas mal formatadas.
        * `salvar_termos(termos)`: Recebe um dicionário de termos e o escreve no arquivo `dicionario.txt`, sobrescrevendo o conteúdo anterior, com cada entrada no formato `termo::definicao`.
    * Inclui um bloco `if __name__ == '__main__':` para testes unitários das funcionalidades de carga e salvamento, permitindo executar este arquivo diretamente para verificar sua corretude.


