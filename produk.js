/* Roda.asia catalogue enhancements. Static HTML remains usable without JavaScript. */
(() => {
  'use strict';
  const search = document.querySelector('#search-motor');
  const grid = document.querySelector('#motor-grid');
  if (search && grid) {
    const cards = [...grid.querySelectorAll('.motor-card')];
    const categoryButtons = [...document.querySelectorAll('.catalog-filter')];
    const sort = document.querySelector('#sort-motor');
    const counter = document.querySelector('#catalog-result-count');
    const empty = document.querySelector('#catalog-empty');
    const reset = document.querySelector('#catalog-reset');
    let category = 'ALL';

    const filter = () => {
      const q = search.value.toLocaleLowerCase('id-ID').trim();
      let visible = 0;
      cards.forEach((card) => {
        const show = (category === 'ALL' || category === card.dataset.category) &&
          (card.dataset.name.includes(q) || card.dataset.keywords.includes(q) || card.textContent.toLocaleLowerCase('id-ID').includes(q));
        card.hidden = !show;
        if (show) visible++;
      });
      if (counter) counter.textContent = `Menampilkan ${visible} dari ${cards.length} model`;
      if (empty) empty.hidden = visible !== 0;
    };

    const applySort = () => {
      const mode = sort?.value || 'default';
      const sorted = [...cards];
      if (mode === 'price-asc') sorted.sort((a, b) => Number(a.dataset.price) - Number(b.dataset.price));
      else if (mode === 'price-desc') sorted.sort((a, b) => Number(b.dataset.price) - Number(a.dataset.price));
      else if (mode === 'name-asc') sorted.sort((a, b) => a.dataset.name.localeCompare(b.dataset.name, 'id'));
      // Original source order is preserved in the cards array.
      sorted.forEach((card) => grid.appendChild(card));
    };

    categoryButtons.forEach((button) => button.addEventListener('click', () => {
      category = button.dataset.category;
      categoryButtons.forEach((other) => {
        const selected = other === button;
        other.classList.toggle('active', selected);
        other.setAttribute('aria-pressed', String(selected));
      });
      filter();
    }));
    search.addEventListener('input', filter);
    sort?.addEventListener('change', applySort);
    reset?.addEventListener('click', () => {
      search.value = '';
      categoryButtons.find((b) => b.dataset.category === 'ALL')?.click();
      search.focus();
    });
    // Allow category links like produk.html?kategori=CLASSY without a backend.
    const requested = new URLSearchParams(window.location.search).get('kategori');
    if (requested) categoryButtons.find((b) => b.dataset.category === requested.toUpperCase())?.click();
  }

  const detail = document.querySelector('.product-detail');
  if (!detail) return;
  const buttons = [...document.querySelectorAll('.catalog-variant')];
  const price = document.querySelector('#selected-price');
  const label = document.querySelector('#selected-price-label');
  const basis = document.querySelector('#selected-price-basis');
  const selected = document.querySelector('#selected-variant');
  const color = document.querySelector('#selected-color');
  const note = document.querySelector('#selected-variant-note');
  const wa = document.querySelector('#detail-wa');
  const formatPrice = (amount) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(amount).replace(/\s+/g, ' ');

  const selectVariant = (button) => {
    buttons.forEach((other) => {
      const active = other === button;
      other.classList.toggle('is-active', active);
      other.setAttribute('aria-pressed', String(active));
    });
    const variant = button.dataset.variant;
    const amount = Number(button.dataset.price);
    const priceBasis = button.dataset.basis;
    const displayColor = button.querySelector('.variant-main small')?.textContent.replace(/^Warna tampilan awal:\s*/, '') || 'Tidak tercatat';
    const basisLabel = priceBasis.toLowerCase().includes('off the road') ? 'Off the road' : 'OTR Jakarta';
    if (price) price.textContent = formatPrice(amount);
    if (label) label.textContent = `Harga referensi · ${basisLabel}`;
    if (basis) basis.textContent = priceBasis;
    if (selected) selected.textContent = variant;
    if (color) color.textContent = displayColor;
    if (note) {
      note.textContent = button.dataset.note || '';
      note.hidden = !button.dataset.note;
    }
    if (wa) {
      const message = `Halo Roda.asia, saya ingin tanya harga Yamaha ${detail.dataset.productName} varian ${variant} untuk Bogor. Mohon info harga OTR, DP, cicilan dan ketersediaannya. Referensi dari katalog Yamaha: ${formatPrice(amount)} (${basisLabel}, data ${detail.dataset.date}).`;
      wa.href = `https://wa.me/${detail.dataset.wa}?text=${encodeURIComponent(message)}`;
    }
  };
  buttons.forEach((button) => button.addEventListener('click', () => selectVariant(button)));
})();
