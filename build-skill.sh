#!/usr/bin/env bash
#
# Rigenera editing-portfolio.skill dai sorgenti e aggiorna l'inventario
# dentro SKILL.md, sezione "Versione e integrità".
#
# Da eseguire dalla radice del repository, dopo ogni modifica alla skill:
#
#     ./build-skill.sh
#
# Poi: git add -A && git commit && git push
# E infine, il passo che si dimentica: ricaricare il .skill nella app di Claude.

set -euo pipefail

CARTELLA="editing-portfolio"
PACCHETTO="editing-portfolio.skill"
SKILLMD="$CARTELLA/SKILL.md"

cd "$(dirname "$0")"

if [ ! -f "$SKILLMD" ]; then
  echo "Errore: $SKILLMD non trovato. Esegui lo script dalla radice del repository." >&2
  exit 1
fi

# --- versione: data di oggi più il progressivo del giorno -------------------
OGGI=$(date +%Y-%m-%d)
PROG=1
if [ -f VERSIONE ]; then
  PRECEDENTE=$(head -1 VERSIONE | tr -d ' ')
  if [[ "$PRECEDENTE" == "$OGGI".* ]]; then
    PROG=$(( ${PRECEDENTE##*.} + 1 ))
  fi
fi
VERSIONE="$OGGI.$PROG"

# --- inventario: un file per riga, con le dimensioni ------------------------
INVENTARIO=$(mktemp)
{
  echo "**Versione $VERSIONE.** Oltre a questo SKILL.md, la skill è composta dai file"
  echo "qui sotto, e li vuole tutti."
  echo
  echo "| File | Byte |"
  echo "|---|---|"
  find "$CARTELLA/references" "$CARTELLA/scripts" -type f \
       \( -name '*.md' -o -name '*.py' -o -name '*.html' \) \
    | LC_ALL=C sort \
    | while read -r f; do
        printf "| \`%s\` | %s |\n" "${f#"$CARTELLA"/}" "$(wc -c < "$f" | tr -d ' ')"
      done
} > "$INVENTARIO"

N_FILE=$(grep -c '^| `' "$INVENTARIO")

# --- sostituzione fra i marcatori, senza toccare il resto -------------------
python3 - "$SKILLMD" "$INVENTARIO" <<'PY'
import sys, re
skillmd, inventario = sys.argv[1], sys.argv[2]
testo = open(skillmd, encoding="utf-8").read()
nuovo = open(inventario, encoding="utf-8").read().strip()
inizio = "<!-- INIZIO INVENTARIO: generato da build-skill.sh, non modificare a mano -->"
fine = "<!-- FINE INVENTARIO -->"
if inizio not in testo or fine not in testo:
    sys.exit("Errore: marcatori dell'inventario non trovati in SKILL.md. "
             "Ripristina la sezione 'Versione e integrità'.")
testo = re.sub(re.escape(inizio) + r".*?" + re.escape(fine),
               inizio + "\n\n" + nuovo + "\n\n" + fine, testo, flags=re.S)
open(skillmd, "w", encoding="utf-8").write(testo)
PY

echo "$VERSIONE" > VERSIONE
rm -f "$INVENTARIO"

# --- pacchetto ---------------------------------------------------------------
rm -f "$PACCHETTO"
zip -q -r -X "$PACCHETTO" "$CARTELLA" \
  -x '*.DS_Store' -x '*__pycache__*' -x '*.pyc'

echo "Versione:  $VERSIONE"
echo "File:      $N_FILE nella skill"
echo "Pacchetto: $PACCHETTO ($(wc -c < "$PACCHETTO" | tr -d ' ') byte)"
echo
echo "Ora, nell'ordine:"
echo "  1. git add -A && git commit -m \"...\" && git push"
echo "  2. ricarica $PACCHETTO nelle impostazioni delle skill della app di Claude"
echo
echo "Senza il passo 2 le sessioni continuano a usare la versione precedente."
