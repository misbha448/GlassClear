<script>
  import { t } from '$lib/state.svelte.js';

  function safeText(value, fallback = '') {
    if (typeof value === 'string') return value;
    if (value && typeof value === 'object') {
      return value.label || value.title || value.name || fallback;
    }
    return fallback;
  }

  function labelFor(key, fallback) {
    const value = t(key);
    return typeof value === 'string' && value !== key ? value : fallback;
  }

  const navLinks = [
    { labelKey: 'footer.home', fallback: 'Home', href: '/' },
    { labelKey: 'common.howItWorks', fallback: 'How It Works', href: '#how-it-works' },
    { labelKey: 'common.seeItInAction', fallback: 'See It in Action', href: '#demo' },
    { labelKey: 'common.faq', fallback: 'FAQ', href: '#faq' },
    { labelKey: 'footer.dashboard', fallback: 'Dashboard', href: '/dashboard' }
  ];

  const socialLinks = [
    { label: 'X / Twitter', href: '#!', icon: 'bi-twitter-x' },
    { label: 'Instagram', href: '#!', icon: 'bi-instagram' },
    { label: 'LinkedIn', href: '#!', icon: 'bi-linkedin' },
    { label: 'GitHub', href: '#!', icon: 'bi-github' }
  ];

  let email = $state('');
  let subscribed = $state(false);

  function handleSubscribe(e) {
    e.preventDefault();
    if (email.trim()) {
      subscribed = true;
      email = '';
      setTimeout(() => (subscribed = false), 3000);
    }
  }
</script>

