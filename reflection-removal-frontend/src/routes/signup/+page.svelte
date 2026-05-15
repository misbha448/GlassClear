<!-- src/routes/signup/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  import Navbar from '$lib/components/Navbar.svelte';
  import { apiFetch } from '$lib/api/api.js';
  import { t } from '$lib/state.svelte.js';
  import {
    getPasswordChecks,
    mapAuthServerError,
    normalizeEmail,
    normalizeName,
    validateConfirmPassword,
    validateEmail,
    validateName,
    validatePassword
  } from '$lib/utils/authValidation.js';

  let name = $state("");
  let email = $state("");
  let password = $state("");
  let confirmPassword = $state("");
  let successMessage = $state("");
  let errorMessage = $state("");
  let showPassword = $state(false);
  let isSubmitting = $state(false);
  let touched = $state({
    name: false,
    email: false,
    password: false,
    confirmPassword: false
  });
  let fieldErrors = $state({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const passwordChecks = $derived(getPasswordChecks(password));
  const isFormValid = $derived(
    !validateName(name) &&
    !validateEmail(email) &&
    !validatePassword(password) &&
    !validateConfirmPassword(password, confirmPassword)
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
    if (field === 'name') {
      setFieldError('name', validateName(name));
      return;
    }
    if (field === 'email') {
      setFieldError('email', validateEmail(email));
      return;
    }
    if (field === 'password') {
      setFieldError('password', validatePassword(password));
      if (touched.confirmPassword || confirmPassword) {
        setFieldError('confirmPassword', validateConfirmPassword(password, confirmPassword));
      }
      return;
    }
    if (field === 'confirmPassword') {
      setFieldError('confirmPassword', validateConfirmPassword(password, confirmPassword));
    }
  }

  function validateForm(markAllTouched = false) {
    if (markAllTouched) {
      touched = {
        name: true,
        email: true,
        password: true,
        confirmPassword: true
      };
    }

    const nextErrors = {
      name: validateName(name),
      email: validateEmail(email),
      password: validatePassword(password),
      confirmPassword: validateConfirmPassword(password, confirmPassword)
    };
    fieldErrors = nextErrors;
    return !nextErrors.name && !nextErrors.email && !nextErrors.password && !nextErrors.confirmPassword;
  }

  function handleBlur(field) {
    if (field === 'name') {
      name = normalizeName(name);
    } else if (field === 'email') {
      email = normalizeEmail(email);
    }

    setTouched(field);
    validateField(field);
  }

  function handleInput(field, value) {
    if (field === 'name') {
      name = value;
    } else if (field === 'email') {
      email = value;
    } else if (field === 'password') {
      password = value;
    } else if (field === 'confirmPassword') {
      confirmPassword = value;
    }

    successMessage = "";
    errorMessage = "";

    if (touched[field]) {
      validateField(field);
    }
    if (field === 'password' && (touched.confirmPassword || confirmPassword)) {
      validateField('confirmPassword');
    }
  }

  async function signup() {
    successMessage = "";
    errorMessage = "";
    if (!validateForm(true)) {
      return;
    }

    isSubmitting = true;
    try {
      const trimmedName = normalizeName(name);
      const trimmedEmail = normalizeEmail(email);
      const rawPassword = password;
      name = trimmedName;
      email = trimmedEmail;

      const response = await apiFetch("/api/v1/auth/register", {
        method: "POST",
        body: { name: trimmedName, email: trimmedEmail, password: rawPassword }
      });
      const data = await response.json();
      if (!response.ok) {
        const serverMessage = typeof data.detail === 'string' ? data.detail : t('signup_error_msg');
        const mappedError = mapAuthServerError(serverMessage);

        if (mappedError.field) {
          setTouched(mappedError.field);
          setFieldError(mappedError.field, mappedError.message);
        } else {
          errorMessage = mappedError.message || t('signup_error_msg');
        }
        return;
      }
      const loginResponse = await apiFetch("/api/v1/auth/login", {
        method: "POST",
        body: { email: trimmedEmail, password: rawPassword }
      });
      const loginData = await loginResponse.json();
      if (!loginResponse.ok) {
        successMessage = t('signup_success');
        errorMessage = t('auth.accountCreatedLogin');
        name = ""; email = ""; password = ""; confirmPassword = "";
        touched = { name: false, email: false, password: false, confirmPassword: false };
        fieldErrors = { name: '', email: '', password: '', confirmPassword: '' };
        return;
      }

      localStorage.setItem("token", loginData.access_token);
      localStorage.setItem("token_type", loginData.token_type);
      localStorage.setItem("role", loginData.role);
      if (loginData.user_name) {
        localStorage.setItem("user_name", loginData.user_name);
      }
      window.location.href = loginData.role === 'admin' ? '/admin/dashboard' : '/dashboard';
    } catch (error) {
      errorMessage = t('signup_error_msg');
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
        {t('auth.signupBadge')}
      </div>
      <h1 class="brand-heading">
        {t('auth.signupHeroLine1')}<br />
        <span>{t('auth.signupHeroLine2')}</span>
      </h1>
      <p class="brand-sub">
        {t('auth.signupHeroSubtitle')}
      </p>
      <div class="brand-stats">
        <div class="bstat">
          <span class="bstat-val">99.2%</span>
          <span class="bstat-lbl">{t('auth.accuracy')}</span>
        </div>
        <div class="bstat-div"></div>
        <div class="bstat">
          <span class="bstat-val">&lt; 3s</span>
          <span class="bstat-lbl">{t('auth.processingLabel')}</span>
        </div>
        <div class="bstat-div"></div>
        <div class="bstat">
          <span class="bstat-val">4K</span>
          <span class="bstat-lbl">{t('auth.resolution')}</span>
        </div>
      </div>
      <!-- Floating testimonial snippet -->
      <div class="brand-testi">
        <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Arjun" class="btesti-avatar" />
        <div>
          <p class="btesti-quote">"{t('auth.signupQuote')}"</p>
          <span class="btesti-name">{t('auth.signupQuoteAuthor')}</span>
        </div>
      </div>
    </div>

    <!-- Right panel — form -->
    <div class="auth-card">
      <div class="auth-card-inner">

        <!-- Header -->
        <div class="auth-header">
          <div class="auth-icon-wrap">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/>
            </svg>
          </div>
          <h2 class="auth-title">{t('auth.signupTitle')}</h2>
          <p class="auth-subtitle">{t('auth.signupSubtitle')}</p>
        </div>

        <!-- Fields -->
        <div class="auth-fields">
          <div class:field-group--error={touched.name && !!fieldErrors.name} class="field-group">
            <label class="field-label" for="signup-name">{t('auth.fullNameLabel')}</label>
            <div class="field-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
              <input
                id="signup-name"
                class="field-input"
                type="text"
                placeholder={t('signup_name')}
                bind:value={name}
                autocomplete="name"
                oninput={(event) => handleInput('name', event.currentTarget.value)}
                onblur={() => handleBlur('name')}
              />
            </div>
            {#if touched.name && fieldErrors.name}
              <p class="field-error">{fieldErrors.name}</p>
            {/if}
          </div>

          <div class:field-group--error={touched.email && !!fieldErrors.email} class="field-group">
            <label class="field-label" for="signup-email">{t('auth.emailLabel')}</label>
            <div class="field-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
              </svg>
              <input
                id="signup-email"
                class="field-input"
                type="email"
                placeholder={t('signup_email')}
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
            <label class="field-label" for="signup-password">{t('auth.passwordLabel')}</label>
            <div class="field-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
              </svg>
              <input
                id="signup-password"
                class="field-input field-input-pw"
                type={showPassword ? "text" : "password"}
                placeholder={t('signup_pass')}
                bind:value={password}
                autocomplete="new-password"
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

            <div class="password-helper">
              <p class="password-helper__title">Password must include:</p>
              <div class="password-helper__list">
                <span class:password-helper__item--done={passwordChecks.minLength} class="password-helper__item">8 characters</span>
                <span class:password-helper__item--done={passwordChecks.uppercase} class="password-helper__item">Uppercase letter</span>
                <span class:password-helper__item--done={passwordChecks.lowercase} class="password-helper__item">Lowercase letter</span>
                <span class:password-helper__item--done={passwordChecks.number} class="password-helper__item">Number</span>
                <span class:password-helper__item--done={passwordChecks.special} class="password-helper__item">Special character</span>
              </div>
            </div>
          </div>

          <div class:field-group--error={touched.confirmPassword && !!fieldErrors.confirmPassword} class="field-group">
            <label class="field-label" for="signup-confirm-password">Confirm Password</label>
            <div class="field-wrap">
              <svg class="field-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
              </svg>
              <input
                id="signup-confirm-password"
                class="field-input field-input-pw"
                type={showPassword ? "text" : "password"}
                placeholder="Confirm your password"
                bind:value={confirmPassword}
                autocomplete="new-password"
                oninput={(event) => handleInput('confirmPassword', event.currentTarget.value)}
                onblur={() => handleBlur('confirmPassword')}
              />
            </div>
            {#if touched.confirmPassword && fieldErrors.confirmPassword}
              <p class="field-error">{fieldErrors.confirmPassword}</p>
            {/if}
          </div>
        </div>

        <!-- Submit -->
        <button type="button" class="auth-submit" onclick={signup} disabled={isSubmitting || !isFormValid}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/>
            <line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/>
          </svg>
          {isSubmitting ? 'Creating Account...' : t('signup_btn')}
        </button>

        {#if successMessage}
          <div class="auth-alert auth-alert-success">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            {successMessage}
          </div>
        {/if}

        {#if errorMessage}
          <div class="auth-alert auth-alert-error">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            {errorMessage}
          </div>
        {/if}

        <p class="auth-footer-link">
          {t('auth.alreadyHaveAccount')} <a href="/login">{t('auth.signIn')}</a>
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

  /* ── Orb glows — unchanged colors ── */
  .auth-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(110px);
    pointer-events: none;
    z-index: 0;
  }
  .auth-orb-1 {
    width: 680px; height: 680px;
    background: radial-gradient(circle, #7c3aed 0%, transparent 70%);
    top: -240px; left: -200px;
    opacity: 0.28;
  }
  .auth-orb-2 {
    width: 480px; height: 480px;
    background: radial-gradient(circle, #4c1d95 0%, transparent 70%);
    bottom: -120px; right: -100px;
    opacity: 0.22;
  }
  .auth-grid-overlay {
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background-image:
      linear-gradient(rgba(124,58,237,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(124,58,237,0.04) 1px, transparent 1px);
    background-size: 56px 56px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 0%, black 30%, transparent 100%);
  }

  /* ── Two-column container ── */
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
    margin: 0 0 34px;
    max-width: 380px;
    font-weight: 400;
  }

  /* Stats row */
  .brand-stats {
    display: flex;
    align-items: center;
    gap: 24px;
    margin-bottom: 32px;
    padding: 18px 22px;
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(99,102,241,0.13);
    border-radius: 16px;
    width: fit-content;
    box-shadow: 0 2px 12px rgba(99,102,241,0.06), 0 1px 3px rgba(0,0,0,0.04);
  }
  .bstat {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
  }
  .bstat-val {
    font-family: 'Sora', sans-serif;
    font-size: 19px;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #c4b5fd, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .bstat-lbl {
    font-size: 10.5px;
    color: #9ca3af;
    letter-spacing: 0.04em;
    font-weight: 500;
  }
  .bstat-div {
    width: 1px;
    height: 28px;
    background: rgba(124,58,237,0.15);
  }

  /* Testimonial */
  .brand-testi {
    display: flex;
    align-items: flex-start;
    gap: 13px;
    padding: 16px 18px;
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(99,102,241,0.11);
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(99,102,241,0.05), 0 1px 3px rgba(0,0,0,0.04);
  }
  .btesti-avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    object-fit: cover;
    border: 1.5px solid rgba(124,58,237,0.22);
    flex-shrink: 0;
  }
  .btesti-quote {
    font-size: 13.5px;
    color: #374151;
    line-height: 1.6;
    margin: 0 0 5px;
    font-style: italic;
    font-weight: 400;
  }
  .btesti-name {
    font-size: 11px;
    color: rgba(124,58,237,0.55);
    font-weight: 600;
    letter-spacing: 0.01em;
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
  .password-helper {
    margin-top: 10px;
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(196,181,253,0.36);
  }
  .password-helper__title {
    margin: 0 0 8px;
    font-size: 12px;
    font-weight: 700;
    color: #6d28d9;
  }
  .password-helper__list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
  }
  .password-helper__item {
    font-size: 12px;
    color: #6b7280;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .password-helper__item::before {
    content: '○';
    color: #c4b5fd;
    font-size: 11px;
  }
  .password-helper__item--done {
    color: #166534;
    font-weight: 600;
  }
  .password-helper__item--done::before {
    content: '✓';
    color: #16a34a;
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

  /* Alerts */
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
  .auth-alert-success {
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.2);
    color: #16a34a;
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
      gap: 40px;
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
