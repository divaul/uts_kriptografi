import math
import string

ALFABET = string.ascii_uppercase
MOD = 26


def bersihkan(teks):
    """Mengubah teks menjadi huruf kapital dan menghapus spasi/tanda baca."""
    return ''.join(h for h in teks.upper() if h in ALFABET)


def invers_modulo(a, m=MOD):
    """Mencari invers a modulo m dengan Extended Euclidean Algorithm."""
    a %= m
    t, t_baru = 0, 1
    r, r_baru = m, a

    while r_baru != 0:
        q = r // r_baru
        t, t_baru = t_baru, t - q * t_baru
        r, r_baru = r_baru, r - q * r_baru

    if r != 1:
        raise ValueError(
            f"Kunci a={a} tidak valid: gcd({a}, {m}) bukan 1, "
            "sehingga invers modulo tidak ada."
        )

    return t % m


def validasi_kunci_affine(a):
    if not isinstance(a, int) or math.gcd(a, MOD) != 1:
        raise ValueError(
            f"Kunci a={a} tidak valid. Nilai a harus relatif prima "
            "dengan 26 (contoh: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)."
        )


def affine_enkripsi(plain, a, b):
    validasi_kunci_affine(a)
    plain = bersihkan(plain)
    hasil = []

    for huruf in plain:
        p = ord(huruf) - ord('A')
        c = (a * p + b) % MOD
        hasil.append(chr(c + ord('A')))

    return ''.join(hasil)


def affine_dekripsi(cipher, a, b):
    validasi_kunci_affine(a)
    cipher = bersihkan(cipher)
    a_inv = invers_modulo(a, MOD)
    hasil = []

    for huruf in cipher:
        c = ord(huruf) - ord('A')
        p = (a_inv * (c - b)) % MOD
        hasil.append(chr(p + ord('A')))

    return ''.join(hasil)


def brute_force_affine(cipher, kata):
    """Mencoba seluruh pasangan kunci valid dan menampilkan kandidat."""
    cipher = bersihkan(cipher)
    kata = bersihkan(kata)
    nilai_a = [a for a in range(MOD) if math.gcd(a, MOD) == 1]
    kandidat = []

    for a in nilai_a:
        for b in range(MOD):
            plain = affine_dekripsi(cipher, a, b)
            if kata in plain:
                kandidat.append((a, b, plain))

    return kandidat


def urutan_kolom(kunci):
    """Menghasilkan indeks kolom menurut abjad kunci, termasuk huruf berulang."""
    kunci = bersihkan(kunci)
    if not kunci:
        raise ValueError("Kunci Columnar tidak boleh kosong.")

    return sorted(range(len(kunci)), key=lambda i: (kunci[i], i))


def columnar_enkripsi(plain, kunci):
    plain = bersihkan(plain)
    kunci = bersihkan(kunci)

    if not kunci:
        raise ValueError("Kunci Columnar tidak boleh kosong.")

    jumlah_kolom = len(kunci)
    while len(plain) % jumlah_kolom != 0:
        plain += 'X'

    matriks = [
        plain[i:i + jumlah_kolom]
        for i in range(0, len(plain), jumlah_kolom)
    ]

    urutan = urutan_kolom(kunci)
    cipher = ''

    for kolom in urutan:
        for baris in matriks:
            cipher += baris[kolom]

    return cipher


def columnar_dekripsi(cipher, kunci):
    cipher = bersihkan(cipher)
    kunci = bersihkan(kunci)

    if not kunci:
        raise ValueError("Kunci Columnar tidak boleh kosong.")

    jumlah_kolom = len(kunci)
    if len(cipher) % jumlah_kolom != 0:
        raise ValueError(
            "Panjang ciphertext harus habis dibagi jumlah kolom kunci."
        )

    jumlah_baris = len(cipher) // jumlah_kolom
    urutan = urutan_kolom(kunci)
    matriks = [[''] * jumlah_kolom for _ in range(jumlah_baris)]

    posisi = 0
    for kolom in urutan:
        for baris in range(jumlah_baris):
            matriks[baris][kolom] = cipher[posisi]
            posisi += 1

    plain = ''.join(''.join(baris) for baris in matriks)
    # Menghapus X pengisi di akhir. Jika plaintext asli memang berakhir X,
    # gunakan catatan/panjang plaintext asli agar X tersebut tidak ikut terhapus.
    return plain.rstrip('X')


