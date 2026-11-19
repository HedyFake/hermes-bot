#!/usr/bin/env python3
"""Kalkulator deterministik HdyBot (port dari perawat.ts + utilitas). Angka akhir SELALU dihitung di sini, bukan oleh model.
Pakai: hitung.py imt <kg> <cm> | gcs <E> <V> <M> | tetesan <ml> <jam> [faktor_tetes] | balance <masuk_ml> <keluar_ml>
       hitung.py ipk <sks:bobot,sks:bobot,...> | calc "<ekspresi>" | konversi <nilai> <dari> <ke>"""
import sys, ast, operator as op, re

def fmt(x):
    return f"{x:.2f}".rstrip("0").rstrip(".") if abs(x - round(x)) > 1e-9 else str(int(round(x)))

def imt(kg, cm):
    kg, cm = float(kg), float(cm)
    if kg <= 0 or cm <= 0: return "Berat dan tinggi harus > 0."
    v = kg / (cm / 100) ** 2
    return f"IMT = {fmt(v)} kg/m² (hitung untuk belajar, bukan diagnosis)"

def gcs(e, v, m):
    e, v, m = int(e), int(v), int(m)
    if not (1 <= e <= 4 and 1 <= v <= 5 and 1 <= m <= 6): return "Rentang: E1–4, V1–5, M1–6. Jika komponen tidak dapat diuji, total tidak dihitung."
    return f"E{e} V{v} M{m} = GCS {e+v+m}/15"

def tetesan(ml, jam, faktor=None):
    ml, jam = float(ml), float(jam)
    if ml <= 0 or jam <= 0: return "Volume dan jam harus > 0."
    if faktor is None: return f"{fmt(ml/jam)} mL/jam. Tambahkan faktor tetes (tetes/mL, dari kemasan set infus) untuk tetes/menit."
    f = float(faktor)
    if f <= 0: return "Faktor tetes harus > 0."
    return f"{round(ml*f/(jam*60))} tetes/menit\n{fmt(ml)} mL × {fmt(f)} tetes/mL ÷ {fmt(jam*60)} menit. Contoh hitung untuk belajar."

def balance(masuk, keluar):
    a, b = float(masuk), float(keluar)
    return f"Balance cairan tercatat: {fmt(a-b)} mL\nMasuk {fmt(a)} mL − keluar {fmt(b)} mL."

def ipk(spec):
    tot_sks = tot = 0.0
    for part in spec.replace(" ", "").split(","):
        s, b = part.split(":"); s, b = float(s), float(b); tot_sks += s; tot += s * b
    if tot_sks <= 0: return "Masukkan minimal satu pasang sks:bobot."
    return f"IP/IPK = {tot/tot_sks:.2f} dari {fmt(tot_sks)} SKS"

OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod, ast.USub: op.neg, ast.UAdd: op.pos}
def _ev(n):
    if isinstance(n, ast.Expression): return _ev(n.body)
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
    if isinstance(n, ast.BinOp) and type(n.op) in OPS:
        if isinstance(n.op, ast.Pow) and abs(_ev(n.right)) > 100: raise ValueError("pangkat terlalu besar")
        return OPS[type(n.op)](_ev(n.left), _ev(n.right))
    if isinstance(n, ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](_ev(n.operand))
    raise ValueError("ekspresi tidak diizinkan")
def calc(expr):
    try: return fmt(_ev(ast.parse(expr.replace("^", "**").replace(",", "."), mode="eval")))
    except ZeroDivisionError: return "Tidak bisa dibagi nol."
    except Exception as e: return f"Ekspresi tidak valid ({e})."

LEN = {"mm": .001, "cm": .01, "m": 1, "km": 1000, "inch": .0254, "in": .0254, "ft": .3048, "mil": 1609.344}
MASS = {"mg": 1e-6, "g": 1e-3, "kg": 1, "lb": .45359237, "oz": .028349523}
VOL = {"ml": 1e-3, "l": 1, "cc": 1e-3}
def konversi(val, a, b):
    v, a, b = float(val), a.lower(), b.lower()
    if a in "cfk" and b in "cfk" and len(a) == len(b) == 1:
        c = v if a == "c" else (v - 32) * 5 / 9 if a == "f" else v - 273.15
        r = c if b == "c" else c * 9 / 5 + 32 if b == "f" else c + 273.15
        return f"{fmt(v)}°{a.upper()} = {fmt(r)}°{b.upper()}"
    for t in (LEN, MASS, VOL):
        if a in t and b in t: return f"{fmt(v)} {a} = {fmt(v*t[a]/t[b])} {b}"
    return "Satuan tidak didukung. Kurs mata uang tidak ada di sini (butuh data terkini); cari lewat web."

if __name__ == "__main__":
    a = sys.argv[1:]
    try:
        k = a[0].lower() if a else ""
        if k == "imt": print(imt(*a[1:3]))
        elif k == "bmi": print(imt(*a[1:3]))
        elif k == "gcs": print(gcs(*[re.sub(r"\D", "", x) for x in a[1:4]]))
        elif k == "tetesan": print(tetesan(*a[1:4]))
        elif k == "balance": print(balance(*a[1:3]))
        elif k == "ipk": print(ipk(a[1]))
        elif k == "calc": print(calc(" ".join(a[1:])))
        elif k == "konversi": print(konversi(*a[1:4]))
        else: print(__doc__)
    except (TypeError, ValueError, IndexError):
        print("Argumen tidak valid.\n" + __doc__)
