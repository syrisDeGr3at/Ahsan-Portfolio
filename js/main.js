{
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const LINKEDIN = 'https://www.linkedin.com/in/muhammad-ahsan-a28b18326';

/* ---------- light / dark via pull rope (window blind) ---------- */
const setMode = m => {
  root.dataset.mode = m;
  try { localStorage.setItem('ahsan-mode', m); } catch (e) {}
  const meta = $('meta[name=theme-color]');
  if (meta) meta.content = m === 'light' ? '#E8E4E0' : '#1A1818';
};
setMode(root.dataset.mode === 'light' ? 'light' : 'dark');
const toggleMode = () => {
  const next = root.dataset.mode === 'light' ? 'dark' : 'light';
  if (!document.startViewTransition || reduced) { setMode(next); return; }
  root.classList.remove('vt-open', 'vt-close');
  root.classList.add(next === 'light' ? 'vt-open' : 'vt-close');
  const vt = document.startViewTransition(() => setMode(next));
  vt.finished.finally(() => root.classList.remove('vt-open', 'vt-close'));
};
const rope = $('.rope');
if (rope) {
  const cord = $('.cord', rope);
  let pending = false, pull = 0, vel = 0, ang = 0, angV = reduced ? 0 : 1.6, drag = null, toggled = false, moved = false, raf = 0;
  const base = () => parseFloat(getComputedStyle(cord).getPropertyValue('--len')) || 290;
  const render = () => {
    cord.style.height = (base() * (rope.classList.contains('short') ? .35 : 1) + pull) + 'px';
    rope.style.transform = `rotate(${ang}deg)`;
  };
  const step = () => {
    if (drag === null) {
      vel = (vel - pull * 0.09) * 0.84; pull += vel;
      if (pending && vel <= 0) { pending = false; toggleMode(); }
    }
    angV = (angV - ang * 0.035) * 0.965; ang += angV;
    render();
    if (Math.abs(pull) > .1 || Math.abs(vel) > .1 || Math.abs(ang) > .02 || Math.abs(angV) > .02 || drag !== null) raf = requestAnimationFrame(step);
    else { pull = vel = ang = angV = 0; render(); raf = 0; }
  };
  const kick = () => { if (!raf) raf = requestAnimationFrame(step); };
  rope.addEventListener('pointerdown', e => { drag = { y: e.clientY, x: e.clientX }; moved = false; toggled = false; rope.setPointerCapture(e.pointerId); kick(); });
  rope.addEventListener('pointermove', e => {
    if (drag) {
      const dy = e.clientY - drag.y;
      if (Math.abs(dy) > 4) moved = true;
      pull = Math.max(0, Math.min(150, dy * 0.85));
      ang = Math.max(-14, Math.min(14, -(e.clientX - drag.x) * 0.12));
      if (!toggled && pull > 60) { toggled = true; toggleMode(); }
    } else if (!reduced && Math.abs(ang) < 4) { angV += -e.movementX * 0.006; kick(); }
  });
  const release = () => { if (!drag) return; drag = null; vel = -2; kick(); };
  rope.addEventListener('pointerup', release);
  rope.addEventListener('pointercancel', release);
  rope.addEventListener('click', e => {
    if (moved) { moved = false; return; }
    pending = true; vel = 20; angV += 1.2; kick();   // click / Enter / Space: give it a tug
  });
  addEventListener('scroll', () => { const sh = scrollY > 160; if (sh !== rope.classList.contains('short')) { rope.classList.toggle('short', sh); render(); } }, { passive: true });
  render(); kick();
}

/* ---------- local time (Mirpur, PKT) ---------- */
const fmtTime = () => {
  const d = new Date();
  const t = d.toLocaleTimeString('en-GB', { timeZone: 'Asia/Karachi', hour: 'numeric', minute: '2-digit', hour12: true }).replace(' ', '').toLowerCase();
  const day = d.toLocaleDateString('en-GB', { timeZone: 'Asia/Karachi', day: 'numeric', month: 'long', year: 'numeric' });
  return `${t}, ${day}`;
};
const tick = () => {
  $$('[data-time]').forEach(el => el.textContent = fmtTime());
  const [t, d] = fmtTime().split(', ');
  $$('[data-t]').forEach(el => el.textContent = t);
  $$('[data-d]').forEach(el => el.textContent = d.replace(/ (\d{4})$/, ', $1'));
};
tick(); setInterval(tick, 20000);

/* ---------- smooth scroll (desktop) ---------- */
let lenis = null;
if (!reduced && window.Lenis && matchMedia('(pointer:fine)').matches) {
  lenis = new Lenis({ duration: 1.15, smoothWheel: true });
  const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
}
const scrollTo = target => lenis ? lenis.scrollTo(target, { offset: -70 }) : (typeof target === 'number' ? scrollTo0(target) : target.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' }));
const scrollTo0 = y => window.scrollTo({ top: y, behavior: reduced ? 'auto' : 'smooth' });
$$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
  const id = a.getAttribute('href');
  if (id === '#contact') { e.preventDefault(); closeMenu(); openModal(); return; }
  if (id === '#top') { e.preventDefault(); closeMenu(); lenis ? lenis.scrollTo(0) : scrollTo0(0); return; }
  const el = id.length > 1 && document.getElementById(id.slice(1));
  if (el) { e.preventDefault(); closeMenu(); scrollTo(el); }
}));

