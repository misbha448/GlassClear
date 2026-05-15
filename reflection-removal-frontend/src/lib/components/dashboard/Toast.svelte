<svelte:options runes={false} />

<script>
  export let toast = { type: 'info', message: '' };
  export let onDismiss = () => {};
</script>

<div class={`gc-toast gc-toast--${toast.type || 'info'}`} role="status" aria-live="polite">
  <span>{toast.message}</span>
  <button type="button" class="gc-toast__close" onclick={onDismiss} aria-label="Dismiss notification">x</button>
</div>
