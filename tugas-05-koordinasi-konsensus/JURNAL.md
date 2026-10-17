# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4:
  - TODO 1: Awalnya bingung membedakan fungsi pesan ELECTION, OK, dan COORDINATOR, kapan setiap pesan harus dikirim, dan bagaimana memperbarui informasi leader.
  - TODO 2: Terkendala dalam menentukan cara menangani respons dari node lain selama pemiliihan leader, terutama ketika node menerima pesan ELECTION dan perlu memberikan balasan OK.
  - TODO 3: Mengalami kesulitan saat mengatur pengiriman pesan COORDINATOR agar informasi leader baru dapat diterima oleh node lainnya.
  - TODO 4: Kesulitan menentukan proses pengecekan kondisi leader dan kapan harus memilih leader baru jika leader sebelumnya berhenti berjalan.
  - Kendala saat menjalankan program: Perintah python3 yang terdapat pada instruksi tidak dapat dijalankan, dan akhirnya menggunakan perintah python.

## Skenario 1: Start normal
- Leader yang terpilih: Node 5 (port 5005)
- Log/observasi:
  1. Kelima node berhasil dijalankan pada terminal masing-masing
  2. Setiap node menampilkan pesan Listening sesuai port yang digunakan
  3. Node 5 terpilih sebagai leader karena memiliki ID tertinggi
  4. Node 5 mengirimkan pesan COORDINATOR kepada Node 1, 2, 3, 4
  5. Node lain menerima informasi bahwa Node 5 merupakan leader baru

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4 (port 5004)
- Berapa lama waktu sampai leader baru terdeteksi: 10 detik
- Log/observasi:
  1. Node 5 sebagai leader awal dihentikan menggunakan Ctrl + C
  2. Node lain mendeteksi bahwa Node 5 tidak lagi aktif
  3. Terminal menampilkan pesan 'Leader 5 mati!'
  4. Node 4 terpilih menjadi leader baru karena memiliki ID tertinggi diantara node yang masih aktif
  5. Node mengirimkan pesan COORDINATOR kepada Node 1, 2, 3
  6. Node lain menerima informasi bahwa Node 4 merupakan leader baru

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
