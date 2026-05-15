<script>
  import { slide } from 'svelte/transition';
  import { untrack } from 'svelte';
  import { onMount } from 'svelte';
  import { appState, t } from '$lib/state.svelte.js';

  let isOpen = $state(false);
  let messages = $state([]);
  let userInput = $state('');
  let isTyping = $state(false);
  let chatBodyEl = $state(null);

  // Initialise greeting after mount so t() store is fully ready
  onMount(() => {
    messages = [{ role: 'ai', text: t('chat_greet') }];
  });

  // Keep greeting in sync with language changes
  $effect(() => {
    const newGreeting = t('chat_greet');
    untrack(() => {
      if (messages.length === 1 && messages[0]?.role === 'ai') {
        messages[0].text = newGreeting;
      }
    });
  });

  // Auto-scroll to bottom on new messages
  $effect(() => {
    if (messages.length && chatBodyEl) {
      setTimeout(() => {
        chatBodyEl.scrollTop = chatBodyEl.scrollHeight;
      }, 60);
    }
  });

  const examplePrompts = [
    'chat_p1',
    'chat_p2',
    'chat_p3'
  ];

  async function sendMessage(text = null) {
    const messageToSend = text ? t(text) : userInput;
    if (!messageToSend.trim() || isTyping) return;

    messages.push({ role: 'user', text: messageToSend });
    if (!text) userInput = '';
    isTyping = true;

    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageToSend })
      });

      const data = await response.json();
      messages.push({ role: 'ai', text: data.response });
    } catch (error) {
      messages.push({ role: 'ai', text: t('chat_error') });
    } finally {
      isTyping = false;
    }
  }
</script>

