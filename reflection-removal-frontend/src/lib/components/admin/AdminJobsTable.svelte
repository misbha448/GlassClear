<svelte:options runes={false} />

<script>
  import AdminEmptyState from './AdminEmptyState.svelte';
  import AdminStatusBadge from './AdminStatusBadge.svelte';

  export let items = [];
  export let loading = false;
  export let onView = () => {};
  export let onDelete = () => {};

  let imageErrors = {};

  function getImageSource(item) {
    return item.thumbnailUrl || item.originalUrl || item.processedUrl || item.imageUrl || item.fileUrl || null;
  }

  function hasImage(item) {
    return Boolean(getImageSource(item)) && !imageErrors[item.id];
  }

  function markImageError(itemId) {
    imageErrors = { ...imageErrors, [itemId]: true };
  }
</script>

<section class="gc-admin-panel">
  <div class="gc-admin-panel__header">
    <div>
      <span class="gc-admin-eyebrow">Jobs</span>
      <h3>Recent Processing Jobs</h3>
    </div>
  </div>

  {#if loading}
    <div class="gc-admin-table-skeleton"></div>
  {:else if !items.length}
    <AdminEmptyState title="No jobs found" message="Processed images will appear here once jobs are created." />
  {:else}
    <div class="gc-admin-table-wrap">
      <table class="gc-admin-table">
        <thead>
          <tr>
            <th>Image</th>
            <th>Filename</th>
            <th>User</th>
            <th>Status</th>
            <th>Processing Time</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each items as item}
            <tr>
              <td data-label="Image">
                {#if hasImage(item)}
                  <img class="gc-admin-thumb" src={getImageSource(item)} alt={item.filename} on:error={() => markImageError(item.id)} />
                {:else}
                  <div class="gc-admin-thumb gc-admin-thumb--placeholder" aria-label={`No thumbnail available for ${item.filename}`}>
                    <span>{item.filename?.slice(0, 1)?.toUpperCase() || '?'}</span>
                  </div>
                {/if}
              </td>
              <td data-label="Filename">{item.filename}</td>
              <td data-label="User">{item.userName}</td>
              <td data-label="Status"><AdminStatusBadge status={item.status} /></td>
              <td data-label="Processing Time">{item.processingTimeLabel}</td>
              <td data-label="Date">{item.createdAt}</td>
              <td data-label="Actions">
                <div class="gc-admin-row-actions">
                  <button type="button" class="gc-admin-text-button" on:click={() => onView(item)}>View</button>
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
