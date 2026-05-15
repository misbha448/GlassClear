<svelte:options runes={false} />

<script>
  import EmptyCanvasState from './EmptyCanvasState.svelte';
  import BeforeAfterSlider from './BeforeAfterSlider.svelte';

  export let hasPendingGuestImage = false;
  export let hasWorkspaceImage = false;
  export let originalImage = '';
  export let processedImage = '';
  export let sampleImage = '';
  export let selectedPoints = [];
  export let selectiveCleanupMode = false;
  export let viewMode = 'original';
  export let zoom = 1;
  export let previewFilter = '';
  export let currentFileName = '';
  export let applying = false;
  export let saveProjectDisabled = false;
  export let saveProjectHint = '';
  export let onSelectViewMode = () => {};
  export let onZoomIn = () => {};
  export let onZoomOut = () => {};
  export let onFitToScreen = () => {};
  export let onContinueEditing = () => {};
  export let onSaveProject = () => {};
  export let onTrySample = () => {};
  export let onUploadImage = () => {};
  export let onAddPoint = () => {};

  function handleCanvasClick(event) {
    if (!selectiveCleanupMode || viewMode === 'compare') return;
    const rect = event.currentTarget.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    onAddPoint({ x: Number(x.toFixed(2)), y: Number(y.toFixed(2)) });
  }
</script>

<section class="gc-canvas-panel">
  {#if hasPendingGuestImage}
    <div class="gc-continue-banner">
      <div>
        <strong>Continue your last restoration</strong>
        <p>Bring your guest result into the full GlassClear editing workspace.</p>
      </div>

      <div class="gc-continue-banner__actions">
        <button type="button" on:click={onContinueEditing}>Continue Editing</button>
        <button type="button" on:click={onSaveProject} disabled={saveProjectDisabled}>
          Save to Project
        </button>
      </div>
    </div>
  {/if}

  <div class="gc-canvas-toolbar">
    <div class="gc-canvas-toolbar__left">
      <strong title={currentFileName}>{currentFileName}</strong>
      <span>{selectiveCleanupMode ? 'Selective cleanup active' : 'Workspace ready'}</span>
    </div>

    <div class="gc-canvas-toolbar__controls">
      <div class="gc-segmented">
        <button type="button" class:gc-active={viewMode === 'original'} on:click={() => onSelectViewMode('original')}>
          Original
        </button>
        <button type="button" class:gc-active={viewMode === 'processed'} on:click={() => onSelectViewMode('processed')}>
          GlassClear Output
        </button>
        <button type="button" class:gc-active={viewMode === 'compare'} on:click={() => onSelectViewMode('compare')}>
          Compare
        </button>
      </div>

      <button class="gc-mini-button" type="button" on:click={onZoomOut}>-</button>
      <button class="gc-mini-button" type="button" on:click={onZoomIn}>+</button>
      <button class="gc-mini-button" type="button" on:click={onFitToScreen}>Fit</button>
    </div>
  </div>

  <div class="gc-canvas-stage">
    {#if hasWorkspaceImage}
      {#if viewMode === 'compare'}
        <BeforeAfterSlider beforeImage={originalImage} afterImage={processedImage} imageFilter={previewFilter} />
      {:else}
        <button
          type="button"
          class:gc-marking={selectiveCleanupMode}
          class="gc-canvas-image-button"
          on:click={handleCanvasClick}
        >
          <img
            src={viewMode === 'processed' ? processedImage : originalImage}
            alt={viewMode === 'processed' ? 'Processed architectural output' : 'Original architectural image'}
            class="gc-canvas-image"
            style={`transform: scale(${zoom}); filter: ${previewFilter || 'none'};`}
          />

          {#each selectedPoints as point}
            <span class="gc-canvas-point" style={`left:${point.x}%; top:${point.y}%;`}></span>
          {/each}

          {#if applying}
            <div class="gc-canvas-loading">
              <strong>Applying AI restoration...</strong>
            </div>
          {/if}
        </button>
      {/if}
    {:else}
      <EmptyCanvasState
        sampleImage={sampleImage}
        onTrySample={onTrySample}
        onUploadImage={onUploadImage}
      />
    {/if}
  </div>

  {#if hasPendingGuestImage && saveProjectHint}
    <p class="gc-canvas-hint">{saveProjectHint}</p>
  {/if}
</section>
