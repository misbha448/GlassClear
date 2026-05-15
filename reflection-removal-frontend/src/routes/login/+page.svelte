<!-- src/routes/login/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  import Navbar from '$lib/components/Navbar.svelte';
  import { apiFetch } from '$lib/api/api.js';
  import { t } from '$lib/state.svelte.js';
  import {
    mapAuthServerError,
    normalizeEmail,
    validateEmail,
    validateLoginPassword
  } from '$lib/utils/authValidation.js';

  let email = $state("");
  let password = $state("");
  let errorMessage = $state("");
  let showPassword = $state(false);
  let isSubmitting = $state(false);
  let touched = $state({ email: false, password: false });
  let fieldErrors = $state({ email: '', password: '' });

  const isFormValid = $derived(
    !validateEmail(email) &&
    !validateLoginPassword(password)
  );

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    const error = params.get("error");
    if (error) {
      errorMessage = error;
    }
  });

  function setFieldError(field, message) {
    fieldErrors = { ...fieldErrors, [field]: message };
  }

  function setTouched(field, value = true) {
    touched = { ...touched, [field]: value };
  }

  function validateField(field) {
    if (field === 'email') {
      setFieldError('email', validateEmail(email));
      return;
    }

    if (field === 'password') {
      setFieldError('password', validateLoginPassword(password));
    }
  }

  function validateForm(markAllTouched = false) {
    if (markAllTouched) {
      touched = { email: true, password: true };
    }

    const nextErrors = {
      email: validateEmail(email),
      password: validateLoginPassword(password)
    };
    fieldErrors = nextErrors;
    return !nextErrors.email && !nextErrors.password;
  }

  function handleBlur(field) {
    if (field === 'email') {
      email = normalizeEmail(email);
    }
    setTouched(field);
    validateField(field);
  }

  function handleInput(field, value) {
    if (field === 'email') {
      email = value;
    } else if (field === 'password') {
      password = value;
    }

    errorMessage = "";
    if (touched[field]) {
      validateField(field);
    }
  }

  async function login() {
    errorMessage = "";
    if (!validateForm(true)) {
      return;
    }

    isSubmitting = true;
    email = normalizeEmail(email);

    try {
      const response = await apiFetch("/api/v1/auth/login", {
        method: "POST",
        body: { email, password }
      });
      const data = await response.json();
      if (!response.ok) {
        const serverMessage = typeof data.detail === 'string' ? data.detail : t('login_error_msg');
        const mappedError = mapAuthServerError(serverMessage);

        if (mappedError.field) {
          setTouched(mappedError.field);
          setFieldError(mappedError.field, mappedError.message);
        } else {
          errorMessage = mappedError.message || t('login_error_msg');
        }
        return;
      }
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("token_type", data.token_type);
      localStorage.setItem("role", data.role);
      if (data.user_name) {
        localStorage.setItem("user_name", data.user_name);
      }

      if (data.role === 'admin') {
        window.location.href = "/admin/dashboard";
      } else {
        window.location.href = "/dashboard";
      }
    } catch (error) {
      errorMessage = t('login_error_msg');
    } finally {
      isSubmitting = false;
    }
  }
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@700;800&display=swap" rel="stylesheet" />
</svelte:head>

<Navbar />