def rail_fence_enkripsi(plain, rel):
    plain = bersihkan(plain)

    if not isinstance(rel, int) or rel < 1:
        raise ValueError("Jumlah rel harus berupa bilangan bulat minimal 1.")
    if rel == 1 or rel >= len(plain):
        return plain

    baris = ['' for _ in range(rel)]
    rel_sekarang = 0
    arah = 1

    for huruf in plain:
        baris[rel_sekarang] += huruf

        if rel_sekarang == 0:
            arah = 1
        elif rel_sekarang == rel - 1:
            arah = -1

        rel_sekarang += arah

    return ''.join(baris)


def rail_fence_dekripsi(cipher, rel):
    cipher = bersihkan(cipher)

    if not isinstance(rel, int) or rel < 1:
        raise ValueError("Jumlah rel harus berupa bilangan bulat minimal 1.")
    if rel == 1 or rel >= len(cipher):
        return cipher

    pola = []
    rel_sekarang = 0
    arah = 1

    for _ in cipher:
        pola.append(rel_sekarang)

        if rel_sekarang == 0:
            arah = 1
        elif rel_sekarang == rel - 1:
            arah = -1

        rel_sekarang += arah

    jumlah_per_rel = [pola.count(i) for i in range(rel)]
    isi_rel = []
    posisi = 0

    for jumlah in jumlah_per_rel:
        isi_rel.append(list(cipher[posisi:posisi + jumlah]))
        posisi += jumlah

    indeks_rel = [0] * rel
    hasil = []

    for nomor_rel in pola:
        hasil.append(isi_rel[nomor_rel][indeks_rel[nomor_rel]])
        indeks_rel[nomor_rel] += 1

    return ''.join(hasil)


def tampilkan_tabel_affine(plain, a, b):
    validasi_kunci_affine(a)
    plain = bersihkan(plain)

    print("\nTabel Enkripsi Affine Cipher")
    print(f"{'Huruf':<10}{'Nilai P':<10}{'(aP+b) mod 26':<18}{'Cipher'}")

    for huruf in plain:
        p = ord(huruf) - ord('A')
        c = (a * p + b) % MOD
        cipher_huruf = chr(c + ord('A'))
        print(f"{huruf:<10}{p:<10}{c:<18}{cipher_huruf}")


