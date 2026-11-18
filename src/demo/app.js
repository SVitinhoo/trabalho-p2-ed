const $ = id => document.getElementById(id);
let resp = null, pos = 0, timer = null, vetor = null; // vetor = array atual (veio do Python)

async function pedir(extra = {}) {
    pausar();
    const corpo = { algoritmo: $('algo').value, n: +$('n').value, ...extra };
    try {
        const r = await fetch('/api/ordenar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(corpo) });
        if (!r.ok) throw new Error('HTTP ' + r.status);
        resp = await r.json(); vetor = resp.vetor_inicial; $('erro').hidden = true;
    } catch (e) {
        $('erro').hidden = false;
        $('erro').textContent = 'Não foi possível falar com o servidor Python. Rode "python servidor.py" e abra http://localhost:5000';
        return;
    }
    pos = 0; $('log').innerHTML = ''; desenhar();
}

const quadro = () => pos === 0 ? null : resp.quadros[pos - 1];

function barras(el, valores, classes, mostrar) {
    const max = 100;
    if (el.children.length !== valores.length) {
        el.innerHTML = ''; valores.forEach(() => el.appendChild(document.createElement('div')));
    }
    [...el.children].forEach((b, i) => {
        b.className = 'b ' + (classes[i] || '');
        b.style.height = (valores[i] / max * 92 + 4) + '%';
        b.innerHTML = mostrar ? `<span>${valores[i]}</span>` : '';
    });
}

function desenhar() {
    const q = quadro(), v = q ? q.vetor : resp.vetor_inicial, n = v.length, cls = [];
    if (q) {
        if (q.faixa) for (let i = q.faixa[0]; i <= q.faixa[1]; i++) cls[i] = 'faixa';
        q.ordenados.forEach(i => cls[i] = 'ok');
        if (q.pivo != null && !q.ordenados.includes(q.pivo)) cls[q.pivo] = 'pivo';
        (q.cmp || []).forEach(i => cls[i] = 'cmp');
        (q.troca || []).forEach(i => cls[i] = 'troca');
    }
    barras($('barras'), v, cls, n <= 30);
    const tem = q && q.esq; $('auxbox').hidden = !tem;
    if (tem) {
        const aux = (lista, ptr, cmpIdx) => lista.map((_, i) => i === cmpIdx ? 'cmp' : i < ptr ? 'gasto' : '');
        barras($('esq'), q.esq, aux(q.esq, q.pi, q.cmp_aux && q.cmp_aux[0]), true);
        barras($('dir'), q.dir, aux(q.dir, q.pj, q.cmp_aux && q.cmp_aux[1]), true);
    }
    const s = resp.resumo;
    $('mc').textContent = q ? q.comparacoes : 0;
    $('mt').textContent = q ? q.trocas : 0;
    $('ml').textContent = s.rotulo_trocas;
    $('mp').textContent = pos + ' / ' + resp.quadros.length;
    $('md').textContent = pos === resp.quadros.length ? s.profundidade : '–';
    $('m2').textContent = s.pior_caso_n2; $('mn').textContent = s.n_log_n;
    $('anterior').disabled = pos === 0; $('passo').disabled = pos >= resp.quadros.length;
}

function logar(q) {
    const d = document.createElement('div'); d.className = 't-' + q.tipo; d.textContent = q.msg;
    $('log').prepend(d);
}

function avancar() {
    if (pos >= resp.quadros.length) return pausar();
    logar(resp.quadros[pos++]); desenhar();
    if (pos >= resp.quadros.length) { pausar(); fim(); }
}
function voltar() {
    if (pos === 0) return;
    pos--; $('log').firstChild && $('log').firstChild.remove(); desenhar();
}
function fim() {
    const s = resp.resumo;
    logar({ tipo: 'fim', msg: `Fim: ${s.comparacoes} comparações, ${s.trocas} ${s.rotulo_trocas.toLowerCase()}.` });
}
function tocar() {
    if (timer || pos >= resp.quadros.length) return;
    $('play').textContent = '⏸ Pausar';
    timer = setInterval(avancar, Math.max(12, 1000 / Math.pow(1.6, +$('sp').value)));
}

// Atalhos de teclado: → avança um passo, ← volta um passo
document.addEventListener('keydown', e => {
  if (!resp) return;                         
  if (e.key === 'ArrowRight') {
    e.preventDefault();                       // impede o slider de mexer com a seta
    pausar();
    avancar();
  } else if (e.key === 'ArrowLeft') {
    e.preventDefault();
    pausar();
    voltar();
  }
});

function pausar() { clearInterval(timer); timer = null; $('play').textContent = '▶ Play'; }
const aviso = t => { $('aviso').hidden = !t; $('aviso').textContent = t || ''; };

$('play').onclick = () => timer ? pausar() : tocar();
$('passo').onclick = () => { pausar(); avancar(); };
$('anterior').onclick = () => { pausar(); voltar(); };
$('reset').onclick = () => { pausar(); pos = 0; $('log').innerHTML = ''; desenhar(); };
$('algo').onchange = () => pedir({ vetor });            // mesmo array, outro algoritmo
$('novo').onclick = () => { aviso(); pedir({ cenario: 'aleatorio' }); };
$('n').oninput = () => { $('nv').textContent = $('n').value; aviso(); pedir({ cenario: 'aleatorio' }); };
$('sp').oninput = () => { if (timer) { pausar(); tocar(); } };
$('pior').onclick = async () => {
    await pedir({ cenario: 'pior_caso' });
    if (resp) aviso('Pior caso: array já ordenado. Com pivô fixo no último elemento, toda partição fica 0 / n−1 (≈ n²/2 comparações). Troque para o Merge Sort (o mesmo array é mantido) e compare os contadores.');
};
pedir({ cenario: 'aleatorio' });