<div class="auth-page">
  <!-- Background orbs -->
  <div class="auth-orb auth-orb-1"></div>
  <div class="auth-orb auth-orb-2"></div>
  <div class="auth-grid-overlay"></div>

  <div class="auth-container">

    <!-- Left panel — branding -->
    <div class="auth-brand">
      <div class="brand-badge">
        <span class="brand-dot"></span>
        {t('auth.loginBadge')}
      </div>
      <h1 class="brand-heading">
        {t('auth.loginHeroLine1')}<br />
        <span>{t('auth.loginHeroLine2')}</span>
      </h1>
      <p class="brand-sub">
        {t('auth.loginHeroSubtitle')}
      </p>

      <!-- Feature bullets -->
      <div class="brand-features">
        <div class="bfeat">
          <div class="bfeat-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <span>{t('auth.loginFeatureAccuracy')}</span>
        </div>
        <div class="bfeat">
          <div class="bfeat-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <span>{t('auth.loginFeatureSpeed')}</span>
        </div>
        <div class="bfeat">
          <div class="bfeat-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <span>{t('auth.loginFeatureOutput')}</span>
        </div>
        <div class="bfeat">
          <div class="bfeat-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <span>{t('auth.loginFeatureConfidence')}</span>
        </div>
      </div>

      <!-- Mini avatar row -->
      <div class="brand-social">
        <div class="bsocial-avatars">
          <img src="https://randomuser.me/api/portraits/women/1.jpg" alt="" />
          <img src="https://randomuser.me/api/portraits/men/2.jpg" alt="" />
          <img src="https://randomuser.me/api/portraits/women/3.jpg" alt="" />
          <img src="https://randomuser.me/api/portraits/men/4.jpg" alt="" />
        </div>
        <span>{t('auth.trustedBy')} <strong>4,000+</strong> {t('auth.creators')}</span>
      </div>
    </div>

    <!-- Right panel — form card -->
    <div class="auth-card">
      <div class="auth-card-inner">

        <!-- Header -->
        <div class="auth-header">
          <div class="auth-icon-wrap">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4"/>
              <polyline points="10 17 15 12 10 7"/>
              <line x1="15" y1="12" x2="3" y2="12"/>
            </svg>
          </div>
          <h2 class="auth-title">{t('auth.loginTitle')}</h2>
          <p class="auth-subtitle">{t('auth.loginSubtitle')}</p>
        </div>

        <!-- Fields -->
        <div class="auth-fields">
          <div class:field-group--error={touched.email && !!fieldErrors.email} class="field-group">
            <label class="field-label" for="login-email">{t('auth.emailLabel')}</label>
            <div class="field-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
              </svg>
              <input
                id="login-email"
                class="field-input"
                type="email"
                placeholder={t('login_email')}
                bind:value={email}
                autocomplete="email"
                oninput={(event) => handleInput('email', event.currentTarget.value)}
                onblur={() => handleBlur('email')}
              />
            </div>
            {#if touched.email && fieldErrors.email}
              <p class="field-error">{fieldErrors.email}</p>
            {/if}
          </div>

          <div class:field-group--error={touched.password && !!fieldErrors.password} class="field-group">
            <label class="field-label" for="login-password">{t('auth.passwordLabel')}</label>
            <div class="field-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
              </svg>
              <input
                id="login-password"
                class="field-input field-input-pw"
                type={showPassword ? "text" : "password"}
                placeholder={t('login_pass')}
                bind:value={password}
                autocomplete="current-password"
                oninput={(event) => handleInput('password', event.currentTarget.value)}
                onblur={() => handleBlur('password')}
              />
              <button
                type="button"
                class="field-eye"
                onclick={() => showPassword = !showPassword}
                aria-label={t('auth.togglePassword')}
              >
                {#if showPassword}
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                {:else}
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                {/if}
              </button>
            </div>
            {#if touched.password && fieldErrors.password}
              <p class="field-error">{fieldErrors.password}</p>
            {/if}
          </div>
        </div>

        <!-- Submit -->
        <button type="button" class="auth-submit" onclick={login} disabled={isSubmitting || !isFormValid}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4"/>
            <polyline points="10 17 15 12 10 7"/>
            <line x1="15" y1="12" x2="3" y2="12"/>
          </svg>
          {isSubmitting ? 'Signing In...' : t('login_btn')}
        </button>

        {#if errorMessage}
          <div class="auth-alert auth-alert-error">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            {errorMessage}
          </div>
        {/if}

        <p class="auth-footer-link">
          {t('auth.noAccount')} <a href="/signup">{t('auth.signUpFree')}</a>
        </p>

      </div>
    </div>

  </div>
</div>

<style>
  :global(body) {
    background: radial-gradient(125% 125% at 50% 10%, #ffffff 40%, #6366f1 100%);
    color: #374151;
    margin: 0;
    min-height: 100vh;
    font-family: 'Inter', 'DM Sans', sans-serif;
  }

  /* ── Page shell ── */
  .auth-page {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 6rem 1.5rem 3rem;
  }

  .auth-orb {
    position: absolute; border-radius: 50%;
    filter: blur(110px); pointer-events: none; z-index: 0;
  }
  .auth-orb-1 {
    width: 680px; height: 680px;
    background: radial-gradient(circle, #7c3aed 0%, transparent 70%);
    top: -240px; right: -200px; opacity: 0.26;
  }
  .auth-orb-2 {
    width: 480px; height: 480px;
    background: radial-gradient(circle, #4c1d95 0%, transparent 70%);
    bottom: -120px; left: -100px; opacity: 0.20;
  }
  .auth-grid-overlay {
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background-image:
      linear-gradient(rgba(124,58,237,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(124,58,237,0.04) 1px, transparent 1px);
    background-size: 56px 56px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 0%, black 30%, transparent 100%);
  }

  /* ── Two-column layout ── */
  .auth-container {
    position: relative; z-index: 2;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 64px;
    max-width: 980px;
    width: 100%;
    align-items: center;
  }

  /* ── Left: branding ── */
  .auth-brand {
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 999px;
    padding: 5px 14px 5px 9px;
    font-size: 10.5px;
    font-weight: 600;
    color: #6366f1;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 28px;
    width: fit-content;
    box-shadow: 0 1px 4px rgba(99,102,241,0.08);
  }
  .brand-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #7c3aed;
    box-shadow: 0 0 8px #7c3aed;
    animation: bpulse 2s ease-in-out infinite;
  }
  @keyframes bpulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: .5; transform: scale(.75); }
  }

  .brand-heading {
    font-family: 'Sora', sans-serif;
    font-size: clamp(30px, 3.5vw, 44px);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #111827;
    margin: 0 0 18px;
  }
  .brand-heading span {
    background: linear-gradient(135deg, #c4b5fd 0%, #7c3aed 60%, #4c1d95 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .brand-sub {
    font-size: 15px;
    line-height: 1.72;
    color: #6b7280;
    margin: 0 0 30px;
    max-width: 380px;
    font-weight: 400;
  }

  /* Feature bullets */
  .brand-features {
    display: flex;
    flex-direction: column;
    gap: 13px;
    margin-bottom: 32px;
  }
  .bfeat {
    display: flex;
    align-items: center;
    gap: 11px;
    font-size: 14px;
    color: #4b5563;
    font-weight: 400;
  }
  .bfeat-icon {
    width: 24px; height: 24px;
    border-radius: 7px;
    flex-shrink: 0;
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #a78bfa;
  }

  /* Social proof */
  .brand-social {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13.5px;
    color: #6b7280;
    font-weight: 400;
  }
  .bsocial-avatars {
    display: flex;
  }
  .bsocial-avatars img {
    width: 28px; height: 28px;
    border-radius: 50%;
    object-fit: cover;
    border: 1.5px solid rgba(255,255,255,0.92);
    margin-left: -8px;
  }
  .bsocial-avatars img:first-child {
    margin-left: 0;
  }
  .brand-social strong {
    color: #111827;
    font-weight: 600;
  }

  /* ── Right: form card ── */
  .auth-card {
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(255,255,255,0.88);
    border-radius: 24px;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow:
      0 0 0 1px rgba(99,102,241,0.05),
      0 8px 24px rgba(17,24,39,0.07),
      0 32px 64px rgba(17,24,39,0.10),
      0 0 80px rgba(99,102,241,0.07);
  }
  .auth-card-inner {
    padding: 40px 36px;
  }

  /* Header */
  .auth-header {
    text-align: center;
    margin-bottom: 32px;
  }
  .auth-icon-wrap {
    width: 52px; height: 52px;
    border-radius: 14px;
    background: linear-gradient(135deg, #7c3aed, #4c1d95);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    color: #fff;
    box-shadow:
      0 8px 24px rgba(124,58,237,0.35),
      0 2px 6px rgba(124,58,237,0.2),
      inset 0 1px 0 rgba(255,255,255,0.15);
  }
  .auth-title {
    font-family: 'Sora', sans-serif;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -0.025em;
    color: #111827;
    margin: 0 0 7px;
  }
  .auth-subtitle {
    font-size: 13.5px;
    color: #6b7280;
    margin: 0;
    font-weight: 400;
    line-height: 1.5;
  }

  /* Fields */
  .auth-fields {
    display: flex;
    flex-direction: column;
    gap: 18px;
    margin-bottom: 22px;
  }
  .field-group {
    display: flex;
    flex-direction: column;
    gap: 7px;
  }
  .field-label {
    font-size: 11.5px;
    font-weight: 600;
    color: #7c3aed;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    opacity: 0.75;
  }

  .field-wrap {
    position: relative;
    display: flex;
    align-items: center;
    background: rgba(255,255,255,0.8);
    border: 1.5px solid rgba(209,213,219,0.8);
    border-radius: 12px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  }
  .field-wrap:hover {
    border-color: rgba(124,58,237,0.25);
    background: rgba(255,255,255,0.92);
  }
  .field-wrap:focus-within {
    border-color: rgba(124,58,237,0.5);
    background: rgba(255,255,255,0.96);
    box-shadow:
      0 0 0 3.5px rgba(124,58,237,0.10),
      0 2px 8px rgba(124,58,237,0.08);
  }
  .field-wrap:focus-within .field-icon {
    color: #7c3aed;
  }
  .field-group--error .field-wrap {
    border-color: rgba(220,38,38,0.4);
    box-shadow: 0 0 0 3.5px rgba(248,113,113,0.10);
  }
  .field-icon {
    position: absolute;
    left: 14px;
    color: #c4b5fd;
    flex-shrink: 0;
    pointer-events: none;
    transition: color 0.2s ease;
  }
  .field-input {
    width: 100%;
    padding: 13px 14px 13px 40px;
    background: transparent;
    border: none;
    outline: none;
    color: #111827;
    font-size: 14px;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    border-radius: 12px;
    box-sizing: border-box;
  }
  .field-input::placeholder {
    color: #c4b5fd;
    opacity: 0.7;
  }
  .field-input-pw {
    padding-right: 44px;
  }
  .field-eye {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    cursor: pointer;
    color: #c4b5fd;
    display: flex;
    align-items: center;
    padding: 4px;
    border-radius: 6px;
    transition: color 0.2s ease, background 0.2s ease;
  }
  .field-eye:hover {
    color: #7c3aed;
    background: rgba(124,58,237,0.07);
  }
  .field-error {
    margin: 8px 0 0;
    color: #b91c1c;
    font-size: 12.5px;
    font-weight: 600;
    line-height: 1.45;
  }

  /* Submit button */
  .auth-submit {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px;
    background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 50%, #4c1d95 100%);
    border: none;
    border-radius: 12px;
    color: #fff;
    font-size: 14.5px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: all 0.22s ease;
    box-shadow:
      0 8px 28px rgba(124,58,237,0.38),
      0 2px 8px rgba(124,58,237,0.2),
      inset 0 1px 0 rgba(255,255,255,0.12);
    margin-bottom: 0;
    position: relative;
    overflow: hidden;
  }
  .auth-submit::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(255,255,255,0.08) 0%, transparent 100%);
    pointer-events: none;
  }
  .auth-submit:hover {
    transform: translateY(-2px);
    box-shadow:
      0 14px 36px rgba(124,58,237,0.48),
      0 4px 12px rgba(124,58,237,0.22),
      inset 0 1px 0 rgba(255,255,255,0.12);
    filter: brightness(1.06);
  }
  .auth-submit:active {
    transform: translateY(0) scale(0.985);
    box-shadow:
      0 4px 16px rgba(124,58,237,0.3),
      inset 0 1px 0 rgba(255,255,255,0.1);
    filter: brightness(0.98);
  }
  .auth-submit:disabled {
    cursor: not-allowed;
    opacity: 0.68;
    transform: none;
    filter: none;
    box-shadow:
      0 4px 14px rgba(124,58,237,0.18),
      inset 0 1px 0 rgba(255,255,255,0.08);
  }

  /* Alert */
  .auth-alert {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 11px 14px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 500;
    margin-top: 16px;
    line-height: 1.45;
  }
  .auth-alert-error {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.18);
    color: #dc2626;
  }

  .auth-footer-link {
    text-align: center;
    font-size: 13.5px;
    color: #6b7280;
    margin: 20px 0 0;
    font-weight: 400;
  }
  .auth-footer-link a {
    color: #7c3aed;
    font-weight: 600;
    text-decoration: none;
    transition: color 0.2s ease;
  }
  .auth-footer-link a:hover {
    color: #4c1d95;
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  /* ── Responsive ── */
  @media (max-width: 760px) {
    .auth-container {
      grid-template-columns: 1fr;
      gap: 0;
    }
    .auth-brand {
      display: none;
    }
    .auth-page {
      padding: 5rem 1rem 2rem;
    }
    .auth-card-inner {
      padding: 32px 24px;
    }
  }
</style>
