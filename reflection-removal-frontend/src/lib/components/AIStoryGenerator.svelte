<script>
  import { onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';

  let {
    predictionId = null,
    aiMode = { selected_mode: 'fidelity' },
    ssim = 0,
    edgeScore = 0,
    aiReason = ''
  } = $props();

  const API_BASE = 'http://localhost:8000';

  let story = $state('');
  let displayedStory = $state('');
  let loading = $state(false);
  let error = $state('');
  let lastRequestKey = $state('');
  let typingTimer = null;
  let autoRequestKey = '';

  async function fetchStory(force = false) {
    if (!predictionId) return;

    const requestKey = `${predictionId}:${aiMode?.selected_mode || 'fidelity'}:${ssim}:${edgeScore}:${aiReason}`;
    if (!force && lastRequestKey === requestKey && story) return;

    lastRequestKey = requestKey;
    loading = true;
    error = '';
    story = '';
    displayedStory = '';
    clearTypingTimer();

    try {
      const response = await fetch(`${API_BASE}/ai/story`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prediction_id: predictionId,
          ai_mode: aiMode?.selected_mode || 'fidelity',
          ssim,
          edge_score: edgeScore,
          ai_reason: aiReason
        })
      });

      if (!response.ok) throw new Error('Unable to generate story');

      const data = await response.json();
      story = data.story || '';
      typeStory(story);
    } catch (err) {
      error = err.message || 'Unable to generate story';
    } finally {
      loading = false;
    }
  }

  function clearTypingTimer() {
    if (typingTimer) {
      clearInterval(typingTimer);
      typingTimer = null;
    }
  }

  function typeStory(text) {
    clearTypingTimer();
    displayedStory = '';
    if (!text) return;
    let index = 0;
    typingTimer = setInterval(() => {
      displayedStory = text.slice(0, index + 1);
      index += 1;
      if (index >= text.length) clearTypingTimer();
    }, 18);
  }

  $effect(() => {
    const requestKey = predictionId
      ? `${predictionId}:${aiMode?.selected_mode || 'fidelity'}:${ssim}:${edgeScore}:${aiReason}`
      : '';

    if (requestKey && autoRequestKey !== requestKey) {
      autoRequestKey = requestKey;
      void fetchStory(true);
    }
  });

  onDestroy(() => { clearTypingTimer(); });
</script>

<div class="sg" in:fade={{ duration: 300 }}>

  <!-- Loading state -->
  {#if loading}
    <div class="sg-loading">
      <span class="sg-pulse" aria-hidden="true"></span>
      <span>Generating scene summary…</span>
    </div>

  <!-- Error state -->
  {:else if error}
    <div class="sg-error">
      <svg class="sg-error-icon" width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
        <circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.4"/>
        <path d="M7 4.5v3M7 9.5v.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
      </svg>
      {error}
    </div>

  <!-- Story text -->
  {:else}
    <p class="sg-text">{displayedStory || story}</p>
  {/if}

  <!-- Footer action -->
  <div class="sg-footer">
    <button
      class="sg-regen"
      onclick={() => fetchStory(true)}
      disabled={loading || !predictionId}
      aria-label="Regenerate AI summary"
    >
      <!-- Rotate icon -->
      <svg width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true">
        <path d="M2 7a5 5 0 005 5V10l3 3-3 3v-2a7 7 0 11.5-14" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Regenerate
    </button>
  </div>

</div>

<style>
  /* ── Root ── */
  .sg {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  /* ── Loading ── */
  .sg-loading {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.5);
    min-height: 3.5rem;
    padding: 0.25rem 0;
  }

  /* Pulsing dot */
  .sg-pulse {
    flex-shrink: 0;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22d3ee;
    box-shadow: 0 0 10px rgba(34, 211, 238, 0.6);
    animation: sg-pulse 1.4s ease-in-out infinite;
  }

  @keyframes sg-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.65); }
  }

  /* ── Error ── */
  .sg-error {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #fca5a5;
    line-height: 1.55;
    min-height: 3.5rem;
    padding: 0.25rem 0;
  }

  .sg-error-icon {
    flex-shrink: 0;
    margin-top: 1px;
    color: #f87171;
  }

  /* ── Story text ── */
  .sg-text {
    margin: 0;
    font-size: 0.82rem;
    line-height: 1.7;
    color: rgba(255, 255, 255, 0.72);
    /* clamp at 3 lines to keep panel compact */
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
    min-height: 3.5rem;
  }

  /* ── Footer ── */
  .sg-footer {
    display: flex;
    justify-content: flex-end;
    padding-top: 0.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }

  /* ── Regenerate button ── */
  .sg-regen {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.5rem 0.9rem;
    border-radius: 9px;
    border: 1px solid rgba(115, 103, 240, 0.22);
    background: rgba(255, 255, 255, 0.025);
    color: rgba(255, 255, 255, 0.65);
    font-size: 0.74rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition:
      color 0.22s ease,
      border-color 0.22s ease,
      background 0.22s ease,
      transform 0.22s ease;
  }

  .sg-regen:hover:not(:disabled) {
    color: rgba(255, 255, 255, 0.92);
    border-color: rgba(0, 210, 255, 0.35);
    background: rgba(115, 103, 240, 0.08);
    transform: translateY(-1px);
  }

  .sg-regen:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
</style>