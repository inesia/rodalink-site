#!/usr/bin/env python3
"""Regenerate katalog + static detail pages from data/produk.json. Python 3 stdlib only."""
import html
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DB = json.loads((ROOT / 'data/produk.json').read_text(encoding='utf-8'))
PRODUCTS = DB['products']
SITE = DB['site_url'].rstrip('/')
WA = DB['contact_wa']
DATE_LABEL = '7 Agustus 2026'
CATEGORIES = ['MAXI', 'CLASSY', 'MATIC', 'SPORT', 'OFF-ROAD', 'MOPED']
CATEGORY_LABELS = {'MAXI':'MAXi', 'CLASSY':'Classy', 'MATIC':'Matic', 'SPORT':'Sport', 'OFF-ROAD':'Off-Road', 'MOPED':'Moped'}


def h(val):
    return html.escape(str(val), quote=True)


def rupiah(val):
    return 'Rp ' + f'{int(val):,}'.replace(',', '.')


def basis(p):
    return 'Off the road' if p['price_type'].lower().startswith('off') else 'OTR Jakarta'


def wa_link(message):
    return f'https://wa.me/{WA}?text={quote(message)}'


def base_head(title, description, path, *, depth=0, schema=None):
    prefix = '../' if depth else ''
    canonical = SITE + '/' + path
    s = '' if schema is None else ('<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False, separators=(',', ':')).replace('<','\\u003c') + '</script>')
    return f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#10264b">
<title>{h(title)}</title>
<meta name="description" content="{h(description)}">
<link rel="apple-touch-icon" sizes="180x180" href="{prefix}images/favicon/apple-icon-180x180.png">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}images/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{prefix}images/favicon/favicon-16x16.png">
<link rel="shortcut icon" href="{prefix}images/favicon/favicon.ico">
<link rel="canonical" href="{h(canonical)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:locale" content="id_ID">
<meta property="og:site_name" content="RodaLinks">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(description)}">
<meta property="og:url" content="{h(canonical)}">
<meta name="twitter:card" content="summary">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="RodaLinks">
<link rel="manifest" href="{prefix}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=Manrope:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="{prefix}style.css">
<link rel="stylesheet" href="{prefix}produk.css">
{s}
</head>'''


def header(depth=0, active='catalog'):
    prefix='../' if depth else ''
    wa_chat = wa_link('Halo RodaLinks, saya ingin konsultasi layanan RodaLinks.')
    return f'''<header class="site-header">
  <div class="container topbar">
    <a href="{prefix}index.html" class="logo" aria-label="RodaLinks, kembali ke beranda">
      <img src="{prefix}images/logo-rodalink.png" alt="RodaLinks" width="136" height="50">
    </a>
    <button class="menu-toggle" aria-label="Buka menu" aria-expanded="false">☰</button>
    <nav class="nav" aria-label="Navigasi utama">
      <a href="{prefix}index.html">Beranda</a>
      <a href="{prefix}produk.html"{' class="active" aria-current="page"' if active=='catalog' else ''}>Katalog Yamaha</a>
      <a href="{prefix}dana-syariah.html">Dana Syariah</a>
      <a href="{prefix}index.html#cara-kerja">Cara kerja</a>
      <a href="{h(wa_chat)}" target="_blank" rel="noopener noreferrer">Hubungi kami</a>
    </nav>
    <a class="nav-cta" href="{h(wa_chat)}" target="_blank" rel="noopener noreferrer">Chat WhatsApp <span aria-hidden="true">↗</span></a>
  </div>
</header>

<aside id="pwa-install-banner" class="pwa-install-banner" aria-label="Pasang Aplikasi RodaLinks">
  <img src="{prefix}images/favicon/icon-192x192.png" alt="RodaLinks App" class="pwa-install-icon">
  <div class="pwa-install-info">
    <div class="pwa-install-title">Pasang RodaLinks App</div>
    <div class="pwa-install-desc">Akses cepat beli motor &amp; gadai BPKB Bogor</div>
  </div>
  <button id="pwa-install-btn" class="pwa-install-btn">Install</button>
  <button id="pwa-install-close" class="pwa-install-close" aria-label="Tutup">✕</button>
