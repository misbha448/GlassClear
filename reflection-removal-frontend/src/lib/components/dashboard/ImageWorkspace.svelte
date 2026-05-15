<svelte:options runes={false} />

<script>
  import BeforeAfterCompare from './BeforeAfterCompare.svelte';
  import { t } from '$lib/state.svelte.js';

  export let originalImage = '';
  export let processedImage = '';
  export let currentFilename = 'input.jpg';
  export let viewMode = 'compare';
  export let zoom = 1;
  export let filterStyle = '';
  export let isLoading = false;
  export let emptyOutputMessage = 'Run reflection removal to generate output.';
  export let onSelectView = () => {};
  export let onZoomOut = () => {};
  export let onZoomIn = () => {};
  export let onFit = () => {};
</script>

<section class="gc-workspace">
  <div class="gc-workspace__header">
    <div class="gc-workspace__tabs">
      <button type="button" class:gc-tab--active={viewMode === 'original'} class="gc-tab" onclick={() => onSelectView('original')}>{t('common.original')}</button>
      <button type="button" class:gc-tab--active={viewMode === 'output'} class="gc-tab" onclick={() => onSelectView('output')}>{t('common.output')}</button>
      <button type="button" class:gc-tab--active={viewMode === 'compare'} class="gc-tab" onclick={() => onSelectView('compare')}>{t('common.compare')}</button>
    </div>

    <div class="gc-workspace__controls">
      <button type="button" class="gc-icon-button" onclick={onZoomOut}>{t('dashboardUi.zoomOut')}</button>
      <button type="button" class="gc-icon-button" onclick={onZoomIn}>{t('dashboardUi.zoomIn')}</button>
      <button type="button" class="gc-icon-button" onclick={onFit}>{t('dashboardUi.fit')}</button>
    </div>
  </div>

  <div class="gc-workspace__canvas">
    {#if isLoading}
      <div class="gc-workspace__empty">
        <strong>{t('dashboardUi.loadingWorkspace')}</strong>
        <p>{t('dashboardUi.preparingWorkspace')}</p>
      </div>
    {:else if viewMode === 'compare' && processedImage}
      <BeforeAfterCompare beforeImage={originalImage} afterImage={processedImage} {filterStyle} {zoom} />
    {:else if viewMode === 'output' && processedImage}
      <img
        class="gc-workspace__image"
        src={processedImage}
        alt={`${t('dashboardUi.processedPreview')} ${currentFilename}`}
        style={`transform: scale(${zoom}); filter: ${filterStyle};`}
      />
    {:else if viewMode === 'output'}
      <div class="gc-workspace__empty">
        <strong>{t('dashboardUi.noOutput')}</strong>
        <p>{emptyOutputMessage}</p>
      </div>
    {:else if originalImage}
      <img
        class="gc-workspace__image"
        src={originalImage}
        alt={`${t('dashboardUi.originalPreview')} ${currentFilename}`}
        style={`transform: scale(${zoom}); filter: ${filterStyle};`}
      />
    {:else}
      <div class="gc-workspace__empty">
        <strong>{t('dashboardUi.noImage')}</strong>
        <p>{t('dashboardUi.openImage')}</p>
      </div>
    {/if}
  </div>
</section>
