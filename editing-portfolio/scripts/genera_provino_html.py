#!/usr/bin/env python3
"""
genera_provino_html.py: provino interattivo autonomo, in un solo file HTML.

Legge analisi.json e le miniature, e produce un file HTML autosufficiente (immagini
incorporate in base64, nessuna dipendenza esterna, nessuna storage del browser) con:
  - provino a contatto con punteggio, verdetto e ruolo
  - filtri per cluster, verdetto, ruolo, divergenza cieco/ragionato
  - ordinamento per punteggio su ciascuna delle quattro destinazioni
  - pannello di dettaglio con voti sui sei assi
  - vista sequenza a doppia pagina, con le pagine bianche
  - vista cluster e vista scarti

Uso:
  python3 genera_provino_html.py analisi.json [-o provino.html]
                                 [--radice CARTELLA_THUMBS] [--lato-griglia 360]
                                 [--lato-dettaglio 900]
"""

import argparse
import base64
import io
import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Serve Pillow: pip install pillow --break-system-packages")

ASSI = ["autonomia", "forza", "coerenza", "originalita", "tecnica", "funzione"]
PESI = {
    "libro": {"autonomia": 10, "forza": 20, "coerenza": 25, "originalita": 15, "tecnica": 10, "funzione": 20},
    "mostra": {"autonomia": 25, "forza": 25, "coerenza": 15, "originalita": 15, "tecnica": 20, "funzione": 0},
    "web": {"autonomia": 30, "forza": 25, "coerenza": 15, "originalita": 20, "tecnica": 10, "funzione": 0},
    "concorso": {"autonomia": 25, "forza": 30, "coerenza": 10, "originalita": 25, "tecnica": 10, "funzione": 0},
}


def punteggio(voti, pesi):
    tot = sum(pesi.values())
    acc = 0.0
    for a, p in pesi.items():
        if p and voti.get(a) is not None:
            acc += float(voti[a]) * p
    return round(acc / tot, 2) if tot else 0.0


def codifica(percorso, lato, qualita):
    with Image.open(percorso) as im:
        im = im.convert("RGB")
        im.thumbnail((lato, lato), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=qualita, optimize=True)
        w, h = im.size
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii"), w, h