<div class="chatbot-container">
  {#if isOpen}
    <div class="chat-window" transition:slide={{ axis: 'y', duration: 260 }}>

      <!-- ── HEADER ── -->
      <div class="chat-header">
        <div class="header-left">
          <div class="ai-avatar">
            <!-- Sparkle / AI icon -->
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M12 2C12 2 13.5 7 17 8.5C13.5 10 12 15 12 15C12 15 10.5 10 7 8.5C10.5 7 12 2 12 2Z" fill="white" opacity="0.95"/>
              <path d="M19 14C19 14 19.8 16.8 21.5 17.5C19.8 18.2 19 21 19 21C19 21 18.2 18.2 16.5 17.5C18.2 16.8 19 14 19 14Z" fill="white" opacity="0.80"/>
              <path d="M5.5 3C5.5 3 6.1 5.1 7.5 5.8C6.1 6.5 5.5 8.5 5.5 8.5C5.5 8.5 4.9 6.5 3.5 5.8C4.9 5.1 5.5 3 5.5 3Z" fill="white" opacity="0.70"/>
            </svg>
          </div>
          <div class="header-text">
            <span class="header-name">{t('chat_assistant')}</span>
            <span class="header-status">
              <span class="status-dot"></span>
              Online
            </span>
          </div>
        </div>
        <button class="close-btn" onclick={() => isOpen = false} aria-label="Close chat">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <path d="M18 6 6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- ── BODY ── -->
      <div class="chat-body" bind:this={chatBodyEl}>
        {#each messages as msg, i}
          <div class="message-wrapper {msg.role}" style="animation-delay: {i === 0 ? 0 : 0}ms">
            {#if msg.role === 'ai'}
              <div class="ai-mini-avatar">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C12 2 13.5 7 17 8.5C13.5 10 12 15 12 15C12 15 10.5 10 7 8.5C10.5 7 12 2 12 2Z" fill="currentColor"/>
                </svg>
              </div>
            {/if}
            <div class="message-bubble">{msg.text}</div>
          </div>
        {/each}

        <!-- Suggested prompts (only while just the greeting is showing) -->
        {#if messages.length === 1 && messages[0]?.role === 'ai'}
          <div class="example-prompts">
            <p class="prompts-label">{t('chat_suggested')}</p>
            {#each examplePrompts as prompt}
              <button class="prompt-btn" onclick={() => sendMessage(prompt)}>
                <span class="prompt-arrow">→</span>
                {t(prompt)}
              </button>
            {/each}
          </div>
        {/if}

        <!-- Typing indicator -->
        {#if isTyping}
          <div class="message-wrapper ai">
            <div class="ai-mini-avatar">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none">
                <path d="M12 2C12 2 13.5 7 17 8.5C13.5 10 12 15 12 15C12 15 10.5 10 7 8.5C10.5 7 12 2 12 2Z" fill="currentColor"/>
              </svg>
            </div>
            <div class="message-bubble typing-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        {/if}
      </div>

      <!-- ── FOOTER ── -->
      <div class="chat-footer">
        <form onsubmit={(e) => { e.preventDefault(); sendMessage(); }} class="input-row">
          <input
            type="text"
            bind:value={userInput}
            placeholder={t('chat_placeholder')}
            class="chat-input"
            autocomplete="off"
          />
          <button type="submit" class="send-btn" disabled={isTyping} aria-label="Send message">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 2 11 13M22 2 15 22l-4-9-9-4 20-7z"/>
            </svg>
          </button>
        </form>
      </div>

    </div>
  {/if}

  <!-- ── FAB TOGGLE ── -->
  <button class="chat-toggle-btn" onclick={() => isOpen = !isOpen} aria-label="Toggle Chatbot">
    <div class="fab-inner">
      {#if isOpen}
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <path d="M18 6 6 18M6 6l12 12"/>
        </svg>
      {:else}
        <!-- Sparkle star icon — premium AI feel -->
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M12 3C12 3 14 9.5 19 11C14 12.5 12 19 12 19C12 19 10 12.5 5 11C10 9.5 12 3 12 3Z" fill="white"/>
          <path d="M20 2C20 2 20.8 4.5 22.5 5.5C20.8 6.5 20 9 20 9C20 9 19.2 6.5 17.5 5.5C19.2 4.5 20 2 20 2Z" fill="white" opacity="0.75"/>
          <path d="M5 15C5 15 5.6 17 7 17.8C5.6 18.6 5 20.5 5 20.5C5 20.5 4.4 18.6 3 17.8C4.4 17 5 15 5 15Z" fill="white" opacity="0.65"/>
        </svg>
      {/if}
    </div>
    <!-- Glow ring -->
    <div class="fab-glow"></div>
  </button>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

  /* ── DESIGN TOKENS ── */
  .chatbot-container {
    --c-indigo:       #6366f1;
    --c-indigo-dark:  #4f46e5;
    --c-violet:       #8b5cf6;
    --c-ink:          #111827;
    --c-ink-soft:     #374151;
    --c-muted:        #64748b;
    --c-subtle:       #94a3b8;
    --c-border:       rgba(99,102,241,0.13);
    --c-surface:      rgba(255,255,255,0.96);
    --c-body-bg:      #f5f4ff;
    --c-shadow:       0 24px 64px rgba(79,70,229,0.18), 0 6px 20px rgba(15,23,42,0.08);
    --c-font:         'DM Sans', system-ui, sans-serif;

    position: fixed;
    right: 24px;
    bottom: 24px;
    z-index: 6000;
    font-family: var(--c-font);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  /* ════════════════════════════════
     FAB TOGGLE BUTTON
  ════════════════════════════════ */
  .chat-toggle-btn {
    position: relative;
    z-index: 2;
    width: 62px;
    height: 62px;
    border-radius: 22px;
    background: linear-gradient(145deg, #6366f1 0%, #8b5cf6 55%, #a78bfa 100%);
    border: none;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    /* Layered shadow for depth */
    box-shadow:
      0 0 0 1px rgba(255,255,255,0.15) inset,
      0 1px 0 rgba(255,255,255,0.25) inset,
      0 12px 32px rgba(99,102,241,0.40),
      0 4px 10px rgba(99,102,241,0.22);
    transition: transform 0.28s cubic-bezier(0.34,1.56,0.64,1),
                box-shadow 0.28s ease;
    overflow: visible;
  }

  .chat-toggle-btn:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow:
      0 0 0 1px rgba(255,255,255,0.18) inset,
      0 1px 0 rgba(255,255,255,0.28) inset,
      0 20px 48px rgba(99,102,241,0.50),
      0 6px 16px rgba(99,102,241,0.28);
  }

  .fab-inner {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Subtle animated glow ring behind FAB */
  .fab-glow {
    position: absolute;
    inset: -6px;
    border-radius: 28px;
    background: radial-gradient(circle, rgba(99,102,241,0.30) 0%, transparent 70%);
    z-index: 0;
    animation: glow-pulse 3s ease-in-out infinite;
    pointer-events: none;
  }

  @keyframes glow-pulse {
    0%,100% { opacity: 0.6; transform: scale(1); }
    50%      { opacity: 1;   transform: scale(1.08); }
  }

  /* ════════════════════════════════
     CHAT WINDOW
  ════════════════════════════════ */
  .chat-window {
    position: absolute;
    right: 0;
    bottom: 78px;
    z-index: 3;
    width: 384px;
    height: 576px;
    display: flex;
    flex-direction: column;
    /* Glassmorphism surface matching landing page radial */
    background:
      radial-gradient(ellipse 90% 45% at 50% -8%, rgba(99,102,241,0.11) 0%, transparent 58%),
      rgba(255,255,255,0.94);
    backdrop-filter: blur(32px) saturate(2);
    -webkit-backdrop-filter: blur(32px) saturate(2);
    border: 1px solid var(--c-border);
    border-radius: 28px;
    overflow: hidden;
    box-shadow: var(--c-shadow);
  }

  /* ── HEADER ── */
  .chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 18px;
    background: rgba(255,255,255,0.98);
    border-bottom: 1px solid rgba(99,102,241,0.09);
    flex-shrink: 0;
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 11px;
  }

  .ai-avatar {
    width: 40px;
    height: 40px;
    border-radius: 14px;
    background: linear-gradient(145deg, #6366f1 0%, #8b5cf6 60%, #a78bfa 100%);
    display: grid;
    place-items: center;
    color: #fff;
    flex-shrink: 0;
    box-shadow:
      0 4px 14px rgba(99,102,241,0.35),
      0 0 0 1px rgba(255,255,255,0.15) inset;
  }

  .header-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .header-name {
    font-size: 14.5px;
    font-weight: 700;
    color: var(--c-ink);
    letter-spacing: -0.025em;
    line-height: 1.15;
  }

  .header-status {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 11.5px;
    color: var(--c-muted);
    font-weight: 500;
    letter-spacing: 0.01em;
  }

  .status-dot {
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
    animation: status-pulse 2.4s ease-in-out infinite;
  }

  @keyframes status-pulse {
    0%,100% { box-shadow: 0 0 0 0px rgba(16,185,129,0.40); }
    50%      { box-shadow: 0 0 0 4px rgba(16,185,129,0.12); }
  }

  .close-btn {
    width: 30px;
    height: 30px;
    border-radius: 9px;
    border: 1px solid rgba(99,102,241,0.13);
    background: rgba(99,102,241,0.06);
    color: var(--c-muted);
    display: grid;
    place-items: center;
    cursor: pointer;
    transition: background 0.14s ease, color 0.14s ease, border-color 0.14s ease;
    flex-shrink: 0;
  }

  .close-btn:hover {
    background: rgba(99,102,241,0.12);
    border-color: rgba(99,102,241,0.30);
    color: var(--c-indigo);
  }

  /* ── BODY ── */
  .chat-body {
    flex: 1;
    overflow-y: auto;
    padding: 16px 15px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: var(--c-body-bg);
    scroll-behavior: smooth;
  }

  .chat-body::-webkit-scrollbar { width: 3px; }
  .chat-body::-webkit-scrollbar-track { background: transparent; }
  .chat-body::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,0.20);
    border-radius: 10px;
  }

  /* ── MESSAGES ── */
  .message-wrapper {
    display: flex;
    align-items: flex-end;
    gap: 7px;
    width: 100%;
    animation: msgIn 0.20s cubic-bezier(0.34,1.5,0.64,1) both;
  }

  @keyframes msgIn {
    from { opacity: 0; transform: translateY(8px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }

  .message-wrapper.user { justify-content: flex-end; }

  /* Small AI avatar dot beside each AI bubble */
  .ai-mini-avatar {
    width: 24px;
    height: 24px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15));
    border: 1px solid rgba(99,102,241,0.16);
    display: grid;
    place-items: center;
    color: var(--c-indigo);
    flex-shrink: 0;
    margin-bottom: 2px;
  }

  /* ── BUBBLES ── */
  .message-bubble {
    max-width: 80%;
    padding: 11px 14px;
    border-radius: 18px;
    font-size: 13.5px;
    font-weight: 400;
    line-height: 1.62;
    font-family: var(--c-font);
    letter-spacing: -0.005em;
    word-break: break-word;
  }

  /* User bubble */
  .user .message-bubble {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: #ffffff;
    border-bottom-right-radius: 5px;
    box-shadow:
      0 6px 20px rgba(99,102,241,0.30),
      0 2px 6px rgba(99,102,241,0.16);
  }

  /* AI bubble */
  .ai .message-bubble {
    background: #ffffff;
    color: var(--c-ink-soft);
    border: 1px solid rgba(99,102,241,0.11);
    border-bottom-left-radius: 5px;
    box-shadow: 0 2px 8px rgba(15,23,42,0.06);
  }

  /* ── TYPING INDICATOR ── */
  .typing-dots {
    display: flex !important;
    align-items: center;
    gap: 5px;
    padding: 13px 16px !important;
    min-width: 58px;
  }

  .typing-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--c-indigo);
    opacity: 0.30;
    display: block;
    animation: typingBounce 1.4s ease-in-out infinite;
    flex-shrink: 0;
  }

  .typing-dots span:nth-child(2) { animation-delay: 0.18s; }
  .typing-dots span:nth-child(3) { animation-delay: 0.36s; }

  @keyframes typingBounce {
    0%,100% { opacity: 0.30; transform: translateY(0);    }
    50%      { opacity: 1;    transform: translateY(-4px); }
  }

  /* ── SUGGESTED PROMPTS ── */
  .example-prompts {
    display: flex;
    flex-direction: column;
    gap: 7px;
    margin-top: 2px;
    animation: msgIn 0.28s ease 0.12s both;
  }

  .prompts-label {
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--c-subtle);
    margin: 0 0 3px 2px;
  }

  .prompt-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    text-align: left;
    padding: 10px 14px;
    border-radius: 13px;
    border: 1px solid rgba(99,102,241,0.16);
    background: rgba(255,255,255,0.92);
    color: var(--c-ink-soft);
    font-family: var(--c-font);
    font-size: 13px;
    font-weight: 500;
    line-height: 1.45;
    letter-spacing: -0.01em;
    cursor: pointer;
    transition: all 0.15s ease;
    box-shadow: 0 1px 4px rgba(15,23,42,0.05);
  }

  .prompt-arrow {
    color: var(--c-indigo);
    opacity: 0.60;
    font-size: 14px;
    flex-shrink: 0;
    transition: transform 0.15s ease, opacity 0.15s ease;
  }

  .prompt-btn:hover {
    background: rgba(99,102,241,0.07);
    border-color: rgba(99,102,241,0.32);
    color: var(--c-indigo);
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(99,102,241,0.13);
  }

  .prompt-btn:hover .prompt-arrow {
    transform: translateX(3px);
    opacity: 1;
  }

  /* ── FOOTER INPUT ── */
  .chat-footer {
    padding: 13px 15px;
    background: rgba(255,255,255,0.99);
    border-top: 1px solid rgba(99,102,241,0.09);
    flex-shrink: 0;
  }

  .input-row {
    display: flex;
    align-items: center;
    gap: 9px;
    background: rgba(245,244,255,0.90);
    border: 1.5px solid rgba(99,102,241,0.16);
    border-radius: 16px;
    padding: 6px 6px 6px 15px;
    transition: border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
  }

  .input-row:focus-within {
    border-color: rgba(99,102,241,0.42);
    box-shadow: 0 0 0 3px rgba(99,102,241,0.09);
    background: #ffffff;
  }

  .chat-input {
    flex: 1;
    border: none;
    background: transparent;
    color: var(--c-ink);
    font-family: var(--c-font);
    font-size: 13.5px;
    font-weight: 400;
    letter-spacing: -0.005em;
    outline: none;
    min-height: 32px;
    caret-color: var(--c-indigo);
  }

  .chat-input::placeholder {
    color: var(--c-subtle);
    font-weight: 400;
  }

  .send-btn {
    width: 36px;
    height: 36px;
    min-width: 36px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, var(--c-indigo), var(--c-violet));
    color: #fff;
    display: grid;
    place-items: center;
    cursor: pointer;
    flex-shrink: 0;
    box-shadow: 0 3px 10px rgba(99,102,241,0.32);
    transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.15s ease;
  }

  .send-btn:hover:not(:disabled) {
    transform: scale(1.07);
    box-shadow: 0 6px 18px rgba(99,102,241,0.42);
  }

  .send-btn:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }

  /* ── MOBILE ── */
  @media (max-width: 640px) {
    .chatbot-container {
      right: 14px;
      bottom: 14px;
    }

    .chat-window {
      width: min(93vw, 384px);
      height: min(75vh, 576px);
      bottom: 74px;
      border-radius: 24px;
    }

    .chat-toggle-btn {
      width: 56px;
      height: 56px;
      border-radius: 19px;
    }
  }
</style>