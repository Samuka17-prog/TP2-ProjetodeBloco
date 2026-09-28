import asyncio
import time
from pathlib import Path

async def processar_arquivo(caminho: Path):

    def ler_arquivo():
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()

        linhas = conteudo.count("\n")
        if conteudo and not conteudo.endswith("\n"):
            linhas += 1

        palavras = len(conteudo.split())
        return linhas, palavras

    linhas, palavras = await asyncio.to_thread(ler_arquivo)
    return caminho.name, linhas, palavras

async def main():
    pasta = Path("/dados/arquivos")
    arquivos = [a for a in pasta.iterdir() if a.is_file()]

    inicio = time.perf_counter()

    tasks = [asyncio.create_task(processar_arquivo(a)) for a in arquivos]
    resultados = await asyncio.gather(*tasks)

    fim = time.perf_counter()

    for nome, linhas, palavras in resultados:
        print(nome)
        print(f"Linhas: {linhas}")
        print(f"Palavras: {palavras}")
        print()

    print(f"Tempo total: {fim - inicio:.2f} segundos")

if __name__ == "__main__":
    asyncio.run(main())
