// Menyimpan reference timer untuk animasi dan auto-hide
let toastTimer;

// Fungsi global untuk menampilkan notifikasi toast
function showToast(title, message, type = 'normal', duration = 3000) {
  const toastComponent = document.getElementById('toast-component');
  const toastTitle = document.getElementById('toast-title');
  const toastMessage = document.getElementById('toast-message');

  if (!toastComponent) return;

  // Bersihkan variasi gaya border sebelumnya
  toastComponent.classList.remove('toast-success', 'toast-error', 'toast-normal');

  // Pasang class sesuai tipe notifikasi
  if (type === 'success') {
    toastComponent.classList.add('toast-success');
  } else if (type === 'error') {
    toastComponent.classList.add('toast-error');
  } else {
    toastComponent.classList.add('toast-normal');
  }

  // Update teks judul dan isi pesan
  toastTitle.textContent = title;
  toastMessage.textContent = message;

  // Hentikan timer sebelumnya jika toast dipanggil berturut-turut
  clearTimeout(toastTimer);

  // Tampilkan popover ke top layer browser dan pemicu transisi
  if (!toastComponent.matches(':popover-open')) {
    toastComponent.showPopover();
    void toastComponent.offsetHeight; // Paksa re-flow browser agar animasi berjalan
  }
  
  toastComponent.classList.remove('toast-hidden');
  toastComponent.classList.add('toast-show');

  // Atur waktu otomatis menghilang
  toastTimer = setTimeout(() => {
    toastComponent.classList.remove('toast-show');
    toastComponent.classList.add('toast-hidden');
    toastTimer = setTimeout(() => toastComponent.hidePopover(), 300);
  }, duration);
}