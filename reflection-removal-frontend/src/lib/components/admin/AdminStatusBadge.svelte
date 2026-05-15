<svelte:options runes={false} />

<script>
  export let status = 'active';

  const toneMap = {
    active: 'success',
    completed: 'success',
    online: 'success',
    connected: 'success',
    loaded: 'success',
    available: 'info',
    processing: 'info',
    queued: 'warning',
    warning: 'warning',
    disabled: 'danger',
    failed: 'danger',
    error: 'danger',
    expired: 'danger'
  };

  $: normalized = String(status || 'unknown').toLowerCase();
  $: tone = toneMap[normalized] || 'info';
  $: label = normalized.replace(/_/g, ' ');
</script>

<span class={`gc-admin-status gc-admin-status--${tone}`}>
  <span class="gc-admin-status__dot"></span>
  {label}
</span>
