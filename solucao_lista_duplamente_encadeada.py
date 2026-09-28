import time

class No:
    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.proximo = None

class ListaDuplamenteEncadeada:
    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    def inserir_inicio(self, valor):
        novo = No(valor)
        if self.cabeca is None:
            self.cabeca = self.cauda = novo
        else:
            novo.proximo = self.cabeca
            self.cabeca.anterior = novo
            self.cabeca = novo
        self.tamanho += 1

    def inserir_final(self, valor):
        novo = No(valor)
        if self.cauda is None:
            self.cabeca = self.cauda = novo
        else:
            novo.anterior = self.cauda
            self.cauda.proximo = novo
            self.cauda = novo
        self.tamanho += 1

    def buscar(self, valor):
        atual = self.cabeca
        while atual is not None:
            if atual.valor == valor:
                return atual
            atual = atual.proximo
        return None

    def remover(self, valor):
        no = self.buscar(valor)
        if no is None:
            return False

        if no.anterior is not None:
            no.anterior.proximo = no.proximo
        else:
            self.cabeca = no.proximo

        if no.proximo is not None:
            no.proximo.anterior = no.anterior
        else:
            self.cauda = no.anterior

        self.tamanho -= 1
        return True

    def listar_inicio_fim(self):
        valores = []
        atual = self.cabeca
        while atual is not None:
            valores.append(atual.valor)
            atual = atual.proximo
        return valores

    def listar_fim_inicio(self):
        valores = []
        atual = self.cauda
        while atual is not None:
            valores.append(atual.valor)
            atual = atual.anterior
        return valores

def demonstracao_basica():
    print("=== Sequencia obrigatoria ===")
    lista = ListaDuplamenteEncadeada()

    for v in (10, 20, 30, 40, 50):
        lista.inserir_final(v)

    lista.remover(30)

    print(" -> ".join(str(v) for v in lista.listar_inicio_fim()))
    print(" -> ".join(str(v) for v in lista.listar_fim_inicio()))
    print()

def teste_desempenho(n=100_000):
    print(f"=== Teste com {n} elementos ===")
    lista = ListaDuplamenteEncadeada()

    for i in range(n):
        lista.inserir_final(i)

    alvo_inicio = 100
    alvo_meio = n // 2
    alvo_final = n - 100

    for nome, alvo in (
        ("inicio", alvo_inicio),
        ("meio", alvo_meio),
        ("final", alvo_final),
    ):
        inicio = time.perf_counter()
        resultado = lista.buscar(alvo)
        fim = time.perf_counter()
        print(f"Busca proxima ao {nome} (valor {alvo}): "
              f"{fim - inicio:.6f} segundos (encontrado: {resultado is not None})")

if __name__ == "__main__":
    demonstracao_basica()
    teste_desempenho()
