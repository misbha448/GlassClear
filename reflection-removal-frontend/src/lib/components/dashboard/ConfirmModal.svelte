<svelte:options runes={false} />

<script>
  export let title = 'Confirm';
  export let message = '';
  export let confirmLabel = 'Confirm';
  export let cancelLabel = 'Cancel';
  export let tone = 'default';
  export let onConfirm = () => {};
  export let onCancel = () => {};
</script>

<div class="gc-confirm-backdrop" role="presentation" onclick={onCancel}>
  <div class="gc-confirm-modal" role="dialog" aria-modal="true" tabindex="-1" onclick={(event) => event.stopPropagation()} onkeydown={() => {}}>
    <div class="gc-confirm-modal__header">
      <h3>{title}</h3>
      <p>{message}</p>
    </div>

    <div class="gc-confirm-modal__actions">
      <button type="button" class="gc-button gc-button--ghost" onclick={onCancel}>{cancelLabel}</button>
      <button type="button" class:gc-button--danger={tone === 'danger'} class="gc-button gc-button--primary" onclick={onConfirm}>
        {confirmLabel}
      </button>
    </div>
  </div>
</div>
