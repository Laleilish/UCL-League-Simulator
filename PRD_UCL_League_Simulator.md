# PRD: SiKupingBesar (UCL League Simulator)

Aplikasi web prediksi juara Liga Champions berbasis simulasi Monte Carlo · Mata kuliah Probabilitas dan Statistika · Versi 1.0 · 1 November 2026

## 1. Ringkasan

SiKupingBesar (UCL League Simulator) adalah aplikasi web yang memprediksi peluang tiap klub menjadi juara Liga Champions UEFA (format 36 tim sejak 2024/25). Aplikasi memodelkan jumlah gol tiap pertandingan dengan distribusi Poisson, lalu mensimulasikan sisa musim puluhan ribu kali dengan metode Monte Carlo. Dari hasil simulasi dihitung peluang tiap tim mencapai tiap babak sampai juara, lengkap dengan interval kepercayaan.

Aplikasi dikerjakan oleh tim tiga orang, dibangun dengan Python dan Streamlit, memakai Tailwind CSS untuk tampilan kartu, dan hanya memakai dataset laga liga domestik masing-masing klub serta dataset UCL.

## 2. Latar belakang dan masalah

Prediksi juara sepak bola sering disajikan sebagai opini atau angka tanpa dasar yang jelas. Untuk mata kuliah Probabilitas dan Statistika, dibutuhkan proyek yang menunjukkan penerapan konsep kuliah secara nyata dan dapat diverifikasi: variabel acak, distribusi Poisson, nilai ekspektasi, estimasi proporsi, interval kepercayaan, Law of Large Numbers, dan uji hipotesis.

Masalah yang diselesaikan:

- Belum ada alat sederhana yang menunjukkan **peluang** juara beserta **ketidakpastiannya** (bukan sekadar satu tebakan).
- Konsep statistika sulit dipahami jika hanya berupa rumus. Visualisasi interaktif membantu pembaca melihat bagaimana hasil menjadi stabil seiring jumlah simulasi bertambah.

## 3. Tujuan dan bukan tujuan

### Tujuan

1. Menghasilkan peluang tiap tim mencapai Top 8, Top 24, R16, perempat final, semifinal, final, dan juara.
2. Menampilkan ketidakpastian prediksi dengan interval kepercayaan 95%.
3. Menunjukkan secara visual bahwa hasil simulasi konvergen (Law of Large Numbers).
4. Memvalidasi asumsi model dengan uji Chi-square dan Brier score.
5. Menjelaskan metodologi dan keterbatasannya secara transparan.
6. Dapat dijalankan ulang dengan hasil yang sama (seed acak tetap).

### Bukan tujuan

Fitur berikut sengaja tidak dibuat karena tidak didukung oleh dataset yang dipakai:

- Data cedera, skorsing, transfer, atau kondisi pemain.
- Mode what-if (mengubah hasil laga atau kekuatan tim secara manual).
- Form guide 5 laga terakhir.
- Heatmap posisi akhir dan histogram distribusi poin.
- Pembaruan data langsung (live) dari API.
- Taruhan, odds bandar, atau saran finansial.

## 4. Pengguna target

| Pengguna | Kebutuhan |
| --- | --- |
| Dosen dan penilai | Melihat penerapan konsep kuliah dan kebenaran metodologi |
| Mahasiswa (pengembang) | Kode yang rapi, mudah dijelaskan, dan mudah dijalankan ulang |
| Penggemar sepak bola | Melihat peluang juara dengan tampilan yang mudah dibaca |

## 5. Data

### Sumber

- Dataset hasil laga liga domestik klub-klub peserta UCL.
- Dataset laga UCL (sudah dimainkan dan jadwal sisa).

Tidak ada sumber data lain. Data dimasukkan sebagai file CSV, dan tanggal data terakhir ditampilkan di aplikasi.

### Skema CSV

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| date | tanggal | Tanggal pertandingan |
| home | teks | Nama tim kandang |
| away | teks | Nama tim tandang |
| home\_goals | angka | Gol tim kandang (kosong jika belum dimainkan) |
| away\_goals | angka | Gol tim tandang (kosong jika belum dimainkan) |
| competition | teks | `UCL` untuk laga UCL, selain itu nama liga domestik |

### Aturan data

- Harus ada tepat 36 tim yang muncul di laga UCL.
- Nama tim harus konsisten antara dataset liga dan UCL.
- Laga yang belum dimainkan dikosongkan golnya dan dianggap sisa jadwal yang akan disimulasikan.

