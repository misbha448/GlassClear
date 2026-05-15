<svelte:options runes={false} />

<script>
  import BeforeAfterCompare from './BeforeAfterCompare.svelte';
  import AIScanConsole from './AIScanConsole.svelte';

  export let hero = {};
  export let processingMessages = [];
  export let selectedPoints = [];
</script>

<section class="gc-hero">
  <div class="gc-hero__intro">
    <span class="gc-section-kicker">GlassClear Command Center</span>
    <h1>{hero.title}</h1>
    <p>{hero.subtitle}</p>

    <div class="gc-hero__stats">
      <div class="gc-hero__stat gc-glass-card">
        <span>Detected Regions</span>
        <strong>{hero.detectedRegions || 0}</strong>
      </div>
      <div class="gc-hero__stat gc-glass-card">
        <span>Restore Time</span>
        <strong>{hero.restorationTime || '--'}</strong>
      </div>
    </div>
  </div>

  <div class="gc-hero__grid">
    <BeforeAfterCompare
      beforeImage={hero.beforeImage}
      afterImage={hero.afterImage}
      points={selectedPoints}
      scannerPoints={hero.scannerPoints || []}
    />

    <AIScanConsole
      severity={hero.severity}
      confidence={hero.confidence}
      processingMessages={processingMessages}
    />
  </div>
</section>
