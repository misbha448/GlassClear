<svelte:options runes={false} />

<script>
  import StatusBadge from './StatusBadge.svelte';
  import AdminEmptyState from './AdminEmptyState.svelte';

  export let rows = [];
  export let onView = () => {};
  export let onToggleBlock = () => {};
  export let onDelete = () => {};
</script>

<section class="gc-admin-panel">
  <div class="gc-admin-panel__header">
    <div>
      <span class="gc-admin-section-kicker">User Operations</span>
      <h2>Users & Activity</h2>
    </div>
  </div>

  {#if rows.length}
    <div class="gc-admin-table-wrap">
      <table class="gc-admin-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Email</th>
            <th>Uploads</th>
            <th>Projects</th>
            <th>Last Active</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each rows as row}
            <tr>
              <td data-label="User"><strong>{row.name}</strong></td>
              <td data-label="Email">{row.email}</td>
              <td data-label="Uploads">{row.uploads}</td>
              <td data-label="Projects">{row.projects}</td>
              <td data-label="Last Active">{row.lastActive}</td>
              <td data-label="Status"><StatusBadge status={row.status} /></td>
              <td data-label="Actions">
                <div class="gc-admin-action-row">
                  <button type="button" class="gc-admin-text-button" on:click={() => onView(row)}>View</button>
                  <button type="button" class="gc-admin-text-button" on:click={() => onToggleBlock(row)}>
                    {row.status === 'blocked' ? 'Unblock' : 'Block'}
                  </button>
                  <button type="button" class="gc-admin-text-button danger" on:click={() => onDelete(row)}>Delete</button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {:else}
    <AdminEmptyState title="No users found" description="Try a broader search to inspect account activity." />
  {/if}
</section>
