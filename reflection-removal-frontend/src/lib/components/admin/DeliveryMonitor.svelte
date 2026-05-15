<svelte:options runes={false} />

<script>
  import StatusBadge from './StatusBadge.svelte';
  import AdminEmptyState from './AdminEmptyState.svelte';

  export let rows = [];
  export let onView = () => {};
  export let onDelete = () => {};
</script>

<section class="gc-admin-panel">
  <div class="gc-admin-panel__header">
    <div>
      <span class="gc-admin-section-kicker">Delivery Center</span>
      <h2>Delivery Monitor</h2>
      <p>Track share links, collages, and export outputs moving out of user workspaces.</p>
    </div>
  </div>

  {#if rows.length}
    <div class="gc-admin-delivery-list">
      {#each rows as row}
        <article class="gc-admin-delivery-card">
          <div>
            <span class="gc-admin-delivery-card__type">{row.type}</span>
            <h3>{row.related}</h3>
            <p>{row.owner} • {row.createdAt}</p>
          </div>
          <div class="gc-admin-delivery-card__meta">
            <StatusBadge status={row.status} />
            <div class="gc-admin-action-row">
              <button type="button" class="gc-admin-text-button" on:click={() => onView(row)}>View</button>
              {#if row.rawType !== 'export'}
                <button type="button" class="gc-admin-text-button danger" on:click={() => onDelete(row)}>Delete</button>
              {/if}
            </div>
          </div>
        </article>
      {/each}
    </div>
  {:else}
    <AdminEmptyState title="No delivery items" description="Share links, collages, and exports will land here once generated." />
  {/if}
</section>
