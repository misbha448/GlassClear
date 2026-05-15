<svelte:options runes={false} />

<script>
  export let status = 'active';
  export let compact = false;

  const toneMap = {
    active: 'ok',
    completed: 'ok',
    ready: 'ok',
    generated: 'ok',
    live: 'ok',
    yes: 'ok',
    processing: 'info',
    queued: 'muted',
    archived: 'muted',
    expired: 'muted',
    no: 'muted',
    blocked: 'warn',
    failed: 'danger'
  };

  $: tone = toneMap[status] || 'muted';
  $: label = String(status).replace(/_/g, ' ');
</script>

<span class={`gc-admin-badge gc-admin-badge--${tone} ${compact ? 'gc-admin-badge--compact' : ''}`}>
  <span class="gc-admin-badge__dot"></span>
  {label}
</span>
