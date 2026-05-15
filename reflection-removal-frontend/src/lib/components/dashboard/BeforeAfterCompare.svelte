<svelte:options runes={false} />

<script>
  import { t } from '$lib/state.svelte.js';

  export let beforeImage = '';
  export let afterImage = '';
  export let filterStyle = '';
  export let zoom = 1;

  let slider = 50;
</script>

<div class="gc-compare">
  <div class="gc-compare__stage" style={`transform: scale(${zoom});`}>
    <img class="gc-compare__image" src={afterImage || beforeImage} alt={t('common.output')} style={`filter: ${filterStyle};`} />
    <div class="gc-compare__overlay" style={`width: ${slider}%;`}>
      <img class="gc-compare__image" src={beforeImage} alt={t('common.original')} style={`filter: ${filterStyle};`} />
    </div>
    <div class="gc-compare__divider" style={`left: ${slider}%;`}>
      <span></span>
    </div>
  </div>

  <div class="gc-compare__controls">
    <span>{t('common.original')}</span>
    <input type="range" min="0" max="100" bind:value={slider} aria-label={t('common.compare')} />
    <span>{t('common.output')}</span>
  </div>
</div>
