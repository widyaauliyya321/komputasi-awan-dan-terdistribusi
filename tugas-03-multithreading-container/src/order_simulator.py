"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import threading
import random
import time
import os

NUM_ORDERS = 100        # jumlah pesanan simulasi yang masuk
NUM_WORKERS = 10        # jumlah thread pekerja

# Counter bersama untuk menghitung total pesanan yang berhasil diproses.
# Sengaja rawan race condition jika diakses tanpa proteksi.
processed_count = 0

# TODO 1: Buat objek Lock di sini untuk melindungi `processed_count`.
lock = threading.Lock()

# Sakelar mode: USE_LOCK=1 (default) pakai lock, USE_LOCK=0 tanpa lock
USE_LOCK = os.environ.get("USE_LOCK", "1") == "1"

def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasikan kerja nyata (mis. validasi, hitung total harga)
    time.sleep(random.uniform(0.001, 0.01))

    # TODO 2: Tambahkan increment `processed_count` DI SINI.
    if USE_LOCK: 
        with lock:
            temp = processed_count
            time.sleep(0.0001)
            processed_count = temp + 1
    else:
        temp = processed_count
        time.sleep(0.0001)            
        processed_count = temp + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 3: Bagi `order_ids` menjadi NUM_WORKERS bagian, buat satu
    # threading.Thread per bagian yang menjalankan `worker(...)`,
    # start semua thread, lalu join semua thread sebelum lanjut.
    threads = []
    for i in range(NUM_WORKERS) :
        bagian = order_ids[i::NUM_WORKERS] #tumpukan nota untuk pelayan ke-i
        t = threading.Thread(target=worker, args=(bagian,))
        threads.append(t)

    for t in threads: #semuanya mulai bersamaan
        t.start()

    for t in threads: #menunggu semuanya selesai
        t.join()

    print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")
    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!")


if __name__ == "__main__":
    main()
