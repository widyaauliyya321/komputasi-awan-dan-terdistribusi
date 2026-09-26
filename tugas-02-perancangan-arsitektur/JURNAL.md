# Jurnal Proses — Tugas 2

## 25 September 2026
- Opsi arsitektur yang dipertimbangkan:
Sebelum menetapkan pilihan akhir, kelompok mendiskusikan tiga opsi:
1. Layered Architecture — mempertahankan struktur berlapis (presentation, business logic, data) tapi tetap dalam satu aplikasi. Dipertimbangkan karena paling sederhana untuk diimplementasikan, tapi ditolak karena tidak menyelesaikan akar masalah dari Tugas 1: semua modul tetap saling terikat dalam satu proses, sehingga Single Point of Failure dan cascading delay (pesanan menunggu pembayaran) tidak hilang.
2. Peer-to-Peer (P2P) — modul saling berkomunikasi langsung tanpa perantara pusat. Dipertimbangkan untuk skenario desentralisasi penuh, tapi ditolak karena kebutuhan FoodGo bukan menghilangkan otoritas pusat (data pesanan/pembayaran tetap perlu konsisten dan mudah diaudit), dan P2P justru menambah kompleksitas koordinasi tanpa manfaat nyata untuk kasus ini.
3. SOA dikombinasikan dengan Publish-Subscribe, memisahkan modul jadi service independen (SOA) untuk proses yang butuh jawaban langsung, dan memakai event asinkron (Pub-Sub) untuk proses yang tidak butuh jawaban seketika. Opsi ini dipilih karena paling langsung menjawab tiga pitfall yang ditemukan di Tugas 1.
   
- Kenapa akhirnya pilih [SOA/Pub-Sub]:
  Kombinasi ini dipilih karena masalah di Tugas 1 punya dua sifat berbeda dan membutuhkan solusi yang berbeda pula:
  1. Untuk Single Point of Failure, solusinya adalah memisahkan modul jadi service mandiri yang bisa berjalan dan di-deploy sendiri-sendiri → ini yang disediakan SOA.
  2. Untuk "network is reliable" dan "latency is zero", sebagian proses (Pesanan↔Pembayaran) memang butuh jawaban sinkron dan tetap diberi timeout/retry/circuit breaker, tapi proses lain (notifikasi, penugasan kurir, update katalog) sebenarnya tidak perlu menunggu hasil dari modul lain secara langsung → ini yang disediakan Pub-Sub, karena mengubah ketergantungan "menunggu jawaban" menjadi "menerima kabar kalau sudah selesai".

Memilih salah satu dari itu dianggap tidak cukup karen jika SOA saja tidak otomatis menghilangkan masalah latency kalau semua komunikasi antar-service tetap sinkron, sedangkan Pub-Sub saja tidak cocok untuk proses seperti konfirmasi pembayaran yang memang butuh jawaban seketika sebelum pelanggan bisa lanjut checkout.

- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa):
Versi 1 hanya melabeli komunikasi sebagai "Sinkron" tanpa detail penanganan kegagalan, dan hanya punya event sukses (PaymentSuccess) tanpa jalur gagal.
Perubahan di versi 2:
1. Panah OrderSvc → PaymentSvc ditambah detail timeout 5s, retry maks 2x backoff, circuit breaker — supaya klaim bahwa pitfall "network is reliable"/"latency is zero" sudah ditangani punya bukti di diagram, tidak hanya di teks.
2. Ditambah event PaymentFailed selain PaymentSuccess agar ada jalur eksplisit saat pembayaran gagal, sejalan dengan retry/circuit breaker yang baru ditambahkan.
3. Label panah Gateway diperjelas (Sinkron: ambil menu, Sinkron: buat pesanan) dan node Resto diberi keterangan perannya sebagai subscriber (siapkan pesanan) — supaya diagram lebih menjelaskan apa yang terjadi, bukan cuma jenis komunikasinya. 

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 22-09-2026 | ChatGPT | Meminta penjelasan mengenai materi Distributed Systems – Architectures dan konsep arsitektur yang relevan untuk kasus FoodGo. | Menjelaskan beberapa architectural style, termasuk SOA dan Publish-Subscribe, serta karakteristik komunikasi antar-komponen. | Digunakan untuk memahami materi dan menentukan konsep arsitektur yang relevan dengan permasalahan FoodGo. |
| 22-09-2026 | ChatGPT | Meminta penjelasan mengenai cara merancang diagram arsitektur berdasarkan komponen dan pola komunikasi pada sistem yang dirancang. | Memberikan penjelasan mengenai struktur diagram, hubungan antar-service, serta alur komunikasi dalam arsitektur. | sebagai dasar pemahaman, kemudian struktur diagram disesuaikan dengan kebutuhan dan rancangan sistem FoodGo. |
| 22-09-2026 | ChatGPT | Meminta penjelasan mengenai penerapan sintaks Mermaid untuk merepresentasikan arsitektur SOA dan pola komunikasi Publish-Subscribe. | Menjelaskan penggunaan Mermaid untuk menggambarkan service, message broker, serta komunikasi sinkron dan asinkron. | Sintaks dipelajari dan kemudian disesuaikan kembali dengan komponen serta alur komunikasi yang digunakan dalam tugas. |
| 24-09-2026 | ChatGPT | Meminta pemeriksaan terhadap komponen dan komunikasi dalam rancangan FoodGo seperti Order, Payment, Restaurant, Courier, Notification, API Gateway, dan Message Broker. | Memberikan masukan mengenai pembagian fungsi komponen dan membedakan komunikasi request-response dengan komunikasi berbasis event. | Digunakan untuk memperjelas rancangan dan memperbaiki pembagian fungsi antar-komponen. |
| 25-09-2026 | ChatGPT | Meminta analisis mengenai trade-off dari penggunaan SOA dan Publish-Subscribe pada FoodGo. | Mengidentifikasi konsekuensi seperti kompleksitas debugging, monitoring, Message Broker, dan konsistensi data. | Poin tersebut digunakan sebagai bahan diskusi kelompok dan disesuaikan kembali dengan kondisi sistem FoodGo. | 
