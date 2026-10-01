// Signature index: a stroke and its label light up together, whichever one
// the visitor points at, taps or tabs to. Everything works without this file;
// it only adds the highlighting and lets the intro be skipped.
const index = document.querySelector('[data-index]');

if (index) {
  const root = document.documentElement;
  const labels = index.querySelectorAll('.lbl');

  const setActive = (k) => {
    if (k) index.dataset.active = k;
    else delete index.dataset.active;
    labels.forEach((l) => l.classList.toggle('on', l.dataset.k === k));
  };

  index.querySelectorAll('[data-k]').forEach((el) => {
    if (!el.matches('a')) return;
    const k = el.dataset.k;
    el.addEventListener('pointerenter', () => setActive(k));
    el.addEventListener('pointerleave', () => setActive(null));
    el.addEventListener('focus', () => setActive(k));
    el.addEventListener('blur', () => setActive(null));
    el.addEventListener('pointerdown', () => setActive(k)); // touch feedback before navigating
  });

  // The signature writes itself once per visit. Any key, click or scroll finishes it at once.
  const finish = () => root.classList.add('signed');
  if (!root.classList.contains('signed')) {
    ['pointerdown', 'keydown', 'wheel', 'touchstart'].forEach((ev) =>
      window.addEventListener(ev, finish, { once: true, passive: true }));
  }
  try { sessionStorage.setItem('signed', '1'); } catch (e) { /* storage blocked: it just writes again next time */ }

  // Coming back to the index (back button, bfcache) should show the full signature, not a stale highlight
  window.addEventListener('pageshow', () => setActive(null));
}
