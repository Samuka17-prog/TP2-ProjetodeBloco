from pathlib import Path
import sys

sys.setrecursionlimit(10000)

def ler_labirinto(caminho):
    with open(caminho, "r") as f:
        linhas = [linha.rstrip("\n") for linha in f if linha.strip("\n") != ""]
    grade = [list(linha) for linha in linhas]
    return grade

def encontrar_posicao(grade, alvo):
    for i, linha in enumerate(grade):
        for j, char in enumerate(linha):
            if char == alvo:
                return (i, j)
    return None

def dentro_dos_limites(grade, i, j):
    return 0 <= i < len(grade) and 0 <= j < len(grade[i])

def resolver_labirinto(grade, atual, fim, visitados, caminho):
    i, j = atual

    if not dentro_dos_limites(grade, i, j):
        return False
    if grade[i][j] == "#":
        return False
    if atual in visitados:
        return False

    visitados.add(atual)
    caminho.append(atual)

    if atual == fim:
        return True

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in direcoes:
        proxima = (i + di, j + dj)
        if resolver_labirinto(grade, proxima, fim, visitados, caminho):
            return True

    caminho.pop()
    return False

def imprimir_com_caminho(grade, caminho, inicio, fim):
    caminho_set = set(caminho)
    for i, linha in enumerate(grade):
        linha_str = ""
        for j, char in enumerate(linha):
            pos = (i, j)
            if pos == inicio:
                linha_str += "S"
            elif pos == fim:
                linha_str += "E"
            elif pos in caminho_set and char not in ("S", "E"):
                linha_str += "*"
            else:
                linha_str += char
        print(linha_str)

def main():
    caminho_arquivo = Path("/dados/labirinto.txt")
    grade = ler_labirinto(caminho_arquivo)

    inicio = encontrar_posicao(grade, "S")
    fim = encontrar_posicao(grade, "E")

    if inicio is None or fim is None:
        print("Labirinto sem posicao S (inicio) ou E (saida) definida.")
        return

    visitados = set()
    caminho = []

    encontrou = resolver_labirinto(grade, inicio, fim, visitados, caminho)

    if encontrou:
        print("Caminho encontrado!\n")
        imprimir_com_caminho(grade, caminho, inicio, fim)
        print(f"\nTamanho do caminho: {len(caminho)} posicoes")
    else:
        print("Nao existe caminho entre S e E.")

if __name__ == "__main__":
    main()
