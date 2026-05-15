<svelte:options runes={false} />

<script>
  import StatusBadge from './StatusBadge.svelte';
  import AdminEmptyState from './AdminEmptyState.svelte';

  export let rows = [];
  export let filter = 'all';
  export let onFilter = () => {};
  export let onView = () => {};
  export let onRetry = () => {};
  export let onDelete = () => {};

  const filters = ['all', 'completed', 'processing', 'failed', 'queued'];
</script>

<section class="gc-admin-panel">
  <div class="gc-admin-panel__header">
    <div>
      <span class="gc-admin-section-kicker">Processing Monitor</span>
      <h2>Recent Reflection Processing</h2>
      <p>Monitor recent image restoration activity and failed recovery attempts.</p>
    </div>
    <div class="gc-admin-chip-row">
      {#each filters as item}
        <button
          type="button"
          class={`gc-admin-chip ${filter === item ? 'is-active' : ''}`}
          on:click={() => onFilter(item)}
        >
          {item}
        </button>
      {/each}
    </div>
  </div>

  {#if rows.length}
    <div class="gc-admin-table-wrap">
      <table class="gc-admin-table">
        <thead>
          <tr>
            <th>Image Preview</th>
            <th>User</th>
            <th>Reflection Type</th>
            <th>Status</th>
            <th>Confidence</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each rows as row}
            <tr>
              <td data-label="Image Preview">
                <div class="gc-admin-processing-preview">
                  <img src={row.preview} alt={row.project} />
                </div>
              </td>
              <td data-label="User">
                <div class="gc-admin-user-cell">
                  <strong>{row.userName}</strong>
                  <span>{row.userEmail}</span>
                </div>
              </td>
              <td data-label="Reflection Type">{row.reflectionType}</td>
              <td data-label="Status"><StatusBadge status={row.status} /></td>
              <td data-label="Confidence">{row.confidence ? `${row.confidence}%` : '--'}</td>
              <td data-label="Created At">{row.createdAt}</td>
              <td data-label="Actions">
                <div class="gc-admin-action-row">
                  <button type="button" class="gc-admin-text-button" on:click={() => onView(row)}>View</button>
                  {#if row.status === 'failed'}
                    <button type="button" class="gc-admin-text-button" on:click={() => onRetry(row)}>Retry</button>
                  {/if}
                  <button type="button" class="gc-admin-text-button danger" on:click={() => onDelete(row)}>Delete</button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {:else}
    <AdminEmptyState
      title="No processing records match this view"
      description="Try another filter or search term to inspect recent restoration activity."
    />
  {/if}
</section>