</aside>'''


def footer(depth=0):
    prefix='../' if depth else ''
    wa_general = wa_link('Halo RodaLinks, saya ingin konsultasi layanan RodaLinks.')
    wa_motor = wa_link('Halo RodaLinks, saya ingin konsultasi pembelian motor Yamaha di Bogor.')
    return f'''<section class="catalog-bottom-cta">
  <div class="container catalog-bottom-inner">
    <div>
      <span class="catalog-kicker">MULAI DARI PERCAKAPAN</span>
      <h2>Sudah menemukan motor incaran?</h2>
      <p>Tanyakan harga dan ketersediaan untuk Kota atau Kabupaten Bogor melalui WhatsApp.</p>
    </div>
    <a class="button" href="{h(wa_motor)}" target="_blank" rel="noopener noreferrer">Konsultasi via WhatsApp <span aria-hidden="true">↗</span></a>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <b>RodaLinks · Channel Resmi Yamaha Putera Motor Bubulak Bogor</b>
    <span>Kota Bogor &amp; Kabupaten Bogor · <a href="https://wa.me/{WA}" target="_blank" rel="noopener noreferrer">WhatsApp +62 851-1053-9167</a></span>
    <span>© <span id="year">2026</span> RodaLinks. Seluruh hak cipta dilindungi.</span>
  </div>
  <div class="container catalog-footer-note">RodaLinks merupakan channel penjualan motor dari dealer resmi Yamaha Putera Motor Bubulak Bogor. Halaman ini bukan situs resmi Yamaha Motor Indonesia. Harga referensi diambil dari data Yamaha tertanggal {DATE_LABEL} dan bukan penawaran harga OTR Bogor.</div>
</footer>

<!-- PWA Mobile Bottom Navigation Bar -->
<nav class="pwa-bottom-bar" aria-label="Navigasi Mobile PWA">
  <a href="{prefix}index.html" class="pwa-tab" aria-label="Beranda">
    <svg viewBox="0 0 24 24" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-4v6H4a1 1 0 0 1-1-1v-9.5z"/></svg>
    <span>Beranda</span>
  </a>
  <a href="{prefix}produk.html" class="pwa-tab active" aria-label="Katalog Yamaha">
    <svg viewBox="0 0 24 24" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6h-3l-3 6.5h6.5l2-3.5h2.5"/><path d="M9 17.5h6"/></svg>
    <span>Beli Motor</span>
  </a>
  <a href="{prefix}dana-syariah.html" class="pwa-tab" aria-label="Dana Syariah BAF">
    <svg viewBox="0 0 24 24" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L3 7v6c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V7l-9-5z"/><path d="M12 8v8"/><path d="M9 12h6"/></svg>
    <span>Dana Syariah</span>
  </a>
  <a href="{prefix}index.html#faq-heading" class="pwa-tab" aria-label="FAQ &amp; Bantuan">
    <svg viewBox="0 0 24 24" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
    <span>Bantuan</span>
  </a>
  <a href="{h(wa_general)}" target="_blank" rel="noopener noreferrer" class="pwa-tab pwa-tab-wa" aria-label="Chat WhatsApp">
    <div class="pwa-wa-icon-wrap" aria-hidden="true">
      <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
    </div>
    <span>Chat WA</span>
  </a>
</nav>

