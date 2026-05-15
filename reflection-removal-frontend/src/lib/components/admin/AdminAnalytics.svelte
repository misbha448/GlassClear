<svelte:options runes={false} />

<script>
  export let analytics = {
    uploadTrend: [],
    recovery: { success: 0, failed: 0 }
  };

  $: maxUploads = Math.max(...analytics.uploadTrend.map((item) => item.value), 1);
  $: success = analytics.recovery.success ?? 0;
  $: failed = analytics.recovery.failed ?? 0;
  $: donutStyle = `background: conic-gradient(var(--gc-admin-accent) 0 ${success}%, rgba(139, 154, 183, 0.18) ${success}% 100%);`;
</script>

<section class="gc-admin-analytics-grid">
  <article class="gc-admin-panel">
    <div class="gc-admin-panel__header">
      <div>
        <span class="gc-admin-section-kicker">Upload Trend</span>
        <h2>7-Day Upload Activity</h2>
      </div>
    </div>
    <div class="gc-admin-bar-chart">
      {#each analytics.uploadTrend as item}
        <div class="gc-admin-bar-chart__item">
          <div class="gc-admin-bar-chart__bar-wrap">
            <div class="gc-admin-bar-chart__bar" style={`height:${(item.value / maxUploads) * 100}%`}></div>
          </div>
          <strong>{item.value}</strong>
          <span>{item.day}</span>
        </div>
      {/each}
    </div>
  </article>

  <article class="gc-admin-panel">
    <div class="gc-admin-panel__header">
      <div>
        <span class="gc-admin-section-kicker">Recovery Quality</span>
        <h2>Success vs Failed Recovery</h2>
      </div>
    </div>
    <div class="gc-admin-donut">
      <div class="gc-admin-donut__chart" style={donutStyle}>
        <div class="gc-admin-donut__inner">
          <strong>{success}%</strong>
          <span>success</span>
        </div>
      </div>
      <div class="gc-admin-donut__legend">
        <div><span class="swatch ok"></span>Successful recoveries</div>
        <div><span class="swatch muted"></span>Failed recoveries</div>
        <small>{failed}% of attempts required intervention.</small>
      </div>
    </div>
  </article>
</section>
