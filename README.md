Nama : Qanita Syafika

NPM : Qanita Syafika

Kelas : C

### Tugas 1

1. Ya, saya menggunakanelemen semantik HTML5 dalam merancang struktur website, seperti <header>, <nav>, <main>, <section>, dan <footer>

2. Tantangan utama yang saya temukan adalah mengatur layout yang di mode desktop tersusun berdampingan secara horizontal (seperti grid pada bagian Profile dan Cards) agar tidak terlihat sempit, bertumpuk saat dibuka di layar mobile. Dari itu syaa mengevaluasi dengan alur ketika beralih ke mobile, orientasi bacanya menjadi vertikal. Oleh karena itu, pada kode CSS, saya menambahkan Media Query (@media (max-width: 768px)) untuk mematahkan tata letak. Misalnya, .hero-grid yang awalnya dibagi dua kolom (1.4fr 1fr), saya ubah menjadi satu kolom (grid-template-columns: 1fr;) agar teks perkenalan dan foto menyesuaikan lebar layar penuh secara bergantian. Dan juga saya membuat header navigasi yang memanjang secara horizontal di desktop menjadi flex-direction: column dengan memberikan gap agar opsi menu bertumpuk rapi di tengah.

3. Batasan yang saya rasakaan karena ini static web adalah pada informasi yang sifatnya hardcoded(ditulis di dalam file HTML). Jika kedepannya saya harus update portofolio ini, artinya saya harus membuka source code dan mengeditnya manual. Saya merasa hal ini kurang efisien.
Fungsionalitas yang saya ingin tambahkan adalah melakukan Integrasi Database. dengan begini model database (contoh Django models) untuk menyimpan entri Experience, Awards, dan Projects. Dengan itu, konten bisa ditampilkan secara dinamis melalui mekanisme looping (seperti {% for project in projects %}) dan bisa di-update melalui halaman admin tanpa membuka dari awal kode HTML sehingga lebih efisien.

