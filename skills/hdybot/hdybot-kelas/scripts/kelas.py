#!/usr/bin/env python3
"""Info kelas Nursing Class A 5A: jadwal, matkul, dosen, pengurus, hitung mundur, kelompok.
Pakai: kelas.py jadwal [hari|besok|minggu] | next | matkul | dosen [filter] | kelas | pengurus | referensi | hitungmundur YYYY-MM-DD | kelompok N nama1,nama2,..."""
import os, sys, sqlite3, json, random
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

DB = os.environ.get("HDYBOT_DB", os.path.expanduser("~/.hermes/hdybot/hdybot.sqlite"))
WIB = ZoneInfo("Asia/Jakarta")
HARI = {1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu", 7: "Minggu"}
ALIAS_HARI = {"senin": 1, "selasa": 2, "rabu": 3, "kamis": 4, "jumat": 5, "jum'at": 5, "sabtu": 6, "minggu": 7, "ahad": 7}

def conn():
    if not os.path.exists(DB):
        sys.exit(f"Database tidak ditemukan: {DB}. Salin database/hdybot.sqlite ke sana atau set HDYBOT_DB.")
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c

def sesi_hari(c, no):
    return c.execute("""SELECT j.mulai,j.selesai,m.nama,m.kode,j.ruang,j.status_sumber FROM jadwal j
        JOIN matkul m ON m.kode=j.kode_matkul WHERE j.hari_no=? ORDER BY j.mulai""", (no,)).fetchall()

def fmt_hari(c, no, judul=None):
    rows = sesi_hari(c, no)
    ist = c.execute("SELECT mulai,selesai,label FROM istirahat").fetchall()
    out = [f"*Jadwal {judul or HARI[no]}*"]
    if not rows: return "\n".join(out + ["Tidak ada kuliah terjadwal."])
    for r in rows:
        out.append(f"• {r['mulai']}–{r['selesai']} · {r['nama']} ({r['kode']})" + (f" · ruang {r['ruang']}" if r['ruang'] else " · ruang belum diisi"))
    for i in ist: out.append(f"(Istirahat {i['mulai']}–{i['selesai']})")
    out.append("Status: data jadwal diberikan pengguna, menunggu konfirmasi.")
    return "\n".join(out)

def now(): return datetime.now(WIB)

def cmd_jadwal(c, arg):
    a = (arg or "").lower().strip()
    n = now()
    if a in ("", "hariini", "hari ini"): return fmt_hari(c, n.isoweekday(), f"hari ini ({HARI[n.isoweekday()]})")
    if a == "besok":
        t = n + timedelta(days=1); return fmt_hari(c, t.isoweekday(), f"besok ({HARI[t.isoweekday()]})")
    if a in ("minggu", "mingguini", "minggu ini"):
        return "\n\n".join(fmt_hari(c, i) for i in range(1, 6))
    if a in ALIAS_HARI: return fmt_hari(c, ALIAS_HARI[a])
    return "Hari tidak dikenali. Pakai: senin–jumat, besok, minggu."

def cmd_next(c):
    n = now(); hm = n.strftime("%H:%M")
    for off in range(0, 8):
        t = n + timedelta(days=off)
        for r in sesi_hari(c, t.isoweekday()):
            if off > 0 or r["mulai"] > hm:
                kapan = "hari ini" if off == 0 else ("besok" if off == 1 else HARI[t.isoweekday()])
                return f"Kuliah berikutnya: {r['nama']} ({r['kode']}), {kapan} {r['mulai']}–{r['selesai']} WIB."
    return "Tidak ada sesi terjadwal."

def cmd_matkul(c):
    rows = c.execute("SELECT kode,nama,sks FROM matkul ORDER BY nama").fetchall()
    tot = sum(r["sks"] for r in rows)
    return "\n".join([f"*Mata kuliah Semester 5A* ({len(rows)} matkul, {tot} SKS unik)"] + [f"• {r['kode']} · {r['nama']} · {r['sks']} SKS" for r in rows]
        + ["Catatan: SKS adalah atribut matkul, jangan dijumlah per sesi mingguan."])

def cmd_dosen(c, filt):
    q = "SELECT m.kode,m.nama mn,d.nama_asli,md.status_verifikasi FROM matkul_dosen md JOIN matkul m ON m.kode=md.kode_matkul JOIN dosen d ON d.id=md.dosen_id"
    rows = c.execute(q + " ORDER BY m.nama,d.nama_asli").fetchall()
    f = (filt or "").lower()
    rows = [r for r in rows if not f or f in r["kode"].lower() or f in r["mn"].lower()]
    if not rows: return "Tidak ada dosen cocok."
    out, cur = ["*Dosen pengampu*"], None
    for r in rows:
        if r["mn"] != cur: cur = r["mn"]; out.append(f"\n{r['mn']} ({r['kode']})")
        out.append(f"• {r['nama_asli']}")
    out.append("\nPenugasan dosen per sesi belum terkonfirmasi; variasi penulisan nama tidak digabung otomatis.")
    return "\n".join(out)

def cmd_kelas(c):
    k = c.execute("SELECT * FROM kelas").fetchone()
    return f"{k['nama']} · Semester {k['semester']} · zona waktu {k['zona_waktu']}\nTahun ajaran: {k['tahun_ajaran'] or 'belum terkonfirmasi'}"

def cmd_pengurus(c):
    rows = c.execute("SELECT peran,nama FROM pengurus").fetchall()
    return "\n".join(["*Pengurus kelas*"] + [f"• {r['peran']}: {r['nama'] or 'belum diisi'}" for r in rows])

def cmd_ref(c):
    return "\n".join(["*Referensi resmi SHJ* (perlu dicek ulang)"] + [f"• {r['label']}: {r['url']}" for r in c.execute("SELECT label,url FROM referensi_resmi")])

def cmd_hitungmundur(arg):
    try: t = date.fromisoformat((arg or "").strip())
    except ValueError: return "Format tanggal: YYYY-MM-DD"
    d = (t - now().date()).days
    return f"{d} hari lagi menuju {t.isoformat()}" if d > 0 else ("Hari ini!" if d == 0 else f"Sudah lewat {-d} hari yang lalu")

def cmd_kelompok(arg):
    try: n, names = arg.split(None, 1); n = int(n)
    except Exception: return "Pakai: kelompok <jumlah> nama1,nama2,..."
    people = [x.strip() for x in names.split(",") if x.strip()]
    if not 1 <= n <= len(people): return "Jumlah kelompok harus 1..jumlah anggota."
    random.shuffle(people); g = [people[i::n] for i in range(n)]
    return "\n".join(f"*Kelompok {i+1}* (ketua: {x[0]}): " + ", ".join(x) for i, x in enumerate(g))

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    cmd, rest = a[0].lower(), " ".join(a[1:])
    if cmd == "hitungmundur": print(cmd_hitungmundur(rest)); sys.exit()
    if cmd == "kelompok": print(cmd_kelompok(rest)); sys.exit()
    c = conn()
    print({"jadwal": lambda: cmd_jadwal(c, rest), "next": lambda: cmd_next(c), "matkul": lambda: cmd_matkul(c),
           "dosen": lambda: cmd_dosen(c, rest), "kelas": lambda: cmd_kelas(c), "pengurus": lambda: cmd_pengurus(c),
           "referensi": lambda: cmd_ref(c)}.get(cmd, lambda: __doc__)())