/* ---------- header hide on scroll, back to top ---------- */
const hdr = $('.hdr'), totop = $('.totop');
let lastY = 0;
const onScroll = () => {
  const y = window.scrollY;
  hdr.classList.toggle('solid', y > 40);
  hdr.classList.toggle('hide', y > 300 && y > lastY && !document.body.classList.contains('menu-open'));
  totop && totop.classList.toggle('on', y > 900);
  lastY = y;
  doorsPin();
};
addEventListener('scroll', onScroll, { passive: true });

/* ---------- menu ---------- */
const menuBtn = $('.menu-btn');
const closeMenu = () => { document.body.classList.remove('menu-open'); menuBtn && menuBtn.setAttribute('aria-expanded', 'false'); lenis && lenis.start(); };
menuBtn && menuBtn.addEventListener('click', () => {
  const open = !document.body.classList.contains('menu-open');
  document.body.classList.toggle('menu-open', open);
  menuBtn.setAttribute('aria-expanded', String(open));
  $$('.menu li a').forEach((a, i) => a.style.transitionDelay = open ? (0.15 + i * 0.05) + 's' : '0s');
  lenis && (open ? lenis.stop() : lenis.start());
});
addEventListener('keydown', e => { if (e.key === 'Escape') { closeMenu(); closeModal(); } });

/* ---------- word split + reveal ---------- */
$$('[data-split]').forEach(el => {
  const walk = node => {
    [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.append(' '); return; }
          const w = document.createElement('span'); w.className = 'w';
          const s = document.createElement('span'); s.textContent = part; w.append(s); frag.append(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && !n.classList.contains('w')) walk(n);
    });
  };
  walk(el);
  $$('.w>span', el).forEach((s, i) => s.style.transitionDelay = (i * 0.045) + 's');
});
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: 0.15, rootMargin: '0px 0px -6% 0px' });
const armReveals = () => $$('[data-split],[data-reveal]').forEach(el => io.observe(el));

/* ---------- flip calendar of roles ---------- */
const flip = $('.flip');
if (flip) {
  const roles = [['a', 'Software Engineer'], ['an', 'AI Developer'], ['a', 'Web Developer'], ['an', 'Automation Builder']];
  const pages = $$('.page', flip), ct = $('.ct', flip), art = $('.art');
  const fit = pt => {
    pt.style.fontSize = '';
    const avail = pt.parentElement.clientWidth - 68;
    if (pt.scrollWidth > avail) pt.style.fontSize = (parseFloat(getComputedStyle(pt).fontSize) * avail / pt.scrollWidth) + 'px';
  };
  let ri = 0, top = 0;
  fit($('.pt', pages[0]));
  addEventListener('resize', () => pages.forEach(p => fit($('.pt', p))));
  const next = () => {
    const cur = pages[top], under = pages[1 - top];
    ri = (ri + 1) % roles.length;
    const pt = $('.pt', under); pt.textContent = roles[ri][1]; fit(pt);
    cur.classList.add('fly');
    if (art) art.style.opacity = 0;
    setTimeout(() => { if (art) { art.textContent = roles[ri][0]; art.style.opacity = 1; } ct.textContent = `${String(ri + 1).padStart(2, '0')} / ${String(roles.length).padStart(2, '0')}`; }, 380);
    cur.addEventListener('animationend', function done(e) {
      if (e.target !== cur) return;
      cur.removeEventListener('animationend', done);
      cur.classList.remove('fly', 'top'); under.classList.add('top'); top = 1 - top;
    });
  };
  if (!reduced) setInterval(() => { if (!document.hidden) next(); }, 2600);
}

