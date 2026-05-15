<svelte:options runes={false} />

<script>
  import RestorationTimeline from './RestorationTimeline.svelte';

  export let detectionMetrics = [];
  export let reflectionPath = [];
  export let reflectionExplanation = '';
  export let timelineSteps = [];
  export let activeStep = 0;
  export let onReplay = async () => {};
</script>

<section class="gc-zone">
  <div class="gc-zone__heading">
    <span class="gc-section-kicker">AI Reflection Intelligence</span>
    <h2>GlassClear explains what it detected, why it happened, and how it restored the image.</h2>
  </div>

  <div class="gc-zone__grid gc-zone__grid--intelligence">
    <section class="gc-panel gc-glass-card">
      <div class="gc-panel__header">
        <div>
          <h3>What AI Detected</h3>
          <p>Detection confidence across architectural reflection categories.</p>
        </div>
      </div>

      <div class="gc-detection-list">
        {#each detectionMetrics as metric}
          <div class="gc-detection-row">
            <div class="gc-detection-row__meta">
              <span>{metric.label}</span>
              <strong>{metric.value}%</strong>
            </div>
            <div class="gc-progress">
              <span
                class={`gc-progress__fill gc-progress__fill--${metric.tone}`}
                style={`width:${metric.value}%;`}
              ></span>
            </div>
          </div>
        {/each}
      </div>
    </section>

    <section class="gc-panel gc-glass-card">
      <div class="gc-panel__header">
        <div>
          <h3>Why It Happened</h3>
          <p>Reflection source path across the capture environment.</p>
        </div>
      </div>

      <div class="gc-node-path">
        {#each reflectionPath as node, index}
          <div class="gc-node-path__item">
            <span>{node}</span>
            {#if index < reflectionPath.length - 1}
              <em>&rarr;</em>
            {/if}
          </div>
        {/each}
      </div>

      <p class="gc-explanation-copy">{reflectionExplanation}</p>
    </section>

    <RestorationTimeline steps={timelineSteps} activeStep={activeStep} onReplay={onReplay} />
  </div>
</section>
