from flask import Flask, jsonify
app = Flask(__name__)
# ─────────────────────────────────────────────
#  Shared shell: header + animated background
# ─────────────────────────────────────────────
SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
  --bg: #030b14;
  --surface: #071422;
  --glass: rgba(7,30,55,0.7);
  --border: rgba(0,200,255,0.12);
  --border-bright: rgba(0,200,255,0.35);
  --cyan: #00c8ff;
  --green: #00ffb0;
  --gold: #ffc94d;
  --coral: #ff6b5b;
  --text: #e8f4ff;
  --muted: #5a7fa0;
  --glow-cyan: 0 0 24px rgba(0,200,255,0.4);
  --glow-green: 0 0 24px rgba(0,255,176,0.4);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  min-height: 100vh;
  font-family: 'Syne', sans-serif;
  background: var(--bg);
  color: var(--text);
  overflow-x: hidden;
}

/* ── Animated starfield / grid background ── */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 10%, rgba(0,200,255,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 60% 80% at 80% 90%, rgba(0,255,176,0.05) 0%, transparent 60%),
    linear-gradient(90deg, rgba(0,200,255,0.03) 1px, transparent 1px) 0 0 / 48px 48px,
    linear-gradient(rgba(0,200,255,0.03) 1px, transparent 1px) 0 0 / 48px 48px;
  pointer-events: none;
  z-index: 0;
  animation: gridDrift 30s linear infinite;
}

@keyframes gridDrift {
  0%   { background-position: 0 0, 0 0, 0 0, 0 0; }
  100% { background-position: 0 0, 0 0, 48px 0, 0 48px; }
}

/* ── Floating particles ── */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(circle 2px at 15% 25%, rgba(0,200,255,0.6) 0%, transparent 100%),
    radial-gradient(circle 1.5px at 72% 18%, rgba(0,255,176,0.5) 0%, transparent 100%),
    radial-gradient(circle 2px at 88% 55%, rgba(255,201,77,0.4) 0%, transparent 100%),
    radial-gradient(circle 1px at 35% 75%, rgba(0,200,255,0.4) 0%, transparent 100%),
    radial-gradient(circle 2px at 60% 88%, rgba(0,255,176,0.5) 0%, transparent 100%);
  pointer-events: none;
  z-index: 0;
  animation: particleFloat 8s ease-in-out infinite alternate;
}

@keyframes particleFloat {
  0%   { transform: translateY(0px) translateX(0px); opacity: 0.6; }
  100% { transform: translateY(-18px) translateX(8px); opacity: 1; }
}

/* ── Navbar ── */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 48px;
  background: rgba(3,11,20,0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  animation: navSlide 0.7s cubic-bezier(.22,1,.36,1) both;
}

@keyframes navSlide {
  from { transform: translateY(-100%); opacity: 0; }
  to   { transform: translateY(0); opacity: 1; }
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  font-weight: 800;
  font-size: 18px;
  color: var(--text);
  letter-spacing: -0.5px;
}

.brand-mark {
  width: 40px; height: 40px;
  display: grid; place-items: center;
  border-radius: 10px;
  font-size: 13px; font-weight: 800;
  background: linear-gradient(135deg, var(--cyan), var(--green));
  color: #000;
  box-shadow: var(--glow-cyan);
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: var(--glow-cyan); }
  50% { box-shadow: 0 0 40px rgba(0,200,255,0.8); }
}

.nav-links {
  display: flex;
  gap: 4px;
  list-style: none;
}

.nav-links a {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  color: var(--muted);
  text-decoration: none;
  transition: color 0.2s, background 0.2s;
  font-family: 'JetBrains Mono', monospace;
}

.nav-links a:hover, .nav-links a.active {
  color: var(--cyan);
  background: rgba(0,200,255,0.08);
}

/* ── Generic page wrapper ── */
.page {
  position: relative;
  z-index: 1;
  padding-top: 88px;
  min-height: 100vh;
}