/* ---------- doors: horizontal wall ---------- */
const pin = $('.pin'), track = $('.track'), floorBar = $('.wall-floor b');
let pinDist = 0;
const sizePin = () => {
  if (!pin) return;
  if (innerWidth <= 900) { pin.style.height = ''; track.style.transform = ''; pinDist = 0; return; }
  pinDist = Math.max(0, track.scrollWidth - innerWidth);
  pin.style.height = (innerHeight + pinDist) + 'px';
  doorsPin();
};
function doorsPin() {
  if (!pin || !pinDist) return;
  const r = pin.getBoundingClientRect();
  const p = Math.min(1, Math.max(0, -r.top / pinDist));
  track.style.transform = `translate3d(${-p * pinDist}px,0,0)`;
  if (floorBar) floorBar.style.width = (p * 100) + '%';
}
addEventListener('resize', sizePin);
addEventListener('load', sizePin);
sizePin();
if (track && innerWidth <= 900) track.addEventListener('scroll', () => {
  if (floorBar) floorBar.style.width = (track.scrollLeft / Math.max(1, track.scrollWidth - track.clientWidth) * 100) + '%';
}, { passive: true });

/* door click: walk through the door */
$$('.door').forEach(d => d.addEventListener('click', e => {
  if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
  e.preventDefault();
  const href = d.getAttribute('href');
  if (reduced) { location.href = href; return; }
  if (document.body.classList.contains('entering')) return;
  document.body.classList.add('entering');
  try { sessionStorage.setItem('ahsan-arrive', '1'); } catch (err) {}
  lenis && lenis.stop();
  d.classList.add('open');
  const main = $('main'), inside = $('.door-in', d);
  const r0 = inside.getBoundingClientRect(), m0 = main.getBoundingClientRect();
  main.style.transformOrigin = `${r0.left + r0.width / 2 - m0.left}px ${r0.top + r0.height / 2 - m0.top}px`;
  main.animate([{ transform: 'scale(1)', filter: 'blur(0px)' }, { transform: 'scale(1.45)', filter: 'blur(3px)' }],
    { duration: 1500, delay: 250, easing: 'cubic-bezier(.65,0,.25,1)', fill: 'forwards' });
  hdr.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 400, fill: 'forwards' });
  setTimeout(() => {
    const r = inside.getBoundingClientRect();
    const portal = document.createElement('div');
    portal.className = 'portal';
    portal.innerHTML = inside.innerHTML;
    document.body.append(portal);
    const from = { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px', borderRadius: getComputedStyle(inside).borderRadius };
    Object.assign(portal.style, from);
    portal.animate([from, { left: '0px', top: '0px', width: innerWidth + 'px', height: innerHeight + 'px', borderRadius: '0px' }],
      { duration: 1050, easing: 'cubic-bezier(.76,0,.24,1)', fill: 'forwards' })
      .finished.then(() => { portal.classList.add('through'); setTimeout(() => { location.href = href; }, 520); });
  }, 620);
}));
addEventListener('pageshow', () => {
  document.body.classList.remove('entering');
  $$('.portal').forEach(p => p.remove());
  $$('.door.open').forEach(d => d.classList.remove('open'));
  const main = $('main'); main && main.getAnimations().forEach(a => a.cancel());
  hdr && hdr.getAnimations().forEach(a => a.cancel());
  lenis && lenis.start();
});

/* ---------- story timeline ---------- */
const items = $$('.tl>li');
if (items.length) {
  const cur = $('.counter .cur'), bar = $('.ticks b');
  const tio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    items.forEach(li => li.classList.toggle('on', li === e.target));
    const i = items.indexOf(e.target);
    if (cur) cur.textContent = String(i + 1).padStart(2, '0');
    if (bar) bar.style.left = (i / items.length * 100) + '%';
  }), { rootMargin: '-45% 0px -45% 0px' });
  items.forEach(li => tio.observe(li));
  items[0].classList.add('on');
}

