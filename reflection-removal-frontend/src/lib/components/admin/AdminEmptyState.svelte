<svelte:options runes={false} />

<script>
  export let title = 'Nothing to show yet';
  export let message = 'Real admin data will appear here when records are available.';
</script>

<div class="gc-admin-empty-state">
  <div class="gc-admin-empty-state__icon" aria-hidden="true"></div>
  <h3>{title}</h3>
  <p>{message}</p>
</div>
