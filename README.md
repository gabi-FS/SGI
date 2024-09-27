# SGI

Sistema Gráfico Interativo para a disciplina INE5420 - Computação Gráfica.
Feito com GTK e GDK.

Alunas: Gabriela Furtado da Silveira e Samantha Costa de Sousa

## Como rodar

Executar o seguinte comando no diretório raiz do projeto:

```bash
python3 main.py
```

### Interação

Todas as interações requisitadas nas entregas são feitas por interface, inputs de teste em `./test_examples`.

Possíveis erros de validação são capturados e aparecem no terminal.

**Alternativas para ações implementadas até o momento:**

- Zoom: Scroll do mouse

### Importação e exportação de arquivos

Seguindo o formato Wavefront.obj, as diretivas aceitas para desenho são: p, l e f.

A importação de arquivos sempre será limitada ao que é possível fazer no SGI na versão atual.
Exemplo: se o sistema atualmente é 2D, o eixo z do arquivo não será utilizado, apesar de ser requisito para o formato Wavefront.