<!-- WhatsApp Smart Popup Widget -->
<div id="wa-widget" class="wa-widget" aria-live="polite">
  <!-- Speech Bubble Teaser -->
  <div id="wa-teaser" class="wa-teaser" hidden>
    <button id="wa-teaser-close" class="wa-teaser-close" aria-label="Tutup pesan">✕</button>
    <div class="wa-teaser-body" id="wa-teaser-trigger" role="button" tabindex="0">
      <div class="wa-teaser-head">
        <div class="wa-avatar-mini">
          <img src="{prefix}images/logo-rodalink.png" alt="RodaLinks">
        </div>
        <div class="wa-meta">
          <strong>Tim RodaLinks Bogor</strong>
          <span class="wa-status"><span class="wa-dot"></span> Online</span>
        </div>
      </div>
      <p class="wa-teaser-msg">Halo! Butuh info harga OTR Bogor, stok unit, atau simulasi cicilan Yamaha? Chat kami yuk! 😊</p>
      <span class="wa-teaser-action">Mulai percakapan ↗</span>
    </div>
  </div>

  <!-- Expanded Chat Card -->
  <div id="wa-card" class="wa-card" hidden aria-modal="true" role="dialog" aria-label="WhatsApp Chat RodaLinks">
    <div class="wa-card-header">
      <div class="wa-header-info">
        <div class="wa-avatar">
          <img src="{prefix}images/logo-rodalink.png" alt="Admin RodaLinks">
          <span class="wa-status-badge"></span>
        </div>
        <div>
          <strong class="wa-card-title">Tim Konsultasi RodaLinks</strong>
          <span class="wa-card-desc">Yamaha Putera Motor Bubulak Bogor</span>
        </div>
      </div>
      <button id="wa-card-close" class="wa-card-close" aria-label="Tutup obrolan">✕</button>
    </div>
    <div class="wa-card-body">
      <div class="wa-chat-bubble">
        <p>Halo! Selamat datang di <strong>Katalog Yamaha RodaLinks Bogor</strong> 🏍️</p>
        <p>Pilih topik pertanyaan cepat di bawah atau klik tombol chat untuk konsultasi langsung via WhatsApp:</p>
      </div>
      <div class="wa-quick-chips">
        <a class="wa-chip" href="https://wa.me/6285110539167?text=Halo%20RodaLinks%2C%20saya%20ingin%20tanya%20promo%20dan%20harga%20OTR%20Bogor%20motor%20Yamaha." target="_blank" rel="noopener noreferrer">
          🏍️ Cek Promo &amp; Diskon Motor
        </a>
        <a class="wa-chip" href="https://wa.me/6285110539167?text=Halo%20RodaLinks%2C%20saya%20ingin%20simulasi%20DP%20dan%20cicilan%20kredit%20motor%20Yamaha%20Bogor." target="_blank" rel="noopener noreferrer">
          💰 Simulasi DP &amp; Cicilan Kredit
        </a>
        <a class="wa-chip" href="https://wa.me/6285110539167?text=Halo%20RodaLinks%2C%20saya%20ingin%20konsultasi%20Dana%20Syariah%20Gadai%20BPKB." target="_blank" rel="noopener noreferrer">
          🌿 Konsultasi Dana Syariah BPKB
        </a>
      </div>
    </div>
    <div class="wa-card-footer">
      <a id="wa-direct-chat" class="wa-cta-btn" href="https://wa.me/6285110539167?text=Halo%20RodaLinks%2C%20saya%20ingin%20konsultasi%20pembelian%20motor%20Yamaha%20di%20Bogor." target="_blank" rel="noopener noreferrer">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M20.52 3.48A11.85 11.85 0 0 0 12.07 0C5.46 0 .09 5.37.09 11.98c0 2.11.55 4.17 1.6 5.99L0 24l6.2-1.63a11.9 11.9 0 0 0 5.86 1.53h.01c6.61 0 11.98-5.37 11.98-11.98 0-3.2-1.25-6.21-3.53-8.44zm-8.45 18.42h-.01a9.9 9.9 0 0 1-5.04-1.38l-.36-.21-3.75.98 1-3.65-.24-.38a9.92 9.92 0 0 1-1.52-5.28c0-5.48 4.46-9.94 9.94-9.94 2.65 0 5.15 1.03 7.03 2.91 1.88 1.88 2.91 4.38 2.91 7.03 0 5.48-4.46 9.94-9.96 9.94zm5.45-7.44c-.3-.15-1.77-.87-2.04-.97-.28-.1-.48-.15-.68.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.49-.89-.8-1.5-1.78-1.67-2.08-.17-.3-.02-.46.13-.61.14-.14.3-.35.45-.53.15-.17.2-.3.3-.5.1-.2.05-.38-.02-.53-.08-.15-.68-1.64-.93-2.25-.24-.59-.49-.51-.68-.52h-.58c-.2 0-.53.08-.8.38-.28.3-1.07 1.05-1.07 2.56s1.1 2.97 1.25 3.17c.15.2 2.16 3.3 5.23 4.63.73.32 1.3.51 1.74.65.73.23 1.4.2 1.93.12.59-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z"/></svg>
        <span>Chat via WhatsApp</span>
      </a>
    </div>
  </div>

  <!-- Floating Launcher Button -->
  <button id="wa-launcher" class="wa-launcher" aria-label="Buka bantuan WhatsApp RodaLinks">
    <span class="wa-unread-badge" id="wa-badge" hidden>1</span>
    <svg class="wa-icon-msg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
      <path d="M20.52 3.48A11.85 11.85 0 0 0 12.07 0C5.46 0 .09 5.37.09 11.98c0 2.11.55 4.17 1.6 5.99L0 24l6.2-1.63a11.9 11.9 0 0 0 5.86 1.53h.01c6.61 0 11.98-5.37 11.98-11.98 0-3.2-1.25-6.21-3.53-8.44zm-8.45 18.42h-.01a9.9 9.9 0 0 1-5.04-1.38l-.36-.21-3.75.98 1-3.65-.24-.38a9.92 9.92 0 0 1-1.52-5.28c0-5.48 4.46-9.94 9.94-9.94 2.65 0 5.15 1.03 7.03 2.91 1.88 1.88 2.91 4.38 2.91 7.03 0 5.48-4.46 9.94-9.96 9.94zm5.45-7.44c-.3-.15-1.77-.87-2.04-.97-.28-.1-.48-.15-.68.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.49-.89-.8-1.5-1.78-1.67-2.08-.17-.3-.02-.46.13-.61.14-.14.3-.35.45-.53.15-.17.2-.3.3-.5.1-.2.05-.38-.02-.53-.08-.15-.68-1.64-.93-2.25-.24-.59-.49-.51-.68-.52h-.58c-.2 0-.53.08-.8.38-.28.3-1.07 1.05-1.07 2.56s1.1 2.97 1.25 3.17c.15.2 2.16 3.3 5.23 4.63.73.32 1.3.51 1.74.65.73.23 1.4.2 1.93.12.59-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z"/>
    </svg>
    <svg class="wa-icon-close" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  </button>
