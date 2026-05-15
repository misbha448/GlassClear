<svelte:options runes={false} />

<script>
  export let stats = [];
</script>

<section class="gc-admin-overview-grid">
  {#each stats as stat}
    <article class={`gc-admin-stat-card gc-admin-stat-card--${stat.tone}`}>
      <div class={`gc-admin-stat-card__icon gc-admin-sidebar__icon gc-admin-sidebar__icon--${stat.icon}`}></div>
      <div class="gc-admin-stat-card__content">
        <span>{stat.title}</span>
        <strong>{stat.value}</strong>
        <small>{stat.trend}</small>
      </div>
    </article>
  {/each}
</section>
