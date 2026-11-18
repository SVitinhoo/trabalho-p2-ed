# 🎬 Vídeo Explicativo:
> Link do vídeo: https://www.youtube.com/watch?v=uyKRUeW8RHw

---

## 1. Identificação

| Campo | Informação |
|---|---|
| **Nome completo** | Victor Hugo Felipe Moreira |
| **RA** | 2840482521017 |
| **Tema escolhido** | Quick Sort vs Merge Sort |

## Como executar

```
pip install flask
cd src
python servidor.py        # abra http://localhost:5000
python algoritmo.py       # testa só os algoritmos no terminal (3 cenários)
```

**Estrutura do projeto**

- `src/algoritmo.py`: toda a lógica (Quick Sort, Merge Sort, geração de arrays e métricas)
- `src/servidor.py`: servidor Flask (entrega o site e a rota `POST /api/ordenar`)
- `src/demo/`: `index.html`, `styles.css` e `app.js` (apenas desenham os passos recebidos)

**Arquitetura:** o Python executa o algoritmo inteiro e grava um "quadro" (foto do estado) a cada comparação, troca ou escrita. O JavaScript recebe a lista de quadros e só os exibe.

---

## 2. Resumo Teórico e Complexidade Assintótica

### Quick Sort

**Como funciona:** usa a estratégia *dividir para conquistar*. Escolhe um **pivô** (neste projeto, o último elemento do trecho) e faz a **partição**: os menores que o pivô ficam à esquerda e os maiores à direita, e o pivô fica na posição definitiva. Depois repete o processo, recursivamente, nos dois lados. A ordenação é feita **no próprio array**, sem cópias.

**Onde é usado no mundo real:** é a base de muitas rotinas de ordenação de bibliotecas, como o `qsort` da linguagem C, o `std::sort` do C++ (variante *introsort*) e o `Arrays.sort` para tipos primitivos em Java (quicksort de pivô duplo). É muito usado quando se quer velocidade e pouca memória extra.

### Merge Sort

**Como funciona:** também usa *dividir para conquistar*. Divide o array **sempre ao meio** até restarem trechos de 1 elemento e depois **intercala** (merge) as metades já ordenadas, usando vetores auxiliares, até reconstruir o array completo. Com a comparação `<=`, mantém a ordem dos elementos iguais (é **estável**).

**Onde é usado no mundo real:** é a base do **Timsort**, algoritmo usado por `sorted()`/`list.sort()` do Python e por `Arrays.sort` de objetos em Java. Também é usado em ordenação de listas encadeadas, em ordenação externa (dados maiores que a memória, como em bancos de dados) e sempre que a estabilidade é necessária.

### Tabela de Complexidade

| Algoritmo | Caso | Tempo | Espaço auxiliar |
|---|---|---|---|
| **Quick Sort** | Melhor caso | O(n log n) | O(log n) |
| | Caso médio | O(n log n) | O(log n) |
| | **Pior caso** | **O(n²)** | O(n) |
| **Merge Sort** | Melhor caso | O(n log n) | O(n) |
| | Caso médio | O(n log n) | O(n) |
| | Pior caso | O(n log n) | O(n) |

> O espaço auxiliar do Quick Sort vem apenas da **pilha de recursão** (ele ordena no próprio array). No Merge Sort vem dos **vetores auxiliares** da intercalação, mais a pilha O(log n).

### Por que o pior caso ocorre

- **Quick Sort (pivô fixo no último elemento):** o pior caso acontece quando o pivô é sempre o menor ou o maior elemento do trecho, como em um **array já ordenado**, ou com **todos os valores iguais**. Cada partição fica 0 / n−1, então a recursão tem profundidade n e o total de comparações é n + (n−1) + ... + 1 = n(n−1)/2, ou seja, O(n²). No simulador, o botão **"Cenário Pior Caso"** demonstra isso: com n=30, o Quick faz 435 comparações e a profundidade chega a 30.
- **Merge Sort:** a divisão é sempre ao meio, independente dos dados. A altura da recursão é log₂n e cada nível intercala n elementos, então o custo é O(n log n) em qualquer entrada. Com n=30 no mesmo cenário, ele faz 77 comparações.

---

### Conclusão
- Na maior parte dos casos o Quick Sort será mais pesado que o Merge Sort caso o pivô seja fixo, quando um bom pivô é escolhido (por meio de outras algoritmos por exemplo) o Quick Sort supera em muita das vezes o Merge Sort.

## 3. Diário de Engenharia com IA

### Qual modelo/ferramenta foi utilizado?

**Claude (Anthropic), modelo Claude Sonnet 5.5**, pela interface de chat claude.ai, com geração de arquivos e execução de código para testar o projeto.

### Os principais prompts

**Prompts principais**
> "Preciso de um Simulador Visual Interativo em html, css e js, o projeto é sobre os algoritmos de Quick Sort e Merge Sort que serão feitos em python, é necessário permitir alternar entre Merge Sort e Quick Sort, destacando visualmente o pivô/sub-arrays, trocas (swaps) e número de comparações, incluir botão de 'Cenário Pior Caso', painel de métricas e logs didáticos; controles Step-by-step, Play, Reset."

> "Estou com algumas dúvidas sobre ambos os algoritmo, como que o  Merge Sort se torna mais eficiente que o Quick Sort?"

### Erro, limitação ou ajuste que precisou ser corrigido

- **Erro de interpretação da IA:** na primeira resposta, a IA entregou o simulador com **toda a lógica dos algoritmos escrita em JavaScript**, deixando o Python só como uma sugestão de conexão. Isso contrariava o objetivo do projeto, que é ter a lógica em Python. Precisei **corrigir pedindo explicitamente** que o JS apenas desenhasse os dados. 
- **Limitação de projeto:** como cada quadro guarda uma cópia completa do array, o pior caso do Quick Sort gera muitos quadros e um JSON grande (cerca de 450 KB com n=50). Por isso o tamanho do array foi limitado a 50 elementos.
