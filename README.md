# 🔐 UTS Kriptografi — Implementasi Cipher Klasik

Program Python untuk UTS mata kuliah **Kriptografi**, mengimplementasikan tiga algoritma cipher klasik beserta fitur brute-force attack.

---

## 📋 Daftar Isi

- [Deskripsi](#-deskripsi)
- [Fitur](#-fitur)
- [Prasyarat](#-prasyarat)
- [Instalasi & Penggunaan](#-instalasi--penggunaan)
- [Penjelasan Algoritma](#-penjelasan-algoritma)
- [Contoh Output](#-contoh-output)
- [Struktur Program](#-struktur-program)

---

## 📖 Deskripsi

Program ini merupakan implementasi dari beberapa algoritma enkripsi dan dekripsi klasik yang dikerjakan sebagai tugas UTS Kriptografi. Program mencakup:

- **Soal 1** – Enkripsi Affine Cipher & validasi kunci
- **Soal 2** – Dekripsi Affine Cipher & Brute Force Attack
- **Soal 3** – Enkripsi/Dekripsi Columnar Transposition Cipher
- **Tambahan** – Rail Fence Cipher

---

## ✨ Fitur

| Fitur | Keterangan |
|-------|-----------|
| Affine Cipher Enkripsi | Enkripsi teks dengan fungsi `E(P) = (aP + b) mod 26` |
| Affine Cipher Dekripsi | Dekripsi dengan invers modulo menggunakan Extended Euclidean Algorithm |
| Validasi Kunci Affine | Memastikan `gcd(a, 26) = 1` agar kunci valid |
| Brute Force Affine | Mencoba semua 312 pasangan kunci valid `(a, b)` |
| Columnar Transposition | Enkripsi & dekripsi berbasis transposisi kolom berurutan alfabet |
| Rail Fence Cipher | Enkripsi & dekripsi menggunakan pola zig-zag rel |
| Tabel Enkripsi | Menampilkan tabel perhitungan per huruf untuk Affine Cipher |

---

## 🛠 Prasyarat

- **Python 3.8** atau lebih baru
- Tidak memerlukan library eksternal — hanya menggunakan library bawaan Python (`math`, `string`)

---

## 🚀 Instalasi & Penggunaan

### 1. Clone repository

```bash
git clone https://github.com/<username>/uts_kriptografi.git
cd uts_kriptografi
```

### 2. Jalankan program

```bash
python uts_kriptografi.py
```

> Tidak perlu instalasi dependensi tambahan karena program hanya menggunakan standard library Python.

---

## 📐 Penjelasan Algoritma

### 1. Affine Cipher

Affine Cipher adalah substitusi monoalfabetik dengan fungsi matematika:

- **Enkripsi:** `C = (a × P + b) mod 26`
- **Dekripsi:** `P = a⁻¹ × (C − b) mod 26`

Syarat kunci: nilai `a` harus **relatif prima** dengan 26, yaitu `gcd(a, 26) = 1`.

Nilai `a` yang valid: `{1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25}` (12 nilai)

Total pasangan kunci `(a, b)`: **12 × 26 = 312 kunci**

Contoh mengapa `a = 13` tidak valid:
- `gcd(13, 26) = 13 ≠ 1`
- Pemetaan tidak bijektif → dekripsi tidak unik

Invers modulo dicari menggunakan **Extended Euclidean Algorithm**.

---

### 2. Columnar Transposition Cipher

Teks plaintext diatur dalam baris-baris matriks, lalu kolom dibaca sesuai urutan **alfabetis** dari kunci.

**Langkah Enkripsi:**
1. Tulis plaintext baris demi baris ke dalam matriks dengan lebar = panjang kunci
2. Tambahkan padding `'X'` jika teks tidak habis dibagi
3. Baca kolom sesuai urutan alfabetis kunci

**Contoh:**
```
Plaintext : TEKNIKINFORMATIKAUNISBA
Kunci     : KUNCI  →  Urutan kolom: [2, 4, 1, 3, 0]
```

---

### 3. Rail Fence Cipher

Cipher transposisi berbasis pola **zig-zag** (seperti rel kereta).

- **Enkripsi:** Tulis huruf bergantian di setiap "rel", lalu gabungkan per rel
- **Dekripsi:** Rekonstruksi pola zig-zag untuk menempatkan kembali setiap huruf

**Contoh dengan 3 rel:**
```
T . . . I . . . M . . .
. E . N . K . N . O . A
. . K . . . I . . . T .
Cipher: TIMENKNOAKKIT...
```

---

## 📊 Contoh Output

```
=======================================================
       PROGRAM UTS KRIPTOGRAFI
=======================================================

SOAL 1 - AFFINE CIPHER
Nilai a yang valid: [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
Jumlah nilai a valid: 12
Jumlah pasangan kunci (a,b): 312

Tabel Enkripsi Affine Cipher
Huruf     Nilai P   (aP+b) mod 26     Cipher
K         10        96 mod 26 = 18    S
R         17        ...               ...
...

Plaintext  : KRIPTOGRAFI
Ciphertext : SXOLEBZXKDO
Hasil dekripsi: KRIPTOGRAFI

SOAL 3 - COLUMNAR TRANSPOSITION
Plaintext  : TEKNIKINFORMATIKAUNISBA
Kunci      : KUNCI
Ciphertext : ...
```

---

## 🗂 Struktur Program

```
uts_kriptografi/
├── uts_kriptografi.py   # File utama program
├── requirements.txt       # Daftar dependensi (stdlib only)
└── README.md              # Dokumentasi ini
```

### Fungsi-fungsi Utama

| Fungsi | Deskripsi |
|--------|-----------|
| `bersihkan(teks)` | Normalisasi teks: uppercase, hapus non-alfabet |
| `invers_modulo(a, m)` | Extended Euclidean Algorithm untuk invers mod |
| `validasi_kunci_affine(a)` | Validasi syarat `gcd(a, 26) = 1` |
| `affine_enkripsi(plain, a, b)` | Enkripsi Affine Cipher |
| `affine_dekripsi(cipher, a, b)` | Dekripsi Affine Cipher |
| `brute_force_affine(cipher, kata)` | Brute force semua kunci Affine |
| `columnar_enkripsi(plain, kunci)` | Enkripsi Columnar Transposition |
| `columnar_dekripsi(cipher, kunci)` | Dekripsi Columnar Transposition |
| `rail_fence_enkripsi(plain, rel)` | Enkripsi Rail Fence Cipher |
| `rail_fence_dekripsi(cipher, rel)` | Dekripsi Rail Fence Cipher |
| `tampilkan_tabel_affine(plain, a, b)` | Tampilkan tabel enkripsi per huruf |

---

## 👨‍💻 Informasi

- **Mata Kuliah:** Kriptografi
- **Institusi:** Universitas Islam Bandung (UNISBA)
- **Program:** Teknik Informatika
