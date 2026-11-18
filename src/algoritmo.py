import math
import random


class Rastreador:
    def __init__(self, vetor, rotulo_trocas):
        self.v = list(vetor)            # o vetor que está de fato sendo ordenado
        self.comparacoes = 0
        self.trocas = 0                 # trocas (Quick) ou escritas (Merge)
        self.rotulo_trocas = rotulo_trocas
        self.ordenados = set()          # posições já definitivas
        self.profundidade = 0
        self.quadros = []

    def quadro(self, tipo, msg, **extra):
        """ 
        tira a foto do momento. Guarda uma cópia do vetor, as posições ordenadas, os contadores e a mensagem do log. O **extra anexa informações opcionais, como cmp, troca, pivo, faixa, esq e dir. Cada chamada é um passo que o site poderá exibir.
        """
        q = {
            "tipo": tipo, 
             "msg": msg, 
             "vetor": list(self.v),
             "ordenados": sorted(self.ordenados),
             "comparacoes": self.comparacoes, "trocas": self.trocas
        }
        q.update(extra)                 # cmp, troca, pivo, faixa, esq, dir...
        self.quadros.append(q)

    def trocar(self, a, b):
        self.v[a], self.v[b] = self.v[b], self.v[a]
        self.trocas += 1

    def resultado(self, algoritmo, inicial):
        """ 
        monta o pacote final enviado ao site. Ele contém a lista de quadros e o resumo (comparações, trocas, profundidade da recursão, valor teórico n²/2 do pior caso e n·log₂n).
        """
        n = len(inicial)
        return {"algoritmo": algoritmo, "n": n, "vetor_inicial": inicial,
                "quadros": self.quadros,
                "resumo": {"comparacoes": self.comparacoes, "trocas": self.trocas,
                           "rotulo_trocas": self.rotulo_trocas,
                           "profundidade": self.profundidade,
                           "pior_caso_n2": n * (n - 1) // 2,
                           "n_log_n": round(n * math.log2(n)) if n > 1 else 0}}

def quick_sort(vetor):
    """
    Cria o Rastreador e define duas funções internas. Usa a partição de Lomuto com pivô fixo no último elemento, e é esse pivô fixo que causa o pior caso.
    """
    inicial = list(vetor)
    r = Rastreador(vetor, "Trocas (swaps)")

    def particionar(lo, hi):
        """ 
        organiza o trecho [lo..hi] em torno do pivô
        """
        pivo = r.v[hi]
        faixa = [lo, hi]
        r.quadro("pivo", f"Pivô = {pivo} (último de [{lo}..{hi}])", pivo=hi, faixa=faixa)
        i = lo - 1
        for j in range(lo, hi):
            r.comparacoes += 1
            r.quadro("comparacao", f"Compara {r.v[j]} < pivô {pivo}?",
                     cmp=[j, hi], pivo=hi, faixa=faixa)
            if r.v[j] < pivo:
                i += 1
                if i != j:
                    r.trocar(i, j)
                    r.quadro("troca", f"{r.v[i]} é menor: troca posições {i} e {j}",
                             troca=[i, j], pivo=hi, faixa=faixa)
        i += 1
        if i != hi:
            # Trocando o valor do pivo
            r.trocar(i, hi)
            r.quadro("troca", f"Pivô vai para a posição {i}", troca=[i, hi], pivo=i, faixa=faixa)
        r.ordenados.add(i) 
        r.quadro("fixado", f"Pivô {pivo} fixado na posição {i}: esquerda [{lo}..{i-1}] "
                 f"tem {i-lo} elem., direita [{i+1}..{hi}] tem {hi-i}", pivo=i, faixa=faixa)
        return i

    def ordenar(lo, hi, prof):
        """ 
        coordena a divisão
        """
        if lo > hi:
            return
        r.profundidade = max(r.profundidade, prof)
        if lo == hi:
            r.ordenados.add(lo)
            r.quadro("fixado", f"Sub-array de 1 elemento ({r.v[lo]}): já está no lugar", faixa=[lo, hi])
            return
        p = particionar(lo, hi)
        ordenar(lo, p - 1, prof + 1)
        ordenar(p + 1, hi, prof + 1)

    ordenar(0, len(r.v) - 1, 1)
    return r.resultado("quick", inicial)

