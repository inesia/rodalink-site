// Set dynamic year in footer copyright
const yearElement = document.querySelector('#year');
if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

// Sticky Header Scroll Effect
const siteHeader = document.querySelector('.site-header');
if (siteHeader) {
  const onScroll = () => {
    if (window.scrollY > 15) {
      siteHeader.classList.add('is-scrolled');
    } else {
      siteHeader.classList.remove('is-scrolled');
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// PWA Service Worker Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    const swPath = window.location.pathname.includes('/produk/') ? '../sw.js' : 'sw.js';
    navigator.serviceWorker.register(swPath)
      .then((reg) => console.log('RodaLinks PWA Service Worker registered:', reg.scope))
      .catch((err) => console.log('RodaLinks PWA Service Worker registration failed:', err));
  });
}

// PWA Install Prompt Handling
let deferredInstallPrompt = null;
const installBanner = document.querySelector('#pwa-install-banner');
const installBtn = document.querySelector('#pwa-install-btn');
const installClose = document.querySelector('#pwa-install-close');

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredInstallPrompt = e;
  if (installBanner && !localStorage.getItem('pwa_banner_dismissed')) {
    setTimeout(() => {
      installBanner.classList.add('show');
    }, 2500);
  }
});

if (installBtn) {
  installBtn.addEventListener('click', async () => {
    if (deferredInstallPrompt) {
      if (installBanner) installBanner.classList.remove('show');
      deferredInstallPrompt.prompt();
      const { outcome } = await deferredInstallPrompt.userChoice;
      console.log('PWA Install choice:', outcome);
      deferredInstallPrompt = null;
    }
  });
}

if (installClose && installBanner) {
  installClose.addEventListener('click', () => {
    installBanner.classList.remove('show');
    localStorage.setItem('pwa_banner_dismissed', 'true');
  });
}

// Mobile navigation toggle functionality
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
  });

  nav.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Buka menu');
    });
  });
}

// Dana Syariah Lead Generation Form (Forwarded directly to WhatsApp for PIC BAF calculation)
const syariahForm = document.querySelector('#syariah-lead-form');
if (syariahForm) {
  const tabMotor = syariahForm.querySelector('#tab-motor');
  const tabMobil = syariahForm.querySelector('#tab-mobil');
  const inputNama = syariahForm.querySelector('#lead-nama');
  const inputPhone = syariahForm.querySelector('#lead-phone');
  const inputTipe = syariahForm.querySelector('#lead-tipe');
  const inputTahun = syariahForm.querySelector('#lead-tahun');
  const inputDana = syariahForm.querySelector('#lead-dana');

  let selectedVehicle = 'BPKB Motor';

  if (tabMotor && tabMobil) {
    tabMotor.addEventListener('click', () => {
      tabMotor.classList.add('active');
      tabMotor.setAttribute('aria-selected', 'true');
      tabMobil.classList.remove('active');
      tabMobil.setAttribute('aria-selected', 'false');
      selectedVehicle = 'BPKB Motor';
      if (inputTipe && (!inputTipe.value || inputTipe.placeholder.includes('Avanza'))) {
        inputTipe.placeholder = 'Contoh: Honda Beat / NMAX';
      }
    });

    tabMobil.addEventListener('click', () => {
      tabMobil.classList.add('active');
      tabMobil.setAttribute('aria-selected', 'true');
      tabMotor.classList.remove('active');
      tabMotor.setAttribute('aria-selected', 'false');
      selectedVehicle = 'BPKB Mobil';
      if (inputTipe && (!inputTipe.value || inputTipe.placeholder.includes('Beat'))) {
        inputTipe.placeholder = 'Contoh: Toyota Avanza / Honda Brio';
      }
    });
  }

  syariahForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const nama = inputNama ? inputNama.value.trim() : '';
    const phone = inputPhone ? inputPhone.value.trim() : '';
    const tipe = inputTipe ? inputTipe.value.trim() : '';
    const tahun = inputTahun ? inputTahun.value.trim() : '';
    const dana = inputDana ? inputDana.value.trim() : '';

    if (!nama) {
      alert('Mohon isi nama lengkap Anda.');
      inputNama?.focus();
      return;
    }
    if (!phone || phone.length < 8) {
      alert('Mohon isi nomor WhatsApp yang valid.');
      inputPhone?.focus();
      return;
    }
    if (!tipe) {
      alert('Mohon isi merk & tipe kendaraan.');
      inputTipe?.focus();
      return;
    }
    if (!tahun) {
      alert('Mohon isi tahun kendaraan.');
      inputTahun?.focus();
      return;
    }

    let msg = `Halo RodaLinks, saya ingin mengajukan perhitungan simulasi BAF Dana Syariah (Gadai BPKB):\n\n`;
    msg += `👤 *Nama Lengkap:* ${nama}\n`;
    msg += `📱 *No. HP/WA:* ${phone}\n`;
    msg += `🛵/🚗 *Jenis Jaminan:* ${selectedVehicle} (${tipe})\n`;
    msg += `📅 *Tahun Kendaraan:* ${tahun}\n`;
    if (dana) {
      msg += `💰 *Estimasi Kebutuhan Dana:* ${dana}\n`;
    }
    msg += `\nMohon bantu diteruskan ke PIC BAF Syariah Bogor untuk dihitung estimasi nilai pencairan dan simulasi angsurannya. Terima kasih!`;

    const waUrl = `https://wa.me/6285110539167?text=${encodeURIComponent(msg)}`;
    window.open(waUrl, '_blank');
  });
}

