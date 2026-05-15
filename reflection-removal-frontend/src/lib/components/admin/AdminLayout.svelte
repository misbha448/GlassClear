<svelte:options runes={false} />

<script>
  export let sidebar;
  export let topbar;
  export let detailOpen = false;
</script>

<div class={`gc-admin-shell ${detailOpen ? 'has-detail' : ''}`}>
  <slot name="sidebar">{sidebar}</slot>
  <div class="gc-admin-main">
    <slot name="topbar">{topbar}</slot>
    <div class="gc-admin-content">
      <slot></slot>
    </div>
  </div>
</div>
