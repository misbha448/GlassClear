<script>
  import { onMount } from 'svelte';
  import LanguageDropdown from './LanguageDropdown.svelte';
  import { clickOutside } from '$lib/actions/clickOutside';
  import { t } from '$lib/state.svelte.js';
  import { apiFetch } from '$lib/api/api.js';
  import { getDisplayName, getUserInitial } from '$lib/utils/userDisplay.js';

  let isLoggedIn = $state(false);
  let isProfileOpen = $state(false);
  let isMobileMenuOpen = $state(false);
  let openDropdown = $state(null);
  let scrolled = $state(false);
  let currentUser = $state(null);

  const navItems = [
    {
      key: 'features',
      labelKey: 'navbar.features',
      fallback: 'Features',
      icon: 'bi-stars',
      href: '#!',
      groups: [
        {
          titleKey: 'navbarMenu.features.coreTools',
          items: [
            {
              titleKey: 'navbarMenu.features.removeReflection.title',
              descriptionKey: 'navbarMenu.features.removeReflection.description',
              href: '/upload',
              icon: 'bi-magic'
            },
            {
              titleKey: 'navbarMenu.features.batch.title',
              descriptionKey: 'navbarMenu.features.batch.description',
              href: '/dashboard',
              icon: 'bi-layers'
            }
          ]
        },
        {
          titleKey: 'navbarMenu.features.workflow',
          items: [
            {
              titleKey: 'navbarMenu.features.albums.title',
              descriptionKey: 'navbarMenu.features.albums.description',
              href: '/dashboard/albums',
              icon: 'bi-collection'
            },
            {
              titleKey: 'navbarMenu.features.history.title',
              descriptionKey: 'navbarMenu.features.history.description',
              href: '/dashboard/history',
              icon: 'bi-clock-history'
            }
          ]
        }
      ],
      cta: {
        titleKey: 'navbarMenu.features.cta.title',
        descriptionKey: 'navbarMenu.features.cta.description',
        href: '/upload'
      }
    },
    {
      key: 'products',
      labelKey: 'navbar.products',
      fallback: 'Products',
      icon: 'bi-box2-fill',
      href: '#!',
      groups: [
        {
          titleKey: 'navbarMenu.products.workspace',
          items: [
            {
              titleKey: 'navbarMenu.products.dashboard.title',
              descriptionKey: 'navbarMenu.products.dashboard.description',
              href: '/dashboard',
              icon: 'bi-grid-fill'
            },
            {
              titleKey: 'navbarMenu.products.upload.title',
              descriptionKey: 'navbarMenu.products.upload.description',
              href: '/upload',
              icon: 'bi-cloud-arrow-up-fill'
            }
          ]
        },
        {
          titleKey: 'navbarMenu.products.collections',
          items: [
            {
              titleKey: 'navbarMenu.products.albums.title',
              descriptionKey: 'navbarMenu.products.albums.description',
              href: '/dashboard/albums',
              icon: 'bi-images'
            },
            {
              titleKey: 'navbarMenu.products.history.title',
              descriptionKey: 'navbarMenu.products.history.description',
              href: '/dashboard/history',
              icon: 'bi-journal-richtext'
            }
          ]
        }
      ],
      cta: {
        titleKey: 'navbarMenu.products.cta.title',
        descriptionKey: 'navbarMenu.products.cta.description',
        href: '/dashboard'
      }
    },
    {
      key: 'resources',
      labelKey: 'navbar.resources',
      fallback: 'Resources',
      icon: 'bi-book-fill',
      href: '#!',
      groups: [
        {
          titleKey: 'navbarMenu.resources.learn',
          items: [
            {
              titleKey: 'navbarMenu.resources.how.title',
              descriptionKey: 'navbarMenu.resources.how.description',
              href: '/#how-it-works',
              icon: 'bi-diagram-3'
            },
            {
              titleKey: 'navbarMenu.resources.demo.title',
              descriptionKey: 'navbarMenu.resources.demo.description',
              href: '/#demo',
              icon: 'bi-play-circle'
            }
          ]
        },
        {
          titleKey: 'navbarMenu.resources.help',
          items: [
            {
              titleKey: 'navbarMenu.resources.faq.title',
              descriptionKey: 'navbarMenu.resources.faq.description',
              href: '/#faq',
              icon: 'bi-chat-square-text'
            },
            {
              titleKey: 'navbarMenu.resources.guide.title',
              descriptionKey: 'navbarMenu.resources.guide.description',
              href: '/upload',
              icon: 'bi-arrow-up-right-circle'
            }
          ]
        }
      ],
      cta: {
        titleKey: 'navbarMenu.resources.cta.title',
        descriptionKey: 'navbarMenu.resources.cta.description',
        href: '/#demo'
      }
    }
  ];

  function syncLocalUser() {
    const fallbackName = typeof localStorage !== 'undefined' ? localStorage.getItem('user_name') : '';
    currentUser = fallbackName ? { name: fallbackName, email: '' } : null;
  }

  function safeText(value, fallback = '') {
    if (typeof value === 'string') return value;
    if (value && typeof value === 'object') {
      return value.label || value.title || value.name || value.text || fallback;
    }
    return fallback;
  }

  function tr(key, fallback) {
    const value = t(key);
    return typeof value === 'string' && value !== key ? value : fallback;
  }

  function toggleDropdown(key) {
    openDropdown = openDropdown === key ? null : key;
  }

  function closeMenus() {
    openDropdown = null;
    isMobileMenuOpen = false;
    isProfileOpen = false;
  }

  onMount(() => {
    isLoggedIn = !!localStorage.getItem('token');
    syncLocalUser();

    const onScroll = () => { scrolled = window.scrollY > 12; };
    const onResize = () => { if (window.innerWidth > 960) isMobileMenuOpen = false; };

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize);

    if (isLoggedIn) {
      apiFetch('/api/v1/users/me')
        .then(async (response) => {
          if (!response.ok) throw new Error('user-load-failed');
          const payload = await response.json();
          currentUser = payload;
          if (payload?.name) localStorage.setItem('user_name', payload.name);
        })
        .catch(() => { syncLocalUser(); });
    }

    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
    };
  });

  function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('token_type');
    window.location.href = '/login';
  }
