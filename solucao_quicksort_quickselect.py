import random
import time
from pathlib import Path

def ler_numeros(caminho):
    with open(caminho, "r") as f:
        return [int(linha.strip()) for linha in f if linha.strip()]

def partition(arr, baixo, alto, stats):
    pivo_idx = random.randint(baixo, alto)
    arr[pivo_idx], arr[alto] = arr[alto], arr[pivo_idx]
    pivo = arr[alto]

    i = baixo - 1
    for j in range(baixo, alto):
        stats["comparacoes"] += 1
        if arr[j] <= pivo:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    return i + 1

def quicksort(arr, baixo, alto, stats):
    stats["chamadas"] += 1
    if baixo < alto:
        p = partition(arr, baixo, alto, stats)
        quicksort(arr, baixo, p - 1, stats)
        quicksort(arr, p + 1, alto, stats)

def executar_quicksort(numeros):
    arr = numeros.copy()
    stats = {"comparacoes": 0, "chamadas": 0}

    inicio = time.perf_counter()
    quicksort(arr, 0, len(arr) - 1, stats)
    fim = time.perf_counter()

    return arr, stats, fim - inicio

def quickselect(arr, baixo, alto, k, stats):
    stats["chamadas"] += 1

    if baixo == alto:
        return arr[baixo]

    p = partition(arr, baixo, alto, stats)

    if k == p:
        return arr[p]
    elif k < p:
        return quickselect(arr, baixo, p - 1, k, stats)
    else:
        return quickselect(arr, p + 1, alto, k, stats)

def executar_quickselect(numeros, k_esimo):
    arr = numeros.copy()
    stats = {"comparacoes": 0, "chamadas": 0}
    k = k_esimo - 1

    inicio = time.perf_counter()
    resultado = quickselect(arr, 0, len(arr) - 1, k, stats)
    fim = time.perf_counter()

    return resultado, stats, fim - inicio

def main():
    caminho = Path("/dados/numeros.txt")
    numeros = ler_numeros(caminho)
    n = len(numeros)
    K = 1000

    print(f"Total de numeros lidos: {n}\n")

    ordenado, stats_qs, tempo_qs = executar_quicksort(numeros)

    print("=== QuickSort ===")
    print(f"Comparacoes: {stats_qs['comparacoes']}")
    print(f"Chamadas recursivas: {stats_qs['chamadas']}")
    print(f"Tempo de execucao: {tempo_qs:.4f} segundos")
    print(f"{K}o menor numero (via QuickSort + acesso ao indice): {ordenado[K - 1]}\n")

    resultado_qsel, stats_qsel, tempo_qsel = executar_quickselect(numeros, K)

    print("=== QuickSelect ===")
    print(f"Comparacoes: {stats_qsel['comparacoes']}")
    print(f"Chamadas recursivas: {stats_qsel['chamadas']}")
    print(f"Tempo de execucao: {tempo_qsel:.4f} segundos")
    print(f"{K}o menor numero (via QuickSelect): {resultado_qsel}\n")

    print("=== Comparacao QuickSort+acesso vs QuickSelect ===")
    print(f"QuickSort + acesso: {tempo_qs:.4f} segundos")
    print(f"QuickSelect:        {tempo_qsel:.4f} segundos")
    if tempo_qsel > 0:
        print(f"QuickSelect foi {tempo_qs / tempo_qsel:.2f}x mais rapido")

    assert ordenado[K - 1] == resultado_qsel, "Resultados divergentes entre QuickSort e QuickSelect!"

if __name__ == "__main__":
    main()
