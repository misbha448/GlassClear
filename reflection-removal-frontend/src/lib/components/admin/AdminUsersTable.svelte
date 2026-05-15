<svelte:options runes={false} />

<script>
  import AdminEmptyState from './AdminEmptyState.svelte';
  import AdminStatusBadge from './AdminStatusBadge.svelte';

  export let items = [];
  export let loading = false;
  export let onView = () => {};
  export let onToggle = () => {};
  export let onDelete = () => {};
</script>

<section class="gc-admin-panel">
  <div class="gc-admin-panel__header">
    <div>
      <span class="gc-admin-eyebrow">Users</span>
      <h3>Recent Users</h3>
    </div>
  </div>

  {#if loading}
    <div class="gc-admin-table-skeleton"></div>
  {:else if !items.length}
    <AdminEmptyState title="No users found" message="Try a different search or status filter." />
  {:else}
    <div class="gc-admin-table-wrap">
      <table class="gc-admin-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Email</th>
            <th>Joined</th>
            <th>Uploads</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each items as item}
            <tr>
              <td data-label="User">{item.name}</td>
              <td data-label="Email">{item.email}</td>
              <td data-label="Joined">{item.joinedAt}</td>
              <td data-label="Uploads">{item.totalUploads}</td>
              <td data-label="Status"><AdminStatusBadge status={item.status} /></td>
              <td data-label="Actions">
                <div class="gc-admin-row-actions">
                  <button type="button" class="gc-admin-text-button" on:click={() => onView(item)}>View</button>
                  <button type="button" class="gc-admin-text-button" on:click={() => onToggle(item)}>{item.status === 'active' ? 'Disable' : 'Enable'}</button>
                  <button type="button" class="gc-admin-text-button danger" on:click={() => onDelete(item)}>Delete</button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</section>
