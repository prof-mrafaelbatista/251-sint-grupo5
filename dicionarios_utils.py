import os

# 1. Altere o nome do arquivo para .txt
CAMINHO_ARQUIVO = 'dicionario.txt' # Ou use os.path.join(BASE_DIR, 'dicionario.txt') como antes para mais robustez

# Se quiser usar BASE_DIR para garantir que o arquivo fique na mesma pasta do script:
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CAMINHO_ARQUIVO = os.path.join(BASE_DIR, 'dicionario.txt')


def carregar_termos():
    """
    Carrega os termos do dicionário de um arquivo de texto simples.
    Cada linha deve estar no formato: termo::definicao
    Retorna um dicionário com os termos e suas definições.
    Cria um arquivo vazio se ele não existir.
    """
    termos = {}
    if not os.path.exists(CAMINHO_ARQUIVO):
        # Cria o arquivo se ele não existir, para evitar erro na primeira execução
        open(CAMINHO_ARQUIVO, 'w', encoding='utf-8').close() 
        print(f"Arquivo '{CAMINHO_ARQUIVO}' não encontrado. Criando arquivo vazio.")

    try:
        with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip() # Remove espaços em branco extras e quebras de linha
                if '::' in linha:
                    # Divide a linha no primeiro '::' encontrado
                    partes = linha.split('::', 1)
                    if len(partes) == 2:
                        termo, definicao = partes
                        termos[termo.strip()] = definicao.strip()
                    else:
                        # Linha mal formatada (apenas uma parte após o split)
                        print(f"Aviso: Linha mal formatada ignorada no arquivo '{CAMINHO_ARQUIVO}': {linha}")
                elif linha: # Linha não vazia mas sem o delimitador
                    print(f"Aviso: Linha sem delimitador '::' ignorada no arquivo '{CAMINHO_ARQUIVO}': {linha}")
    except Exception as e:
        print(f"Erro ao carregar dicionário de '{CAMINHO_ARQUIVO}': {e}. Iniciando dicionário vazio.")
        termos = {} # Garante que termos seja um dicionário em caso de erro
        
    return termos

def salvar_termos(termos):
    """
    Salva os termos do dicionário em um arquivo de texto simples.
    Cada termo e definição será salvo em uma nova linha no formato: termo::definicao
    """
    try:
        with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as f:
            for termo, definicao in termos.items():
                # Garante que o termo e a definição não contenham quebras de linha internas
                # que poderiam corromper o formato linha a linha.
                # Se precisarem de múltiplas linhas, o formato JSON era melhor.
                termo_limpo = str(termo).replace('\n', ' ').replace('\r', '')
                definicao_limpa = str(definicao).replace('\n', ' ').replace('\r', '')
                f.write(f"{termo_limpo}::{definicao_limpa}\n")
        print(f"Termos salvos com sucesso em {CAMINHO_ARQUIVO}")
    except Exception as e:
        print(f"Erro ao salvar termos em {CAMINHO_ARQUIVO}: {e}")

# Pequeno teste (opcional, pode ser removido ou comentado)
if __name__ == '__main__':
    # Teste de carregamento
    meus_termos = carregar_termos()
    print("Termos carregados:", meus_termos)

    # Teste de adição e salvamento
    meus_termos["TermoTXT1"] = "Definição do Termo TXT 1."
    meus_termos["OutroTermo"] = "Outra definição aqui."
    salvar_termos(meus_termos)

    # Teste de recarregamento
    termos_recarregados = carregar_termos()
    print("Termos recarregados:", termos_recarregados)

    if "TermoTXT1" in termos_recarregados:
        print("Teste de persistência em TXT passou!")
    else:
        print("Falha no teste de persistência em TXT.")