def merge_sort(vetor):
    """Top-down com vetores auxiliares esq/dir (copiados antes de cada intercalação)."""
    inicial = list(vetor)
    r = Rastreador(vetor, "Escritas no array")
    N = len(r.v)

    def ordenar(lo, hi, prof):
        """ 
        se o trecho tem mais de um elemento, calcula o meio, grava o quadro “divisão”, ordena a metade esquerda, ordena a direita e então chama intercalar. 
        """
        if lo >= hi:
            return
        r.profundidade = max(r.profundidade, prof)
        meio = (lo + hi) // 2
        r.quadro("divisao", f"Divide [{lo}..{hi}] em [{lo}..{meio}] e [{meio+1}..{hi}]", faixa=[lo, hi])
        ordenar(lo, meio, prof + 1)
        ordenar(meio + 1, hi, prof + 1)
        intercalar(lo, meio, hi)

    def intercalar(lo, meio, hi):
        """ 
        junta duas metades já ordenadas.
        """
        # Criando a lista da esquerda e lista da direita
        esq, dir_ = r.v[lo:meio + 1], r.v[meio + 1:hi + 1]
        i = j = 0
        k = lo
        final = (lo == 0 and hi == N - 1)
        aux = lambda: {"esq": esq, "dir": dir_, "pi": i, "pj": j}
        r.quadro("intercalar", f"Intercala {esq} com {dir_}", faixa=[lo, hi], **aux())

        def escrever(valor, origem):
            """ 
            escreve o valor em r.v[k], soma 1 em trocas, avança i ou j conforme a origem, grava o quadro e avança k
            """
            nonlocal k, i, j
            r.v[k] = valor
            r.trocas += 1
            if origem == "esq": i += 1
            else: j += 1
            if final: r.ordenados.add(k)
            r.quadro("escrita", f"Escreve {valor} na posição {k}", troca=[k], faixa=[lo, hi], **aux())
            k += 1

        while i < len(esq) and j < len(dir_):
            r.comparacoes += 1
            r.quadro("comparacao", f"Compara {esq[i]} ≤ {dir_[j]}?",
                     cmp_aux=[i, j], faixa=[lo, hi], **aux())
            if esq[i] <= dir_[j]: escrever(esq[i], "esq")
            else: escrever(dir_[j], "dir")
        while i < len(esq): escrever(esq[i], "esq")
        while j < len(dir_): escrever(dir_[j], "dir")

    ordenar(0, N - 1, 1)
    r.ordenados = set(range(N))
    r.quadro("fim", "Concluído", faixa=None)
    return r.resultado("merge", inicial)

def gerar_vetor(n, cenario="aleatorio"):
    # já ordenado: pior caso do Quick (pivô fixo)
    if cenario == "pior_caso":           
        return [5 + round(i * 90 / (n - 1)) for i in range(n)]
    return [random.randint(5, 99) for _ in range(n)]


ALGORITMOS = {"quick": quick_sort, "merge": merge_sort}

def _testar(titulo, vetor):
    """Roda os dois algoritmos no mesmo vetor, confere o resultado e imprime as operações."""
    print(f"\n=== {titulo} ===")
    print(f"Entrada ({len(vetor)} elementos): {vetor if len(vetor) <= 20 else str(vetor[:20])[:-1] + ', ...]'}")
    for nome, funcao in ALGORITMOS.items():
        res = funcao(vetor)
        saida = res["quadros"][-1]["vetor"] if res["quadros"] else []
        assert saida == sorted(vetor), f"{nome} ordenou errado!"   # prova que está correto
        s = res["resumo"]
        total = s["comparacoes"] + s["trocas"]
        print(f"[{nome:5}] saída: {saida if len(saida) <= 20 else '(ordenado, ' + str(len(saida)) + ' elem.)'}")
        print(f"        comparações={s['comparacoes']}  {s['rotulo_trocas'].lower()}={s['trocas']}"
              f"  -> TOTAL de operações = {total}  (profundidade da recursão = {s['profundidade']})")


if __name__ == "__main__":
    random.seed(42)

    # CENÁRIO 1: caso comum
    # Array aleatório. Esperado: comparações perto de n·log2(n) nos dois algoritmos.
    _testar("Cenário 1: caso comum (aleatório, n=10)", gerar_vetor(10))

    # CENÁRIO 2: casos de borda
    # Vazio e 1 elemento: a recursão para no caso base, sem nenhuma comparação.
    # Todos iguais: nenhum elemento é "< pivô", então o Quick fica desbalanceado (parecido com o pior caso).
    _testar("Cenário 2a: borda, vetor vazio", [])
    _testar("Cenário 2b: borda, um único elemento", [7])
    _testar("Cenário 2c: borda, valores repetidos (todos iguais)", [5] * 10)

    # CENÁRIO 3: pior caso do Quick Sort (pivô fixo no último)
    # Array já ordenado. Esperado: Quick faz n(n-1)/2 comparações (n²),
    # enquanto o Merge continua perto de n·log2(n).
    n = 30
    _testar(f"Cenário 3: pior caso (já ordenado, n={n})", gerar_vetor(n, "pior_caso"))
    print(f"\nReferência para n={n}: n(n-1)/2 = {n*(n-1)//2}   |   n·log2(n) = {round(n*math.log2(n))}")