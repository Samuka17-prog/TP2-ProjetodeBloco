#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <omp.h>
 
#define MAX_ARQUIVOS 1000
#define MAX_NOME 256
#define MAX_CAMINHO 512
 
typedef struct {
    char nome[MAX_NOME];
    long linhas;
    long palavras;
} Resultado;
 
void processar_arquivo(const char *caminho, long *linhas, long *palavras) {
    FILE *f = fopen(caminho, "r");
    if (!f) {
        *linhas = 0;
        *palavras = 0;
        return;
    }
 
    long total_linhas = 0;
    long total_palavras = 0;
    int dentro_palavra = 0;
    int c;
    int ultimo_char = '\n';
 
    while ((c = fgetc(f)) != EOF) {
        if (c == '\n') {
            total_linhas++;
        }
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
            dentro_palavra = 0;
        } else if (!dentro_palavra) {
            dentro_palavra = 1;
            total_palavras++;
        }
        ultimo_char = c;
    }
    if (ultimo_char != '\n' && ultimo_char != EOF) {
        total_linhas++;
    }
 
    fclose(f);
    *linhas = total_linhas;
    *palavras = total_palavras;
}
 
int main(void) {
    const char *diretorio = "/dados/arquivos";
    DIR *d = opendir(diretorio);
    if (!d) {
        perror("Erro ao abrir diretorio");
        return 1;
    }
 
    char caminhos[MAX_ARQUIVOS][MAX_CAMINHO];
    char nomes[MAX_ARQUIVOS][MAX_NOME];
    int total = 0;
 
    struct dirent *entrada;
    while ((entrada = readdir(d)) != NULL && total < MAX_ARQUIVOS) {
        if (entrada->d_type == DT_REG) {
            snprintf(caminhos[total], MAX_CAMINHO, "%s/%s", diretorio, entrada->d_name);
            strncpy(nomes[total], entrada->d_name, MAX_NOME - 1);
            nomes[total][MAX_NOME - 1] = '\0';
            total++;
        }
    }
    closedir(d);
 
    Resultado resultados[MAX_ARQUIVOS];
 
    double inicio = omp_get_wtime();
 
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < total; i++) {
        long linhas, palavras;
        processar_arquivo(caminhos[i], &linhas, &palavras);
        strncpy(resultados[i].nome, nomes[i], MAX_NOME - 1);
        resultados[i].nome[MAX_NOME - 1] = '\0';
        resultados[i].linhas = linhas;
        resultados[i].palavras = palavras;
    }
 
    double fim = omp_get_wtime();
 
    for (int i = 0; i < total; i++) {
        printf("%s\n", resultados[i].nome);
        printf("Linhas: %ld\n", resultados[i].linhas);
        printf("Palavras: %ld\n", resultados[i].palavras);
        printf("\n");
    }
 
    printf("Tempo total: %.4f segundos\n", fim - inicio);
 
    return 0;
}
