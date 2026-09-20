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

// Dana Syariah Calculator Functionality
const syariahCalc = document.querySelector('#syariah-calculator');
if (syariahCalc) {
  const tabMotor = syariahCalc.querySelector('#tab-motor');
  const tabMobil = syariahCalc.querySelector('#tab-mobil');
  const rangeInput = syariahCalc.querySelector('#loan-amount-range');
  const amountDisplay = syariahCalc.querySelector('#loan-amount-display');
  const tenorButtons = syariahCalc.querySelectorAll('.tenors button');
  const resultDisplay = syariahCalc.querySelector('#monthly-installment');
  const resultLoanAmount = syariahCalc.querySelector('#result-loan-amount');
  const resultTenor = syariahCalc.querySelector('#result-tenor');
  const resultVehicleType = syariahCalc.querySelector('#result-vehicle-type');
  const waButton = syariahCalc.querySelector('#apply-syariah-wa');

  let currentType = 'motor'; // 'motor' | 'mobil'
  let currentTenor = 12;

  const config = {
    motor: {
      min: 3000000,
      max: 35000000,
      step: 500000,
      default: 10000000,
      annualRate: 0.14, // 14% p.a.
      tenors: [12, 18, 24, 36],
      typeName: 'BPKB Motor'
    },
    mobil: {
      min: 20000000,
      max: 300000000,
      step: 5000000,
      default: 75000000,
      annualRate: 0.11, // 11% p.a.
      tenors: [12, 24, 36, 48],
      typeName: 'BPKB Mobil'
    }
  };

  function formatRupiah(num) {
    return 'Rp ' + Number(num).toLocaleString('id-ID');
  }

  function setVehicleType(type) {
    currentType = type;
    const cfg = config[type];

    if (type === 'motor') {
      tabMotor.classList.add('active');
      tabMobil.classList.remove('active');
    } else {
      tabMobil.classList.add('active');
      tabMotor.classList.remove('active');
    }

    rangeInput.min = cfg.min;
    rangeInput.max = cfg.max;
    rangeInput.step = cfg.step;
    rangeInput.value = cfg.default;

    // Set tenor buttons according to vehicle
    tenorButtons.forEach((btn, idx) => {
      const t = cfg.tenors[idx];
      if (t) {
        btn.textContent = t + ' Bulan';
        btn.dataset.tenor = t;
        btn.style.display = 'block';
      } else {
        btn.style.display = 'none';
      }
    });

    // Reset default active tenor
    currentTenor = cfg.tenors[0];
    tenorButtons.forEach((btn, idx) => {
      btn.classList.toggle('active', idx === 0);
    });

    calculate();
  }

  function calculate() {
    const loan = Number(rangeInput.value);
    const cfg = config[currentType];
    const years = currentTenor / 12;
    const totalMargin = loan * (cfg.annualRate * years);
    const totalPayment = loan + totalMargin;
    const monthly = Math.round(totalPayment / currentTenor);

    amountDisplay.textContent = formatRupiah(loan);
    resultDisplay.textContent = formatRupiah(monthly);
    if (resultLoanAmount) resultLoanAmount.textContent = formatRupiah(loan);
    if (resultTenor) resultTenor.textContent = currentTenor + ' Bulan';
    if (resultVehicleType) resultVehicleType.textContent = cfg.typeName;

    // Update WhatsApp CTA link
    if (waButton) {
      const message = `Halo RodaLinks, saya ingin konsultasi BAF Dana Syariah Gadai ${cfg.typeName} di Bogor. Estimasi pinjaman: ${formatRupiah(loan)}, Tenor: ${currentTenor} bulan (Estimasi angsuran: ${formatRupiah(monthly)}/bln). Mohon info kelengkapan syarat dan prosesnya.`;
      waButton.href = `https://wa.me/6285110539167?text=${encodeURIComponent(message)}`;
    }
  }

  if (tabMotor) {
    tabMotor.addEventListener('click', () => setVehicleType('motor'));
  }
  if (tabMobil) {
    tabMobil.addEventListener('click', () => setVehicleType('mobil'));
  }

  rangeInput.addEventListener('input', calculate);

  tenorButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      tenorButtons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      currentTenor = Number(btn.dataset.tenor);
      calculate();
    });
  });

  // Initial calculation
  setVehicleType('motor');
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

  let isDismissed = sessionStorage.getItem(STORAGE_DISMISSED) === 'true';
  let isOpened = sessionStorage.getItem(STORAGE_OPENED) === 'true';
  let teaserTimer = null;
  let autoHideTeaserTimer = null;

  const showTeaser = () => {
    if (isDismissed || isOpened) return;
    if (teaser) {
      teaser.hidden = false;
    }
    if (badge) {
      badge.hidden = false;
    }
    // Auto-minimize teaser to badge only after 18 seconds if user doesn't touch it
    autoHideTeaserTimer = setTimeout(() => {
      if (teaser && !card.hidden) return;
      if (teaser && !teaser.hidden) {
        teaser.hidden = true;
      }
    }, 18000);
  };

  const openCard = () => {
    if (teaser) teaser.hidden = true;
    if (badge) badge.hidden = true;
    if (card) card.hidden = false;
    if (launcher) launcher.classList.add('is-active');
    isOpened = true;
    sessionStorage.setItem(STORAGE_OPENED, 'true');
    if (autoHideTeaserTimer) clearTimeout(autoHideTeaserTimer);
  };

  const closeCard = () => {
    if (card) card.hidden = true;
    if (launcher) launcher.classList.remove('is-active');
    isDismissed = true;
    sessionStorage.setItem(STORAGE_DISMISSED, 'true');
  };

  const dismissTeaser = (e) => {
    if (e) e.stopPropagation();
    if (teaser) teaser.hidden = true;
    if (badge) badge.hidden = true;
    isDismissed = true;
    sessionStorage.setItem(STORAGE_DISMISSED, 'true');
    if (autoHideTeaserTimer) clearTimeout(autoHideTeaserTimer);
  };

  if (launcher) {
    launcher.addEventListener('click', () => {
      if (card && !card.hidden) {
        closeCard();
      } else {
        openCard();
      }
    });
  }

  if (teaserTrigger) {
    teaserTrigger.addEventListener('click', openCard);
  }

  if (teaserClose) {
    teaserClose.addEventListener('click', dismissTeaser);
  }

  if (cardClose) {
    cardClose.addEventListener('click', closeCard);
  }

  // Trigger popup teaser after 10 seconds or when user scrolls past 35% of page
  if (!isDismissed && !isOpened) {
    teaserTimer = setTimeout(showTeaser, 10000);

    const onScroll = () => {
      const scrollY = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight > 0 && (scrollY / docHeight) > 0.35) {
        window.removeEventListener('scroll', onScroll);
        if (teaserTimer) clearTimeout(teaserTimer);
        showTeaser();
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
  }
})();
