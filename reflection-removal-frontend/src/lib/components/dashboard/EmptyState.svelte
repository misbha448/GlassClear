<svelte:options runes={false} />

<script>
  export let title = '';
  export let message = '';
  export let actionLabel = '';
  export let onAction = null;
</script>

<div class="gc-empty-state">
  <div class="gc-empty-state__icon" aria-hidden="true">
    <svg viewBox="0 0 24 24" fill="none">
      <path d="M4 7.5A2.5 2.5 0 0 1 6.5 5h11A2.5 2.5 0 0 1 20 7.5v9A2.5 2.5 0 0 1 17.5 19h-11A2.5 2.5 0 0 1 4 16.5v-9Z" stroke="currentColor" stroke-width="1.6" />
      <path d="m7.5 15 2.4-2.4a1.5 1.5 0 0 1 2.12 0L14 14.58l1.4-1.4a1.5 1.5 0 0 1 2.12 0L19 14.66" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
      <circle cx="9" cy="9" r="1.3" fill="currentColor" />
    </svg>
  </div>
  <h3>{title}</h3>
  <p>{message}</p>
  {#if actionLabel && onAction}
    <button type="button" class="gc-button gc-button--primary" onclick={onAction}>{actionLabel}</button>
  {/if}
</div>
