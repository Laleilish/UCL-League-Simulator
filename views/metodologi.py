"""Methodology: formulas, assumptions, and limitations, written for assessment."""

from __future__ import annotations

import streamlit as st

from ui.components import note, section_header


def render() -> None:
    section_header(
        "Metodologi",
        "Transparansi model",
        "Semua rumus, asumsi, dan keterbatasan yang dipakai SiKupingBesar.",
    )

    st.markdown(
        """
SiKupingBesar memprediksi peluang juara Liga Champions dengan **simulasi Monte
Carlo**. Kekuatan menyerang dan bertahan tiap tim diestimasi dari hasil laga
liga domestik dan UCL, lalu sisa musim dimainkan ribuan kali dengan jumlah gol
yang dibangkitkan dari distribusi Poisson.
        """
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Model gol")
        st.markdown(
            "Jumlah gol tiap tim dalam satu laga dimodelkan sebagai variabel acak "
            "Poisson:"
        )
        st.latex(r"G_{home} \sim \mathrm{Poisson}(\lambda_{home}), \quad " r"G_{away} \sim \mathrm{Poisson}(\lambda_{away})")
        st.latex(
            r"\lambda_{home} = \mu \cdot H \cdot a_{home} \cdot d_{away}"
        )
        st.latex(
            r"\lambda_{away} = \mu \cdot a_{away} \cdot d_{home}"
        )
        st.markdown(
            r"""
- $\mu$ adalah rata-rata gol dasar per tim per laga.
- $H$ adalah home advantage.
- $a_i$ adalah kekuatan menyerang tim $i$.
- $d_i$ adalah kelemahan bertahan tim $i$; nilai lebih besar berarti pertahanan lebih lemah.
            """
        )
    with right:
        st.subheader("Estimasi parameter")
        st.markdown(
            "Parameter diestimasi dengan iterasi maximum likelihood berbobot. "
            "Bobot tiap laga menurun secara eksponensial dan dibedakan menurut "
            "kompetisi:"
        )
        st.latex(
            r"w_i = 0{,}5^{\,\text{umur}_i / \text{half-life}} \times "
            r"\begin{cases} 1 & \text{UCL} \\ w_{dom} & \text{liga domestik} \end{cases}"
        )
        st.markdown(
            "Shrinkage ke nilai 1 menjaga rating tetap stabil ketika sebuah tim "
            "hanya punya sedikit laga:"
        )
        st.latex(
            r"\hat{a}_i = \frac{\sum_j w_j g_{ij} + k}"
            r"{\sum_j w_j \lambda_{ij} + k}"
        )
        st.markdown(
            "Rumus yang sama dipakai untuk $\\hat{d}_i$. Nilai $k$ adalah "
            "kekuatan shrinkage yang dapat diatur di halaman Simulator."
        )

    st.subheader("Alur simulasi Monte Carlo")
    st.markdown(
        """
1. Hitung poin, selisih gol, dan gol dari laga UCL yang sudah dimainkan.
2. Untuk setiap laga sisa, bangkitkan gol kandang dan tandang dari Poisson
   sebanyak $N$ simulasi tervektorisasi.
3. Urutkan klasemen tiap simulasi memakai **poin, selisih gol, gol, lalu
   undian acak**.
4. Peringkat 1–8 langsung ke 16 besar. Peringkat 9–24 bermain playoff dua leg
   dengan pasangan 9–24, 10–23, dan seterusnya.
5. Simulasikan 16 besar, perempat final, dan semifinal dua leg. Jika agregat
   imbang, pemenang ditentukan 50:50 untuk mewakili perpanjangan waktu dan
   penalti. Final dimainkan satu laga di tempat netral.
6. Peluang tiap tahap = jumlah simulasi yang berhasil mencapai tahap itu
   dibagi $N$.
        """
    )

    st.subheader("Interval kepercayaan dan validasi")
    col_ci, col_chi, col_brier = st.columns(3)
    with col_ci:
        st.markdown("**Wilson 95%** untuk peluang juara:")
        st.latex(
            r"\frac{\hat{p} + \frac{z^2}{2n} \pm "
            r"z\sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}"
            r"{1 + \frac{z^2}{n}}"
        )
    with col_chi:
        st.markdown("**Uji Chi-square** kecocokan gol dengan Poisson:")
        st.latex(
            r"\chi^2 = \sum_{k} \frac{(O_k - E_k)^2}{E_k}"
        )
        st.caption("Derajat bebas = jumlah bin − 1 − 1 parameter μ.")
    with col_brier:
        st.markdown("**Brier score** 1X2 (semakin kecil semakin baik):")
        st.latex(
            r"BS = \frac{1}{N}\sum_{i=1}^{N}\sum_{k=1}^{3}(p_{ik} - o_{ik})^2"
        )
        st.caption("Nilai acuan seragam adalah 0,667.")

    st.subheader("Konsep mata kuliah yang diterapkan")
    st.markdown(
        """
| Konsep | Penerapan di aplikasi |
| --- | --- |
| Distribusi Poisson | Model jumlah gol tiap tim per laga |
| Variabel acak dan nilai ekspektasi | Rata-rata poin dan posisi hasil simulasi |
| Monte Carlo dan Law of Large Numbers | Mesin simulasi dan grafik konvergensi |
| Estimasi proporsi dan interval kepercayaan | Peluang juara dengan CI Wilson 95% |
| Distribusi gabungan dan independensi | Matriks skor Head-to-Head |
| Uji hipotesis (Chi-square) | Menguji kecocokan gol dengan Poisson |
| Evaluasi probabilistik | Brier score 1X2 |
        """
    )

    st.subheader("Asumsi")
    st.markdown(
        """
- Gol kedua tim dalam satu laga saling independen.
- Kekuatan tim dianggap tetap selama sisa musim; hanya bobot form saat
  estimasi yang berubah.
- Laga yang lebih lama diberi bobot lebih kecil, dan laga UCL lebih berat
  daripada liga domestik.
- Playoff, 16 besar, perempat final, dan semifinal disederhanakan menjadi
  bracket dua leg standar.
- Jika agregat knockout imbang, peluang lolos dibagi 50:50.
- Final dianggap dimainkan di tempat netral tanpa home advantage.
        """
    )

    st.subheader("Keterbatasan")
    st.markdown(
        """
- Tidak ada data cedera, skorsing, transfer, rotasi pemain, atau motivasi.
- Kekuatan antarliga hanya dihubungkan oleh laga UCL, sehingga tim dengan
  sedikit laga UCL memiliki rating yang lebih tidak pasti.
- Asumsi Poisson tidak selalu cocok untuk sepak bola; uji Chi-square
  ditampilkan agar penyimpangan terlihat.
- Brier score bersifat **in-sample**, jadi cenderung optimistis. Backtest
  walk-forward per matchday adalah pengembangan lanjutan.
- Bracket knockout tidak persis sama dengan aturan seeding resmi UEFA.
- Angka adalah peluang, bukan jaminan hasil.
        """
    )

    st.subheader("Reproduksibilitas dan data")
    st.markdown(
        """
Simulasi memakai `numpy.random.default_rng(seed)`. Seed dan parameter yang sama
menghasilkan tabel identik. Data dibaca dari CSV dengan kolom `date`, `home`,
`away`, `home_goals`, `away_goals`, dan `competition`; dataset harus memuat
tepat 36 tim UCL. Dataset bawaan menggabungkan 11 liga domestik 2026/27
(1.048 laga), **189 laga UCL 2025/26** sebagai histori rating, dan **144 jadwal
UCL 2026/27** untuk 36 klub baru. Hasil UCL 2025/26 dipakai untuk menghubungkan
kekuatan antarliga; seluruh laga UCL 2026/27 belum dimainkan, sehingga prediksi
bersifat pra-turnamen. Lima klub (LASK, Sabah, Shakhtar Donetsk, Slovan
Bratislava, Viking) tidak punya data domestik maupun histori UCL, jadi
ratingnya tetap di nilai awal 1 dan sangat tidak pasti. Dataset dibangun ulang
dengan `build_dataset.py` dari file di folder `data/`.
        """
    )
    note(
        "Model dipisahkan dari tampilan di folder core/ agar bisa diuji tanpa "
        "Streamlit. Semua pengaturan dapat diubah di halaman Simulator dan "
        "langsung dipakai oleh halaman lain."
    )
