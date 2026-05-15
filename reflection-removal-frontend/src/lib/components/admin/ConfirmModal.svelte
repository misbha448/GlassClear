<svelte:options runes={false} />

<script>
  export let open = false;
  export let title = 'Confirm action';
  export let message = 'Are you sure you want to continue?';
  export let confirmLabel = 'Confirm';
  export let tone = 'danger';
  export let onConfirm = () => {};
  export let onClose = () => {};
</script>

{#if open}
  <div class="gc-admin-modal-backdrop" role="presentation" on:click={onClose}>
    <div class="gc-admin-modal" role="dialog" aria-modal="true" aria-label={title} tabindex="-1">
      <div class="gc-admin-modal__header">
        <div>
          <span class="gc-admin-section-kicker">Action Check</span>
          <h3>{title}</h3>
        </div>
        <button type="button" class="gc-admin-icon-button" aria-label="Close confirmation" on:click={onClose}>x</button>
      </div>
      <p class="gc-admin-modal__message">{message}</p>
      <div class="gc-admin-modal__actions">
        <button type="button" class="gc-admin-button gc-admin-button--ghost" on:click={onClose}>Cancel</button>
        <button
          type="button"
          class={`gc-admin-button ${tone === 'danger' ? 'gc-admin-button--danger' : 'gc-admin-button--primary'}`}
          on:click={onConfirm}
        >
          {confirmLabel}
        </button>
      </div>
    </div>
  </div>
{/if}
