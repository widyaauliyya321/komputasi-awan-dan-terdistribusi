# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:

Berdasarkan kasus FoodGo, kelompok kami mempertimbangkan masalah perbedaan saldo antara server Jakarta dan Bandung. Ketika pelanggan melakukan top-up melalui server Jakarta, perubahan saldo tersebut belum tentu langsung diterima oleh server Bandung. Akibatnya, saat pelanggan melakukan pemesanan, server Bandung masih menampilkan saldo sebelumnya sehingga transaksi bisa ditolak.

Menurut kelompok kami, hal ini cukup serius karena saldo e-wallet berhubungan langsung dengan uang pelanggan. Berbeda dengan data seperti jumlah like di media sosial, keterlambatan pembaruan saldo dapat menyebabkan pelanggan tidak bisa melakukan transaksi meskipun memiliki saldo yang cukup.

Kami juga mempertimbangkan penggunaan Client-Centric Consistency, khususnya Read-Your-Writes Consistency. Dengan pendekatan ini, perubahan yang dilakukan pelanggan sebelumnya tetap bisa terlihat ketika pelanggan mengakses server yang berbeda. Jadi, pelanggan bisa mendapatkan informasi saldo terbaru setelah melakukan top-up.

- Kesimpulan akhir & alasan:

Setelah mempertimbangkan beberapa model konsistensi, kelompok kami menyimpulkan bahwa Eventual Consistency saja belum cukup untuk digunakan pada pengelolaan saldo e-wallet FoodGo. Kami memilih penggunaan Sequential Consistency karena setiap replika perlu melihat urutan operasi yang sama agar perubahan saldo tidak diproses secara berbeda.

Selain itu, FoodGo dapat menerapkan Read-Your-Writes Consistency sebagai pendekatan tambahan agar pelanggan tetap dapat melihat perubahan saldo yang baru saja dilakukan meskipun berpindah server. Dengan penerapan tersebut, diharapkan masalah penolakan transaksi akibat pembacaan saldo lama dapat dikurangi dan informasi saldo pelanggan menjadi lebih konsisten.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 12 November 2026 | ChatGPT | Membantu memahami studi kasus konsistensi data pada sistem e-wallet FoodGo. | AI menjelaskan perbedaan Eventual Consistency, Sequential Consistency, dan Read-Your-Writes serta memberikan gambaran solusi untuk masalah saldo yang belum tersinkronisasi. | Penjelasan digunakan sebagai bahan pemahaman. Saya perlu memeriksa kembali konsep dan menyusun analisis dengan pemahaman sendiri. |
| 13 November 2026 | ChatGPT | Membantu membuat simulasi replikasi data dan penerapan Read-Your-Writes menggunakan Python. | AI memberikan contoh alur dan kode simulasi untuk menunjukkan pembacaan data yang belum diperbarui serta proses menunggu replikasi. | Kode perlu diperiksa, dipahami, diuji, dan disesuaikan sendiri. |
| 13 November 2026 | ChatGPT | Membantu menyusun log hasil simulasi untuk README.md. | AI membantu merapikan keluaran terminal menjadi bagian dokumentasi skenario tanpa dan dengan Read-Your-Writes. | Dokumentasi perlu dicocokkan dengan hasil program yang benar-benar dijalankan. |