# Stringa grezza: i backslash devono arrivare intatti a JavaScript (regex e apostrofi
# protetti). Senza la r, Python interpreta \n dentro le regex e le spezza.
TEMPLATE = r"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITOLO__ | provino</title>
<style>
:root{--fondo:#111214;--carta:#191a1d;--bordo:#2b2d31;--testo:#e9e9ea;--tenue:#9a9ba0;
--accento:#c8a26a;--ok:#6ea87f;--medio:#c9a227;--basso:#a55b4b;}
*{box-sizing:border-box}
body{margin:0;background:var(--fondo);color:var(--testo);
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;font-size:14px}
header{padding:22px 26px 16px;border-bottom:1px solid var(--bordo);background:var(--carta)}
h1{margin:0 0 4px;font-size:22px;font-weight:600;letter-spacing:.2px}
.sotto{color:var(--tenue);font-size:13px;max-width:900px;line-height:1.5}
.filo{margin-top:10px;padding:10px 14px;border-left:2px solid var(--accento);background:#00000030;
font-style:italic;color:#d9d9db;max-width:900px}
nav{display:flex;gap:2px;padding:0 26px;background:var(--carta);border-bottom:1px solid var(--bordo)}
nav button{background:none;border:none;border-bottom:2px solid transparent;color:var(--tenue);
padding:11px 16px;font-size:13px;cursor:pointer;font-family:inherit}
nav button.on{color:var(--testo);border-bottom-color:var(--accento)}
.barra{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:14px 26px;
border-bottom:1px solid var(--bordo)}
select,input[type=search]{background:#0d0e10;color:var(--testo);border:1px solid var(--bordo);
border-radius:5px;padding:6px 9px;font-size:13px;font-family:inherit}
label.mini{color:var(--tenue);font-size:12px;margin-right:4px}
main{padding:20px 26px 60px}
.griglia{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px}
.scheda{background:var(--carta);border:1px solid var(--bordo);border-radius:7px;overflow:hidden;
cursor:pointer;transition:border-color .15s,transform .15s}
.scheda:hover{border-color:var(--accento);transform:translateY(-2px)}
.scheda .im{width:100%;height:150px;display:flex;align-items:center;justify-content:center;
background:#0a0b0c}
.scheda img{max-width:100%;max-height:150px;display:block}
.piede{padding:7px 9px;display:flex;justify-content:space-between;align-items:center;gap:6px}
.ident{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;color:var(--tenue)}
.voto{font-weight:600;font-size:13px}
.riga2{padding:0 9px 8px;font-size:11px;color:var(--tenue);display:flex;gap:6px;flex-wrap:wrap}
.tag{border:1px solid var(--bordo);border-radius:20px;padding:1px 7px}
.alto{color:var(--ok)}.medio{color:var(--medio)}.basso{color:var(--basso)}
.pannello{position:fixed;top:0;right:0;width:min(560px,94vw);height:100%;background:var(--carta);
border-left:1px solid var(--bordo);overflow-y:auto;transform:translateX(100%);
transition:transform .22s;z-index:40;padding:22px}
.pannello.on{transform:none}
.pannello img{width:100%;border-radius:5px;background:#000}
.chiudi{position:absolute;top:12px;right:16px;background:none;border:none;color:var(--tenue);
font-size:24px;cursor:pointer}
.assi{margin:16px 0}
.asse{display:grid;grid-template-columns:96px 1fr 26px;gap:9px;align-items:center;margin-bottom:5px;
font-size:12px;color:var(--tenue)}
.tratto{height:6px;background:#0d0e10;border-radius:3px;overflow:hidden}
.tratto i{display:block;height:100%;background:var(--accento)}
.blocco{margin:13px 0}.blocco h4{margin:0 0 3px;font-size:11px;text-transform:uppercase;
letter-spacing:.7px;color:var(--tenue);font-weight:600}
.blocco p{margin:0;line-height:1.55}
.spread{display:flex;gap:0;justify-content:center;margin:0 auto 26px;max-width:1080px;
background:var(--carta);border:1px solid var(--bordo);border-radius:5px;padding:22px;
box-shadow:0 10px 30px #0006}
.pagina{width:50%;padding:0 20px;display:flex;flex-direction:column;align-items:center;
justify-content:center;min-height:250px}
.pagina.sx{border-right:1px solid #ffffff12}
.pagina img{max-width:100%;max-height:380px;width:auto;box-shadow:0 3px 14px #0008}
.bianca{color:#3a3c40;font-size:12px;letter-spacing:1px;text-transform:uppercase}
.didasc{margin-top:9px;font-size:11.5px;color:var(--tenue);text-align:center;max-width:88%;
line-height:1.5}
.numsp{text-align:center;color:#4c4e54;font-size:11px;margin-bottom:7px;
font-family:ui-monospace,Menlo,monospace}
.gruppo{margin-bottom:34px}
.gruppo h3{margin:0 0 3px;font-size:17px}
.gruppo .tesi{color:var(--tenue);margin:0 0 12px;max-width:820px;line-height:1.5}
.ritmo{font-family:ui-monospace,Menlo,monospace;letter-spacing:2px;color:var(--accento);
background:#00000040;padding:8px 12px;border-radius:5px;display:inline-block;margin-bottom:16px}
.didcard{padding:0 9px 9px;font-size:11.5px;color:#b9b6b0;font-style:italic;line-height:1.45}
.didpanel{margin:9px 0 4px;padding:9px 12px;border-left:2px solid var(--accento);
background:#00000030;font-style:italic;color:#dcdad6;font-size:13px;line-height:1.5}
.didpanel.manca{border-left-color:var(--basso);color:var(--basso);font-style:normal}
.testi{max-width:760px}
.testi h3{font-size:12px;text-transform:uppercase;letter-spacing:.8px;color:var(--tenue);
margin:30px 0 8px;font-weight:600}
.testi p{line-height:1.75;font-size:14.5px;margin:0 0 14px}
.testi .conta{color:#5a5c62;font-size:11.5px;font-family:ui-monospace,Menlo,monospace}
.tav{display:grid;grid-template-columns:74px 1fr;gap:12px;padding:9px 0;
border-bottom:1px solid var(--bordo);align-items:baseline}
.tav b{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:var(--tenue);font-weight:400}
.tav span{font-style:italic;color:#dcdad6}
mark{background:#5a4423;color:#f0d9a8;border-radius:3px;padding:0 3px}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--bordo)}
th{color:var(--tenue);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.5px}
.vuoto{color:var(--tenue);padding:40px 0;text-align:center}
footer{padding:18px 26px;color:#5a5c62;font-size:11.5px;border-top:1px solid var(--bordo)}
</style></head><body>
<header>
<h1>__TITOLO__</h1>
<div class="sotto">__SOTTO__</div>
__FILO__
</header>
<nav>
<button class="on" data-vista="provino">Provino</button>
<button data-vista="sequenza">Sequenza</button>
<button data-vista="cluster">Cluster</button>
<button data-vista="testi">Testi</button>
<button data-vista="scarti">Scarti</button>
<button data-vista="dati">Dati</button>
</nav>
<div class="barra" id="barra">
<label class="mini">ordina</label>
<select id="ordine">
<option value="p_libro">punteggio libro</option>
<option value="p_mostra">punteggio mostra</option>
<option value="p_web">punteggio web</option>
<option value="p_concorso">punteggio concorso</option>
<option value="id">id</option>
</select>
<label class="mini">cluster</label><select id="fcluster"></select>
<label class="mini">verdetto</label><select id="fverdetto"></select>
<label class="mini">cieco</label><select id="fcieco"></select>
<input type="search" id="cerca" placeholder="cerca file, ruolo, nota">
<span class="mini" id="conteggio"></span>
</div>
<main>
<div id="vista-provino"><div class="griglia" id="griglia"></div></div>
<div id="vista-sequenza" hidden></div>
<div id="vista-cluster" hidden></div>
<div id="vista-testi" hidden></div>
<div id="vista-scarti" hidden></div>
<div id="vista-dati" hidden></div>
</main>
<div class="pannello" id="pannello"><button class="chiudi" onclick="chiudi()">&times;</button>
<div id="dettaglio"></div></div>
<footer>__PIEDE__</footer>
<script>
const D = __DATI__;
const ASSI = ["autonomia","forza","coerenza","originalita","tecnica","funzione"];
const per = {}; D.immagini.forEach(i => per[i.id] = i);
function classe(v){ return v >= 7.5 ? "alto" : (v >= 6 ? "medio" : "basso"); }
function opzioni(sel, valori, etichetta){
  sel.innerHTML = '<option value="">' + etichetta + '</option>' +
    valori.map(v => '<option value="' + v + '">' + v + '</option>').join('');
}
const cl = [...new Set(D.immagini.flatMap(i => i.cluster || []))].sort();
const vd = [...new Set(D.immagini.map(i => i.verdetto).filter(Boolean))];
const cc = [...new Set(D.immagini.map(i => i.cieco).filter(Boolean))];
opzioni(document.getElementById('fcluster'), cl, 'tutti');
opzioni(document.getElementById('fverdetto'), vd, 'tutti');
opzioni(document.getElementById('fcieco'), cc, 'tutti');

function disegnaGriglia(){
  const ord = document.getElementById('ordine').value;
  const fc = document.getElementById('fcluster').value;
  const fv = document.getElementById('fverdetto').value;
  const fk = document.getElementById('fcieco').value;
  const q = document.getElementById('cerca').value.toLowerCase();
  let lista = D.immagini.filter(i =>
    (!fc || (i.cluster || []).includes(fc)) && (!fv || i.verdetto === fv) &&
    (!fk || i.cieco === fk) &&
    (!q || JSON.stringify(i).toLowerCase().includes(q)));
  lista.sort((a, b) => ord === 'id' ? a.id.localeCompare(b.id) : (b[ord] || 0) - (a[ord] || 0));
  document.getElementById('conteggio').textContent = lista.length + ' di ' + D.immagini.length;
  document.getElementById('griglia').innerHTML = lista.map(i => `
    <div class="scheda" onclick="apri('${i.id}')">
      <div class="im"><img src="${i.mini}" alt="${i.id}"></div>
      <div class="piede"><span class="ident">${i.id}</span>
        <span class="voto ${classe(i[ord] || i.p_libro)}">${(i[ord === 'id' ? 'p_libro' : ord] || 0).toFixed(1)}</span></div>
      <div class="riga2">${i.verdetto ? '<span class="tag">' + i.verdetto + '</span>' : ''}
        ${i.ruolo ? '<span class="tag">' + i.ruolo + '</span>' : ''}
        ${i.cieco ? '<span class="tag">' + i.cieco + '</span>' : ''}</div>
      ${i.didascalia ? '<div class="didcard">' + i.didascalia + '</div>' : ''}
    </div>`).join('') || '<div class="vuoto">Nessuna immagine con questi filtri.</div>';
}
function apri(id){
  const i = per[id];
  document.getElementById('dettaglio').innerHTML = `
    <img src="${i.grande || i.mini}" alt="${i.id}">
    <h3 style="margin:14px 0 2px">${i.titolo || i.file}</h3>
    <div class="ident">${i.id} &middot; ${i.file}${i.genere ? ' &middot; ' + i.genere : ''}</div>
    ${i.didascalia ? '<div class="didpanel">' + i.didascalia + '</div>' : '<div class="didpanel manca">didascalia mancante</div>'}
    <div class="assi">${ASSI.map(a => {
      const v = (i.voti || {})[a];
      return `<div class="asse"><span>${a}</span><span class="tratto"><i style="width:${(v || 0) * 10}%"></i></span><span>${v ?? '-'}</span></div>`;
    }).join('')}</div>
    <table><tr><th>libro</th><th>mostra</th><th>web</th><th>concorso</th></tr>
    <tr><td class="${classe(i.p_libro)}">${i.p_libro.toFixed(2)}</td>
    <td class="${classe(i.p_mostra)}">${i.p_mostra.toFixed(2)}</td>
    <td class="${classe(i.p_web)}">${i.p_web.toFixed(2)}</td>
    <td class="${classe(i.p_concorso)}">${i.p_concorso.toFixed(2)}</td></tr></table>
    ${i.verdetto ? blocco('verdetto', i.verdetto) : ''}
    ${i.ruolo ? blocco('ruolo in sequenza', i.ruolo) : ''}
    ${i.cieco ? blocco('passaggio cieco', i.cieco) : ''}
    ${(i.cluster || []).length ? blocco('cluster', i.cluster.join(', ')) : ''}
    ${i.forza_principale ? blocco('forza', i.forza_principale) : ''}
    ${i.limite_principale ? blocco('limite', i.limite_principale) : ''}
    ${i.note ? blocco('note', i.note) : ''}`;
  document.getElementById('pannello').classList.add('on');
}
function blocco(t, c){ return `<div class="blocco"><h4>${t}</h4><p>${c}</p></div>`; }
function chiudi(){ document.getElementById('pannello').classList.remove('on'); }
document.addEventListener('keydown', e => { if (e.key === 'Escape') chiudi(); });

function pagina(id, lato){
  if (!id) return `<div class="pagina ${lato}"><span class="bianca">pagina bianca</span></div>`;
  const i = per[id];
  if (!i) return `<div class="pagina ${lato}"><span class="bianca">${id} assente</span></div>`;
  return `<div class="pagina ${lato}"><img src="${i.grande || i.mini}" alt="${id}">
    <div class="didasc"><span class="ident">${id}</span>${i.didascalia ? ' &middot; ' + i.didascalia : ''}</div></div>`;
}
function disegnaSequenza(){
  const s = (D.sequenza && D.sequenza.spread) || [];
  const el = document.getElementById('vista-sequenza');
  if (!s.length) { el.innerHTML = '<div class="vuoto">Nessuna sequenza in analisi.json.</div>'; return; }
  el.innerHTML = (D.ritmo ? '<div class="ritmo">' + D.ritmo + '</div>' : '') + s.map((c, n) =>
    `<div class="numsp">spread ${n + 1}</div><div class="spread">${pagina(c[0], 'sx')}${pagina(c[1], 'dx')}</div>`
  ).join('');
}
function disegnaCluster(){
  const el = document.getElementById('vista-cluster');
  const g = D.cluster || [];
  if (!g.length) { el.innerHTML = '<div class="vuoto">Nessun cluster in analisi.json.</div>'; return; }
  el.innerHTML = g.map(c => `<div class="gruppo"><h3>${c.nome || c.id}
    ${c.forza ? '<span class="voto ' + classe(c.forza) + '" style="font-size:14px"> ' + c.forza + '/10</span>' : ''}</h3>
    <p class="tesi">${c.tesi || ''}${c.registro_nome ? ' <span class="tag">' + c.registro_nome + '</span>' : ''}</p>
    <div class="griglia">${(c.immagini || []).map(id => per[id] ? `
      <div class="scheda" onclick="apri('${id}')"><div class="im"><img src="${per[id].mini}"></div>
      <div class="piede"><span class="ident">${id}</span>
      <span class="voto ${classe(per[id].p_libro)}">${per[id].p_libro.toFixed(1)}</span></div></div>` : '').join('')}</div></div>`
  ).join('');
}
function conta(t){ return (String(t||'').match(/[\wàèéìòùÀÈÉÌÒÙ']+/g) || []).length; }
function segna(t){ return String(t||'').replace(/\[([^\]]+)\]/g, '<mark>[$1]</mark>'); }
function paragrafi(t){ return String(t||'').split(/\n\s*\n/).map(p => '<p>' + segna(p.trim()) + '</p>').join(''); }
function disegnaTesti(){
  const P = D.progetto || {};
  const el = document.getElementById('vista-testi');
  let h = '<div class="testi">';
  h += '<h3>Titolo</h3><p style="font-size:22px;margin-bottom:4px">' + (P.titolo || 'senza titolo') +
       (P.sottotitolo ? '<span style="font-size:14px;color:var(--tenue)"><br>' + P.sottotitolo + '</span>' : '') + '</p>';
  if ((P.titoli_candidati || []).length)
    h += '<table><tr><th>candidato</th><th>registro</th><th>perché</th></tr>' +
      P.titoli_candidati.map(c => '<tr><td>' + (c.titolo||'') + '</td><td>' + (c.registro||'') +
      '</td><td>' + (c.motivazione||'') + '</td></tr>').join('') + '</table>';
  if (P.introduzione)
    h += '<h3>Introduzione <span class="conta">' + (P.registro_introduzione || 'registro non dichiarato') +
         ', ' + conta(P.introduzione) + ' parole</span></h3>' + paragrafi(P.introduzione);
  if (P.nota_autore)
    h += '<h3>Nota dell\'autore <span class="conta">' + conta(P.nota_autore) + ' parole</span></h3>' + paragrafi(P.nota_autore);
  if (P.statement)
    h += '<h3>Statement <span class="conta">' + conta(P.statement) + ' parole</span></h3>' + paragrafi(P.statement);
  const tav = D.tavole || [];
  if (tav.length){
    h += '<h3>Didascalie <span class="conta">registro ' + (P.registro_didascalie || 'non dichiarato') +
         ', ' + tav.length + ' tavole</span></h3>';
    h += tav.map((id, n) => {
      const i = per[id] || {};
      return '<div class="tav"><b>Tavola ' + (n+1) + ' &middot; ' + id + '</b><span>' +
        segna(i.didascalia || 'manca') + '</span></div>';
    }).join('');
    const aperti = tav.reduce((a, id) => a + ((String((per[id]||{}).didascalia||'').match(/\[[^\]]+\]/g)||[]).length), 0);
    if (aperti) h += '<p class="conta" style="margin-top:14px">Segnaposto ancora da compilare: ' + aperti +
      '. Sono evidenziati sopra.</p>';
  }
  el.innerHTML = h + '</div>';
}
function disegnaScarti(){
  const el = document.getElementById('vista-scarti');
  const s = D.scarti || [];
  if (!s.length) { el.innerHTML = '<div class="vuoto">Nessuno scarto dichiarato.</div>'; return; }
  el.innerHTML = '<div class="griglia">' + s.map(x => {
    const i = per[x.id]; if (!i) return '';
    return `<div class="scheda" onclick="apri('${x.id}')"><div class="im"><img src="${i.mini}"></div>
      <div class="piede"><span class="ident">${x.id}</span></div>
      <div class="riga2">${x.motivo || ''}</div></div>`;
  }).join('') + '</div>';
}
function disegnaDati(){
  const righe = D.immagini.map(i => `<tr><td>${i.id}</td><td>${i.file}</td>
    ${ASSI.map(a => '<td>' + ((i.voti || {})[a] ?? '-') + '</td>').join('')}
    <td class="${classe(i.p_libro)}">${i.p_libro.toFixed(2)}</td>
    <td class="${classe(i.p_mostra)}">${i.p_mostra.toFixed(2)}</td>
    <td class="${classe(i.p_web)}">${i.p_web.toFixed(2)}</td>
    <td class="${classe(i.p_concorso)}">${i.p_concorso.toFixed(2)}</td>
    <td>${i.verdetto || ''}</td><td>${i.ruolo || ''}</td></tr>`).join('');
  document.getElementById('vista-dati').innerHTML = `<table><tr><th>id</th><th>file</th>
    ${ASSI.map(a => '<th>' + a.slice(0, 4) + '</th>').join('')}
    <th>libro</th><th>mostra</th><th>web</th><th>conc</th><th>verdetto</th><th>ruolo</th></tr>${righe}</table>`;
}
document.querySelectorAll('nav button').forEach(b => b.onclick = () => {
  document.querySelectorAll('nav button').forEach(x => x.classList.remove('on'));
  b.classList.add('on');
  const v = b.dataset.vista;
  ['provino', 'sequenza', 'cluster', 'testi', 'scarti', 'dati'].forEach(n =>
    document.getElementById('vista-' + n).hidden = (n !== v));
  document.getElementById('barra').style.display = (v === 'provino') ? 'flex' : 'none';
});
['ordine', 'fcluster', 'fverdetto', 'fcieco'].forEach(k =>
  document.getElementById(k).onchange = disegnaGriglia);
document.getElementById('cerca').oninput = disegnaGriglia;
disegnaGriglia(); disegnaSequenza(); disegnaCluster(); disegnaTesti(); disegnaScarti(); disegnaDati();
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Provino interattivo autonomo da analisi.json")
    ap.add_argument("analisi")
    ap.add_argument("-o", "--uscita", default=None)
    ap.add_argument("--radice", default=None, help="cartella base per i percorsi thumb")
    ap.add_argument("--lato-griglia", type=int, default=360)
    ap.add_argument("--lato-dettaglio", type=int, default=900)
    args = ap.parse_args()

    percorso = os.path.abspath(os.path.expanduser(args.analisi))
    with open(percorso, encoding="utf-8") as fh:
        dati = json.load(fh)
    base = os.path.abspath(os.path.expanduser(args.radice or os.path.dirname(percorso) or "."))
    prog = dati.get("progetto") or {}

    immagini = []
    mancanti = []
    for im in dati.get("immagini") or []:
        rel = im.get("thumb") or im.get("file")
        p = rel if os.path.isabs(rel) else os.path.join(base, rel)
        if not os.path.exists(p):
            mancanti.append(rel)
            continue
        mini, _, _ = codifica(p, args.lato_griglia, 70)
        grande, _, _ = codifica(p, args.lato_dettaglio, 72)
        voti = im.get("voti", {})
        immagini.append(
            {
                "id": im["id"], "file": im.get("file", ""), "titolo": im.get("titolo", ""),
                "genere": im.get("genere", ""), "voti": voti, "verdetto": im.get("verdetto", ""),
                "ruolo": im.get("ruolo", ""), "cluster": im.get("cluster", []) or [],
                "didascalia": im.get("didascalia", ""), "cieco": im.get("cieco", ""),
                "forza_principale": im.get("forza_principale", ""),
                "limite_principale": im.get("limite_principale", ""),
                "note": im.get("note", ""),
                "mini": mini, "grande": grande,
                "p_libro": punteggio(voti, PESI["libro"]),
                "p_mostra": punteggio(voti, PESI["mostra"]),
                "p_web": punteggio(voti, PESI["web"]),
                "p_concorso": punteggio(voti, PESI["concorso"]),
            }
        )
    if not immagini:
        sys.exit("Nessuna miniatura trovata. Controlla i percorsi thumb o passa --radice.")
    if mancanti:
        print("Attenzione, miniature non trovate: %s" % ", ".join(mancanti[:8]))

    seq = (dati.get("sequenza") or {}).get("spread") or []
    tavole = [x for coppia in seq for x in coppia if x]
    if not tavole:
        gall = dati.get("gallerie") or []
        tavole = list(gall[0].get("ordine") or []) if gall else [i["id"] for i in immagini]
    carico = {
        "immagini": immagini,
        "cluster": dati.get("cluster") or [],
        "sequenza": dati.get("sequenza") or {},
        "scarti": dati.get("scarti") or [],
        "ritmo": (dati.get("sequenza") or {}).get("ritmo", ""),
        "tavole": [t for t in tavole if any(i["id"] == t for i in immagini)],
        "progetto": {
            k: prog.get(k) for k in (
                "titolo", "sottotitolo", "autore", "fil_rouge", "introduzione",
                "registro_introduzione", "statement", "nota_autore",
                "registro_didascalie", "titoli_candidati",
            ) if prog.get(k)
        },
    }
    sotto = " &middot; ".join(
        [x for x in [
            prog.get("autore"), prog.get("modalita"), prog.get("destinazione"),
            "%d immagini" % len(immagini),
        ] if x]
    )
    filo = ('<div class="filo">%s</div>' % prog["fil_rouge"]) if prog.get("fil_rouge") else ""
    piede = "Provino generato dalla skill editing-portfolio. Le miniature sono incorporate: il file funziona anche offline."

    html = (
        TEMPLATE.replace("__TITOLO__", prog.get("titolo") or "Provino")
        .replace("__SOTTO__", sotto)
        .replace("__FILO__", filo)
        .replace("__PIEDE__", piede)
        .replace("__DATI__", json.dumps(carico, ensure_ascii=False))
    )
    out = os.path.abspath(os.path.expanduser(args.uscita or os.path.join(os.path.dirname(percorso) or ".", "provino.html")))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("Scritto: %s (%.1f MB, %d immagini)" % (out, os.path.getsize(out) / 1048576.0, len(immagini)))


if __name__ == "__main__":
    main()