</div>

<script src="{prefix}script.js" defer></script><script src="{prefix}produk.js" defer></script>'''


def card(p, depth=0, compact=False):
    prefix='../' if depth else ''
    url=f'{prefix}produk/{p["slug"]}.html'
    ref='Off the road' if basis(p)=='Off the road' else 'OTR Jakarta'
    msg=f'Halo RodaLinks, saya ingin tanya harga Yamaha {p["name"]} untuk Bogor. Mohon info harga OTR, DP dan cicilan yang tersedia.'
    return f'''<article class="motor-card" data-name="{h(p['name'].lower())}" data-keywords="{h(' '.join(v['name'] for v in p['variants']).lower())}" data-category="{h(p['category'])}" data-price="{p['price_min']}" data-variants="{p['variant_count']}">
<a class="motor-photo" href="{h(url)}" aria-label="Lihat detail Yamaha {h(p['name'])}"><img src="{prefix}{h(p['image'])}" loading="lazy" width="1000" height="760" alt="Gambar produk Yamaha {h(p['name'])}"><span class="motor-photo-arrow" aria-hidden="true">↗</span></a>
<div class="motor-card-body"><div class="motor-card-top"><span class="catalog-tag">{h(CATEGORY_LABELS.get(p['category'],p['category']))}</span><span class="motor-variant-count">{p['variant_count']} varian</span></div>
<h3><a href="{h(url)}">Yamaha {h(p['name'])}</a></h3><span class="motor-price-label">Harga referensi mulai · {h(ref)}</span><strong class="motor-price">{rupiah(p['price_min'])}</strong>
<p class="motor-card-note">Harga Bogor, DP, dan cicilan: konfirmasi melalui WhatsApp.</p>
<div class="motor-card-actions"><a class="motor-detail-link" href="{h(url)}">Lihat detail <span aria-hidden="true">↗</span></a><a class="motor-wa-link" href="{h(wa_link(msg))}" target="_blank" rel="noopener noreferrer" aria-label="Tanya harga Yamaha {h(p['name'])} untuk Bogor">Tanya harga</a></div></div></article>'''


def breadcrumb(items):
    li=[]
    for i,(label,url) in enumerate(items):
        if i==len(items)-1:
            li.append(f'<span aria-current="page">{h(label)}</span>')
        else:
            li.append(f'<a href="{h(url)}">{h(label)}</a><span class="crumb-divider" aria-hidden="true">/</span>')
    return '<nav class="catalog-breadcrumb" aria-label="Breadcrumb">'+''.join(li)+'</nav>'


def listing_page():
    title='Katalog Motor Yamaha Bogor | Harga Referensi & Varian - RodaLinks'
    desc='Jelajahi 28 model dan 65 varian motor Yamaha di RodaLinks Bogor. Cek harga referensi Jakarta per 7 Agustus 2026, lalu konsultasikan harga OTR Bogor lewat WhatsApp.'
    schema={'@context':'https://schema.org','@graph':[{'@type':'CollectionPage','name':'Katalog Motor Yamaha Bogor','url':SITE+'/produk.html','description':desc,'inLanguage':'id-ID'},{'@type':'ItemList','numberOfItems':len(PRODUCTS),'itemListElement':[{'@type':'ListItem','position':i+1,'name':'Yamaha '+p['name'],'url':SITE+'/produk/'+p['slug']+'.html'} for i,p in enumerate(PRODUCTS)]}]}
    counts=Counter(p['category'] for p in PRODUCTS)
    chips='<button class="catalog-filter active" data-category="ALL" aria-pressed="true" type="button">Semua <span>'+str(len(PRODUCTS))+'</span></button>'+''.join(f'<button class="catalog-filter" data-category="{c}" aria-pressed="false" type="button">{h(CATEGORY_LABELS[c])} <span>{counts[c]}</span></button>' for c in CATEGORIES)
    return base_head(title,desc,'produk.html',schema=schema)+f'''<body class="catalog-body">{header()}
