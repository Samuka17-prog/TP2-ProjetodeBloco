import time
from pathlib import Path

def ler_itens(caminho):
    with open(caminho, "r") as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    primeira = linhas[0].split()
    quantidade_itens = int(primeira[0])
    capacidade = int(primeira[1])

    itens = []
    for linha in linhas[1:1 + quantidade_itens]:
        partes = linha.split()

        peso = int(partes[1])
        valor = int(partes[2])
        itens.append((peso, valor))

    return itens, capacidade

def mochila_recursiva(itens, indice, capacidade, stats):
    stats["chamadas"] += 1

    if indice == len(itens) or capacidade == 0:
        return 0

    peso, valor = itens[indice]

    if peso > capacidade:
        return mochila_recursiva(itens, indice + 1, capacidade, stats)

    nao_pegar = mochila_recursiva(itens, indice + 1, capacidade, stats)
    pegar = valor + mochila_recursiva(itens, indice + 1, capacidade - peso, stats)

    return max(nao_pegar, pegar)

def executar_parte_a(itens, capacidade):
    stats = {"chamadas": 0}
    inicio = time.perf_counter()
    resultado = mochila_recursiva(itens, 0, capacidade, stats)
    fim = time.perf_counter()
    return resultado, stats, fim - inicio

def mochila_memoizada(itens, indice, capacidade, memo, stats):
    if indice == len(itens) or capacidade == 0:
        return 0

    chave = (indice, capacidade)
    if chave in memo:
        return memo[chave]

    stats["estados"] += 1

    peso, valor = itens[indice]

    if peso > capacidade:
        resultado = mochila_memoizada(itens, indice + 1, capacidade, memo, stats)
    else:
        nao_pegar = mochila_memoizada(itens, indice + 1, capacidade, memo, stats)
        pegar = valor + mochila_memoizada(itens, indice + 1, capacidade - peso, memo, stats)
        resultado = max(nao_pegar, pegar)

    memo[chave] = resultado
    return resultado

def executar_parte_b(itens, capacidade):
    memo = {}
    stats = {"estados": 0}
    inicio = time.perf_counter()
    resultado = mochila_memoizada(itens, 0, capacidade, memo, stats)
    fim = time.perf_counter()
    return resultado, stats, fim - inicio

def main():
    itens, capacidade = ler_itens(Path("/dados/mochila.txt"))
    print(f"Total de itens lidos: {len(itens)}")
    print(f"Capacidade da mochila: {capacidade}\n")

    print("=== Parte A: Recursiva pura ===")
    valor_a, stats_a, tempo_a = executar_parte_a(itens, capacidade)
    print(f"Valor maximo encontrado: {valor_a}")
    print(f"Chamadas recursivas: {stats_a['chamadas']}")
    print(f"Tempo de execucao: {tempo_a:.4f} segundos\n")

    print("=== Parte B: Programacao dinamica (memoizacao) ===")
    valor_b, stats_b, tempo_b = executar_parte_b(itens, capacidade)
    print(f"Valor maximo encontrado: {valor_b}")
    print(f"Estados calculados: {stats_b['estados']}")
    print(f"Tempo de execucao: {tempo_b:.4f} segundos\n")

    print("=== Comparacao ===")
    print(f"Recursiva pura: {tempo_a:.4f}s / {stats_a['chamadas']} chamadas")
    print(f"Prog. dinamica: {tempo_b:.4f}s / {stats_b['estados']} estados")
    if tempo_b > 0:
        print(f"Programacao dinamica foi {tempo_a / tempo_b:.2f}x mais rapida")

    assert valor_a == valor_b, "Resultados divergentes entre as duas abordagens!"

if __name__ == "__main__":
    main()
