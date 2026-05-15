<svelte:options runes={false} />

<script>
  import AdminStatusBadge from './AdminStatusBadge.svelte';

  export let cards = [];
  export let loading = false;
</script>

<section class="gc-admin-panel">
  <div class="gc-admin-panel__header">
    <div>
      <span class="gc-admin-eyebrow">System</span>
      <h3>System Health</h3>
    </div>
  </div>

  {#if loading}
    <div class="gc-admin-health-grid">
      {#each Array(6) as _}
        <div class="gc-admin-health-card gc-admin-skeleton-block"></div>
      {/each}
    </div>
  {:else}
    <div class="gc-admin-health-grid">
      {#each cards as card}
        <article class="gc-admin-health-card">
          <span>{card.label}</span>
          {#if card.status}
            <AdminStatusBadge status={card.status} />
          {:else}
            <strong>{card.value}</strong>
          {/if}
          {#if card.value && card.status}
            <small>{card.value}</small>
          {/if}
        </article>
      {/each}
    </div>
  {/if}
</section>