<main id="atas">
<section class="catalog-hero"><div class="container catalog-hero-layout"><div class="catalog-hero-copy">
{breadcrumb([('Beranda','index.html'),('Katalog Yamaha','')])}
<span class="catalog-kicker">PILIH MOTOR · KOTA &amp; KABUPATEN BOGOR</span><h1>Temukan motor Yamaha <em>yang cocok buatmu.</em></h1>
<p>Jelajahi model dan varian Yamaha, bandingkan harga referensi, lalu konsultasikan harga OTR serta pilihan pembiayaan untuk wilayah Bogor.</p>
<a class="button catalog-hero-button" href="#daftar-motor">Jelajahi katalog <span aria-hidden="true">↓</span></a></div>
<div class="catalog-hero-panel" aria-label="Ringkasan katalog"><span class="hero-panel-eyebrow">KATALOG RODALINKS</span><div class="hero-panel-metric"><strong>{len(PRODUCTS)}</strong><span>model motor Yamaha</span></div><div class="hero-panel-rule"></div><div class="hero-panel-metric"><strong>{sum(len(p['variants']) for p in PRODUCTS)}</strong><span>pilihan varian</span></div><div class="hero-panel-categories">MAXi <span>·</span> Classy <span>·</span> Matic <span>·</span> Sport <span>·</span> Off-Road <span>·</span> Moped</div></div>
</div></section>
<section class="catalog-listing container" id="daftar-motor" aria-labelledby="catalog-heading">
<div class="catalog-listing-title"><div><span class="catalog-kicker catalog-kicker-dark">JELAJAHI PILIHAN MOTOR</span><h2 id="catalog-heading">Katalog Yamaha</h2><p>Data model, varian, dan harga referensi bersumber dari dokumen Yamaha yang diakses {DATE_LABEL}.</p></div><span class="catalog-data-badge">Harga referensi, bukan OTR Bogor</span></div>
<div class="catalog-controls"><label class="catalog-search" for="search-motor"><span aria-hidden="true">⌕</span><input id="search-motor" type="search" placeholder="Cari NMAX, Fazzio, R15..." autocomplete="off" aria-label="Cari nama motor atau varian"></label><label class="catalog-sort-label" for="sort-motor">Urutkan <select id="sort-motor"><option value="default">Kategori katalog</option><option value="price-asc">Harga terendah</option><option value="price-desc">Harga tertinggi</option><option value="name-asc">Nama A–Z</option></select></label></div>
<div class="catalog-filters" role="group" aria-label="Filter kategori motor">{chips}</div>
<div class="catalog-results"><p id="catalog-result-count" role="status" aria-live="polite">Menampilkan {len(PRODUCTS)} model</p><p>Harga tiap model merupakan harga awal varian menurut referensi Yamaha.</p></div>
<div class="motor-grid" id="motor-grid">{''.join(card(p) for p in PRODUCTS)}</div>
<div class="catalog-empty" id="catalog-empty" hidden><strong>Motor tidak ditemukan.</strong><p>Coba kata kunci lain atau pilih kategori Semua.</p><button class="catalog-reset" type="button" id="catalog-reset">Reset pencarian</button></div>
<div class="catalog-disclosure"><strong>Informasi harga</strong><p>Harga yang ditampilkan adalah referensi per {DATE_LABEL} dari dokumen yang kamu berikan. Untuk sebagian model Off-Road, harga bersifat <em>off the road</em>. Harga, promo, ketersediaan, DP, dan cicilan wilayah Kota/Kabupaten Bogor wajib dikonfirmasi melalui RodaLinks. Gambar produk digunakan sebagai ilustrasi; periksa foto dan warna terbaru sebelum membeli.</p></div>
</section></main>{footer()}</body></html>'''


def variant_row(p,v,index,initial_idx):
    selected=index==initial_idx
    return f'''<button type="button" class="catalog-variant {'is-active' if selected else ''}" aria-pressed="{'true' if selected else 'false'}" data-variant="{h(v['name'])}" data-price="{v['price']}" data-basis="{h(v['price_basis'])}" data-note="{h(v['notes'])}">
