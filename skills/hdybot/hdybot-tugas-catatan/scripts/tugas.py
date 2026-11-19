#!/usr/bin/env python3
"""Tugas & catatan kelas (port dari FunAndUtilityService). Data di tabel `tugas` dan `catatan` pada hdybot.sqlite.
Pakai: tugas.py add "<matkul>|<judul>|<YYYY-MM-DD>|<keterangan>" | list [semua] | done <id> | del <id>
       tugas.py note-add "<judul>|<isi>" | note-list | note-del <id>"""
import os, sys, sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
DB = os.environ.get("HDYBOT_DB", os.path.expanduser("~/.hermes/hdybot/hdybot.sqlite"))
def conn():
    if not os.path.exists(DB): sys.exit(f"Database tidak ditemukan: {DB}")
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c
def matkul_kode(c, s):
    s = s.strip().lower()
    for r in c.execute("SELECT kode,nama,alias FROM matkul"):
        if s in (r["kode"].lower(), r["nama"].lower()) or s in r["alias"].lower(): return r["kode"]
    return None
def main(a):
    c = conn(); k = a[0] if a else ""
    rest = " ".join(a[1:])
    if k == "add":
        p = [x.strip() for x in rest.split("|")] + ["", "", "", ""]
        mk, judul, tgl, ket = p[:4]
        if not judul: return "Format: add matkul|judul|YYYY-MM-DD|keterangan"
        if tgl:
            try: datetime.strptime(tgl, "%Y-%m-%d")
            except ValueError: return "Tanggal harus YYYY-MM-DD."
        kode = matkul_kode(c, mk) if mk else None
        cur = c.execute("INSERT INTO tugas(kode_matkul,judul,keterangan,tenggat) VALUES(?,?,?,?)", (kode, judul, ket, tgl or None)); c.commit()
        return f"Tugas TUG-{cur.lastrowid} ditambahkan: {judul}" + (f" ({kode})" if kode else "") + (f", tenggat {tgl}" if tgl else "")
    if k == "list":
        q = "SELECT * FROM tugas" + ("" if rest == "semua" else " WHERE status='aktif'") + " ORDER BY tenggat IS NULL, tenggat"
        rows = c.execute(q).fetchall()
        if not rows: return "Tidak ada tugas."
        today = datetime.now(ZoneInfo("Asia/Jakarta")).date().isoformat()
        return "\n".join(["*Tugas*"] + [f"• TUG-{r['id']} [{r['status']}] {r['judul']}" + (f" · {r['kode_matkul']}" if r['kode_matkul'] else "") +
            (f" · tenggat {r['tenggat']}" + (" ⚠️ lewat" if r['tenggat'] < today and r['status']=='aktif' else "") if r['tenggat'] else "") for r in rows])
    if k in ("done", "del"):
        i = int(rest.upper().replace("TUG-", "") or 0)
        if k == "done": n = c.execute("UPDATE tugas SET status='selesai' WHERE id=?", (i,)).rowcount
        else: n = c.execute("DELETE FROM tugas WHERE id=?", (i,)).rowcount
        c.commit(); return ("OK" if n else "ID tidak ditemukan") + f" (TUG-{i})"
    if k == "note-add":
        j, _, isi = rest.partition("|")
        if not j.strip(): return "Format: note-add judul|isi"
        cur = c.execute("INSERT INTO catatan(judul,isi) VALUES(?,?)", (j.strip(), isi.strip())); c.commit(); return f"Catatan NOTE-{cur.lastrowid} disimpan."
    if k == "note-list":
        rows = c.execute("SELECT * FROM catatan ORDER BY id DESC").fetchall()
        return "\n".join(["*Catatan*"] + [f"• NOTE-{r['id']} {r['judul']}: {r['isi']}" for r in rows]) if rows else "Belum ada catatan."
    if k == "note-del":
        i = int(rest.upper().replace("NOTE-", "") or 0); n = c.execute("DELETE FROM catatan WHERE id=?", (i,)).rowcount; c.commit()
        return ("OK" if n else "ID tidak ditemukan") + f" (NOTE-{i})"
    return __doc__
if __name__ == "__main__":
    try: print(main(sys.argv[1:]))
    except ValueError: print("ID tidak valid.")