<footer class="gc-footer">
  <div class="gc-footer__noise" aria-hidden="true"></div>

  <div class="gc-footer__container">

    <!-- Top gradient rule -->
    <div class="gc-footer__rule"></div>

    <!-- ── TOP GRID ─────────────────────────────────── -->
    <div class="gc-footer__grid">

      <!-- COL 1 · Contact -->
      <div class="gc-footer__col" style="--delay:0s">
        <div class="gc-footer__contact-block">
          <span class="gc-footer__label">{labelFor('footer.email', 'EMAIL')}</span>
          <a href="mailto:hello@glassclear.ai" class="gc-footer__contact-link">
            hello@glassclear.ai
          </a>
        </div>
        <div class="gc-footer__contact-block">
          <span class="gc-footer__label">{labelFor('footer.support', 'SUPPORT')}</span>
          <a href="tel:+919876543210" class="gc-footer__contact-link">
            +91 98765 43210
          </a>
        </div>
      </div>

      <!-- COL 2 · Links -->
      <div class="gc-footer__col" style="--delay:0.08s">
        <span class="gc-footer__label">{labelFor('footer.links', 'LINKS')}</span>
        <nav class="gc-footer__nav">
          {#each navLinks as link, i}
            <a href={link.href} class="gc-footer__nav-link" style="--i:{i}">
              <span class="gc-footer__arrow" aria-hidden="true">↗</span>
              {labelFor(link.labelKey, link.fallback)}
            </a>
          {/each}
        </nav>
      </div>

      <!-- COL 3 · Socials -->
      <div class="gc-footer__col" style="--delay:0.16s">
        <span class="gc-footer__label">{labelFor('footer.socials', 'SOCIALS')}</span>
        <nav class="gc-footer__nav">
          {#each socialLinks as link, i}
            <a href={link.href} class="gc-footer__nav-link" style="--i:{i}" aria-label={link.label}>
              <span class="gc-footer__arrow" aria-hidden="true">↗</span>
              {link.label}
            </a>
          {/each}
        </nav>
      </div>

      <!-- COL 4 · Newsletter -->
      <div class="gc-footer__col gc-footer__col--news" style="--delay:0.24s">
        <span class="gc-footer__label">{labelFor('footer.newsletter', 'NEWSLETTER')}</span>
        <h3 class="gc-footer__news-heading">{labelFor('footer.heading', 'Stay updated with GlassClear')}</h3>
        <p class="gc-footer__news-body">
          {labelFor('footer.body', 'Get updates on AI restoration, reflection removal, and architectural imaging workflows.')}
        </p>
        <form class="gc-footer__form" onsubmit={handleSubscribe} novalidate>
          <input
            type="email"
            bind:value={email}
            placeholder={labelFor('footer.inputPlaceholder', 'Enter email address')}
            class="gc-footer__input"
            aria-label={labelFor('common.email', 'Email')}
          />
          <button type="submit" class="gc-footer__btn" class:gc-footer__btn--done={subscribed}>
            {subscribed ? `✓ ${labelFor('footer.subscribed', 'Subscribed!')}` : labelFor('footer.subscribe', 'SUBSCRIBE')}
          </button>
        </form>
      </div>

    </div>
    <!-- /TOP GRID -->

    <!-- ── BRAND ZONE ──────────────────────────────── -->
    <div class="gc-footer__brand-zone">
      <div class="gc-footer__brand-rule"></div>

      <div class="gc-footer__brand-row">

        <!-- Wordmark split into two spans so letter-spacing differs per half -->
        <div class="gc-footer__wordmark-wrap">
          <p class="gc-footer__wordmark" aria-label="GlassClear">
            <span class="gc-wm__glass">Glass</span><span class="gc-wm__clear">Clear</span>
          </p>
        </div>

        <div class="gc-footer__tagline-wrap">
          <p class="gc-footer__tagline">
            {labelFor('footer.taglineLine1', 'Beyond Reflections.')}<br />{labelFor('footer.taglineLine2', 'Built for Clarity.')}
          </p>
          <div class="gc-footer__tagline-accent"></div>
        </div>

      </div>

      <!-- Bottom bar -->
      <div class="gc-footer__bottom">
        <span class="gc-footer__copy">{labelFor('footer.copyright', '© 2026 GlassClear AI. All rights reserved.')}</span>
        <div class="gc-footer__legal">
          <a href="/privacy" class="gc-footer__legal-link">{labelFor('footer.privacy', 'Privacy Policy')}</a>
          <span class="gc-footer__dot" aria-hidden="true">·</span>
          <a href="/terms" class="gc-footer__legal-link">{labelFor('footer.terms', 'Terms of Service')}</a>
        </div>
      </div>

    </div>
    <!-- /BRAND ZONE -->

  </div>
</footer>

<style>
  /* ── Reset ──────────────────────────────────────────────── */
  .gc-footer *,
  .gc-footer *::before,
  .gc-footer *::after {
    box-sizing: border-box;
  }

  /* ── Shell ──────────────────────────────────────────────── */
  .gc-footer {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
      175deg,
      rgba(255, 255, 255, 0.98) 0%,
      rgba(238, 242, 255, 0.99) 60%,
      rgba(224, 231, 255, 1) 100%
    );
    border-top: 1px solid rgba(99, 102, 241, 0.13);
    font-family: 'DM Sans', 'Inter', system-ui, sans-serif;
  }

  /* Subtle noise */
  .gc-footer__noise {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  }

  /* ── Container ──────────────────────────────────────────── */
  .gc-footer__container {
    position: relative;
    z-index: 1;
    max-width: 1480px;
    margin: 0 auto;
    padding: 64px 52px 32px;
  }

  /* ── Top rule ───────────────────────────────────────────── */
  .gc-footer__rule {
    height: 1px;
    margin-bottom: 52px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(99, 102, 241, 0.32) 28%,
      rgba(139, 92, 246, 0.32) 72%,
      transparent 100%
    );
    animation: rulePulse 5s ease-in-out infinite alternate;
  }

  @keyframes rulePulse {
    from { opacity: 0.65; }
    to   { opacity: 1; }
  }

  /* ── Grid ───────────────────────────────────────────────── */
  .gc-footer__grid {
    display: grid;
    grid-template-columns: 1.1fr 0.85fr 0.85fr 1.2fr;
    gap: 52px;
    align-items: start;
  }

  /* Staggered fade-up per column */
  .gc-footer__col {
    animation: colFadeUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
    animation-delay: var(--delay, 0s);
  }

  @keyframes colFadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* ── Labels ─────────────────────────────────────────────── */
  .gc-footer__label {
    display: block;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.22em;
    color: #6366f1;
    text-transform: uppercase;
    margin-bottom: 18px;
  }

  /* ── Contact ─────────────────────────────────────────────── */
  .gc-footer__contact-block {
    margin-bottom: 30px;
  }

  .gc-footer__contact-block:last-child {
    margin-bottom: 0;
  }

  .gc-footer__contact-link {
    display: inline-block;
    margin-top: 4px;
    font-size: 0.98rem;
    font-weight: 700;
    color: #1e1b4b;
    text-decoration: none;
    position: relative;
    transition: color 0.22s ease;
  }

  .gc-footer__contact-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 1.5px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border-radius: 2px;
    transition: width 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .gc-footer__contact-link:hover {
    color: #4f46e5;
  }

  .gc-footer__contact-link:hover::after {
    width: 100%;
  }

  /* ── Nav links ───────────────────────────────────────────── */
  .gc-footer__nav {
    display: flex;
    flex-direction: column;
    gap: 1px;
  }

  .gc-footer__nav-link {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: clamp(16px, 1.55vw, 21px);
    font-weight: 700;
    color: #1e1b4b;
    text-decoration: none;
    padding: 5px 0;
    letter-spacing: -0.015em;
    transition:
      color 0.2s ease,
      transform 0.24s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .gc-footer__arrow {
    font-size: 12px;
    color: #818cf8;
    opacity: 0;
    transform: translate(-5px, 2px);
    transition:
      opacity 0.2s ease,
      transform 0.24s cubic-bezier(0.22, 1, 0.36, 1);
    flex-shrink: 0;
    line-height: 1;
  }

  .gc-footer__nav-link:hover {
    color: #4f46e5;
    transform: translateX(7px);
  }

  .gc-footer__nav-link:hover .gc-footer__arrow {
    opacity: 1;
    transform: translate(0, 0);
  }

  /* ── Newsletter card ─────────────────────────────────────── */
  .gc-footer__col--news {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.14);
    border-radius: 20px;
    padding: 26px 24px 24px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
  }

  .gc-footer__col--news:hover {
    box-shadow: 0 12px 48px rgba(99, 102, 241, 0.12);
    border-color: rgba(99, 102, 241, 0.22);
  }

  .gc-footer__news-heading {
    margin: 0 0 10px;
    font-size: 1.1rem;
    font-weight: 800;
    color: #1e1b4b;
    line-height: 1.3;
    letter-spacing: -0.025em;
  }

  .gc-footer__news-body {
    margin: 0 0 20px;
    font-size: 0.855rem;
    color: #64748b;
    line-height: 1.7;
  }

  .gc-footer__form {
    display: flex;
    flex-direction: column;
    gap: 9px;
  }

  .gc-footer__input {
    width: 100%;
    padding: 10px 16px;
    font-size: 0.86rem;
    font-weight: 500;
    color: #1e1b4b;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 100px;
    outline: none;
    transition: border-color 0.22s ease, box-shadow 0.22s ease;
  }

  .gc-footer__input::placeholder {
    color: #94a3b8;
  }

  .gc-footer__input:focus {
    border-color: rgba(99, 102, 241, 0.45);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.09);
  }

  .gc-footer__btn {
    align-self: flex-start;
    padding: 10px 24px;
    font-size: 0.71rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #4f46e5;
    background: rgba(255, 255, 255, 0.88);
    border: 1.5px solid rgba(99, 102, 241, 0.32);
    border-radius: 100px;
    cursor: pointer;
    transition:
      background 0.25s ease,
      color 0.25s ease,
      box-shadow 0.25s ease,
      transform 0.18s ease;
  }

  .gc-footer__btn:hover {
    background: #4f46e5;
    color: #fff;
    box-shadow: 0 6px 24px rgba(99, 102, 241, 0.3);
    transform: translateY(-1px);
  }

  .gc-footer__btn:active {
    transform: translateY(0);
  }

  .gc-footer__btn--done {
    background: #4f46e5;
    color: #fff;
    pointer-events: none;
  }

  /* ── Brand zone ──────────────────────────────────────────── */
  .gc-footer__brand-zone {
    margin-top: 68px;
  }

  .gc-footer__brand-rule {
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      rgba(99, 102, 241, 0.2) 30%,
      rgba(139, 92, 246, 0.2) 70%,
      transparent 100%
    );
    margin-bottom: 40px;
  }

  .gc-footer__brand-row {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
    overflow: hidden;
  }

  /* ── Wordmark ────────────────────────────────────────────── */
  .gc-footer__wordmark-wrap {
    flex: 1 1 auto;
    min-width: 0;
    overflow: hidden;
  }

  .gc-footer__wordmark {
    margin: 0;
    display: flex;
    align-items: baseline;
    line-height: 0.88;
    white-space: nowrap;
    overflow: hidden;
    animation: wordmarkIn 1s cubic-bezier(0.22, 1, 0.36, 1) 0.15s both;
  }

  @keyframes wordmarkIn {
    from { opacity: 0; transform: translateY(36px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /*
   * KEY FIX: split "Glass" and "Clear" into separate spans.
   * "Glass" gets -0.04em — tighter, all round shapes, no issue.
   * "Clear" gets -0.01em — much more open so "Cl" never touches.
   * A small gap between spans acts as the word boundary.
   */
  .gc-wm__glass {
    font-size: clamp(66px, 13vw, 220px);
    font-weight: 900;
    letter-spacing: -0.04em;
    background: linear-gradient(105deg, #3730a3 0%, #4f46e5 55%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    /* tiny right margin = space between the two halves */
    margin-right: 0.015em;
  }

  .gc-wm__clear {
    font-size: clamp(66px, 13vw, 220px);
    font-weight: 900;
    /*
     * CRITICAL: less negative than "Glass" so the C↔l gap is preserved.
     * -0.01em keeps the look tight but never merges the letters.
     */
    letter-spacing: -0.01em;
    background: linear-gradient(105deg, #6366f1 0%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* ── Tagline ─────────────────────────────────────────────── */
  .gc-footer__tagline-wrap {
    flex: 0 0 auto;
    padding-bottom: 10px;
    text-align: right;
    animation: taglineIn 0.85s cubic-bezier(0.22, 1, 0.36, 1) 0.35s both;
  }

  @keyframes taglineIn {
    from { opacity: 0; transform: translateX(18px); }
    to   { opacity: 1; transform: translateX(0); }
  }

  .gc-footer__tagline {
    margin: 0 0 10px;
    font-size: clamp(0.82rem, 1.1vw, 1.05rem);
    font-weight: 700;
    color: #64748b;
    line-height: 1.65;
    letter-spacing: -0.01em;
  }

  .gc-footer__tagline-accent {
    width: 32px;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border-radius: 2px;
    margin-left: auto;
    animation: accentGrow 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.6s both;
  }

  @keyframes accentGrow {
    from { transform: scaleX(0); transform-origin: right; }
    to   { transform: scaleX(1); transform-origin: right; }
  }

  /* ── Bottom bar ──────────────────────────────────────────── */
  .gc-footer__bottom {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 26px;
    padding-top: 18px;
    border-top: 1px solid rgba(99, 102, 241, 0.1);
  }

  .gc-footer__copy {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748b;
  }

  .gc-footer__legal {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .gc-footer__legal-link {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748b;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .gc-footer__legal-link:hover {
    color: #4f46e5;
  }

  .gc-footer__dot {
    color: #94a3b8;
  }

  /* ── Responsive ──────────────────────────────────────────── */
  @media (max-width: 1100px) {
    .gc-footer__grid {
      grid-template-columns: 1fr 1fr;
      gap: 36px;
    }
    .gc-footer__col--news {
      grid-column: 1 / -1;
    }
  }

  @media (max-width: 768px) {
    .gc-footer__container {
      padding: 48px 24px 28px;
    }
    .gc-footer__grid {
      grid-template-columns: 1fr;
      gap: 32px;
    }
    .gc-footer__col--news {
      grid-column: auto;
    }
    .gc-footer__brand-row {
      flex-direction: column;
      align-items: flex-start;
      gap: 16px;
    }
    .gc-footer__tagline-wrap {
      text-align: left;
    }
    .gc-footer__tagline-accent {
      margin-left: 0;
    }
    .gc-footer__bottom {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
    .gc-footer__btn {
      align-self: stretch;
      text-align: center;
    }
  }

  @media (max-width: 480px) {
    .gc-footer__container {
      padding: 36px 18px 22px;
    }
    .gc-wm__glass,
    .gc-wm__clear {
      font-size: clamp(48px, 15.5vw, 96px);
    }
  }
</style>
