<svelte:options runes={false} />

<script>
  import AdminEmptyState from './AdminEmptyState.svelte';

  export let weeklyProcessing = [];
  export let statusDistribution = { completed: 0, failed: 0, processing: 0, queued: 0 };

  const colors = {
    uploads: '#6d5dfc',
    completed: '#16a34a',
    failed: '#dc2626',
    processing: '#0ea5e9',
    queued: '#f59e0b'
  };

  $: maxValue = Math.max(1, ...weeklyProcessing.map((item) => Math.max(item.uploads || 0, item.completed || 0, item.failed || 0)));
  $: totalStatus = Object.values(statusDistribution || {}).reduce((sum, value) => sum + value, 0);
  $: distributionSegments = Object.entries(statusDistribution || {}).map(([key, value]) => ({
    key,
    value,
    color: colors[key] || '#667085',
    percent: totalStatus ? (value / totalStatus) * 100 : 0
  }));
  $: gradient = distributionSegments.length
    ? distributionSegments.reduce(
        (parts, segment, index) => {
          const start = parts.offset;
          const end = start + segment.percent;
          parts.values.push(`${segment.color} ${start}% ${end}%`);
          parts.offset = end;
          return parts;
        },
        { offset: 0, values: [] }
      ).values.join(', ')
    : '';
</script>

<div class="gc-admin-chart-grid">
  <section class="gc-admin-panel">
    <div class="gc-admin-panel__header">
      <div>
        <span class="gc-admin-eyebrow">Analytics</span>
        <h3>Weekly Processing Activity</h3>
      </div>
    </div>

    {#if !weeklyProcessing.length}
      <AdminEmptyState title="No processing history" message="Uploads, completed jobs, and failed jobs will appear here." />
    {:else}
      <div class="gc-admin-bar-chart">
        {#each weeklyProcessing as item}
          <div class="gc-admin-bar-chart__group">
            <div class="gc-admin-bar-chart__bars">
              <span style={`height:${((item.uploads || 0) / maxValue) * 100}% ; background:${colors.uploads};`}></span>
              <span style={`height:${((item.completed || 0) / maxValue) * 100}% ; background:${colors.completed};`}></span>
              <span style={`height:${((item.failed || 0) / maxValue) * 100}% ; background:${colors.failed};`}></span>
            </div>
            <small>{new Date(item.date).toLocaleDateString('en-IN', { weekday: 'short' })}</small>
          </div>
        {/each}
      </div>
      <div class="gc-admin-chart-legend">
        <span><i style={`background:${colors.uploads};`}></i>Uploads</span>
        <span><i style={`background:${colors.completed};`}></i>Completed</span>
        <span><i style={`background:${colors.failed};`}></i>Failed</span>
      </div>
    {/if}
  </section>

  <section class="gc-admin-panel">
    <div class="gc-admin-panel__header">
      <div>
        <span class="gc-admin-eyebrow">Distribution</span>
        <h3>Processing Status</h3>
      </div>
    </div>

    {#if !totalStatus}
      <AdminEmptyState title="No status data" message="Job status distribution will appear once jobs exist." />
    {:else}
      <div class="gc-admin-donut-wrap">
        <div class="gc-admin-donut" style={`background: conic-gradient(${gradient});`}>
          <div class="gc-admin-donut__inner">
            <strong>{totalStatus}</strong>
            <span>Total jobs</span>
          </div>
        </div>
        <div class="gc-admin-donut__legend">
          {#each distributionSegments as segment}
            <div>
              <span><i style={`background:${segment.color};`}></i>{segment.key}</span>
              <strong>{segment.value}</strong>
            </div>
          {/each}
        </div>
      </div>
    {/if}
  </section>
</div>