## 6. Persyaratan fungsional

Prioritas: **P0** wajib, **P1** penting, **P2** nilai tambah.

### 6.1 Pemodelan dan simulasi (inti)

| ID | Persyaratan | Prioritas |
| --- | --- | --- |
| F-01 | Memuat dataset CSV (file bawaan atau unggahan pengguna) dan memvalidasi kolom serta jumlah tim UCL | P0 |
| F-02 | Mengestimasi kekuatan serang dan bertahan tiap tim dari laga liga dan UCL dengan model Poisson | P0 |
| F-03 | Memberi bobot lebih kecil pada laga yang lebih lama (peluruhan eksponensial dengan half-life yang dapat diatur) | P0 |
| F-04 | Memberi bobot terpisah untuk laga liga domestik dibanding laga UCL | P1 |
| F-05 | Mensimulasikan sisa league phase dengan urutan klasemen: poin, selisih gol, gol, lalu acak | P0 |
| F-06 | Mensimulasikan playoff (peringkat 9-24), babak 16 besar, perempat final, semifinal, dan final | P0 |
| F-07 | Menghitung peluang tiap tim di tiap babak dan rata-rata poin serta posisi | P0 |
| F-08 | Menghitung interval kepercayaan 95% (Wilson) untuk peluang juara | P0 |
| F-09 | Mendukung seed acak agar hasil dapat direproduksi | P0 |
| F-10 | Home advantage dapat diestimasi dari data atau diatur manual | P1 |

### 6.2 Halaman dan tampilan

| ID | Halaman | Isi | Prioritas |
| --- | --- | --- | --- |
| F-11 | Dashboard | Kartu 3 tim favorit (peluang juara dan CI), bar chart peluang juara, klasemen proyeksi, heatmap peluang per babak | P0 |
| F-12 | Tabel | Tabel probabilitas lengkap 36 tim, dapat diurutkan, dan dapat diunduh sebagai CSV | P0 |
| F-13 | Head-to-Head | Pilih dua tim, tampilkan peluang menang, seri, kalah, ekspektasi gol, dan matriks skor | P0 |
| F-14 | Statistik | Grafik konvergensi dengan pita CI, uji Chi-square Poisson, dan Brier score | P0 |
| F-15 | Metodologi | Rumus, asumsi, dan keterbatasan model | P0 |
| F-16 | Simulator | Halaman tersendiri untuk unggah dataset dan mengatur jumlah simulasi, home advantage, half-life form, bobot liga domestik, dan seed; perubahan langsung dipakai semua halaman | P0 |

### 6.3 Nilai tambah

| ID | Persyaratan | Prioritas |
| --- | --- | --- |
| F-17 | Backtest per matchday (walk-forward) untuk validasi model yang tidak in-sample | P2 |
| F-18 | Perbandingan model Poisson sederhana dengan Dixon-Coles | P2 |
| F-19 | Peluang lolos dua leg pada laga knockout di halaman Head-to-Head | P2 |

## 7. Metodologi model

### Model gol

Jumlah gol tiap tim dalam satu laga diasumsikan berdistribusi Poisson:

- λ kandang = μ × H × serang(kandang) × bertahan(tandang)
- λ tandang = μ × serang(tandang) × bertahan(kandang)

μ adalah rata-rata gol dasar, H adalah home advantage, dan nilai bertahan yang lebih besar berarti pertahanan lebih lemah. Parameter diestimasi dengan iterasi maximum likelihood dan shrinkage ke nilai 1 agar stabil pada tim dengan sedikit data.

### Simulasi Monte Carlo

1. Hitung poin, gol, dan kebobolan dari laga UCL yang sudah dimainkan.
2. Untuk tiap laga sisa, ambil sampel gol dari Poisson, sebanyak N kali.
3. Urutkan klasemen tiap simulasi. Peringkat 1-8 lolos langsung ke R16, peringkat 9-24 ke playoff.
4. Simulasikan laga knockout dua leg. Jika agregat imbang, pemenang ditentukan 50:50 (mewakili perpanjangan waktu dan penalti). Final dimainkan satu laga di tempat netral.
5. Hitung proporsi: peluang = jumlah simulasi yang berhasil dibagi N.

### Konsep kuliah yang diterapkan

