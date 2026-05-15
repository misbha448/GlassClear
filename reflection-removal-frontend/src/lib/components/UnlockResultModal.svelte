<svelte:options runes={false} />

<script>
  import { appState, t } from '$lib/state.svelte.js';

  export let open = false;
  export let onLogin = () => {};
  export let onSignup = () => {};
  export let onClose = () => {};

  const MODAL_COPY = {
    en: {
      kicker: 'Download Image',
      title: 'Login or signup to download this image',
      body: 'Please login or create an account to download your processed result.',
      noteTitle: 'Download is available after login',
      noteBody: 'Once you login or signup, you can download this image and access your saved results.',
      login: 'Login',
      signup: 'Signup',
      close: 'Close'
    },
    hi: {
      kicker: 'इमेज डाउनलोड',
      title: 'इस इमेज को डाउनलोड करने के लिए लॉगिन या साइनअप करें',
      body: 'कृपया अपना प्रोसेस्ड रिजल्ट डाउनलोड करने के लिए लॉगिन करें या अकाउंट बनाएं।',
      noteTitle: 'लॉगिन के बाद डाउनलोड उपलब्ध है',
      noteBody: 'लॉगिन या साइनअप करने के बाद आप इस इमेज को डाउनलोड कर सकते हैं और सेव रिजल्ट देख सकते हैं।',
      login: 'लॉगिन',
      signup: 'साइनअप',
      close: 'बंद करें'
    },
    kn: {
      kicker: 'ಚಿತ್ರ ಡೌನ್‌ಲೋಡ್',
      title: 'ಈ ಚಿತ್ರವನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಲು ಲಾಗಿನ್ ಅಥವಾ ಸೈನ್‌ಅಪ್ ಮಾಡಿ',
      body: 'ನಿಮ್ಮ ಪ್ರೊಸೆಸ್ಡ್ ಫಲಿತಾಂಶವನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಲು ದಯವಿಟ್ಟು ಲಾಗಿನ್ ಮಾಡಿ ಅಥವಾ ಖಾತೆ ರಚಿಸಿ.',
      noteTitle: 'ಲಾಗಿನ್ ಆದ ಮೇಲೆ ಡೌನ್‌ಲೋಡ್ ಲಭ್ಯ',
      noteBody: 'ನೀವು ಲಾಗಿನ್ ಅಥವಾ ಸೈನ್‌ಅಪ್ ಮಾಡಿದ ಬಳಿಕ ಈ ಚಿತ್ರವನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಬಹುದು ಮತ್ತು ಉಳಿಸಿದ ಫಲಿತಾಂಶಗಳನ್ನು ನೋಡಬಹುದು.',
      login: 'ಲಾಗಿನ್',
      signup: 'ಸೈನ್‌ಅಪ್',
      close: 'ಮುಚ್ಚಿ'
    }
  };

  $: modalCopy = MODAL_COPY[appState.languageCode] || MODAL_COPY.en;
</script>

{#if open}
  <div class="gc-unlock-backdrop" role="presentation" on:click={onClose}>
    <div
      class="gc-unlock-modal"
      role="dialog"
      aria-modal="true"
      aria-label={t('unlockResult.ariaLabel')}
      tabindex="-1"
      on:click|stopPropagation
      on:keydown|stopPropagation
    >
      <div class="gc-unlock-modal__header">
        <span class="gc-unlock-kicker">{modalCopy.kicker}</span>
        <h2>{modalCopy.title}</h2>
        <p>{modalCopy.body}</p>
      </div>

      <div class="gc-unlock-note">
        <div class="gc-unlock-note__icon" aria-hidden="true">
          <i class="bi bi-download"></i>
        </div>
        <div>
          <strong>{modalCopy.noteTitle}</strong>
          <p>{modalCopy.noteBody}</p>
        </div>
      </div>

      <div class="gc-unlock-modal__actions">
        <button type="button" class="gc-unlock-button gc-unlock-button--primary" on:click={onLogin}>
          {modalCopy.login}
        </button>
        <button type="button" class="gc-unlock-button gc-unlock-button--secondary" on:click={onSignup}>
          {modalCopy.signup}
        </button>
        <button type="button" class="gc-unlock-button gc-unlock-button--ghost" on:click={onClose}>
          {modalCopy.close}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .gc-unlock-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(31, 41, 55, 0.22);
    backdrop-filter: blur(8px);
    display: grid;
    place-items: center;
    padding: 24px;
    z-index: 120;
  }

  .gc-unlock-modal {
    width: min(480px, 100%);
    padding: 30px;
    border-radius: 28px;
    background: linear-gradient(180deg, #ffffff 0%, #f8faff 100%);
    border: 1px solid rgba(99, 102, 241, 0.12);
    box-shadow: 0 24px 60px rgba(99, 102, 241, 0.14);
    color: #182033;
  }

  .gc-unlock-kicker {
    display: inline-block;
    margin-bottom: 12px;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5b4ff5;
    background: rgba(99, 102, 241, 0.08);
  }

  .gc-unlock-modal__header h2 {
    margin: 0 0 10px;
    font-size: 30px;
    line-height: 1.15;
    color: #111827;
  }

  .gc-unlock-modal__header p {
    margin: 0;
    color: #5b6477;
    line-height: 1.65;
  }

  .gc-unlock-note {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    margin: 24px 0 22px;
    padding: 16px 18px;
    border-radius: 18px;
    background: #eef2ff;
    border: 1px solid rgba(99, 102, 241, 0.12);
  }

  .gc-unlock-note__icon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    background: linear-gradient(135deg, #6d5dfc, #4f46e5);
    color: #fff;
    font-size: 18px;
    box-shadow: 0 10px 24px rgba(99, 102, 241, 0.24);
  }

  .gc-unlock-note strong {
    display: block;
    margin-bottom: 4px;
    color: #1f2937;
    font-size: 15px;
  }

  .gc-unlock-note p {
    margin: 0;
    color: #606b80;
    font-size: 14px;
    line-height: 1.55;
  }

  .gc-unlock-modal__actions {
    display: grid;
    gap: 10px;
  }

  .gc-unlock-button {
    border: 1px solid transparent;
    border-radius: 14px;
    padding: 13px 16px;
    font: inherit;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.18s ease, filter 0.18s ease, border-color 0.18s ease;
  }

  .gc-unlock-button:hover {
    transform: translateY(-1px);
  }

  .gc-unlock-button--primary {
    color: white;
    background: linear-gradient(135deg, #6d5dfc, #4f46e5);
    box-shadow: 0 14px 28px rgba(99, 102, 241, 0.24);
  }

  .gc-unlock-button--secondary,
  .gc-unlock-button--ghost {
    color: #273046;
    background: #ffffff;
    border-color: rgba(148, 163, 184, 0.28);
  }

  .gc-unlock-button--secondary:hover,
  .gc-unlock-button--ghost:hover {
    border-color: rgba(99, 102, 241, 0.28);
    background: #f8faff;
  }

  @media (max-width: 640px) {
    .gc-unlock-modal {
      padding: 22px;
    }

    .gc-unlock-note {
      padding: 14px;
    }
  }
</style>