<span class="variant-main"><strong>{h(v['name'])}</strong><small>Warna tampilan awal: {h(v['display_color'] or 'Tidak tercatat')}</small></span>
<span class="variant-right"><strong>{rupiah(v['price'])}</strong><small>{h('Off the road' if 'off the road' in v['price_basis'].lower() else 'OTR Jakarta')}</small></span><span class="variant-indicator" aria-hidden="true">✓</span></button>'''


def detail_page(p):
    name='Yamaha '+p['name']
    title=f'{name} – Harga Referensi, {p["variant_count"]} Varian | RodaLinks Bogor'
    description=f'Lihat {p["variant_count"]} varian {name}, harga referensi mulai {rupiah(p["price_min"])} ({basis(p)}, 7 Agustus 2026). Tanya harga OTR Bogor dan cicilan ke RodaLinks.'
    url='produk/'+p['slug']+'.html'
    initial_idx=next(i for i,v in enumerate(p['variants']) if v['price']==p['price_min'])
    initial=p['variants'][initial_idx]
    msg=f'Halo RodaLinks, saya ingin tanya harga Yamaha {p["name"]} varian {initial["name"]} untuk Bogor. Mohon info harga OTR, DP, cicilan dan ketersediaannya. Referensi dari katalog Yamaha: {rupiah(initial["price"])} ({basis(p)}, data {DATE_LABEL}).'
    schema={'@context':'https://schema.org','@graph':[{'@type':'Product','name':name,'brand':{'@type':'Brand','name':'Yamaha'},'category':p['category'],'url':SITE+'/'+url,'sameAs':p['source_url'],'description':description},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Beranda','item':SITE+'/'},{'@type':'ListItem','position':2,'name':'Katalog Yamaha','item':SITE+'/produk.html'},{'@type':'ListItem','position':3,'name':name,'item':SITE+'/'+url}]}]}
    related=[other for other in PRODUCTS if other['slug']!=p['slug'] and other['category']==p['category']][:3]
    if len(related)<3:
        related+= [other for other in PRODUCTS if other['slug']!=p['slug'] and other not in related][:3-len(related)]
    badge=f'{p["variant_count"]} pilihan varian' if p['variant_count']>1 else '1 pilihan varian'
    color=initial['display_color'] or 'Tidak tercatat'
    return base_head(title,description,url,depth=1,schema=schema)+f'''<body class="catalog-body product-detail" data-product-slug="{h(p['slug'])}" data-product-name="{h(p['name'])}" data-wa="{WA}" data-date="{DATE_LABEL}" data-price-type="{h(basis(p))}">{header(depth=1)}
