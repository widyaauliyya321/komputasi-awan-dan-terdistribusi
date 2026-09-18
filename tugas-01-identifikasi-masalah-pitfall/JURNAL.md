# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## 16 September 2026
- Peserta: Ni Putu Widya Auliya Pratama, Zafri Ahmad Fahriza, Abied Zilachuzzulfiq
- Poin diskusi:
  1. Membaca dan memahami studi kasus FoodGo dan masalah apa saja yang terjadi pada sistem antar-pesan tsb terutama saat jumlah pesanan meningkat.
  2. Membahas apa yang dimaksud dengan Faallacies of Distributed Computing dan mencari bagian  skenario yang merupakan pitfall.
  3. Di awal kami menemukan pitfall yang paling jelas adalah The Network is Reliable, karena pada skenario ada kode network is always reliable, no need for retry.
  4. Selain itu, kami juga menemukan masalah tidak adanya timeout ketika modul pesanan menunggu respons dari modul pembayaran.
  5. Terakhir membahas dampak apa yang terjadi ke FoodGo jika terjadi request secara terus menerus, terutama ketika jumlah pesanan meningkat. Serta menentukan bagaimana solusi awal yang bisa diterapkan dan apa resiko/trade off yang terjadi jika solusi tsb diterapkan.
- Perbedaan pendapat (jika ada):
  1. Sebenarnya kami agak bingung apakah tidak terjadi timeout termasuk The Network is Reliable atau The Latency is Zero. Kemudian kami menarik kesimpulan, bahwa The Network is Reliable adalah asumsi bahwa jaringan selalu dapat berjalan dengan baik, sedangkan The Laatency is Zero adalah asumsi bahwa proses komunikasi tidak mengalami keterlambatan.

## 17 September 2026
- Peserta: Ni Putu Widya Auliya Pratama, Zafri Ahmad Fahriza, Abied Zilachuzzulfiq
- Poin diskusi:
  1. Disini kami membahas masalah Single Point of Failure karena semua modul FoodGo masih berjalan pada satu server dan juga satu proses monolitik. Disini kami menyimpulkan bahwa jika server tsb mengalami masalah atau crash, maka modul pesanan, pembayaran juga akan terganggu.
- Perubahan Pikiran:
  1. Awalnya kami berfokus pada pitfall yang ada pada daftar, tapi setelah membaca lagi, kami menyadari bahwa masalah satu server yang menangani semua modul juga bisa dibahas sebagai Single Point of Failure karena arsitektur monolotik.

## Review Silang
- Ni Putu Widya Auliya Pratama mengomentari analisis Zafri Ahmad Fahriza: bagian The Latency is Zero sudah sesuai dengan kondisi FoodGo, tapi dampak request yang menunggu mungkin perlu dijelaskan lebih lanjut.
- Zafri Ahmad Fahriza mengomentari analisis Abied Ziachuzzulfiq: pemisahan modul dapat membantu mengurangi ketergantungan pada satu server, tapi juga membuat sistem lebih kompleks oleh karena itu perlu sehingga hal itu juga perlu dipertimbangkan.
- Abied Ziachuzzulfiq mengomentari analisis Ni Putu Widya Auliya Pratama: solusi retry yang diberikan perlu disertai batas percobaan dan jeda agar tidak semakin membebani layanan yang sedang bermasalah.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ChatGPT | Bantu saya memahami pitfall The network is reliable pada sistem terdistribusi lalu berikan ide solusi dan trade-off nya untuk aplikasi pesan-antar makanan | AI menjelaskan bahwa request jaringan bisa gagal atau hilang, menyarankan konsep timeout, retry dengan backoff, dan circuit breaker | Ide dari AI ditulis ulang menggunakan bahasa sendiri dan dihubungkan langsung dengan skenario modul pesanan FoodGo yang menunggu modul pembayaran |
| ... | ChatGPT | Bantu saya memahami pitfall The network is reliable pada sistem terdistribusi lalu berikan ide solusi dan trade-off nya untuk aplikasi pesan-antar makanan | AI menjelaskan bahwa request jaringan bisa gagal atau hilang, menyarankan konsep timeout, retry dengan backoff, dan circuit breaker | Ide dari AI ditulis ulang menggunakan bahasa sendiri dan dihubungkan langsung dengan skenario modul pesanan FoodGo yang menunggu modul pembayaran |
