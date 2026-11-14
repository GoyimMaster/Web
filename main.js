(() => {
  const S = window.SITE || {}, $ = (q, r = document) => r.querySelector(q), $$ = (q, r = document) => [...r.querySelectorAll(q)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v) => Math.max(0, Math.min(1, v));

  /* scroll scenes: each [data-scene] gets --p from 0 to 1 */
  const scenes = $$('[data-scene]').map((el) => ({ el, mode: el.dataset.scene, cur: -1, target: 0 }));
  if (reduce) scenes.forEach((s) => s.el.style.setProperty('--p', s.mode === 'exit' ? 0 : 0.8));
  else if (scenes.length) {
    let ticking = false;
    const measure = () => {
      const vh = innerHeight;
      for (const s of scenes) {
        const r = s.el.getBoundingClientRect();
        s.target = clamp(s.mode === 'exit' ? -r.top / r.height : s.mode === 'pin' ? -r.top / Math.max(1, r.height - vh) : (vh - r.top) / (vh + r.height));
      }
    };
    const frame = () => {
      let moving = false;
      for (const s of scenes) {
        const next = s.cur < 0 ? s.target : s.cur + (s.target - s.cur) * 0.14;
        if (Math.abs(next - s.cur) > 0.0004) { s.cur = next; s.el.style.setProperty('--p', next.toFixed(4)); moving = true; }
      }
      if (moving) requestAnimationFrame(frame); else ticking = false;
    };
    const kick = () => { measure(); if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
    addEventListener('scroll', kick, { passive: true }); addEventListener('resize', kick); kick();
  }

  /* header: solid after scroll, hides on the way down; progress bar */
  const head = $('.head'), bar = $('.progress i');
  let lastY = 0;
  const onScroll = () => {
    const y = scrollY;
    head.classList.toggle('solid', y > 30);
    head.classList.toggle('away', y > 500 && y > lastY && !document.body.classList.contains('menu-open'));
    lastY = y;
    if (bar) bar.style.transform = `scaleX(${clamp(y / Math.max(1, document.documentElement.scrollHeight - innerHeight))})`;
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* mobile menu, announcement bar */
  const burger = $('.burger');
  if (burger) burger.addEventListener('click', () => { const o = document.body.classList.toggle('menu-open'); burger.setAttribute('aria-expanded', o); });
  $$('.drawer a').forEach((a) => a.addEventListener('click', () => document.body.classList.remove('menu-open')));
  const ann = $('.announce');
  try { if (sessionStorage.getItem('ann') === '1') ann.remove(); } catch (e) {}
  const annX = $('.announce button');
  if (annX) annX.addEventListener('click', () => { ann.remove(); try { sessionStorage.setItem('ann', '1'); } catch (e) {} });

  /* reveal on scroll */
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
  $$('.rv').forEach((el) => io.observe(el));

  /* side dots (home) */
  const dotSecs = $$('[data-dot]');
  if (dotSecs.length > 2) {
    const nav = document.createElement('nav'); nav.className = 'dots'; nav.setAttribute('aria-label', 'Sections');
    const btns = dotSecs.map((sec) => { const b = document.createElement('a'); b.href = '#' + sec.id; b.innerHTML = `<span>${sec.dataset.dot}</span>`; nav.appendChild(b); return b; });
    document.body.appendChild(nav);
    const dio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { btns.forEach((b, i) => b.classList.toggle('on', dotSecs[i] === e.target)); nav.classList.toggle('light', e.target.classList.contains('dark')); } }), { rootMargin: '-45% 0px -45% 0px' });
    dotSecs.forEach((s) => dio.observe(s));
  }

  /* card tilt */
  if (!reduce && matchMedia('(hover:hover)').matches) $$('.tilt').forEach((c) => {
    c.addEventListener('mousemove', (e) => { const r = c.getBoundingClientRect(); c.style.setProperty('--ry', ((e.clientX - r.left) / r.width - 0.5) * 8 + 'deg'); c.style.setProperty('--rx', (0.5 - (e.clientY - r.top) / r.height) * 8 + 'deg'); });
    c.addEventListener('mouseleave', () => { c.style.setProperty('--ry', '0deg'); c.style.setProperty('--rx', '0deg'); });
  });

  /* video slots: filled from config.js, empty ones show a placeholder */
  const vids = S.videos || {};
  const box = $('#lightbox');
  $$('.vslot').forEach((el) => {
    const id = el.dataset.slot, v = vids[id] || {};
    if (!v.src) { el.classList.add('empty'); el.innerHTML = `<div class="vs-empty"><svg aria-hidden="true"><use href="art.svg#mark"/></svg><b>Coming soon</b><small>${v.title || 'New work is on the way'}</small></div>`; return; }
    el.innerHTML = `<button class="vs-play" aria-label="Play ${v.title || 'video'}">${v.poster ? `<img src="${v.poster}" alt="" loading="lazy" decoding="async">` : `<video src="${v.src}#t=0.1" preload="metadata" muted playsinline></video>`}<span class="vs-btn" aria-hidden="true"></span>${v.title ? `<span class="vs-cap">${v.tag ? `<i>${v.tag}</i>` : ''}${v.title}</span>` : ''}</button>`;
    el.firstChild.addEventListener('click', () => {
      if (el.dataset.inline !== undefined) { el.innerHTML = `<video src="${v.src}" controls autoplay playsinline></video>`; return; }
      box.querySelector('.lb-body').innerHTML = `<video src="${v.src}" controls autoplay playsinline></video>`; box.showModal();
    });
  });
  if (box) { const close = () => { box.querySelector('.lb-body').innerHTML = ''; }; box.addEventListener('close', close); box.addEventListener('click', (e) => { if (e.target === box || e.target.closest('.lb-x')) box.close(); }); }

  /* Calendly: popup on [data-calendly], inline on .cal-inline; without a link, buttons lead to the form */
  const cal = S.calendly ? S.calendly + (S.calendly.includes('?') ? '&' : '?') + 'hide_gdpr_banner=1&primary_color=ff2e88' : '';
  const loadCal = () => new Promise((res) => {
    if (window.Calendly) return res();
    const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = 'https://assets.calendly.com/assets/external/widget.css'; document.head.appendChild(l);
    const s = document.createElement('script'); s.src = 'https://assets.calendly.com/assets/external/widget.js'; s.onload = res; document.head.appendChild(s);
  });
  $$('[data-calendly]').forEach((a) => {
    if (!cal) { a.href = 'contact.html#inquiry'; return; }
    a.href = cal; a.addEventListener('click', (e) => { e.preventDefault(); loadCal().then(() => window.Calendly.initPopupWidget({ url: cal })); });
  });
  const inline = $('.cal-inline');
  if (inline) {
    if (!cal) inline.innerHTML = '<p class="cal-none">Prefer a call? Leave your phone number in the form and we will call you back.</p>';
    else { const cio = new IntersectionObserver((es) => { if (es[0].isIntersecting) { cio.disconnect(); loadCal().then(() => window.Calendly.initInlineWidget({ url: cal, parentElement: inline })); } }, { rootMargin: '300px' }); cio.observe(inline); }
  }

  /* inquiry forms */
  $$('form.inquiry').forEach((f) => {
    const note = $('.form-note', f), btn = $('button[type=submit]', f);
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (f.company_site_url.value) return; /* honeypot */
      const d = new FormData(f); d.delete('company_site_url');
      const lines = [...d.entries()].filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join('\n');
      if (!S.formEndpoint) {
        location.href = `mailto:${S.email}?subject=${encodeURIComponent('Inquiry from ' + (d.get('business') || d.get('name')))}&body=${encodeURIComponent(lines)}`;
        note.textContent = 'Your email app should open with the message ready. If it does not, write to ' + S.email + '.'; note.className = 'form-note ok'; return;
      }
      btn.disabled = true; note.textContent = 'Sending…'; note.className = 'form-note';
      try {
        if (S.formAccessKey) d.append('access_key', S.formAccessKey);
        d.append('subject', 'Inquiry from ' + (d.get('business') || d.get('name')));
        const r = await fetch(S.formEndpoint, { method: 'POST', body: d, headers: { Accept: 'application/json' } });
        if (!r.ok) throw new Error(r.status);
        f.reset(); note.textContent = 'Got it. A real person will reply soon.'; note.className = 'form-note ok';
      } catch (err) { note.textContent = 'That did not send. Please email ' + S.email + ' instead.'; note.className = 'form-note bad'; }
      btn.disabled = false;
    });
  });
  $$('[data-email]').forEach((a) => { a.href = 'mailto:' + S.email; if (!a.textContent.trim()) a.textContent = S.email; });
})();
