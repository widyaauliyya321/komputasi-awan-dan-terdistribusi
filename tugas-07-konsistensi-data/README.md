# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).

### Hasil Analisis 1:
Menurut kelompok kami, penggunaan Eventual Consistency saja belum cukup untuk menangani data saldo e-wallet FoodGo. Kami memilih Sequential Consistency karena saldo pelanggan harus memiliki informasi yang konsisten di setiap server.

Pada kasus ini masalah yang terjadi adalah ketika pelanggan melakukan top-up melalui server Jakarta, tetapi beberapa detik kemudian saat melakukan pemesanan melalui server Bandung, saldo yang terbaca masih saldo lama. Hal ini terjadi karena perubahan saldo dari server Jakarta belum sampai ke server Bandung. Akibatnya, pelanggan bisa mengalami penolakan transaksi meskipun sebenarnya saldo mereka sudah mencukupi. Jika masalah seperti ini sering terjadi, pelanggan tentu bisa merasa dirugikan dan kehilangan kepercayaan terhadap layanan FoodGo.

Penggunaaan Sequential Consistency memastikan bahwa operasi dari seluruh proses terlihat seolah-olah dijalankan dalam satu urutan yang sama. Jadi, setiap server harus melihat urutan perubahan data yang konsisten. Berbeda dengan Sequential Consistency, Eventual Consistency masih memperbolehkan adanya perbedaan data antar-replika untuk sementara waktu. Data tersebut memang akan disamakan setelah proses sinkronisasi selesai, tetapi selama proses tersebut belum selesai, kemungkinan server membaca data lama masih bisa terjadi. Model ini lebih cocok untuk data yang tidak terlalu berpengaruh jika terlambat diperbarui, seperti jumlah like pada media sosial.

Kesimpulan: Menurut kelompok kami, Sequential Consistency lebih sesuai untuk pengelolaan saldo e-wallet FoodGo dibandingkan hanya menggunakan Eventual Consistency. Hal ini karena kesalahan informasi saldo bisa langsung memengaruhi transaksi pelanggan.

2. Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. *Read-Your-Writes*: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).

### Hasil Analisis 2:

Selain Sequential Consistency, FoodGo juga dapat menerapkan Client-Centric Consistency, khususnya Read-Your-Writes Consistency. Read-Your-Writes Consistency merupakan jaminan bahwa perubahan data yang dilakukan oleh seorang pengguna dapat dilihat kembali ketika pengguna tersebut melakukan pembacaan data berikutnya.

Pada studi kasus FoodGo, penerapannya dapat dilakukan dengan cara:
1. Pelanggan melakukan top-up saldo melalui server Jakarta.
2. Server Jakarta mencatat perubahan saldo dan memberikan identitas unik pada transaksi top-up tersebut.
3. Ketika pelanggan berpindah ke server Bandung untuk melakukan pemesanan, aplikasi membawa informasi mengenai perubahan saldo yang sebelumnya dilakukan.
4. Server Bandung memeriksa apakah perubahan saldo tersebut sudah diterima. Jika belum, server mengambil pembaruan terlebih dahulu sebelum menampilkan saldo pelanggan.
5. Setelah saldo terbaru berhasil diperoleh, pelanggan dapat melanjutkan proses pemesanan.
Dengan cara ini, pelanggan tidak perlu khawatir melihat saldo lama hanya karena berpindah server setelah melakukan top-up.

Namun, karena sistem ini berkaitan dengan uang, FoodGo tetap perlu memastikan bahwa proses pemotongan saldo berjalan dengan aman. Misalnya, sistem harus mencegah pemotongan saldo dua kali atau transaksi yang membuat saldo menjadi tidak sesuai. Hal ini karena Read-Your-Writes hanya menjamin perubahan pengguna terlihat pada pembacaan berikutnya, bukan menjamin seluruh proses transaksi keuangan berjalan aman secara otomatis.

3. Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.

'''mermaid
sequenceDiagram
    actor P as Pelanggan
    participant J as Server Jakarta
    participant R as Proses Replikasi
    participant B as Server Bandung

    Note over J,B: Saldo awal Rp50.000

    P->>J: Melakukan top-up Rp50.000
    J->>J: Update saldo menjadi Rp100.000
    J-->>P: Top-up berhasil

    J->>R: Mengirim perubahan saldo ke Bandung

    Note over R,B: Replikasi belum selesai

    P->>B: Memesan makanan Rp75.000
    B->>B: Membaca saldo pelanggan
    B->>B: Saldo terbaca Rp50.000
    B-->>P: Transaksi ditolak (saldo tidak cukup)

    R-->>B: Mengirim update saldo Rp100.000
    B->>B: Memperbarui saldo menjadi Rp100.000

    Note over P,B: Terjadi bug karena server Bandung membaca saldo lama


### Bagian 2 — Simulasi (opsional, nilai tambah)

Skeleton `src/replica_simulation.py` mensimulasikan dua replika (Jakarta & Bandung) dengan delay replikasi buatan. Lengkapi TODO untuk:
1. Menunjukkan kondisi **inconsistent read** (replika Bandung masih menunjukkan saldo lama walau Jakarta sudah update).
2. Mengimplementasikan mekanisme **Read-Your-Writes** sederhana (mis. dengan version/timestamp per client) yang memperbaiki masalah tersebut.

```bash
python3 src/replica_simulation.py
```

## Struktur Submission

```
tugas-07-konsistensi-data/
├── README.md      # Analisis konsistensi + sequence diagram Mermaid
├── JURNAL.md
├── src/            # (opsional) simulasi replikasi
└── bukti/          # (jika mengerjakan simulasi) output program
```

## Rubrik Penilaian (Tugas 7)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan model konsistensi | 30% | Argumen berbasis dampak bisnis nyata, bukan hafalan definisi |
| Kualitas sequence diagram | 30% | Menunjukkan jelas titik kegagalan & titik perbaikan |
| Usulan solusi client-centric | 25% | Solusi konkret dan dapat diimplementasikan (bukan wacana abstrak) |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history (+ bonus jika simulasi dikerjakan) |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistency model ke AI untuk brainstorming; **tidak boleh** meminta AI menuliskan analisis akhir/sequence diagram atau isi `# TODO` di `src/replica_simulation.py` yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Sebagai bukti pemahaman konsep (bukan hafalan jawaban skenario FoodGo saja), `README.md` wajib menyertakan **satu skenario tambahan** yang kalian buat sendiri (mis. kasus lain di aplikasi ojek online) dan menentukan model konsistensi yang tepat untuk skenario tambahan tersebut.
