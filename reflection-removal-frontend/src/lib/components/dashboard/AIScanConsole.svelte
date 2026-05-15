<svelte:options runes={false} />

<script>
  import { onDestroy, onMount } from 'svelte';

  export let severity = { label: 'Reflection Severity', level: 'HIGH', percent: 82 };
  export let confidence = 96.4;
  export let processingMessages = [];

  let activeMessageIndex = 0;
  let interval;

  onMount(() => {
    if (processingMessages.length < 2) return;

    interval = setInterval(() => {
      activeMessageIndex = (activeMessageIndex + 1) % processingMessages.length;
    }, 2000);
  });

  onDestroy(() => {
    clearInterval(interval);
  });
</script>

<section class="gc-ai-console gc-panel gc-glass-card">
  <div class="gc-ai-console__header">
    <span class="gc-section-kicker">Live Intelligence</span>
    <div class="gc-ai-console__pulse">
      <span></span>
      Neural scan active
    </div>
  </div>

  <div class="gc-console-grid">
    <div class="gc-meter" style={`--value:${severity.percent};`}>
      <div class="gc-meter__inner">
        <span>{severity.label}</span>
        <strong>{severity.level}</strong>
        <em>{severity.percent}%</em>
      </div>
    </div>

    <div class="gc-orb gc-glass-card">
      <span>AI Confidence</span>
      <strong>{confidence}%</strong>
    </div>
  </div>

  <div class="gc-console-status gc-glass-card">
    <span class="gc-section-kicker">Processing Status</span>
    <p>{processingMessages[activeMessageIndex] || 'Scanning reflective regions...'}</p>
    <div class="gc-console-status__bars">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
</section>