/* ---------- contact flow (5 steps) ---------- */
const modal = $('#contact-modal');
let lastFocus = null;
const data = { need: '', details: '', where: '', when: '', name: '', org: '' };
const NEEDS = {
  'An engineering role': 'Share the role, the team’s work and the main technologies involved.',
  'An MS or research opportunity': 'Share the programme or research group, the area of study and any timeline.',
  'An AI or automation project': 'Start with the problem, the intended users and the outcome you want.',
  'A web application': 'Describe the current workflow and what the application should make easier.',
  'A question about this site': 'Ask away.'
};
const steps = modal ? $$('.step', modal) : [];
let si = 0;
const showStep = i => {
  si = i;
  steps.forEach((s, k) => s.classList.toggle('on', k === i));
  $('.steps-count', modal).textContent = i < 5 ? `${i + 1} of 5` : 'Done';
  $('.steps-bar i', modal).style.width = Math.min(100, (i + 1) * 20) + '%';
  const f = $('input,textarea,button.opt', steps[i]); f && setTimeout(() => f.focus(), 80);
};
function openModal() {
  if (!modal) return;
  lastFocus = document.activeElement;
  modal.classList.add('on'); modal.setAttribute('aria-hidden', 'false');
  document.body.classList.add('locked'); lenis && lenis.stop();
  showStep(0);
}
function closeModal() {
  if (!modal || !modal.classList.contains('on')) return;
  modal.classList.remove('on'); modal.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('locked'); lenis && lenis.start();
  lastFocus && lastFocus.focus();
}
if (modal) {
  $$('[data-hire]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); closeMenu(); openModal(); }));
  $$('[data-close]', modal).forEach(b => b.addEventListener('click', closeModal));
  $$('.opt', modal).forEach(o => o.addEventListener('click', () => {
    $$('.opt', modal).forEach(x => x.setAttribute('aria-pressed', String(x === o)));
    data.need = o.dataset.v;
    $('#c-details').placeholder = NEEDS[data.need];
    $('#c-need-label').textContent = data.need;
    showStep(1);
  }));
  const err = (i, m) => { const el = $('.err', steps[i]); if (el) el.textContent = m; };
  const message = () => [
    `Hi Ahsan,`, ``,
    `I'm ${data.name}${data.org ? ' from ' + data.org : ''}. I'm reaching out about ${data.need.charAt(0).toLowerCase() + data.need.slice(1)}.`, ``,
    data.details, ``,
    data.where ? `Location / arrangement: ${data.where}` : '',
    data.when ? `Timeline: ${data.when}` : '',
    ``, `Best,`, data.name
  ].filter((l, i, a) => !(l === '' && a[i - 1] === '')).join('\n').trim();
  $$('[data-next]', modal).forEach(b => b.addEventListener('click', () => {
    if (si === 1) { data.details = $('#c-details').value.trim(); if (data.details.length < 10) return err(1, 'A sentence or two helps me reply well.'); err(1, ''); }
    if (si === 2) { data.where = $('#c-where').value.trim(); data.when = $('#c-when').value.trim(); }
    if (si === 3) {
      if ($('#c-trap').value) return; // bot
      data.name = $('#c-name').value.trim(); data.org = $('#c-org').value.trim();
      if (!data.name) return err(3, 'Please add your name.'); err(3, '');
      $('#c-preview').textContent = message();
    }
    showStep(si + 1);
  }));
  $$('[data-prev]', modal).forEach(b => b.addEventListener('click', () => showStep(Math.max(0, si - 1))));
  $('#c-send').addEventListener('click', async () => {
    const text = message();
    let ok = false;
    try { await navigator.clipboard.writeText(text); ok = true; } catch (e) {}
    $('#c-final').textContent = text;
    $('#c-copied').textContent = ok
      ? 'Your message is copied. LinkedIn has opened in a new tab: paste it into a message to Ahsan.'
      : 'LinkedIn has opened in a new tab. Copy the message below and paste it into a message to Ahsan.';
    showStep(5);
  });
}

/* ---------- start ---------- */
requestAnimationFrame(armReveals);
}