</script>

<nav class:navbar--scrolled={scrolled} class="navbar-shell">
  <div class="navbar-inner">

    <!-- LOGO -->
    <a class="brand" href="/" aria-label="GlassClear home">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2 20 6.5v11L12 22l-8-4.5v-11L12 2Z" fill="url(#navBrandGrad)" />
          <path d="M12 6 17.5 9.2v6.8L12 19l-5.5-3V9.2L12 6Z" fill="rgba(255,255,255,0.45)" />
          <path d="M12 9.5l3 1.8v3.5L12 16.5l-3-1.7v-3.5L12 9.5Z" fill="rgba(255,255,255,0.75)" />
          <defs>
            <linearGradient id="navBrandGrad" x1="4" y1="2" x2="20" y2="22" gradientUnits="userSpaceOnUse">
              <stop stop-color="#818cf8" />
              <stop offset="1" stop-color="#6366f1" />
            </linearGradient>
          </defs>
        </svg>
      </span>
      <span class="brand-title">GlassClear</span>
    </a>

    <!-- HAMBURGER -->
    <button
      class="menu-toggle"
      type="button"
      aria-label={tr('navbar.toggleNavigation', 'Toggle navigation')}
      aria-expanded={isMobileMenuOpen}
      onclick={() => (isMobileMenuOpen = !isMobileMenuOpen)}
    >
      <span class:bar--top-open={isMobileMenuOpen}></span>
      <span class:bar--mid-open={isMobileMenuOpen}></span>
      <span class:bar--bot-open={isMobileMenuOpen}></span>
    </button>

    <!-- NAV PANEL -->
    <div class:menu-open={isMobileMenuOpen} class="nav-panel">

      <!-- LINKS -->
      <div class="nav-links" role="navigation" aria-label={tr('navbar.primaryNavigation', 'Primary navigation')}>
        {#each navItems as item}
          <div
            class="nav-dropdown"
            class:nav-dropdown--open={openDropdown === item.key}
            use:clickOutside={() => { if (openDropdown === item.key) openDropdown = null; }}
          >
            <button
              class="nav-link nav-trigger"
              type="button"
              aria-expanded={openDropdown === item.key}
              onclick={() => toggleDropdown(item.key)}
            >
              <i class={`bi ${safeText(item.icon)}`} aria-hidden="true"></i>
              <span>{tr(item.labelKey, item.fallback)}</span>
              <i
                class="bi bi-chevron-down nav-chevron"
                class:chevron--open={openDropdown === item.key}
                aria-hidden="true"
              ></i>
            </button>

            <div class="mega-menu" role="region" aria-label={tr(item.labelKey, item.fallback)}>
              <div class="mega-grid">
                {#each item.groups as group}
                  <div class="mega-group">
                    <h3 class="mega-group-title">{tr(group.titleKey, safeText(group.title))}</h3>
                    <div class="mega-items">
                      {#each group.items as link}
                        <a class="mega-link" href={safeText(link.href, '#!')} onclick={closeMenus}>
                          <span class="mega-icon" aria-hidden="true">
                            <i class={`bi ${safeText(link.icon)}`}></i>
                          </span>
                          <span class="mega-copy">
                            <span class="mega-title">{tr(link.titleKey, safeText(link.title))}</span>
                            <span class="mega-desc">{tr(link.descriptionKey, safeText(link.description))}</span>
                          </span>
                        </a>
                      {/each}
                    </div>
                  </div>
                {/each}
                <a class="mega-cta" href={safeText(item.cta.href, '#!')} onclick={closeMenus}>
                  <span class="mega-cta-badge">
                    <i class="bi bi-lightning-charge-fill"></i>
                    {tr('navbar.quickStart', 'Quick Start')}
                  </span>
                  <span class="mega-cta-label">{tr(item.cta.titleKey, safeText(item.cta.title))}</span>
                  <span class="mega-cta-desc">{tr(item.cta.descriptionKey, safeText(item.cta.description))}</span>
                  <span class="mega-cta-arrow">
                    <i class="bi bi-arrow-right-short"></i>
                  </span>
                </a>
              </div>
            </div>
          </div>
        {/each}

        {#if isLoggedIn}
          <a href="/dashboard" class="nav-link nav-link--accent" onclick={closeMenus}>
            <i class="bi bi-grid-fill" aria-hidden="true"></i>
            <span>{tr('nav_dashboard', tr('common.dashboard', 'Dashboard'))}</span>
          </a>
        {/if}
      </div>

      <!-- ACTIONS -->
      <div class="nav-actions">
        <!-- Language dropdown wrapper -->
        <div class="language-slot">
          <LanguageDropdown />
        </div>

        {#if isLoggedIn}
          <div class="profile-wrap" use:clickOutside={() => (isProfileOpen = false)}>
            <button
              class="profile-trigger"
              class:profile-trigger--open={isProfileOpen}
              type="button"
              aria-expanded={isProfileOpen}
              aria-label={tr('navbar.userMenu', 'User profile menu')}
              onclick={() => (isProfileOpen = !isProfileOpen)}
            >
              <span class="profile-avatar">{getUserInitial(currentUser)}</span>
              <span class="profile-meta">
                <span class="profile-name">{getDisplayName(currentUser)}</span>
                <span class="profile-role">{tr('navbar.pro', 'Pro')}</span>
              </span>
              <i class="bi bi-chevron-down nav-chevron" class:chevron--open={isProfileOpen} aria-hidden="true"></i>
            </button>

            <div class="profile-menu" class:profile-menu--open={isProfileOpen}>
              <div class="profile-summary">
                <span class="profile-summary-avatar">{getUserInitial(currentUser)}</span>
                <div class="profile-summary-info">
                  <strong>{getDisplayName(currentUser)}</strong>
                  <span>{currentUser?.email || ''}</span>
                </div>
              </div>
              <a href="/dashboard" onclick={() => (isProfileOpen = false)}>
                <i class="bi bi-grid-fill" aria-hidden="true"></i>
                <span>{tr('nav_dashboard', tr('common.dashboard', 'Dashboard'))}</span>
              </a>
              <a href="/upload" onclick={() => (isProfileOpen = false)}>
                <i class="bi bi-cloud-arrow-up-fill" aria-hidden="true"></i>
                <span>{tr('nav_new_upload', tr('common.uploadNew', 'New Upload'))}</span>
              </a>
              <button type="button" class="logout-btn" onclick={() => logout()}>
                <i class="bi bi-box-arrow-right" aria-hidden="true"></i>
                <span>{tr('nav_logout', tr('common.logout', 'Logout'))}</span>
              </button>
            </div>
          </div>
        {:else}
          <div class="guest-actions">
            <a class="ghost-btn" href="/login" onclick={closeMenus}>{tr('common.login', 'Login')}</a>
            <a class="primary-btn" href="/signup" onclick={closeMenus}>
              <span>{tr('common.signUp', 'Sign Up')}</span>
              <i class="bi bi-arrow-right" aria-hidden="true"></i>
            </a>
          </div>
        {/if}
      </div>
    </div>
  </div>
</nav>

<style>
  *, *::before, *::after { box-sizing: border-box; }

  /* ── SHELL ─────────────────────────────────────────── */
  .navbar-shell {
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 14px 24px 0;
    background: transparent;
    font-family: Inter, 'Space Grotesk', system-ui, sans-serif;
  }

  /* ── INNER PILL ─────────────────────────────────────── */
  .navbar-inner {
    max-width: 1280px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    padding: 0 10px 0 16px;
    height: 72px;
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    border: 1px solid rgba(255,255,255,0.76);
    border-bottom: 1px solid rgba(99,102,241,0.12);
    box-shadow: 0 20px 60px rgba(79,70,229,0.13);
    border-radius: 999px;
    transition: background .25s ease, box-shadow .3s ease;
  }

  .navbar--scrolled .navbar-inner {
    background: rgba(255,255,255,0.88);
    box-shadow: 0 24px 70px rgba(79,70,229,0.18);
  }

  /* ── BRAND ──────────────────────────────────────────── */
  .brand {
    display: inline-flex;
    align-items: center;
    gap: 11px;
    text-decoration: none;
    flex-shrink: 0;
    padding: 4px 0;
  }
  .brand-mark {
    width: 46px; height: 46px;
    display: inline-flex; align-items: center; justify-content: center;
    border-radius: 16px;
    background: linear-gradient(135deg,#eef2ff 0%,#ddd6fe 100%);
    box-shadow: 0 0 0 1px rgba(99,102,241,.18), 0 14px 35px rgba(99,102,241,.22), inset 0 1px 0 rgba(255,255,255,.9);
    flex-shrink: 0;
  }
  .brand-mark svg { width: 24px; height: 24px; }
  .brand-title {
    color: #111827; font-size: 18px; font-weight: 900;
    letter-spacing: -.04em; line-height: 1;
  }

  /* ── HAMBURGER ──────────────────────────────────────── */
  .menu-toggle {
    display: none; margin-left: auto;
    width: 44px; height: 44px;
    border: 1px solid rgba(99,102,241,.16); border-radius: 14px;
    background: rgba(255,255,255,.76);
    align-items: center; justify-content: center; flex-direction: column; gap: 5px;
    cursor: pointer; transition: background .2s ease;
  }
  .menu-toggle:hover { background: #eef2ff; }
  .menu-toggle span {
    width: 18px; height: 2px; border-radius: 999px;
    background: #111827; transition: transform .2s ease, opacity .2s ease; display: block;
  }
  .bar--top-open { transform: translateY(7px) rotate(45deg); }
  .bar--mid-open { opacity: 0; }
  .bar--bot-open { transform: translateY(-7px) rotate(-45deg); }

  /* ── NAV PANEL ──────────────────────────────────────── */
  .nav-panel {
    display: grid; grid-template-columns: 1fr auto;
    align-items: center; gap: 8px; height: 100%;
  }

  /* ── NAV LINKS ──────────────────────────────────────── */
  .nav-links {
    display: flex; align-items: center; justify-content: center;
    gap: 4px; flex-wrap: wrap; height: 100%;
  }
  .nav-link {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 9px 14px; border-radius: 999px;
    color: #475569; text-decoration: none;
    font-size: 15px; font-weight: 800; letter-spacing: -.01em; line-height: 1;
    transition: background .18s ease, color .18s ease;
    cursor: pointer; white-space: nowrap;
  }
  .nav-trigger { border: none; background: transparent; font-family: inherit; }
  .nav-link i { color: #6366f1; font-size: 14px; flex-shrink: 0; }
  .nav-link:hover, .nav-dropdown--open > .nav-trigger { background: #eef2ff; color: #4f46e5; }
  .nav-link:hover i, .nav-dropdown--open > .nav-trigger i { color: #4f46e5; }
  .nav-link--accent { background: #eef2ff; color: #4f46e5; }

  /* ── CHEVRON ────────────────────────────────────────── */
  .nav-chevron {
    color: #94a3b8; font-size: 11px;
    transition: transform .2s ease, color .18s ease; flex-shrink: 0;
  }
  .chevron--open { transform: rotate(180deg); color: #4f46e5; }

  /* ── DROPDOWN WRAPPER ───────────────────────────────── */
  .nav-dropdown { position: relative; height: 100%; display: flex; align-items: center; }

  /* ── MEGA MENU ──────────────────────────────────────── */
  .mega-menu {
    position: absolute; top: calc(100% + 10px); left: 50%;
    transform: translateX(-50%) translateY(-6px);
    width: min(1120px, calc(100vw - 48px)); padding: 28px;
    background: rgba(255,255,255,.97); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(99,102,241,.16);
    box-shadow: 0 28px 80px rgba(79,70,229,.18), 0 4px 16px rgba(0,0,0,.06);
    border-radius: 28px; opacity: 0; visibility: hidden; pointer-events: none;
    transition: opacity .2s ease, visibility .2s ease, transform .2s ease;
    z-index: 9998;
  }
  .nav-dropdown--open .mega-menu {
    opacity: 1; visibility: visible; pointer-events: auto;
    transform: translateX(-50%) translateY(0);
  }
  .mega-grid { display: grid; grid-template-columns: 1fr 1fr .9fr; gap: 28px; align-items: start; }
  .mega-group-title {
    margin: 0 0 14px; color: #111827; font-size: 13px; font-weight: 900;
    letter-spacing: .04em; text-transform: uppercase; line-height: 1;
  }
  .mega-items { display: grid; gap: 8px; }
  .mega-link {
    display: grid; grid-template-columns: 44px 1fr; gap: 14px;
    align-items: center; padding: 13px 14px; border-radius: 18px;
    text-decoration: none; transition: background .18s ease, transform .18s ease;
  }
  .mega-link:hover { background: rgba(238,242,255,.9); transform: translateY(-2px); }
  .mega-icon {
    width: 44px; height: 44px; display: inline-flex; align-items: center; justify-content: center;
    border-radius: 14px; background: #eef2ff; color: #6366f1; font-size: 18px; flex-shrink: 0;
  }
  .mega-copy { display: flex; flex-direction: column; gap: 5px; min-width: 0; }
  .mega-title { color: #111827; font-size: 15px; font-weight: 800; line-height: 1.25; letter-spacing: -.01em; display: block; }
  .mega-desc { color: #64748b; font-size: 13px; font-weight: 500; line-height: 1.5; display: block; }
  .mega-cta {
    display: flex; flex-direction: column; justify-content: space-between; gap: 10px;
    min-height: 100%; padding: 22px 20px; border-radius: 22px; text-decoration: none;
    background: linear-gradient(135deg,#f8fafc 0%,#eef2ff 100%);
    border: 1px solid rgba(99,102,241,.16);
    transition: background .2s ease, box-shadow .2s ease, transform .2s ease;
    position: relative; overflow: hidden;
  }
  .mega-cta::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 80% 20%,rgba(99,102,241,.07),transparent 60%);
    pointer-events: none;
  }
  .mega-cta:hover {
    background: linear-gradient(135deg,#eef2ff 0%,#e0e7ff 100%);
    box-shadow: 0 12px 28px rgba(99,102,241,.14); transform: translateY(-2px);
  }
  .mega-cta-badge {
    display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px;
    border-radius: 999px; background: rgba(99,102,241,.1); color: #4f46e5;
    font-size: 12px; font-weight: 800; width: fit-content;
  }
  .mega-cta-badge i { font-size: 11px; }
  .mega-cta-label { color: #111827; font-size: 16px; font-weight: 900; line-height: 1.3; letter-spacing: -.02em; }
  .mega-cta-desc { color: #64748b; font-size: 13.5px; font-weight: 500; line-height: 1.55; flex: 1; }
  .mega-cta-arrow {
    display: inline-flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 10px;
    background: rgba(99,102,241,.1); color: #4f46e5; font-size: 20px;
    transition: background .18s ease, transform .18s ease;
  }
  .mega-cta:hover .mega-cta-arrow { background: #4f46e5; color: #fff; transform: translateX(2px); }

  /* ── NAV ACTIONS ────────────────────────────────────── */
  .nav-actions { display: flex; align-items: center; gap: 10px; flex-shrink: 0; padding: 0 4px; }

  /* ================================================================
     LANGUAGE SLOT
     The core fix: hide the dropdown panel by default using display:none,
     then show it only when the trigger is in an active/open state.
     We detect "open" via aria-expanded="true" on the trigger button,
     which is the standard pattern all dropdown libs use.
  ================================================================ */
  .language-slot {
    position: relative;
    display: inline-flex;
    align-items: center;
    z-index: 10001;
  }

  /* ---- TRIGGER BUTTON ---- */
  :global(.language-slot button),
  :global(.language-slot [role="button"]),
  :global(.language-slot .trigger),
  :global(.language-slot .lang-trigger),
  :global(.language-slot .lang-btn),
  :global(.language-slot .lang-select),
  :global(.language-slot .lang-dropdown-trigger),
  :global(.language-slot .dropdown-trigger),
  :global(.language-slot .select-trigger),
  :global(.language-slot > div > button),
  :global(.language-slot > div > [role="button"]) {
    all: unset !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding: 8px 16px !important;
    border-radius: 999px !important;
    white-space: nowrap !important;
    cursor: pointer !important;
    background: rgba(255,255,255,0.82) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1.5px solid rgba(148,163,184,0.35) !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.08) !important;
    font-family: Inter, 'Noto Sans Devanagari', 'Noto Sans Kannada', system-ui, sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    line-height: 1 !important;
    color: #1e293b !important;
    letter-spacing: -0.01em !important;
    transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease !important;
    box-sizing: border-box !important;
  }

  :global(.language-slot button:hover),
  :global(.language-slot [role="button"]:hover),
  :global(.language-slot .lang-trigger:hover),
  :global(.language-slot .dropdown-trigger:hover),
  :global(.language-slot .lang-dropdown-trigger:hover),
  :global(.language-slot > div > button:hover) {
    background: rgba(255,255,255,0.97) !important;
    border-color: rgba(99,102,241,0.40) !important;
    color: #4f46e5 !important;
  }

  /* "Language" muted label text */
  :global(.language-slot button .lang-label),
  :global(.language-slot button .label),
  :global(.language-slot button span.muted),
  :global(.language-slot button > span:first-child) {
    color: #94a3b8 !important;
    font-weight: 500 !important;
  }

  /* Selected language value — dark bold */
  :global(.language-slot button .lang-value),
  :global(.language-slot button .value),
  :global(.language-slot button strong),
  :global(.language-slot button > span:last-of-type) {
    color: #111827 !important;
    font-weight: 700 !important;
  }

  /* Chevron / arrow inside trigger */
  :global(.language-slot button svg),
  :global(.language-slot button i.bi-chevron-down),
  :global(.language-slot button .chevron),
  :global(.language-slot button .arrow) {
    color: #94a3b8 !important;
    fill: #94a3b8 !important;
    font-size: 11px !important;
    flex-shrink: 0 !important;
  }

  /* ---- DROPDOWN PANEL — HIDDEN BY DEFAULT ---- */
  /* This is the KEY FIX: we hide ALL candidate panel elements by default */
  :global(.language-slot .lang-dropdown-panel),
  :global(.language-slot .dropdown-panel),
  :global(.language-slot .lang-panel),
  :global(.language-slot .lang-menu),
  :global(.language-slot .select-panel),
  :global(.language-slot .options-panel),
  :global(.language-slot [role="listbox"]),
  :global(.language-slot ul),
  :global(.language-slot > div > ul),
  :global(.language-slot > div > div:not(:first-child)) {
    all: unset !important;
    display: none !important; /* HIDDEN by default — the fix */
    position: absolute !important;
    top: calc(100% + 10px) !important;
    right: 0 !important;
    left: auto !important;
    z-index: 99999 !important;
    min-width: 170px !important;
    width: max-content !important;
    background: rgba(255,255,255,0.96) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(148,163,184,0.25) !important;
    box-shadow: 0 16px 40px rgba(0,0,0,0.11), 0 2px 8px rgba(99,102,241,0.07) !important;
    border-radius: 18px !important;
    padding: 6px !important;
    color: #1e293b !important;
    list-style: none !important;
    margin: 0 !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
  }

  /*
    SHOW the panel when the trigger button has aria-expanded="true"
    This covers the most common pattern: sibling or cousin panel after an expanded trigger.
    We use the adjacent/general sibling combinator AND the parent [data-open] pattern.
  */
  :global(.language-slot button[aria-expanded="true"] ~ .lang-dropdown-panel),
  :global(.language-slot button[aria-expanded="true"] ~ .dropdown-panel),
  :global(.language-slot button[aria-expanded="true"] ~ .lang-panel),
  :global(.language-slot button[aria-expanded="true"] ~ .lang-menu),
  :global(.language-slot button[aria-expanded="true"] ~ [role="listbox"]),
  :global(.language-slot button[aria-expanded="true"] ~ ul),
  :global(.language-slot [data-open="true"] .lang-dropdown-panel),
  :global(.language-slot [data-open="true"] .dropdown-panel),
  :global(.language-slot [data-open="true"] .lang-panel),
  :global(.language-slot [data-open="true"] .lang-menu),
  :global(.language-slot [data-open="true"] [role="listbox"]),
  :global(.language-slot [data-open="true"] ul),
  :global(.language-slot [data-state="open"] .lang-dropdown-panel),
  :global(.language-slot [data-state="open"] .dropdown-panel),
  :global(.language-slot [data-state="open"] .lang-panel),
  :global(.language-slot [data-state="open"] .lang-menu),
  :global(.language-slot [data-state="open"] [role="listbox"]),
  :global(.language-slot [data-state="open"] ul),
  /* Svelte class-based open states */
  :global(.language-slot .lang-open .lang-dropdown-panel),
  :global(.language-slot .lang-open .dropdown-panel),
  :global(.language-slot .lang-open ul),
  :global(.language-slot .open .lang-dropdown-panel),
  :global(.language-slot .open .dropdown-panel),
  :global(.language-slot .open ul),
  :global(.language-slot .is-open .lang-dropdown-panel),
  :global(.language-slot .is-open .dropdown-panel),
  :global(.language-slot .is-open ul) {
    display: block !important;
  }

  /* ---- DROPDOWN ITEMS ---- */
  :global(.language-slot [role="option"]),
  :global(.language-slot li),
  :global(.language-slot .lang-option),
  :global(.language-slot .lang-item),
  :global(.language-slot .option),
  :global(.language-slot .dropdown-item),
  :global(.language-slot > div > ul > li),
  :global(.language-slot > div > div > button) {
    all: unset !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 8px !important;
    padding: 10px 14px !important;
    border-radius: 12px !important;
    font-family: Inter, 'Noto Sans Devanagari', 'Noto Sans Kannada', system-ui, sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    line-height: 1.3 !important;
    color: #1e293b !important;
    background: transparent !important;
    cursor: pointer !important;
    width: 100% !important;
    box-sizing: border-box !important;
    transition: background 0.15s ease, color 0.15s ease !important;
  }

  :global(.language-slot [role="option"]:hover),
  :global(.language-slot li:hover),
  :global(.language-slot .lang-option:hover),
  :global(.language-slot .lang-item:hover),
  :global(.language-slot .option:hover),
  :global(.language-slot .dropdown-item:hover),
  :global(.language-slot > div > ul > li:hover),
  :global(.language-slot > div > div > button:hover) {
    background: rgba(99,102,241,0.08) !important;
    color: #4f46e5 !important;
  }

  /* Active / selected item */
  :global(.language-slot [aria-selected="true"]),
  :global(.language-slot .lang-option--active),
  :global(.language-slot .lang-item--active),
  :global(.language-slot .active),
  :global(.language-slot .selected),
  :global(.language-slot [data-active="true"]),
  :global(.language-slot [data-selected="true"]),
  :global(.language-slot li.active),
  :global(.language-slot .option--selected) {
    background: rgba(99,102,241,0.12) !important;
    color: #4f46e5 !important;
    font-weight: 700 !important;
  }

  :global(.language-slot [aria-selected="true"] svg),
  :global(.language-slot [aria-selected="true"] i),
  :global(.language-slot .active svg),
  :global(.language-slot .active i),
  :global(.language-slot .selected svg),
  :global(.language-slot .selected i) {
    color: #4f46e5 !important;
    fill: #4f46e5 !important;
  }

  /* ── GUEST ACTIONS ──────────────────────────────────── */
  .guest-actions { display: flex; align-items: center; gap: 8px; }
  .ghost-btn, .primary-btn {
    display: inline-flex; align-items: center; gap: 7px;
    border-radius: 999px; text-decoration: none;
    font-size: 14px; font-weight: 800; letter-spacing: -.01em; line-height: 1;
    white-space: nowrap;
    transition: background .18s ease, box-shadow .18s ease, color .18s ease;
  }
  .ghost-btn {
    padding: 10px 16px; color: #374151;
    background: rgba(255,255,255,.72); border: 1px solid rgba(99,102,241,.14);
  }
  .ghost-btn:hover { background: #eef2ff; color: #4f46e5; }
  .primary-btn {
    padding: 10px 18px; color: #fff;
    background: linear-gradient(135deg,#6366f1,#4f46e5);
    box-shadow: 0 10px 24px rgba(99,102,241,.28); border: none;
  }
  .primary-btn:hover { box-shadow: 0 14px 30px rgba(99,102,241,.38); color: #fff; transform: translateY(-1px); }

  /* ── PROFILE TRIGGER ────────────────────────────────── */
  .profile-wrap { position: relative; }
  .profile-trigger {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 7px 12px 7px 7px;
    background: rgba(255,255,255,.78); border: 1px solid rgba(99,102,241,.14);
    border-radius: 999px; color: #111827; cursor: pointer;
    transition: background .18s ease; font-family: inherit;
  }
  .profile-trigger--open, .profile-trigger:hover { background: #eef2ff; }
  .profile-avatar, .profile-summary-avatar {
    width: 36px; height: 36px;
    display: inline-flex; align-items: center; justify-content: center;
    border-radius: 50%; background: linear-gradient(135deg,#6366f1,#8b5cf6);
    color: #fff; font-weight: 900; font-size: 15px; flex-shrink: 0;
  }
  .profile-meta { display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }
  .profile-name { color: #111827; font-size: 13.5px; font-weight: 800; line-height: 1; letter-spacing: -.01em; }
  .profile-role { color: #6366f1; font-size: 11px; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }

  /* ── PROFILE MENU ───────────────────────────────────── */
  .profile-menu {
    position: absolute; top: calc(100% + 12px); right: 0; width: 256px; padding: 12px;
    border-radius: 24px; background: rgba(255,255,255,.97);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(99,102,241,.16);
    box-shadow: 0 24px 70px rgba(79,70,229,.18);
    opacity: 0; visibility: hidden; pointer-events: none;
    transform: translateY(-6px);
    transition: opacity .2s ease, transform .2s ease, visibility .2s ease;
    z-index: 9999;
  }
  .profile-menu--open { opacity: 1; visibility: visible; pointer-events: auto; transform: translateY(0); }
  .profile-summary {
    display: flex; align-items: center; gap: 12px;
    padding: 6px 8px 14px; margin-bottom: 8px;
    border-bottom: 1px solid rgba(99,102,241,.1);
  }
  .profile-summary-info strong { display: block; color: #111827; font-size: 14px; font-weight: 900; line-height: 1.2; letter-spacing: -.01em; }
  .profile-summary-info span { display: block; color: #64748b; font-size: 12px; font-weight: 500; margin-top: 3px; }
  .profile-menu a, .logout-btn {
    width: 100%; display: inline-flex; align-items: center; gap: 10px;
    padding: 11px 14px; border-radius: 15px; color: #374151; text-decoration: none;
    font-size: 14px; font-weight: 700; background: transparent; border: none;
    cursor: pointer; font-family: inherit;
    transition: background .15s ease, color .15s ease;
  }
  .profile-menu a i, .logout-btn i { color: #6366f1; font-size: 15px; }
  .profile-menu a:hover { background: #eef2ff; color: #4f46e5; }
  .profile-menu a:hover i { color: #4f46e5; }
  .logout-btn { color: #dc2626; margin-top: 4px; }
  .logout-btn i { color: #dc2626 !important; }
  .logout-btn:hover { background: #fef2f2; color: #b91c1c; }

  /* ── MOBILE ≤ 960px ─────────────────────────────────── */
  @media (max-width: 960px) {
    .navbar-shell { padding: 10px 14px 0; }
    .navbar-inner { grid-template-columns: auto auto; height: auto; padding: 12px 14px; border-radius: 28px; gap: 12px; }
    .menu-toggle { display: inline-flex; }
    .nav-panel { grid-column: 1 / -1; display: none; grid-template-columns: 1fr; gap: 12px; padding-top: 6px; padding-bottom: 10px; }
    .menu-open { display: grid; }
    .nav-links { flex-direction: column; align-items: stretch; gap: 4px; }
    .nav-actions { flex-direction: column; align-items: stretch; gap: 8px; padding: 0; }
    .guest-actions { flex-direction: column; align-items: stretch; gap: 8px; }
    .nav-dropdown { width: 100%; height: auto; }

    .language-slot { width: 100%; }

    :global(.language-slot > *) { width: 100% !important; }

    :global(.language-slot button),
    :global(.language-slot .lang-trigger),
    :global(.language-slot .lang-dropdown-trigger),
    :global(.language-slot .dropdown-trigger) {
      width: 100% !important;
      border-radius: 16px !important;
      justify-content: space-between !important;
    }

    :global(.language-slot .lang-dropdown-panel),
    :global(.language-slot .dropdown-panel),
    :global(.language-slot [role="listbox"]),
    :global(.language-slot ul) {
      right: 0 !important;
      left: 0 !important;
      width: 100% !important;
      min-width: unset !important;
    }

    .profile-wrap { width: 100%; }
    .nav-link, .ghost-btn, .primary-btn, .nav-trigger {
      justify-content: space-between; width: 100%; border-radius: 16px; text-align: left;
    }
    .ghost-btn, .primary-btn { justify-content: center; padding: 13px 18px; }
    .mega-menu {
      position: static; width: 100%; margin-top: 8px; padding: 16px;
      transform: none !important; opacity: 1 !important; visibility: hidden;
      pointer-events: none; display: none; border-radius: 20px;
      box-shadow: 0 12px 40px rgba(79,70,229,.12);
    }
    .nav-dropdown--open .mega-menu { display: block; visibility: visible; pointer-events: auto; opacity: 1; }
    .mega-grid { grid-template-columns: 1fr; gap: 16px; }
    .mega-cta { min-height: auto; }
    .profile-trigger { width: 100%; justify-content: space-between; border-radius: 16px; }
    .profile-menu { position: static; width: 100%; margin-top: 8px; display: none; opacity: 1; visibility: visible; transform: none; pointer-events: auto; border-radius: 20px; }
    .profile-menu--open { display: block; }
  }

  /* ── TABLET 961–1100px ──────────────────────────────── */
  @media (min-width: 961px) and (max-width: 1100px) {
    .mega-grid { grid-template-columns: 1fr 1fr; }
    .mega-cta { grid-column: 1 / -1; flex-direction: row; align-items: center; min-height: auto; }
    .mega-cta-label { flex: 1; }
  }
</style> 