| Konsep | Penerapan |
| --- | --- |
| Distribusi Poisson | Model gol per laga |
| Variabel acak dan nilai ekspektasi | Poin dan posisi yang diharapkan |
| Monte Carlo dan Law of Large Numbers | Mesin simulasi dan grafik konvergensi |
| Estimasi proporsi dan interval kepercayaan | Peluang juara dengan CI Wilson 95% |
| Distribusi gabungan dan independensi | Matriks skor head-to-head |
| Uji hipotesis (Chi-square) | Menguji kecocokan gol dengan Poisson |
| Evaluasi probabilistik | Brier score 1X2 |

### Asumsi dan keterbatasan

- Gol tim dalam satu laga saling independen.
- Kekuatan tim dianggap tetap selama sisa musim (kecuali bobot form pada saat estimasi).
- Tidak memperhitungkan cedera, rotasi pemain, motivasi, atau faktor di luar data.
- Bracket knockout dari perempat final ke atas disederhanakan menjadi bracket standar.
- Brier score awal bersifat in-sample sehingga cenderung optimistis.

## 8. Desain antarmuka

- **Gaya:** terinspirasi situs resmi UCL: navbar atas dengan menu berbentuk pil, latar terang, kartu putih bersudut membulat, dan panel samping.
- **Warna dasar:** kuning (#FFB800 dan turunannya) dengan teks cokelat gelap (#1A1400) agar kontras terjaga. Teks kuning tidak dipakai di atas latar putih.
- **Implementasi:** tema Streamlit lewat `.streamlit/config.toml`, kartu hero dengan Tailwind CSS (CDN) lewat `components.html`, grafik dengan Plotly.
- **Navigasi:** navbar kuning selebar layar di atas halaman dengan menu Dashboard, Tabel, Simulator, Head-to-Head, Statistik, dan Metodologi. Tidak memakai sidebar bawaan Streamlit. Di layar sempit, menu dapat digeser ke samping.
- **Aset:** tanpa foto pemain dan logo resmi klub (hak cipta). Klub diwakili lingkaran singkatan atau gambar yang disediakan sendiri.
- **Referensi visual:** mockup desktop tersedia dan menjadi acuan tampilan.

## 9. Persyaratan non-fungsional

| Aspek | Target |
| --- | --- |
| Kinerja | 10.000 simulasi selesai di bawah 2 detik, 100.000 simulasi di bawah 20 detik pada laptop biasa |
| Reproduktibilitas | Seed dan parameter yang sama menghasilkan hasil identik |
| Keterbacaan | Kontras teks memadai, angka persen jelas, ketidakpastian selalu ditampilkan, dan tampilan menyesuaikan lebar layar |
| Transparansi | Semua asumsi dijelaskan di halaman Metodologi |
| Kemudahan jalan | Berjalan dengan `pip install -r requirements.txt` dan `streamlit run app.py` |
| Kualitas kode | Logika model dipisah dari tampilan (folder `core/`) agar mudah diuji |

## 10. Arsitektur dan tech stack

| Lapisan | Teknologi |
| --- | --- |
| Antarmuka | Streamlit, Tailwind CSS (via CDN), Plotly |
| Komputasi | Python, NumPy (simulasi tervektorisasi), pandas, SciPy |
| Data | File CSV lokal |

Struktur proyek:

- `app.py`: pintu masuk, tema, dan navigasi antarhalaman.
- `core/ratings.py`: estimasi kekuatan tim dan bobot form.
- `core/simulate.py`: mesin Monte Carlo dan bracket.
- `core/stats.py`: CI, konvergensi, Chi-square, Brier score, head-to-head.
- `data/matches.csv`: dataset laga.
- `.streamlit/config.toml`: tema kuning.
- `generate_sample_data.py`: pembuat data sintetis untuk uji coba.

* `views/`: satu file satu halaman (dashboard, tabel, simulator, head\_to\_head, statistik, metodologi).
* `ui/`: navbar, tema, komponen, dan template Tailwind di `ui/templates/`.
* `core/pipeline.py`: alur data, rating, dan simulasi tanpa kode Streamlit.
* `tests/`: uji untuk `core/` dan template.

## 11. Kriteria penerimaan

1. Jumlah peluang juara seluruh tim sama dengan 100%, jumlah peluang Top 8 sama dengan 8 tim, dan Top 24 sama dengan 24 tim.
2. Seed yang sama menghasilkan tabel hasil yang identik.
3. Grafik konvergensi menunjukkan pita CI yang menyempit seiring N bertambah.
4. Peluang menang, seri, dan kalah pada Head-to-Head berjumlah 100%.
5. Uji Chi-square menampilkan statistik, derajat bebas, dan p-value, disertai penjelasan hipotesis.
6. Semua halaman P0 berjalan tanpa error dengan dataset nyata milik pengguna.
7. Halaman Metodologi memuat rumus, asumsi, dan keterbatasan.

## 12. Risiko dan mitigasi

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| Dataset tidak lengkap atau nama tim tidak konsisten | Simulasi gagal atau bias | Validasi data saat dimuat dan tampilkan pesan error yang jelas |
| Kekuatan antarliga sulit dibandingkan | Rating tim lintas liga tidak adil | Gunakan laga UCL sebagai penghubung antarliga dan bobot liga domestik yang lebih kecil |
| Asumsi Poisson tidak sepenuhnya cocok | Prediksi kurang akurat | Uji Chi-square, dan pertimbangkan Dixon-Coles sebagai pengembangan |
| Brier score in-sample terlalu optimistis | Validasi terlihat lebih baik dari kenyataan | Tandai sebagai in-sample, lalu tambahkan backtest walk-forward (F-17) |
| Bracket knockout tidak persis sama dengan aturan resmi | Peluang babak akhir sedikit bergeser | Dokumentasikan sebagai penyederhanaan dan siapkan fungsi bracket yang mudah diubah |
| Hasil dianggap sebagai kepastian | Salah tafsir | Selalu tampilkan CI dan catatan bahwa angka adalah peluang, bukan jaminan |

## 13. Milestone yang disarankan

| Tahap | Pekerjaan | Hasil |
| --- | --- | --- |
| 1 | Menyiapkan dan membersihkan dataset, menyamakan nama tim | `matches.csv` valid |
| 2 | Estimasi rating dan simulasi league phase | Peluang Top 8 dan Top 24 |
| 3 | Simulasi knockout dan interval kepercayaan | Peluang juara dengan CI |
| 4 | Halaman Dashboard, Tabel, dan Head-to-Head | Aplikasi dapat dipakai |
| 5 | Halaman Statistik dan validasi model | Konvergensi, Chi-square, Brier score |
| 6 | Halaman Metodologi, pengujian, dan perapian tampilan | Siap dipresentasikan |
| 7 | (Opsional) Backtest walk-forward dan Dixon-Coles | Validasi lebih kuat |

## 14. Pertanyaan terbuka

- Musim dan rentang tanggal dataset mana yang dipakai sebagai acuan prediksi?
- Berapa bobot laga liga domestik yang paling masuk akal setelah dicoba pada data nyata?
- Apakah bracket knockout perlu disesuaikan persis dengan aturan resmi UEFA untuk presentasi?
- Apakah backtest walk-forward (F-17) akan dikerjakan atau cukup dicantumkan sebagai pengembangan lanjutan?

## 15. Kerja tim dan alur Git

Tiga anggota mengerjakan satu repository GitHub bernama SiKupingBesar. Pekerjaan dibagi per fitur lewat branch, dan tiap file hanya dimiliki satu orang agar tidak terjadi konflik saat digabung.

| Branch | File yang dimiliki | Isi pekerjaan |
| --- | --- | --- |
| feat/engine-simulasi | `core/ratings.py`, `core/simulate.py`, `core/pipeline.py`, `tests/` | Kualitas model, kalibrasi bobot, bracket knockout, validasi data nyata |
| feat/dashboard-tabel | `views/dashboard.py`, `views/tabel.py`, `views/simulator.py`, `ui/` | Tampilan Dashboard, Tabel, Simulator, navbar, dan template Tailwind |
| feat/h2h-statistik | `views/head_to_head.py`, `views/statistik.py`, `views/metodologi.py`, `core/stats.py` | Head-to-Head, konvergensi, Chi-square, Brier score, backtest, Metodologi |

Aturan kerja:

- `main` hanya berisi kode yang berjalan; perubahan masuk lewat Pull Request yang ditinjau satu anggota lain.
- File bersama (`app.py`, `ui/state.py`, `requirements.txt`, `.gitignore`, `README.md`) diubah lewat PR kecil tersendiri dan diumumkan ke tim.
- Jangan memindahkan atau mengganti nama file setelah branch dibuat, dan jangan memformat ulang seluruh file.
- Ambil perubahan terbaru dari `main` ke branch masing-masing minimal sekali sehari.
- Satu commit untuk satu langkah, dengan pesan seperti `feat: ...`, `fix: ...`, atau `docs: ...`.
- Dataset asli tidak di-commit jika lisensinya membatasi; sumber dan lisensi dicantumkan di README.

Pemilik tiap branch (nama anggota) diisi oleh tim.
