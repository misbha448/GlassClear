<svelte:options runes={false} />

<script>
  export let open = false;
  export let title = 'Confirm action';
  export let message = 'Are you sure?';
  export let confirmLabel = 'Confirm';
  export let tone = 'danger';
  export let busy = false;
  export let onConfirm = () => {};
  export let onClose = () => {};
</script>

{#if open}
  <div class="gc-admin-modal-backdrop" role="presentation" on:click={onClose}>
    <div
      class="gc-admin-modal"
      role="dialog"
      aria-modal="true"
      aria-label={title}
      tabindex="-1"
      on:click|stopPropagation
      on:keydown|stopPropagation
    >
      <div class="gc-admin-modal__header">
        <div>
          <span class="gc-admin-eyebrow">Action</span>
          <h3>{title}</h3>
        </div>
        <button type="button" class="gc-admin-icon-button" on:click={onClose} aria-label="Close dialog">x</button>
      </div>
      <p class="gc-admin-modal__message">{message}</p>
      <div class="gc-admin-modal__actions">
        <button type="button" class="gc-admin-button gc-admin-button--ghost" on:click={onClose} disabled={busy}>Cancel</button>
        <button
          type="button"
          class={`gc-admin-button ${tone === 'danger' ? 'gc-admin-button--danger' : 'gc-admin-button--primary'}`}
          on:click={onConfirm}
          disabled={busy}
        >
          {busy ? 'Working...' : confirmLabel}
        </button>
      </div>
    </div>
  </div>
{/if}
