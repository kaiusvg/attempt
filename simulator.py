import json
import csv
#inicio do código
def carregar_afd(arquivo):
    with open(arquivo, 'r') as f:
        dados = json.load(f)
    
    inicial = dados["initial"]
    finais = [0] * 100  
    for estado in dados["final"]:
        finais[estado] = 1
    
    transicoes = []
    for t in dados["transitions"]:
        transicoes.append((t["from"], t["read"], t["to"]))
    
    return inicial, finais, transicoes

def eh_final(estado, finais):
    return finais[estado] == 1

def proximo_estado(estado_atual, simbolo, transicoes):
    for de, simbolo_transicao, para in transicoes:
        if de == estado_atual and simbolo_transicao == simbolo:
            return para
    return -1

def aceita(palavra, inicial, finais, transicoes):
    estado_atual = inicial
    for simbolo in palavra:
        estado_atual = proximo_estado(estado_atual, simbolo, transicoes)
        if estado_atual == -1:
            return False
    return eh_final(estado_atual, finais)

def simular(arquivo_testes, arquivo_saida, inicial, finais, transicoes):
    with open(arquivo_testes, 'r') as in_file, open(arquivo_saida, 'w', newline='') as out_file:
        leitor = csv.reader(in_file, delimiter=';')
        escritor = csv.writer(out_file, delimiter=';')
        
        for linha in leitor:
            palavra = linha[0]
            esperado = int(linha[1])
            resultado = 1 if aceita(palavra, inicial, finais, transicoes) else 0
            escritor.writerow([palavra, esperado, resultado])

def main(arquivo_automato, arquivo_testes, arquivo_saida):
    inicial, finais, transicoes = carregar_afd(arquivo_automato)
    simular(arquivo_testes, arquivo_saida, inicial, finais, transicoes)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Uso: python simulador.py <automato.json> <testes.csv> <saida.csv>")
        sys.exit(1)
    
    arquivo_automato = sys.argv[1]
    arquivo_testes = sys.argv[2]
    arquivo_saida = sys.argv[3]
    
    main(arquivo_automato, arquivo_testes, arquivo_saida)
