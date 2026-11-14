(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // nav border after scrolling
  const nav = document.querySelector('.nav');
  const onScroll = () => nav.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // reveal on scroll
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

  // ad deck: the top version slides away and the next one comes up
  const deck = document.getElementById('deck');
  if (!deck) return;
  const cards = [...deck.querySelectorAll('.ad')];
  const dots = [...document.querySelectorAll('#dots i')];
  let order = cards.map((_, i) => i);
  const paint = () => {
    order.forEach((cardIdx, pos) => cards[cardIdx].dataset.pos = String(pos));
    dots.forEach((d, i) => d.classList.toggle('on', i === order[0]));
  };
  paint();
  if (reduce) return;
  let timer, paused = false, busy = false;
  const next = () => {
    if (busy) return; busy = true;
    const top = cards[order[0]];
    top.classList.add('leaving');
    setTimeout(() => {
      order = [...order.slice(1), order[0]];
      top.classList.remove('leaving');
      paint();
      busy = false;
    }, 520);
  };
  const start = () => { clearInterval(timer); timer = setInterval(() => { if (!paused && !document.hidden) next(); }, 2800); };
  deck.addEventListener('mouseenter', () => paused = true);
  deck.addEventListener('mouseleave', () => paused = false);
  deck.addEventListener('click', next);
  deck.style.cursor = 'pointer';
  start();
})();
