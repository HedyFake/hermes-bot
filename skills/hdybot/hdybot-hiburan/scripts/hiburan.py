#!/usr/bin/env python3
"""Hiburan & kuis ringan kelas (port dari FunAndUtilityService). Konten ada di ../data/bank.json.
Pakai: hiburan.py quote [umum|islami|motivasi] | fakta | pantun | doa | surah | truth | dare | dadu | koin | suit <batu|gunting|kertas>
       hiburan.py soal [tebakkata|caklontong|family100|<kategori game>] | cek <kategori> <indeks> <jawaban> | hilih|alay|besarkecil|balikhuruf <teks>"""
import json, os, random, sys, re
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "bank.json")
B = json.load(open(D, encoding="utf-8"))
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

def soal(kat):
    pools = {"tebakkata": [(x["q"], x["hint"], x["q"]) for x in B["tebak_kata_bank"]],
             "caklontong": [(x["q"], x["hint"], x["a"]) for x in B["cak_lontong_bank"]],
             "family100": [(x["q"], x["hint"], x["a"]) for x in B["family100_bank"]]}
    pools.update({})
    if kat in pools:
        items = pools[kat]; i = random.randrange(len(items)); q, h, a = items[i]
        if kat == "tebakkata":
            w = list(a); random.shuffle(w); q = "Susun huruf ini menjadi istilah: " + " ".join(w).upper() + "\nPetunjuk: " + h; 
        return f"[{kat}#{i}] {q}" + ("" if kat == "tebakkata" else f"\nPetunjuk: {h}")
    items = [(i, s) for i, s in enumerate(B["soal_game"]) if not kat or s["category"] == kat]
    if not items: return "Kategori: tebakkata, caklontong, family100, " + ", ".join(sorted({s['category'] for s in B['soal_game']}))
    i, s = random.choice(items)
    return f"[{s['category']}#{i}] ({s['level']}) {s['prompt']}\nPetunjuk: {s['hint']}"

def cek(kat, idx, jawab):
    idx = int(idx)
    if kat == "tebakkata": a = B["tebak_kata_bank"][idx]["q"]; pen = ""
    elif kat == "caklontong": a = B["cak_lontong_bank"][idx]["a"]; pen = ""
    elif kat == "family100": a = B["family100_bank"][idx]["a"]; pen = ""
    else: s = B["soal_game"][idx]; a = s["answer"]; pen = "\n" + s["explanation"]
    return ("✅ Benar! (+15 XP bila opt-in aktif)" if norm(jawab) == norm(a) else f"❌ Belum tepat. Jawaban: {a}") + pen

def main(a):
    k = a[0].lower() if a else ""; r = " ".join(a[1:])
    if k == "quote": return random.choice(B["quotes_" + (r if r in ("umum", "islami", "motivasi") else "umum")])
    if k == "fakta": return random.choice(B["fakta_unik"])
    if k == "pantun": return random.choice(B["pantun_koleksi"])
    if k == "doa": return random.choice(B["doa_harian"])
    if k == "surah": return "\n".join(B["daftar_surah_ringkas"])
    if k == "truth": return random.choice(B["truth_list"])
    if k == "dare": return random.choice(B["dare_list"])
    if k == "dadu": return f"🎲 {random.randint(1, 6)}"
    if k == "koin": return random.choice(["Gambar", "Angka"])
    if k == "suit":
        m = {"batu": 0, "gunting": 1, "kertas": 2}
        if r not in m: return "Pilih: batu, gunting, kertas"
        b = random.choice(list(m)); res = "Seri" if m[r] == m[b] else ("Kamu menang" if (m[r] - m[b]) % 3 == 2 else "Bot menang")
        return f"Kamu {r}, bot {b}. {res}!"
    if k == "soal": return soal(r.lower())
    if k == "cek":
        kat, idx, *j = r.split(); return cek(kat.lower(), idx, " ".join(j))
    if k in ("hilih", "alay", "besarkecil", "balikhuruf") and r:
        if k == "hilih": return re.sub(r"[aeiouAEIOU]", "i", r)
        if k == "balikhuruf": return r[::-1]
        if k == "besarkecil": return "".join(ch.upper() if i % 2 else ch.lower() for i, ch in enumerate(r))
        return r.translate(str.maketrans("aAiIeEoOsS", "4411330055"))
    return __doc__
if __name__ == "__main__": print(main(sys.argv[1:]))
