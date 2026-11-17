# SiKupingBesar · UCL League Simulator

Aplikasi web untuk memprediksi peluang juara Liga Champions UEFA format 36 tim.
Kekuatan tim diestimasi dari hasil liga domestik dan UCL dengan model Poisson,
lalu sisa musim disimulasikan puluhan ribu kali dengan Monte Carlo.

Proyek mata kuliah Probabilitas dan Statistika. Dibangun dengan Python,
Streamlit, NumPy, pandas, SciPy, Plotly, dan Tailwind CSS untuk kartu hero.

## Yang ditampilkan

- Peluang setiap tim mencapai Top 24, Top 8, 16 besar, perempat final,
  semifinal, final, dan juara.
- Interval kepercayaan 95% Wilson untuk peluang juara.
- Klasemen proyeksi dan heatmap peluang per babak.
- Head-to-head lengkap dengan matriks skor dan peluang lolos dua leg.
- Grafik konvergensi Monte Carlo, uji Chi-square Poisson, dan Brier score 1X2.
- Simulator untuk mengunggah CSV dan mengatur jumlah simulasi, home advantage,
  half-life form, bobot liga domestik, shrinkage, dan seed.

## Menjalankan

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Buka alamat yang ditampilkan Streamlit (biasanya `http://localhost:8501`).

Dataset gabungan sudah tersedia di `data/matches.csv`. Untuk membuat ulang dari
11 file liga domestik, histori UCL 2025/26, dan daftar 36 tim UCL 2026/27 di
`data/`:

```bash
python build_dataset.py
```

Dataset contoh lama tetap tersimpan di `data/matches_sample.csv` dan bisa
dibuat ulang dengan `python generate_sample_data.py`.

### Pengujian

```bash
pytest -q
```

## Dataset

File CSV dengan kolom berikut:

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `date` | tanggal | Tanggal pertandingan |
| `home` | teks | Tim kandang |
| `away` | teks | Tim tandang |
| `home_goals` | angka | Gol kandang; kosong jika belum dimainkan |
| `away_goals` | angka | Gol tandang; kosong jika belum dimainkan |
| `competition` | teks | `UCL` untuk laga UCL musim ini, `UCL 2025/26` untuk histori rating, selain itu nama liga domestik |

Aturan validasi:

- Harus ada tepat 36 tim yang muncul di baris `competition = UCL` musim ini.
  Baris histori `UCL 2025/26` tidak dihitung untuk aturan ini.
- Nama tim harus konsisten antara laga domestik dan UCL.
- Gol kandang dan tandang diisi keduanya atau dikosongkan keduanya.
- Laga UCL yang belum dimainkan dianggap sisa jadwal yang akan disimulasikan.

`data/matches.csv` berisi **1.381 laga**:

- **1.048 laga domestik** dari 11 liga 2026/27 (`E0`, `SP1`, `D1`, `I1`, `F1`,
  `N1`, `B1`, `P1`, `T1`, `G1`, `SC0`),
- **189 laga UCL 2025/26** (league phase sampai final) sebagai histori rating,
  dengan label kompetisi `UCL 2025/26`,
- **144 laga UCL 2026/27** untuk 36 klub dari `ucl_2026_27_teams.csv`, semuanya
  belum dimainkan sehingga seluruh league phase diproyeksikan.

`build_dataset.py` menyamakan nama klub, memakai hasil UCL 2025/26 untuk
menghubungkan kekuatan antarliga, lalu membuat jadwal league phase 2026/27.
Lima klub tidak punya data domestik maupun histori UCL (LASK, Sabah, Shakhtar
Donetsk, Slovan Bratislava, Viking), jadi ratingnya bertumpu pada shrinkage dan
ditampilkan dengan jumlah laga 0. Ganti dengan dataset lain lewat halaman
Simulator. Tanggal data terakhir selalu ditampilkan di aplikasi.

## Struktur proyek

```
app.py                     pintu masuk, tema, navigasi
build_dataset.py           penggabung domestik + histori UCL + jadwal UCL baru
generate_sample_data.py    pembuat dataset contoh sintetis
core/ratings.py            estimasi attack/defence/mu/home advantage
core/simulate.py           mesin Monte Carlo dan bracket knockout
core/stats.py              Wilson CI, konvergensi, Chi-square, Brier, H2H
core/pipeline.py           validasi data dan alur data -> rating -> simulasi
data/matches.csv           dataset bawaan hasil build_dataset.py
data/matches_sample.csv    dataset contoh sintetis
data/ucl_2025_26.csv       histori UCL 2025/26
data/ucl_2026_27_teams.csv 36 peserta UCL 2026/27
data/*.csv                 file liga domestik (football-data.co.uk)
views/                     satu file satu halaman
ui/theme.py                CSS tema kuning dan tema Plotly
ui/navbar.py               navbar tanpa sidebar
ui/components.py           kartu, hero, dan format angka
ui/charts.py               grafik Plotly
ui/state.py                session state dan cache Streamlit
ui/templates/hero.html     template Tailwind untuk kartu hero
tests/                     uji core dan template
.streamlit/config.toml     tema Streamlit
```

## Model singkat

Untuk laga kandang-tandang:

```
lambda_home = mu * H * attack(home) * defence(away)
lambda_away = mu * attack(away) * defence(home)
```

Gol disampel dari Poisson. Parameter diestimasi dengan iterasi maximum
likelihood berbobot; laga yang lebih tua diberi bobot eksponensial dengan
half-life yang bisa diatur, laga UCL lebih berat daripada liga domestik, dan
rating di-shrink ke 1. Klasemen diurutkan berdasarkan poin, selisih gol, gol,
lalu undian acak. Playoff, 16 besar, perempat final, dan semifinal dimainkan dua
leg; agregat imbang diselesaikan 50:50. Final satu laga di tempat netral.

Reproduksibilitas: seed dan parameter yang sama menghasilkan tabel identik.

## Kriteria penerimaan yang diperiksa

1. Jumlah peluang juara = 100%; jumlah peluang Top 8 = 8; Top 24 = 24.
2. Seed sama menghasilkan hasil identik.
3. Pita CI konvergensi menyempit seiring jumlah simulasi.
4. Peluang menang + seri + kalah Head-to-Head = 100%.
5. Uji Chi-square menampilkan statistik, derajat bebas, p-value, dan hipotesis.
6. Semua halaman berjalan dengan dataset valid.
7. Halaman Metodologi memuat rumus, asumsi, dan keterbatasan.

## Catatan kerja tim

Lihat `PRD_UCL_League_Simulator.md` untuk pembagian branch dan aturan Git.
File bersama (`app.py`, `ui/state.py`, `requirements.txt`, `.gitignore`,
`README.md`) sebaiknya diubah lewat PR kecil tersendiri.
