# Cyberlab — Evaluasi Respons Server

## Tujuan
Membandingkan server HTTPServer dan ThreadingHTTPServer
pada lab lokal 127.0.0.1:8081.

## Metode
- 20 request HTTP
- Maksimal 3 worker
- Timeout klien 3 detik
- Target hanya localhost

## Hasil sebelum perubahan
- HTTP 200: 20/20
- Total waktu: 0.141 detik
- Rata-rata respons: 18.01 ms
- Respons terlama: 71.84 ms

## Hasil sesudah perubahan
- HTTP 200: 20/20
- Total waktu: 0.083 detik
- Rata-rata respons: 10.74 ms
- Respons terlama: 46.02 ms

## Interpretasi
Pada pengujian terbatas ini, total waktu turun sekitar 41.1%.
Hasil awal menjanjikan, tetapi pengujian berulang diperlukan.
Ini bukan bukti bahwa server tahan terhadap semua serangan DoS.

## Pengujian Rate Limiting
- Batas: 30 request per 10 detik per alamat klien
- Total request: 35
- HTTP 200: 30
- HTTP 429: 5
- Hasil: rate limiter menolak request setelah batas tercapai

## Keterbatasan
Pengujian hanya dilakukan pada localhost dan satu alamat klien.
Hasil ini membuktikan perilaku rate limiter pada skenario uji,
bukan ketahanan terhadap seluruh jenis DoS atau DDoS.

## Pengujian Validasi dan Output
- Input normal: HTTP 200
- Input 101 karakter: HTTP 400
- Payload HTML <script>: output di-escape menjadi teks
- Hasil: ketiga pemeriksaan berperilaku sesuai rancangan

## Ringkasan
Lab menunjukkan implementasi dan pengujian:
1. Penanganan koneksi dengan ThreadingHTTPServer
2. Pembatasan request sederhana per alamat klien
3. Validasi panjang input
4. Escaping output HTML
5. Pengukuran performa sebelum dan sesudah perubahan

## Batasan
- Seluruh pengujian dilakukan pada localhost.
- Sampel beban kecil tidak membuktikan ketahanan terhadap DoS/DDoS.
- Rate limiter dalam memori bukan kontrol produksi yang lengkap.
- Pengujian XSS terbatas pada payload dan konteks yang diperiksa.
