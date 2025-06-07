from flask import Flask, render_template, request, redirect, url_for, flash 
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Importando o módulo de utilidades do dicionário

from dicionarios_utils import carregar_termos, salvar_termos

# --- INICIALIZAÇÃO DO FLASK  ---
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'uma_chave_secreta_padrao_forte') # Necessário para flash messages

# --- CONFIGURAÇÃO DO GEMINI ---
load_dotenv()
gemini_api_key = os.getenv('GOOGLE_API_KEY')

if not gemini_api_key:
    raise ValueError("A variável de ambiente 'GOOGLE_API_KEY' não está definida. "
                     "Por favor, crie um arquivo .env com sua chave.")

genai.configure(api_key=gemini_api_key)

# Inicializar o modelo Gemini
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    print(f"Erro ao inicializar o modelo Gemini: {e}")
    model = None # Define model como None se houver erro na inicialização

# --- DEFINIÇÃO DA EQUIPE (Variável Global) ---
equipe_data = [
    {
        "nome": "Luana Patrícia Gomes da Silva",
        "github": "https://github.com/luanapatriciasilva",
        "foto": "static/images/luana.jpg",
        "descricao": "Sistemas para Internet, Uniesp -PB. Apaixonada por tecnologia e programação."
    }
]

# --- ROTAS DA APLICAÇÃO ---

# Rota para a Página Inicial
@app.route('/')
def pagina_inicial():
    return render_template('index.html', titulo_pagina="Página Inicial")

# Rota do Gemini (IA)
@app.route('/ia', methods=['GET', 'POST'])
def ia():
    ai_response = None
    error = None
    user_input = ""

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        if not model:
            error = "O modelo Gemini não foi inicializado. Verifique sua chave da API e conexão."
        elif not user_input.strip():
            error = "Por favor, digite sua pergunta."
        else:
            try:
                response = model.generate_content(user_input)
                ai_response = response.text
            except Exception as e:
                error = f"Erro ao obter resposta do Gemini: {e}"
                flash(f"Erro ao contatar o Gemini: {e}", "danger")


    return render_template('ia.html',
                           ai_response=ai_response,
                           user_input=user_input,
                           error=error,
                           titulo_pagina="Interagir com IA")

# Rota para a Página da Equipe
@app.route('/equipe')
def pagina_equipe():
    return render_template('equipe.html', titulo_pagina="Nossa Equipe", equipe=equipe_data)

# Rotas de Fundamentos
@app.route('/fundamentos')
def fundamentos():
    return render_template('fundamentos.html', titulo_pagina="Fundamentos da Programação")

@app.route('/selecao')
def fundamentos_selecao():
    return render_template('selecao.html', titulo_pagina="Estruturas de Seleção")

@app.route('/repeticao')
def fundamentos_repeticao():
    return render_template('repeticao.html', titulo_pagina="Estruturas de Repetição")

@app.route('/vetores-matrizes')
def fundamentos_vetores_matrizes():
    return render_template('vetores_matrizes.html', titulo_pagina="Vetores e Matrizes")

@app.route('/funcoes')
def fundamentos_funcoes():
    return render_template('funcoes.html', titulo_pagina="Funções e Procedimentos")

@app.route('/excecoes')
def fundamentos_excecoes():
    return render_template('excecoes.html', titulo_pagina="Tratamento de Exceções")

# Rotas do Dicionário de Termos
@app.route('/dicionario')
def dicionario():
    termos = carregar_termos()
    return render_template('dicionario.html', termos=termos, titulo_pagina="Dicionário de Termos")

@app.route('/adicionar', methods=['POST'])
def adicionar():
    termo = request.form.get('termo', '').strip()
    definicao = request.form.get('definicao', '').strip()

    if termo and definicao:
        termos = carregar_termos()
        if termo in termos:
            flash(f"O termo '{termo}' já existe. Use a função de alterar se desejar modificá-lo.", "warning")
        else:
            termos[termo] = definicao
            salvar_termos(termos)
            flash(f"Termo '{termo}' adicionado com sucesso!", "success")
    else:
        flash("Termo e definição não podem estar vazios.", "danger")

    return redirect(url_for('dicionario'))

# FUNÇÃO ALTERAR MODIFICADA
@app.route('/alterar', methods=['POST'])
def alterar():
    termo_original = request.form.get('termo_original', '').strip()
    novo_termo = request.form.get('novo_termo', '').strip()
    nova_definicao = request.form.get('nova_definicao', '').strip()

    if not termo_original or not novo_termo or not nova_definicao:
        flash("Para alterar, todos os campos (termo original, novo termo e nova definição) são obrigatórios.", "danger")
        return redirect(url_for('dicionario'))

    termos = carregar_termos()

    if termo_original not in termos:
        flash(f"Erro: Termo original '{termo_original}' não encontrado para alteração.", "danger")
        return redirect(url_for('dicionario'))

    # Se o nome do termo foi alterado E o novo nome já existe (e não é o próprio termo original)
    if novo_termo != termo_original and novo_termo in termos:
        flash(f"Erro: O novo nome de termo '{novo_termo}' já existe. Escolha outro nome.", "warning")
        return redirect(url_for('dicionario'))

    # Processar a alteração
    if novo_termo != termo_original:
        # O nome do termo mudou: remover o antigo e adicionar o novo
        del termos[termo_original]
        termos[novo_termo] = nova_definicao
        flash(f"Termo '{termo_original}' renomeado para '{novo_termo}' e definição atualizada!", "success")
    else:
        # O nome do termo não mudou, apenas atualiza a definição
        termos[termo_original] = nova_definicao
        flash(f"Definição do termo '{termo_original}' atualizada com sucesso!", "success")

    salvar_termos(termos)
    return redirect(url_for('dicionario'))

@app.route('/deletar', methods=['POST'])
def deletar():
    termo = request.form.get('termo', '').strip() # Adicionado strip
    if not termo:
        flash("Nenhum termo selecionado para deletar.", "warning")
        return redirect(url_for('dicionario'))

    termos = carregar_termos()
    if termo in termos:
        del termos[termo]
        salvar_termos(termos)
        flash(f"Termo '{termo}' deletado com sucesso!", "success")
    else:
        flash(f"Termo '{termo}' não encontrado para deleção.", "warning")
    return redirect(url_for('dicionario'))

if __name__ == '__main__':
    app.run(debug=True)