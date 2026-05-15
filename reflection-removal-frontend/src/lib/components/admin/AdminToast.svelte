<svelte:options runes={false} />

<script>
  export let toast = null;
  export let onClose = () => {};
</script>

{#if toast}
  <div class={`gc-admin-toast gc-admin-toast--${toast.type || 'info'}`} role="status" aria-live="polite">
    <div>
      <strong>{toast.title || 'Notice'}</strong>
      <p>{toast.message}</p>
    </div>
    <button type="button" class="gc-admin-icon-button" on:click={onClose} aria-label="Close notification">x</button>
  </div>
{/if}
