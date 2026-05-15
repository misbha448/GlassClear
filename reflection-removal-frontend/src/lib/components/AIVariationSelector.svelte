<script>
  let {
    variations = [],
    selectedKey = '',
    loading = false,
    error = ''
  } = $props();
</script>

<section class="vs">

  {#if loading}
    <div class="vs-state">
      <span class="vs-spinner" aria-hidden="true"></span>
      <span>Generating alternatives…</span>
    </div>

  {:else if error}
    <div class="vs-state vs-state--error">{error}</div>

  {:else if variations.length}
    <ul class="vs-list" role="list">
      {#each variations as variation}
        <li>
          <button
            class="vs-card"
            class:vs-card--active={variation.key === selectedKey}
            onclick={() => variation.onSelect?.(variation)}
            aria-pressed={variation.key === selectedKey}
          >
            <!-- Thumbnail -->
            <div class="vs-thumb-wrap">
              <img
                src={variation.image_url}
                alt={variation.label}
                loading="lazy"
                class="vs-thumb"
              />
              <!-- Active checkmark -->
              {#if variation.key === selectedKey}
                <div class="vs-check" aria-hidden="true">
                  <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                    <path d="M2 5l2.5 2.5L8 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              {/if}
            </div>

            <!-- Label -->
            <span class="vs-label">{variation.label}</span>
          </button>
        </li>
      {/each}
    </ul>
  {/if}

</section>

<style>
  /* ── Root ── */
  .vs {
    width: 100%;
  }

  /* ── State messages ── */
  .vs-state {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.5);
    padding: 0.5rem 0;
  }

  .vs-state--error {
    color: #fca5a5;
  }

  /* ── Spinner ── */
  .vs-spinner {
    display: inline-block;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    border: 2px solid rgba(255, 255, 255, 0.12);
    border-top-color: rgba(115, 103, 240, 0.8);
    animation: vs-spin 0.75s linear infinite;
    flex-shrink: 0;
  }

  @keyframes vs-spin {
    to { transform: rotate(360deg); }
  }

  /* ── List ── */
  .vs-list {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 4px;
    list-style: none;
    margin: 0;
    padding: 0 0 4px 0;
    /* hide scrollbar on webkit but keep functionality */
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.08) transparent;
  }

  .vs-list::-webkit-scrollbar { height: 3px; }
  .vs-list::-webkit-scrollbar-track { background: transparent; }
  .vs-list::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 99px; }

  /* ── Card ── */
  .vs-card {
    flex-shrink: 0;
    min-width: 120px;
    max-width: 148px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    background: rgba(255, 255, 255, 0.02);
    cursor: pointer;
    transition:
      border-color 0.22s ease,
      background 0.22s ease,
      transform 0.22s ease,
      box-shadow 0.22s ease;
  }

  .vs-card:hover {
    border-color: rgba(255, 255, 255, 0.14);
    background: rgba(255, 255, 255, 0.04);
    transform: translateY(-2px);
  }

  .vs-card--active {
    border-color: rgba(115, 103, 240, 0.6);
    background: rgba(115, 103, 240, 0.06);
    box-shadow:
      0 0 0 1px rgba(115, 103, 240, 0.2),
      0 0 20px rgba(115, 103, 240, 0.1);
    transform: translateY(-2px);
  }

  /* ── Thumbnail wrapper ── */
  .vs-thumb-wrap {
    position: relative;
    width: 100%;
  }

  .vs-thumb {
    width: 100%;
    aspect-ratio: 4 / 3;
    object-fit: cover;
    border-radius: 9px;
    display: block;
  }

  /* ── Active check badge ── */
  .vs-check {
    position: absolute;
    top: 5px;
    right: 5px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7367f0, #00d2ff);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    box-shadow: 0 2px 8px rgba(115, 103, 240, 0.4);
  }

  /* ── Label ── */
  .vs-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.65);
    padding: 0 2px;
    letter-spacing: 0.01em;
    transition: color 0.22s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }

  .vs-card--active .vs-label {
    color: rgba(255, 255, 255, 0.92);
  }
</style>