<svelte:options runes={false} />

<script>
  export let items = [];
</script>

<div class="gc-admin-stats-grid">
  {#each items as item}
    <article class="gc-admin-stat-card">
      <div class={`gc-admin-stat-card__icon gc-admin-stat-card__icon--${item.tone || 'primary'}`}>{item.icon || '•'}</div>
      <div class="gc-admin-stat-card__content">
        <span>{item.label}</span>
        <strong>{item.value}</strong>
        <small>{item.helper}</small>
      </div>
    </article>
  {/each}
</div>