/* ── Buttons ── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  font-family: 'Syne', sans-serif;
  text-decoration: none;
  cursor: pointer;
  border: none;
  transition: transform 0.2s, box-shadow 0.2s;
  letter-spacing: 0.3px;
}

.btn:hover { transform: translateY(-3px); }

.btn-primary {
  background: linear-gradient(135deg, var(--cyan), #0090cc);
  color: #000;
  box-shadow: 0 8px 32px rgba(0,200,255,0.35);
}
.btn-primary:hover { box-shadow: 0 12px 48px rgba(0,200,255,0.55); }

.btn-outline {
  background: transparent;
  color: var(--cyan);
  border: 1px solid var(--border-bright);
}
.btn-outline:hover { background: rgba(0,200,255,0.08); box-shadow: var(--glow-cyan); }

/* ── Cards / Glass panels ── */
.card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 16px;
  backdrop-filter: blur(12px);
  transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s;
}

.card:hover {
  border-color: var(--border-bright);
  box-shadow: 0 0 32px rgba(0,200,255,0.12);
  transform: translateY(-4px);
}

/* ── Section eyebrow ── */
.eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--cyan);
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.eyebrow::before {
  content: '';
  width: 24px; height: 2px;
  background: var(--cyan);
  display: inline-block;
  box-shadow: var(--glow-cyan);
}

/* ── Animate on load ── */
.fade-up {
  opacity: 0;
  transform: translateY(30px);
  animation: fadeUp 0.8s cubic-bezier(.22,1,.36,1) forwards;
}

@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
.delay-5 { animation-delay: 0.5s; }
.delay-6 { animation-delay: 0.6s; }
.delay-7 { animation-delay: 0.7s; }
.delay-8 { animation-delay: 0.8s; }

/* ── Glow text ── */
.glow-text {
  background: linear-gradient(90deg, var(--cyan), var(--green), var(--cyan));
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 4s linear infinite;
}

@keyframes shimmer {
  to { background-position: 200% center; }
}

/* ── Status badge ── */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.badge-green { background: rgba(0,255,176,0.12); color: var(--green); border: 1px solid rgba(0,255,176,0.3); }
.badge-cyan  { background: rgba(0,200,255,0.12); color: var(--cyan);  border: 1px solid rgba(0,200,255,0.3); }
.badge-gold  { background: rgba(255,201,77,0.12); color: var(--gold);  border: 1px solid rgba(255,201,77,0.3); }

.dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: blink 1.5s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.2; }
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .nav { padding: 14px 20px; }
  .nav-links a { padding: 8px 12px; font-size: 12px; }
}
"""

SHARED_JS = """
// Smooth active nav link
document.querySelectorAll('.nav-links a').forEach(link => {
  if (link.href === window.location.href) link.classList.add('active');
});