<main id="atas"><section class="detail-shell"><div class="container">
{breadcrumb([('Beranda','../index.html'),('Katalog Yamaha','../produk.html'),(name,'')])}
<div class="detail-layout"><div class="detail-visual"><div class="detail-photo"><img src="../{h(p['image'])}" width="1000" height="760" alt="Gambar produk {h(name)}"></div><div class="detail-image-note">Foto dan pilihan warna dapat berbeda antarvarian. Konfirmasi tampilan serta ketersediaan unit saat konsultasi.</div></div>
<div class="detail-summary"><div class="detail-tags"><span class="catalog-tag">{h(CATEGORY_LABELS.get(p['category'],p['category']))}</span><span class="detail-variant-badge">{badge}</span></div>
<h1>{h(name)}</h1><p class="detail-lead">Lihat pilihan varian dan harga referensinya. Untuk harga pembelian di Bogor, promo, serta simulasi DP dan cicilan, konsultasikan langsung dengan RodaLinks.</p>
<div class="detail-price-box"><span id="selected-price-label">Harga referensi · {h(basis(p))}</span><strong id="selected-price">{rupiah(initial['price'])}</strong><small id="selected-price-basis">{h(initial['price_basis'])}</small><p>Data harga per {DATE_LABEL}; bukan harga final atau penawaran OTR Bogor.</p></div>
<div class="detail-variant-heading"><h2>Pilih varian</h2><span id="selected-variant-count">{badge}</span></div><div class="catalog-variants" id="catalog-variants" role="group" aria-label="Pilihan varian {h(name)}">{''.join(variant_row(p,v,i,initial_idx) for i,v in enumerate(p['variants']))}</div>
<div class="detail-selected-info"><div><span>Varian dipilih</span><strong id="selected-variant">{h(initial['name'])}</strong></div><div><span>Warna yang tercatat</span><strong id="selected-color">{h(color)}</strong></div></div>
<p class="detail-variant-note" id="selected-variant-note" {'hidden' if not initial['notes'] else ''}>{h(initial['notes'])}</p>
<div class="detail-actions"><a class="button" id="detail-wa" href="{h(wa_link(msg))}" target="_blank" rel="noopener noreferrer">Tanya harga Bogor via WhatsApp <span aria-hidden="true">↗</span></a><a class="detail-back" href="../produk.html">← Kembali ke katalog</a></div>
<p class="detail-trust">RodaLinks membantu menghubungkan konsultasi pembelian motor dengan dealer di area Bogor. Persediaan, harga dan persetujuan pembiayaan mengikuti ketentuan pihak terkait.</p>
</div></div></div></section>
<section class="detail-information"><div class="container detail-info-grid"><div><span class="catalog-kicker catalog-kicker-dark">INFORMASI PRODUK</span><h2>Informasi {h(name)}</h2><p>Data yang tersedia di dokumen sumber meliputi kategori, nama varian, harga, warna tampilan awal, dan tautan produk. Spesifikasi mesin, dimensi, fitur, serta pilihan warna lengkap belum tersedia dalam Excel dan tidak ditambahkan secara perkiraan.</p></div><div class="detail-fact-list"><div><span>Merek</span><strong>Yamaha</strong></div><div><span>Kategori</span><strong>{h(CATEGORY_LABELS.get(p['category'],p['category']))}</strong></div><div><span>Jumlah varian</span><strong>{p['variant_count']} varian</strong></div><div><span>Kisaran harga referensi</span><strong>{rupiah(p['price_min'])}{' – '+rupiah(p['price_max']) if p['price_max'] != p['price_min'] else ''}</strong></div><div><span>Jenis harga</span><strong>{h(basis(p))}</strong></div><div><span>Tanggal akses data</span><strong>{DATE_LABEL}</strong></div></div></div>
<div class="container detail-source"><div><strong>Butuh spesifikasi lengkap atau foto resmi?</strong><p>Lihat halaman model di Yamaha Indonesia untuk informasi teknis dan foto terbaru.</p></div><a href="{h(p['source_url'])}" target="_blank" rel="noopener noreferrer">Lihat produk di Yamaha Indonesia ↗</a></div></section>
<section class="container related-section"><div class="related-heading"><div><span class="catalog-kicker catalog-kicker-dark">PILIHAN LAINNYA</span><h2>Motor Yamaha lainnya</h2></div><a href="../produk.html">Lihat semua motor ↗</a></div><div class="motor-grid related-grid">{''.join(card(r,depth=1,compact=True) for r in related)}</div></section></main>{footer(depth=1)}</body></html>'''


def main():
    (ROOT/'produk').mkdir(exist_ok=True)
    assert len(PRODUCTS)==len({p['slug'] for p in PRODUCTS})
    (ROOT/'produk.html').write_text(listing_page(),encoding='utf-8')
    for p in PRODUCTS:
        (ROOT/'produk'/f'{p["slug"]}.html').write_text(detail_page(p),encoding='utf-8')
    print(f'Generated: 1 katalog + {len(PRODUCTS)} static detail pages ({sum(len(p["variants"]) for p in PRODUCTS)} varian)')

if __name__=='__main__':
    main()