def main():
    print("=" * 55)
    print("       PROGRAM UTS KRIPTOGRAFI")
    print("=" * 55)

    # SOAL 1: Affine Cipher
    print("\nSOAL 1 - AFFINE CIPHER")
    nilai_a_valid = [a for a in range(MOD) if math.gcd(a, MOD) == 1]
    print("Nilai a yang valid:", nilai_a_valid)
    print("Jumlah nilai a valid:", len(nilai_a_valid))
    print("Jumlah pasangan kunci (a,b):", len(nilai_a_valid) * MOD)

    tampilkan_tabel_affine("KRIPTOGRAFI", 7, 10)
    cipher1 = affine_enkripsi("KRIPTOGRAFI", 7, 10)
    print("Plaintext          :", "KRIPTOGRAFI")
    print("Ciphertext         :", cipher1)
    print("Hasil dekripsi     :", affine_dekripsi(cipher1, 7, 10))

    # SOAL 1b: mengapa a = 13 tidak valid
    print("\nSOAL 1b - MENGAPA a = 13 TIDAK VALID")
    print("gcd(13, 26) =", math.gcd(13, MOD), "(syarat: harus 1)")
    print("Contoh perhitungan E(P) = (13P + b) mod 26 dengan b = 0:")
    for huruf, p in (("A", 0), ("B", 1), ("C", 2), ("D", 3)):
        print(f"  {huruf} (P={p}): 13 x {p} mod 26 = {(13 * p) % MOD}")
    print("A dan C sama-sama menjadi 'A'; B dan D sama-sama menjadi 'N'.")
    print("Satu huruf cipher bisa berasal dari banyak huruf plaintext,")
    print("sehingga dekripsi tidak unik (13 tidak punya invers mod 26).")
    try:
        affine_enkripsi("KRIPTOGRAFI", 13, 0)
    except ValueError as e:
        print("Program menolak kunci:", e)
        
    # SOAL 2: Dekripsi Affine Cipher
    print("\nSOAL 2 - DEKRIPSI AFFINE CIPHER")
    cipher2 = "EVWUNINLWZIP"
    a, b = 5, 8
    a_inv = invers_modulo(a, MOD)
    print(f"Invers {a} modulo 26:", a_inv)
    print(f"Bukti: ({a} x {a_inv}) mod 26 = {(a * a_inv) % MOD}")
    print("Fungsi dekripsi    : P = (21 x (C - 8)) mod 26")
    print("Ciphertext         :", cipher2)
    print("Plaintext          :", affine_dekripsi(cipher2, a, b))

    print("\nBrute Force Affine untuk ciphertext Soal 2")
    hasil_brute = brute_force_affine(cipher2, "KRIPTOGRAFI")
    if hasil_brute:
        for a_hasil, b_hasil, plain_hasil in hasil_brute:
            print(f"a={a_hasil}, b={b_hasil} -> {plain_hasil}")
    else:
        print("Tidak ditemukan kandidat yang memuat kata tersebut.")

    # SOAL 3: Columnar Transposition
    print("\nSOAL 3 - COLUMNAR TRANSPOSITION")
    plain3 = "TEKNIK INFORMATIKA UNISBA"
    kunci3 = "KUNCI"
    cipher3 = columnar_enkripsi(plain3, kunci3)
    hasil_dekripsi3 = columnar_dekripsi(cipher3, kunci3)
    print("Plaintext          :", bersihkan(plain3))
    print("Kunci              :", kunci3)
    print("Urutan kolom       :", [i + 1 for i in urutan_kolom(kunci3)])
    print("Ciphertext         :", cipher3)
    print("Hasil dekripsi     :", hasil_dekripsi3)

    print("\nBrute Force Affine pada ciphertext Soal 3 (kata: INFORMATIKA)")
    print("Catatan: Soal 3 menghasilkan ciphertext Columnar Transposition,")
    print("sedangkan brute force ini khusus untuk ciphertext Affine.")
    hasil_soal3 = brute_force_affine(cipher3, "INFORMATIKA")
    if hasil_soal3:
        for a_hasil, b_hasil, plain_hasil in hasil_soal3:
            print(f"a={a_hasil}, b={b_hasil} -> {plain_hasil}")
    else:
        print("Tidak ditemukan kandidat. Ini wajar karena ciphertext Soal 3")
        print("dibuat dengan Columnar Transposition, bukan Affine Cipher.")

    # Contoh Rail Fence (diminta di Bagian C)
    print("\nPENGUJIAN RAIL FENCE CIPHER")
    data_rail = "TEKNIK INFORMATIKA"
    jumlah_rel = 3
    cipher_rail = rail_fence_enkripsi(data_rail, jumlah_rel)
    plain_rail = rail_fence_dekripsi(cipher_rail, jumlah_rel)
    print("Plaintext          :", bersihkan(data_rail))
    print("Jumlah rel         :", jumlah_rel)
    print("Ciphertext         :", cipher_rail)
    print("Hasil dekripsi     :", plain_rail)
    print("Berhasil kembali   :", plain_rail == bersihkan(data_rail))

    # Uji data pribadi: silakan ganti dengan nama/kalimat kelompok.
    print("\nPENGUJIAN DATA PRIBADI")
    data_pribadi = "NAMA KELOMPOK ANDA"
    a_pribadi, b_pribadi = 7, 10
    cipher_pribadi = affine_enkripsi(data_pribadi, a_pribadi, b_pribadi)
    plain_pribadi = affine_dekripsi(cipher_pribadi, a_pribadi, b_pribadi)
    print("Data asli          :", bersihkan(data_pribadi))
    print("Hasil enkripsi     :", cipher_pribadi)
    print("Hasil dekripsi     :", plain_pribadi)
    print("Sama dengan awal   :", plain_pribadi == bersihkan(data_pribadi))

    print("\n" + "=" * 55)
    print("PROGRAM SELESAI")
    print("=" * 55)


if __name__ == "__main__":
    main()
