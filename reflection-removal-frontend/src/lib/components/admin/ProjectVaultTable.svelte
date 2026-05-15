<svelte:options runes={false} />

<script>
  import StatusBadge from './StatusBadge.svelte';
  import AdminEmptyState from './AdminEmptyState.svelte';

  export let rows = [];
  export let onView = () => {};
  export let onArchive = () => {};
</script>

<section class="gc-admin-panel">
  <div class="gc-admin-panel__header">
    <div>
      <span class="gc-admin-section-kicker">Project Control</span>
      <h2>Project Vault</h2>
    </div>
  </div>

  {#if rows.length}
    <div class="gc-admin-table-wrap">
      <table class="gc-admin-table">
        <thead>
          <tr>
            <th>Project Name</th>
            <th>Owner</th>
            <th>Images</th>
            <th>Shared</th>
            <th>Last Updated</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each rows as row}
            <tr>
              <td data-label="Project Name"><strong>{row.name}</strong></td>
              <td data-label="Owner">{row.owner}</td>
              <td data-label="Images">{row.images}</td>
              <td data-label="Shared"><StatusBadge status={row.shared ? 'yes' : 'no'} compact={true} /></td>
              <td data-label="Last Updated">{row.lastUpdated}</td>
              <td data-label="Status"><StatusBadge status={row.status} /></td>
              <td data-label="Actions">
                <div class="gc-admin-action-row">
                  <button type="button" class="gc-admin-text-button" on:click={() => onView(row)}>View</button>
                  <button type="button" class="gc-admin-text-button" on:click={() => onArchive(row)}>Archive</button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {:else}
    <AdminEmptyState title="No project records" description="Project-level activity will appear here as teams create vaults." />
  {/if}
</section>