// WhatsApp Smart Popup Widget Logic (Non-intrusive timing & session handling)
(() => {
  const widget = document.querySelector('#wa-widget');
  if (!widget) return;

  const launcher = widget.querySelector('#wa-launcher');
  const badge = widget.querySelector('#wa-badge');
  const teaser = widget.querySelector('#wa-teaser');
  const teaserClose = widget.querySelector('#wa-teaser-close');
  const teaserTrigger = widget.querySelector('#wa-teaser-trigger');
  const card = widget.querySelector('#wa-card');
  const cardClose = widget.querySelector('#wa-card-close');
  const directChat = widget.querySelector('#wa-direct-chat');

  const STORAGE_DISMISSED = 'rodalinks_wa_dismissed';
  const STORAGE_OPENED = 'rodalinks_wa_opened';

  // Context-aware message prefill if on product detail page
  const productDetail = document.querySelector('.product-detail');
  if (productDetail && directChat) {
    const prodName = productDetail.dataset.productName || 'motor Yamaha';
    const msg = `Halo RodaLinks, saya sedang melihat Yamaha ${prodName} di website. Ingin konsultasi harga OTR Bogor, promo, dan ketersediaan unitnya.`;
    directChat.href = `https://wa.me/6285110539167?text=${encodeURIComponent(msg)}`;
  }

  let isDismissed = false;
  let isOpened = false;
  try {
    isDismissed = sessionStorage.getItem(STORAGE_DISMISSED) === 'true';
    isOpened = sessionStorage.getItem(STORAGE_OPENED) === 'true';
  } catch (err) {
    isDismissed = false;
    isOpened = false;
  }

  let teaserTimer = null;
  let autoHideTeaserTimer = null;
  let scrollListenerAttached = false;

  const onScroll = () => {
    const scrollY = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (docHeight > 0 && (scrollY / docHeight) > 0.35) {
      if (scrollListenerAttached) {
        window.removeEventListener('scroll', onScroll);
        scrollListenerAttached = false;
      }
      if (teaserTimer) clearTimeout(teaserTimer);
      showTeaser();
    }
  };

  const showTeaser = () => {
    if (isDismissed || isOpened) return;
    if (teaser) {
      teaser.hidden = false;
      teaser.style.display = 'block';
    }
    if (badge) {
      badge.hidden = false;
      badge.style.display = 'flex';
    }
    // Auto-minimize teaser to badge only after 18 seconds if user doesn't touch it
    if (autoHideTeaserTimer) clearTimeout(autoHideTeaserTimer);
    autoHideTeaserTimer = setTimeout(() => {
      if (card && !card.hidden && card.style.display !== 'none') return;
      if (teaser) {
        teaser.hidden = true;
        teaser.style.display = 'none';
      }
    }, 18000);
  };

  const openCard = (e) => {
    if (e) {
      e.stopPropagation();
      if (typeof e.preventDefault === 'function') e.preventDefault();
    }
    if (teaser) {
      teaser.hidden = true;
      teaser.style.display = 'none';
    }
    if (badge) {
      badge.hidden = true;
      badge.style.display = 'none';
    }
    if (card) {
      card.hidden = false;
      card.style.display = 'flex';
    }
    if (launcher) launcher.classList.add('is-active');
    isOpened = true;
    try {
      sessionStorage.setItem(STORAGE_OPENED, 'true');
    } catch (err) {}
    if (teaserTimer) clearTimeout(teaserTimer);
    if (autoHideTeaserTimer) clearTimeout(autoHideTeaserTimer);
    if (scrollListenerAttached) {
      window.removeEventListener('scroll', onScroll);
      scrollListenerAttached = false;
    }
  };

  const closeCard = (e) => {
    if (e) {
      e.stopPropagation();
      if (typeof e.preventDefault === 'function') e.preventDefault();
    }
    if (card) {
      card.hidden = true;
      card.style.display = 'none';
    }
    if (launcher) launcher.classList.remove('is-active');
    isDismissed = true;
    try {
      sessionStorage.setItem(STORAGE_DISMISSED, 'true');
    } catch (err) {}
    if (teaserTimer) clearTimeout(teaserTimer);
    if (autoHideTeaserTimer) clearTimeout(autoHideTeaserTimer);
  };

  const dismissTeaser = (e) => {
    if (e) {
      e.stopPropagation();
      if (typeof e.preventDefault === 'function') e.preventDefault();
    }
    if (teaser) {
      teaser.hidden = true;
      teaser.style.display = 'none';
    }
    if (badge) {
      badge.hidden = true;
      badge.style.display = 'none';
    }
    isDismissed = true;
    try {
      sessionStorage.setItem(STORAGE_DISMISSED, 'true');
    } catch (err) {}
    if (teaserTimer) clearTimeout(teaserTimer);
    if (autoHideTeaserTimer) clearTimeout(autoHideTeaserTimer);
    if (scrollListenerAttached) {
      window.removeEventListener('scroll', onScroll);
      scrollListenerAttached = false;
    }
  };

  if (launcher) {
    launcher.addEventListener('click', (e) => {
      e.stopPropagation();
      if (card && !card.hidden && card.style.display !== 'none') {
        closeCard(e);
      } else {
        openCard(e);
      }
    });
  }

  if (teaserTrigger) {
    teaserTrigger.addEventListener('click', (e) => {
      if (e.target.closest('#wa-teaser-close')) return;
      openCard(e);
    });
  }

  if (teaserClose) {
    teaserClose.addEventListener('click', dismissTeaser);
    teaserClose.addEventListener('touchend', dismissTeaser, { passive: false });
  }

  if (cardClose) {
    cardClose.addEventListener('click', closeCard);
    cardClose.addEventListener('touchend', closeCard, { passive: false });
  }

  // Trigger popup teaser after 10 seconds or when user scrolls past 35% of page
  if (!isDismissed && !isOpened) {
    teaserTimer = setTimeout(showTeaser, 10000);
    scrollListenerAttached = true;
    window.addEventListener('scroll', onScroll, { passive: true });
  }
})();