// Intersection observer for scroll-reveal
const observer = new IntersectionObserver((entries) => {
  entries.forEach(el => {
    if (el.isIntersecting) {
      el.target.style.animationPlayState = 'running';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('[data-reveal]').forEach(el => {
  el.style.animationPlayState = 'paused';
  observer.observe(el);
});

// Typewriter effect
function typeWriter(el, text, speed = 45) {
  let i = 0;
  el.textContent = '';
  const timer = setInterval(() => {
    if (i < text.length) {
      el.textContent += text[i++];
    } else {
      clearInterval(timer);
    }
  }, speed);
}

document.querySelectorAll('[data-type]').forEach(el => {
  typeWriter(el, el.dataset.type);
});
"""

def shell(title, active, body_html, extra_css="", extra_js=""):
    active_map = {"home": 0, "about": 1, "contact": 2}
    links = [
    ('<a href="/">Home</a>', 'home'),
    ('<a href="/about">About</a>', 'about'),
    ('<a href="/contact">Contact</a>', 'contact'),
  ]
    nav_items = ""
    for label, key in links:
        cls = ' class="active"' if active == key else ''
        nav_items += f'<li><a href="/{key if key != "home" else ""}"{cls}>{label}</a></li>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title} | VS DevOps</title>
  <style>{SHARED_CSS}{extra_css}</style>
</head>
<body>

<nav class="nav">
  <a class="brand" href="/">
    <span class="brand-mark">VS</span>
    <span>Veera Sir Cloud DevOps Engineer AIOPS MLOPS</span>
  </a>

  <ul class="nav-links">
    <li><a href="/" {'class="active"' if active == 'home' else ''}>Home</a></li>
    <li><a href="/about" {'class="active"' if active == 'about' else ''}>About</a></li>
    <li><a href="/contact" {'class="active"' if active == 'contact' else ''}>Contact</a></li>
  </ul>
</nav>

{body_html}

<script>{SHARED_JS}{extra_js}</script>
</body>
</html>"""


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
HOME_CSS = """
.hero {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 40px 60px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  min-height: calc(100vh - 88px);
}

.hero-eyebrow { margin-bottom: 20px; }

h1.hero-title {
  font-size: clamp(44px, 6vw, 80px);
  font-weight: 800;
  line-height: 0.95;
  letter-spacing: -2px;
  margin-bottom: 24px;
}

.hero-sub {
  font-size: 18px;
  line-height: 1.7;
  color: var(--muted);
  max-width: 480px;
  margin-bottom: 36px;
}

.hero-actions { display: flex; gap: 14px; flex-wrap: wrap; }

/* ── Pipeline Visual ── */
.ops-panel {
  padding: 28px;
  position: relative;
  overflow: hidden;
}

.ops-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(0,200,255,0.04) 1px, transparent 1px) 0 0 / 30px 30px,
    linear-gradient(rgba(0,200,255,0.04) 1px, transparent 1px) 0 0 / 30px 30px;
  pointer-events: none;
}

.cloud-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 18px;
  position: relative; z-index: 1;
}

.cloud-tag {
  padding: 14px;
  border-radius: 10px;
  text-align: center;
  font-weight: 800;
  font-size: 13px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 2px;
  border: 1px solid;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s;
}

.cloud-tag:hover { transform: scale(1.05); }

.cloud-tag::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.06) 50%, transparent 70%);
  animation: tagSheen 3s linear infinite;
}

@keyframes tagSheen {
  0% { transform: translateX(-100%) rotate(45deg); }
  100% { transform: translateX(100%) rotate(45deg); }
}

.cloud-tag.aws  { color: var(--gold);  border-color: rgba(255,201,77,0.35); background: rgba(255,201,77,0.08); }
.cloud-tag.az   { color: var(--cyan);  border-color: rgba(0,200,255,0.35);  background: rgba(0,200,255,0.08); }
.cloud-tag.gcp  { color: var(--coral); border-color: rgba(255,107,91,0.35); background: rgba(255,107,91,0.08); }

/* ── Pipeline stages ── */
.pipeline-row {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 18px;
  position: relative; z-index: 1;
  background: rgba(0,0,0,0.3);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  overflow: hidden;
}

.pipeline-progress {
  position: absolute;
  bottom: 0; left: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--cyan), var(--green));
  box-shadow: var(--glow-cyan);
  animation: progress 4s ease-in-out infinite;
}

@keyframes progress {
  0%   { width: 0%;   opacity: 1; }
  80%  { width: 100%; opacity: 1; }
  100% { width: 100%; opacity: 0; }
}

.stage {
  flex: 1;
  text-align: center;
  padding: 10px 6px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 1px;
  text-transform: uppercase;
  position: relative;
  transition: all 0.3s;
}

.stage-arrow {
  color: var(--muted);
  font-size: 16px;
  padding: 0 2px;
  flex-shrink: 0;
}

.stage.done  { color: var(--green); background: rgba(0,255,176,0.12); }
.stage.run   { color: #000; background: var(--cyan); box-shadow: var(--glow-cyan); animation: stageGlow 1s ease-in-out infinite alternate; }
.stage.idle  { color: var(--muted); background: rgba(255,255,255,0.04); }
.stage.ok    { color: #000; background: var(--green); box-shadow: var(--glow-green); }

@keyframes stageGlow {
  from { box-shadow: var(--glow-cyan); }
  to   { box-shadow: 0 0 40px rgba(0,200,255,0.9); }
}

/* ── Stats row ── */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  position: relative; z-index: 1;
}

.stat-box {
  padding: 18px;
  border-radius: 12px;
  text-align: center;
  background: rgba(0,0,0,0.3);
  border: 1px solid var(--border);
}

.stat-num {
  display: block;
  font-size: 28px;
  font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-num.c { color: var(--cyan); }
.stat-num.g { color: var(--green); }
.stat-num.o { color: var(--gold); }

.stat-lbl { font-size: 11px; color: var(--muted); font-weight: 700; letter-spacing: 1px; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; }

/* ── Features section ── */
.features {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 40px;
  position: relative; z-index: 1;
}

.section-head {
  margin-bottom: 48px;
}

.section-head h2 {
  font-size: clamp(32px, 4vw, 52px);
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.05;
  margin-bottom: 16px;
}

.section-head p {
  color: var(--muted);
  font-size: 17px;
  line-height: 1.7;
  max-width: 600px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.feature-card {
  padding: 28px;
  position: relative;
  overflow: hidden;
}

.feature-card::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.feature-card:hover::after { transform: scaleX(1); }

.feature-card:nth-child(1)::after { background: var(--green); }
.feature-card:nth-child(2)::after { background: var(--cyan); }
.feature-card:nth-child(3)::after { background: var(--coral); }
.feature-card:nth-child(4)::after { background: var(--gold); }

.fi {
  width: 48px; height: 48px;
  display: grid; place-items: center;
  border-radius: 12px;
  margin-bottom: 20px;
  font-size: 22px;
}

.fi-1 { background: rgba(0,255,176,0.12); box-shadow: 0 0 20px rgba(0,255,176,0.2); }
.fi-2 { background: rgba(0,200,255,0.12); box-shadow: 0 0 20px rgba(0,200,255,0.2); }
.fi-3 { background: rgba(255,107,91,0.12); box-shadow: 0 0 20px rgba(255,107,91,0.2); }
.fi-4 { background: rgba(255,201,77,0.12); box-shadow: 0 0 20px rgba(255,201,77,0.2); }

.feature-card h3 {
  font-size: 17px;
  font-weight: 800;
  margin-bottom: 10px;
  letter-spacing: -0.3px;
}

.feature-card p {
  font-size: 14px;
  line-height: 1.65;
  color: var(--muted);
}

/* ── Flow section ── */
.flow-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 40px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: start;
  position: relative; z-index: 1;
  border-top: 1px solid var(--border);
}

.flow-section h2 {
  font-size: clamp(28px, 3.5vw, 44px);
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 16px;
}

.flow-section > div > p {
  color: var(--muted);
  font-size: 16px;
  line-height: 1.7;
}

.timeline {
  list-style: none;
  display: grid;
  gap: 12px;
}

.tl-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  border-radius: 12px;
  background: var(--glass);
  border: 1px solid var(--border);
  transition: border-color 0.3s, transform 0.3s;
  animation: fadeUp 0.6s cubic-bezier(.22,1,.36,1) both;
}

.tl-item:hover {
  border-color: var(--border-bright);
  transform: translateX(6px);
}

.tl-num {
  width: 40px; height: 40px;
  flex-shrink: 0;
  display: grid; place-items: center;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
  background: rgba(0,200,255,0.1);
  color: var(--cyan);
  border: 1px solid rgba(0,200,255,0.3);
}

.tl-text {
  font-size: 14px;
  font-weight: 700;
  line-height: 1.5;
}

/* ── CTA banner ── */
.cta-banner {
  max-width: 1200px;
  margin: 0 auto 80px;
  padding: 0 40px;
  position: relative; z-index: 1;
}

.cta-inner {
  padding: 56px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(0,200,255,0.08), rgba(0,255,176,0.05));
  border: 1px solid var(--border-bright);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  flex-wrap: wrap;
  position: relative;
  overflow: hidden;
}

.cta-inner::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 200px; height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,200,255,0.15) 0%, transparent 70%);
  pointer-events: none;
}

.cta-inner h2 {
  font-size: clamp(24px, 3vw, 38px);
  font-weight: 800;
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}

.cta-inner p { color: var(--muted); font-size: 16px; line-height: 1.6; max-width: 480px; }

@media (max-width: 900px) {
  .hero, .flow-section { grid-template-columns: 1fr; gap: 40px; }
  .feature-grid { grid-template-columns: repeat(2, 1fr); }
  .hero { padding: 40px 20px 60px; }
  .features, .flow-section, .cta-banner { padding-left: 20px; padding-right: 20px; }
  .stats-row { grid-template-columns: repeat(3, 1fr); }
}
"""

HOME_JS = """
// Counter animation
function animateCounter(el, target, suffix='') {
  let start = 0;
  const duration = 1800;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const val = Math.round(eased * target);
    el.textContent = val + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const nums = document.querySelectorAll('.stat-num[data-count]');
const countObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const el = e.target;
      animateCounter(el, +el.dataset.count, el.dataset.suffix || '');
      countObserver.unobserve(el);
    }
  });
});
nums.forEach(n => countObserver.observe(n));

// Pipeline stage cycling
const stages = document.querySelectorAll('.stage');
const states = ['done','done','run','idle','idle'];
let offset = 0;
setInterval(() => {
  offset = (offset + 1) % stages.length;
  stages.forEach((s, i) => {
    s.className = 'stage';
    const idx = (i - offset + stages.length) % stages.length;
    if (idx < 2) s.classList.add('done');
    else if (idx === 2) s.classList.add('run');
    else if (idx === stages.length - 1) s.classList.add('ok');
    else s.classList.add('idle');
  });
}, 1200);
"""

HOME_HTML = """
<div class="page">
  <section class="hero">
    <div>
      <div class="eyebrow hero-eyebrow fade-up">
        <span class="dot"></span>
        AI-Powered · AWS · Azure · GCP
      </div>
      <h1 class="hero-title fade-up delay-1">
        Hybridcloud <br>
        <span class="glow-text">Devops</span><br>
        CiCD By Veera sir
      </h1>
      <p class="hero-sub fade-up delay-2">
        Build, scan, deploy, observe and recover modern cloud applications
        with an AI-powered CI/CD pipeline designed for real production confidence.
      </p>
      <div class="hero-actions fade-up delay-3">
        <a class="btn btn-primary" href="/about">⚡ Explore Platform</a>
        <a class="btn btn-outline" href="/contact">Start Learning →</a>
      </div>
    </div>

    <div class="card ops-panel fade-up delay-4">
      <div class="cloud-bar">
        <div class="cloud-tag aws">☁ AWS</div>
        <div class="cloud-tag az">☁ Azure</div>
        <div class="cloud-tag gcp">☁ GCP</div>
      </div>

      <div class="pipeline-row">
        <div class="pipeline-progress"></div>
        <div class="stage done">Code</div>
        <div class="stage-arrow">›</div>
        <div class="stage done">Build</div>
        <div class="stage-arrow">›</div>
        <div class="stage run">Scan</div>
        <div class="stage-arrow">›</div>
        <div class="stage idle">Deploy</div>
        <div class="stage-arrow">›</div>
        <div class="stage ok">Live</div>
      </div>

      <div class="stats-row">
        <div class="stat-box">
          <span class="stat-num c" data-count="99" data-suffix=".9%">0</span>
          <div class="stat-lbl">Uptime</div>
        </div>
        <div class="stat-box">
          <span class="stat-num g" data-count="4" data-suffix=" AI">0</span>
          <div class="stat-lbl">Agents</div>
        </div>
        <div class="stat-box">
          <span class="stat-num o" data-count="24" data-suffix="×7">0</span>
          <div class="stat-lbl">Monitor</div>
        </div>
      </div>
    </div>
  </section>

  <section class="features">
    <div class="section-head fade-up">
      <div class="eyebrow">Platform Capabilities</div>
      <h2>Next-Generation DevSecOps:<br> Harness CI/CD with Automated Analysis Agents</h2>
      <p>Four AI agents handle review, security, observability, and risk — so your team ships with confidence.</p>
    </div>

    <div class="feature-grid">
      <article class="card feature-card fade-up delay-1" data-reveal>
        <div class="fi fi-1">🤖</div>
        <h3>AI Code Review</h3>
        <p>Review commits for quality, maintainability, risky patterns, and release readiness.</p>
      </article>
      <article class="card feature-card fade-up delay-2" data-reveal>
        <div class="fi fi-2">🔐</div>
        <h3>Security Scan</h3>
        <p>Check application changes for vulnerable code, secrets, and unsafe deployment choices.</p>
      </article>
      <article class="card feature-card fade-up delay-3" data-reveal>
        <div class="fi fi-3">📊</div>
        <h3>Log Analysis</h3>
        <p>Use AI to summarize runtime logs, highlight failures, and guide faster troubleshooting.</p>
      </article>
      <article class="card feature-card fade-up delay-4" data-reveal>
        <div class="fi fi-4">⚠️</div>
        <h3>Deployment Risk</h3>
        <p>Estimate release impact before production and prepare rollback recovery when needed.</p>
      </article>
    </div>
  </section>

  <section class="flow-section">
    <div class="fade-up">
      <div class="eyebrow">Delivery Flow</div>
      <h2>From GitHub commit to healthy multicloud release</h2>
      <p>The pipeline combines GitHub Actions, cloud deployment, health checks, security review,
      and observability so teams can move quickly without losing control.</p>
    </div>

    <ol class="timeline">
      <li class="tl-item delay-1">
        <div class="tl-num">01</div>
        <div class="tl-text">Commit code and trigger CI/CD automation</div>
      </li>
      <li class="tl-item delay-2">
        <div class="tl-num">02</div>
        <div class="tl-text">Run AI review, security checks, and build validation</div>
      </li>
      <li class="tl-item delay-3">
        <div class="tl-num">03</div>
        <div class="tl-text">Deploy to cloud infrastructure with health verification</div>
      </li>
      <li class="tl-item delay-4">
        <div class="tl-num">04</div>
        <div class="tl-text">Monitor logs, detect risk, and recover fast</div>
      </li>
    </ol>
  </section>

  <div class="cta-banner">
    <div class="cta-inner">
      <div>
        <h2>Ready to level up your<br>cloud DevOps skills?</h2>
        <p>Hands-on learning with real pipelines across AWS, Azure, and GCP.</p>
      </div>
      <a class="btn btn-primary" href="/contact">Get in Touch →</a>
    </div>
  </div>
</div>
"""


# ─────────────────────────────────────────────
#  ABOUT
# ─────────────────────────────────────────────
ABOUT_CSS = """
.about-wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 80px 40px;
  position: relative; z-index: 1;
}

.about-hero {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 80px;
  align-items: start;
  margin-bottom: 80px;
  padding-bottom: 80px;
  border-bottom: 1px solid var(--border);
}

.about-hero h1 {
  font-size: clamp(40px, 5vw, 68px);
  font-weight: 800;
  letter-spacing: -2px;
  line-height: 0.97;
  margin-bottom: 24px;
}

.about-hero p {
  font-size: 17px;
  line-height: 1.75;
  color: var(--muted);
  margin-bottom: 16px;
}

.about-stats {
  display: grid;
  gap: 14px;
}

.a-stat {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-radius: 12px;
  background: var(--glass);
  border: 1px solid var(--border);
  transition: border-color 0.3s, transform 0.3s;
}

.a-stat:hover {
  border-color: var(--border-bright);
  transform: translateX(6px);
}

.a-stat-label {
  font-size: 14px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  color: var(--muted);
  letter-spacing: 0.5px;
}

.a-stat-value {
  font-size: 15px;
  font-weight: 800;
}

.stack-section {
  margin-bottom: 80px;
}

.stack-section h2 {
  font-size: clamp(28px, 3.5vw, 44px);
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 36px;
}

.stack-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.stack-card {
  padding: 28px;
  border-radius: 16px;
  position: relative;
  overflow: hidden;
}

.stack-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}

.stack-card:nth-child(1)::before { background: linear-gradient(90deg, var(--gold), var(--coral)); }
.stack-card:nth-child(2)::before { background: linear-gradient(90deg, var(--cyan), #0070ff); }
.stack-card:nth-child(3)::before { background: linear-gradient(90deg, var(--green), #00c0a0); }

.stack-card h3 {
  font-size: 16px;
  font-weight: 800;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.stack-card ul {
  list-style: none;
  display: grid;
  gap: 8px;
}

.stack-card li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-family: 'JetBrains Mono', monospace;
  color: var(--muted);
}

.stack-card li::before {
  content: '▸';
  color: var(--cyan);
  font-size: 10px;
}

.about-mission {
  padding: 56px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(0,200,255,0.06), rgba(0,255,176,0.04));
  border: 1px solid var(--border-bright);
  text-align: center;
}

.about-mission h2 {
  font-size: clamp(24px, 3vw, 38px);
  font-weight: 800;
  letter-spacing: -0.5px;
  margin-bottom: 16px;
}

.about-mission p {
  font-size: 17px;
  line-height: 1.75;
  color: var(--muted);
  max-width: 640px;
  margin: 0 auto 28px;
}

@media (max-width: 900px) {
  .about-hero, .stack-grid { grid-template-columns: 1fr; }
  .about-wrap { padding: 40px 20px; }
  .about-mission { padding: 36px 24px; }
}
"""

ABOUT_HTML = """
<div class="page">
  <div class="about-wrap">
    <section class="about-hero">
      <div class="fade-up">
        <div class="eyebrow">About the Project</div>
        <h1>Practical AI DevOps for<br><span class="glow-text">modern multicloud</span><br>teams</h1>
        <p>
          This project demonstrates how a production-style CI/CD website can use AI agents for code
          review, security checks, log analysis, deployment risk signals, health checks, and rollback recovery.
        </p>
        <p>
          Built to show clear DevOps fundamentals while looking polished enough for a live demo,
          classroom session, or portfolio presentation.
        </p>
        <div style="display:flex;gap:12px;margin-top:28px;flex-wrap:wrap;">
          <span class="badge badge-green"><span class="dot"></span>Live Demo Ready</span>
          <span class="badge badge-cyan">Production Grade</span>
          <span class="badge badge-gold">AI Powered</span>
        </div>
      </div>

      <div class="about-stats fade-up delay-2">
        <div class="a-stat">
          <span class="a-stat-label">Cloud Platforms</span>
          <span class="a-stat-value" style="color:var(--gold)">AWS · Azure · GCP</span>
        </div>
        <div class="a-stat">
          <span class="a-stat-label">Automation</span>
          <span class="a-stat-value" style="color:var(--cyan)">GitHub Actions</span>
        </div>
        <div class="a-stat">
          <span class="a-stat-label">AI Agents</span>
          <span class="a-stat-value" style="color:var(--green)">4 Active</span>
        </div>
        <div class="a-stat">
          <span class="a-stat-label">Pipeline Stages</span>
          <span class="a-stat-value" style="color:var(--coral)">5 Steps</span>
        </div>
        <div class="a-stat">
          <span class="a-stat-label">Monitoring</span>
          <span class="a-stat-value">24 × 7</span>
        </div>
        <div class="a-stat">
          <span class="a-stat-label">Uptime Target</span>
          <span class="a-stat-value" style="color:var(--green)">99.9%</span>
        </div>
      </div>
    </section>

    <section class="stack-section fade-up">
      <div class="eyebrow">Tech Stack</div>
      <h2>Built on battle-tested tools</h2>
      <div class="stack-grid">
        <div class="card stack-card">
          <h3>☁️ Cloud Platforms</h3>
          <ul>
            <li>AWS EC2 / ECS / Lambda</li>
            <li>Azure App Service / AKS</li>
            <li>GCP Cloud Run / GKE</li>
            <li>S3 / Blob / GCS Storage</li>
            <li>CloudWatch / Monitor</li>
          </ul>
        </div>
        <div class="card stack-card">
          <h3>⚙️ CI/CD & Automation</h3>
          <ul>
            <li>GitHub Actions Workflows</li>
            <li>Docker / Kubernetes</li>
            <li>Terraform IaC</li>
            <li>Ansible Playbooks</li>
            <li>ArgoCD / Flux GitOps</li>
          </ul>
        </div>
        <div class="card stack-card">
          <h3>🤖 AI & Security</h3>
          <ul>
            <li>Claude AI Code Review</li>
            <li>SAST / DAST Scanning</li>
            <li>Trivy / Snyk / SonarQube</li>
            <li>Log Anomaly Detection</li>
            <li>Risk Scoring Engine</li>
          </ul>
        </div>
      </div>
    </section>

    <div class="about-mission fade-up">
      <div class="eyebrow" style="justify-content:center">Mission</div>
      <h2>Making DevOps accessible<br>for every cloud engineer</h2>
      <p>
        This platform is designed to bridge the gap between theory and real-world cloud operations.
        Every feature demonstrates a practical pattern you can use in production environments today.
      </p>
      <a class="btn btn-primary" href="/contact">Connect with Veera Sir →</a>
    </div>
  </div>
</div>
"""


# ─────────────────────────────────────────────
#  CONTACT
# ─────────────────────────────────────────────
CONTACT_CSS = """
.contact-wrap {
  max-width: 900px;
  margin: 0 auto;
  padding: 80px 40px;
  position: relative; z-index: 1;
  min-height: calc(100vh - 88px);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.contact-wrap h1 {
  font-size: clamp(40px, 5.5vw, 72px);
  font-weight: 800;
  letter-spacing: -2px;
  line-height: 0.97;
  margin-bottom: 20px;
}

.contact-wrap > p {
  font-size: 18px;
  line-height: 1.7;
  color: var(--muted);
  max-width: 560px;
  margin-bottom: 48px;
}

.contact-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 48px;
}

.contact-card {
  padding: 28px 24px;
  border-radius: 16px;
  text-decoration: none;
  color: var(--text);
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.contact-card:hover {
  transform: translateY(-6px);
}

.contact-card::after {
  content: '→';
  position: absolute;
  bottom: 20px; right: 20px;
  font-size: 18px;
  opacity: 0;
  transition: opacity 0.3s, transform 0.3s;
  transform: translateX(-6px);
}

.contact-card:hover::after {
  opacity: 1;
  transform: translateX(0);
}

.cc-icon {
  font-size: 28px;
  width: 52px; height: 52px;
  display: grid; place-items: center;
  border-radius: 12px;
}

.cc-icon-1 { background: rgba(0,200,255,0.12); }
.cc-icon-2 { background: rgba(0,255,176,0.12); }
.cc-icon-3 { background: rgba(255,201,77,0.12); }

.contact-card h3 {
  font-size: 16px;
  font-weight: 800;
  margin-bottom: 4px;
}

.contact-card span {
  font-size: 13px;
  color: var(--muted);
  font-family: 'JetBrains Mono', monospace;
}

.back-home {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  color: var(--muted);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  transition: color 0.2s;
}

.back-home:hover { color: var(--cyan); }

.terminal-block {
  margin-bottom: 40px;
  padding: 24px 28px;
  border-radius: 12px;
  background: rgba(0,0,0,0.5);
  border: 1px solid var(--border);
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  line-height: 1.8;
  position: relative;
}

.terminal-block::before {
  content: '● ● ●';
  display: block;
  color: var(--muted);
  font-size: 10px;
  letter-spacing: 4px;
  margin-bottom: 12px;
}

.t-prompt { color: var(--green); }
.t-cmd    { color: var(--cyan); }
.t-out    { color: var(--muted); }
.t-cursor {
  display: inline-block;
  width: 8px; height: 16px;
  background: var(--cyan);
  animation: blink 1s step-end infinite;
  vertical-align: text-bottom;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

@media (max-width: 700px) {
  .contact-cards { grid-template-columns: 1fr; }
  .contact-wrap { padding: 40px 20px; }
}
"""

CONTACT_HTML = """
<div class="page">
  <div class="contact-wrap">
    <div class="eyebrow fade-up">Contact</div>
    <h1 class="fade-up delay-1">
      Ready to build your<br>
      <span class="glow-text">DevOps pipeline?</span>
    </h1>
    <p class="fade-up delay-2">
      Connect for multicloud DevOps learning, project demos, CI/CD setup,
      and AI-powered deployment automation guidance.
    </p>

    <div class="terminal-block fade-up delay-3">
      <div><span class="t-prompt">veera@devops</span><span style="color:var(--muted)">:~$</span> <span class="t-cmd">reach --out --channels all</span></div>
      <div class="t-out">✓ Email channel ready</div>
      <div class="t-out">✓ LinkedIn channel ready</div>
      <div class="t-out">✓ GitHub channel ready</div>
      <div><span class="t-cursor"></span></div>
    </div>

    <div class="contact-cards fade-up delay-4">
      <a class="card contact-card" href="mailto:veerasir">
        <div class="cc-icon cc-icon-1">📧</div>
        <h3>Email</h3>
        <span>veerasirops</span>
      </a>
      <a class="card contact-card" href="/">
        <div class="cc-icon cc-icon-2">💼</div>
        <h3>LinkedIn</h3>
        <span>Veera Sir DevOps</span>
      </a>
      <a class="card contact-card" href="/">
        <div class="cc-icon cc-icon-3">🐙</div>
        <h3>GitHub</h3>
        <span>@veerasir-devops</span>
      </a>
    </div>

    <a class="back-home fade-up delay-5" href="/">← back to home</a>
  </div>
</div>
"""


# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────
@app.route("/")
def home():
    return shell("Home", "home", HOME_HTML, HOME_CSS, HOME_JS)

@app.route("/about")
def about():
    return shell("About", "about", ABOUT_HTML, ABOUT_CSS)

@app.route("/contact")
def contact():
    return shell("Contact", "contact", CONTACT_HTML, CONTACT_CSS)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "message": "Website running successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)