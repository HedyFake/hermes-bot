#!/usr/bin/env bash
# Memasang paket HdyBot ke Hermes Agent. Aman dijalankan ulang; tidak menimpa SOUL.md tanpa cadangan.
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
echo "Memasang ke: $HERMES_HOME"
mkdir -p "$HERMES_HOME/skills" "$HERMES_HOME/hdybot"

# 1) Skill
cp -r "$AQUI/skills/hdybot" "$HERMES_HOME/skills/"
echo "✓ 8 skill disalin ke $HERMES_HOME/skills/hdybot"

# 2) Database (jangan menimpa bila sudah ada data kerja)
if [ -f "$HERMES_HOME/hdybot/hdybot.sqlite" ]; then
  echo "• hdybot.sqlite sudah ada, TIDAK ditimpa (data tugas/catatan aman). Hapus manual bila ingin mengulang dari seed."
else
  cp "$AQUI/database/hdybot.sqlite" "$HERMES_HOME/hdybot/hdybot.sqlite"
  echo "✓ database awal disalin ke $HERMES_HOME/hdybot/hdybot.sqlite"
fi
cp -r "$AQUI/database/seed" "$HERMES_HOME/hdybot/" 2>/dev/null || true

# 3) Persona
if [ -f "$HERMES_HOME/SOUL.md" ] && ! cmp -s "$AQUI/SOUL.md" "$HERMES_HOME/SOUL.md"; then
  cp "$HERMES_HOME/SOUL.md" "$HERMES_HOME/SOUL.md.bak-$(date +%Y%m%d%H%M%S)"
  echo "• SOUL.md lama dicadangkan"
fi
cp "$AQUI/SOUL.md" "$HERMES_HOME/SOUL.md"
echo "✓ persona SOUL.md terpasang"

# 4) Variabel lingkungan
if ! grep -q '^HDYBOT_DB=' "$HERMES_HOME/.env" 2>/dev/null; then
  echo "HDYBOT_DB=$HERMES_HOME/hdybot/hdybot.sqlite" >> "$HERMES_HOME/.env"
  echo "✓ HDYBOT_DB ditambahkan ke $HERMES_HOME/.env"
fi

# 5) Uji cepat
export HDYBOT_DB="$HERMES_HOME/hdybot/hdybot.sqlite"
HASIL_KELAS="$(python3 "$HERMES_HOME/skills/hdybot/hdybot-kelas/scripts/kelas.py" matkul)"
HASIL_GCS="$(python3 "$HERMES_HOME/skills/hdybot/hdybot-kalkulator/scripts/hitung.py" gcs E4 V5 M6)"
echo "✓ uji skrip: $(echo "$HASIL_KELAS" | head -1) | $HASIL_GCS"
echo; echo "Selesai. Mulai sesi BARU di Hermes (/reset) agar skill terbaca."
