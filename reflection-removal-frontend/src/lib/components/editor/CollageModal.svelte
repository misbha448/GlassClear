<svelte:options runes={false} />

<script>
  export let open = false;
  export let layouts = [];
  export let selectedLayout = 'before_after_split';
  export let selectedImageKeys = [];
  export let availableImages = [];
  export let previewUrl = '';
  export let outputUrl = '';
  export let statusMessage = '';
  export let disabled = false;
  export let onSelectLayout = () => {};
  export let onToggleImage = () => {};
  export let onGenerate = () => {};
  export let onDownload = () => {};
  export let onOpenOutput = () => {};
  export let onClose = () => {};

  $: activeLayout =
    layouts.find((layout) => layout.id === selectedLayout) || layouts[0] || { min: 1, max: 1 };
</script>

{#if open}
  <div class="gc-modal-backdrop" role="presentation" on:click={onClose}>
    <div
      class="gc-modal gc-modal--collage"
      role="dialog"
      aria-modal="true"
      aria-label="Collage maker"
      tabindex="-1"
      on:click|stopPropagation
      on:keydown|stopPropagation
    >
      <div class="gc-modal__header">
        <div>
          <span>Collage Maker</span>
          <h2>Create Client-Ready Collage</h2>
          <p>Select images and choose a layout to generate a polished comparison board.</p>
        </div>
        <button type="button" class="gc-modal__close" aria-label="Close collage maker" on:click={onClose}>x</button>
      </div>

      <div class="gc-collage-builder">
        <section class="gc-modal-card">
          <div class="gc-modal-card__head">
            <strong>Layouts</strong>
            <span>{activeLayout.min} to {activeLayout.max} images</span>
          </div>

          <div class="gc-collage-layout-grid">
            {#each layouts as layout}
              <button
                type="button"
                class:gc-active={layout.id === selectedLayout}
                class="gc-choice-chip gc-collage-layout-card"
                on:click={() => onSelectLayout(layout.id)}
              >
                <strong>{layout.title}</strong>
                <span>{layout.description}</span>
              </button>
            {/each}
          </div>
        </section>

        <section class="gc-modal-card">
          <div class="gc-modal-card__head">
            <strong>Select Images</strong>
            <span>{selectedImageKeys.length} selected</span>
          </div>

          <div class="gc-image-pick-grid">
            {#each availableImages as image}
              <button
                type="button"
                class:gc-active={selectedImageKeys.includes(image.key)}
                class="gc-image-pick-card"
                on:click={() => onToggleImage(image.key)}
              >
                <img src={image.url} alt={image.label} />
                <div class="gc-image-pick-card__body">
                  <strong>{image.label}</strong>
                  <span>{image.meta}</span>
                </div>
                <span class="gc-image-pick-card__check">
                  {selectedImageKeys.includes(image.key) ? 'Selected' : 'Select'}
                </span>
              </button>
            {/each}
          </div>
        </section>

        <section class="gc-modal-card gc-modal-card--preview">
          <div class="gc-modal-card__head">
            <strong>Preview</strong>
          </div>

          {#if previewUrl || outputUrl}
            <div class="gc-modal-preview">
              <img src={outputUrl || previewUrl} alt="Generated collage preview" />
            </div>
          {:else}
            <div class="gc-modal-placeholder">
              <strong>Live preview area</strong>
              <p>Choose a layout and images, then generate a board to preview it here.</p>
            </div>
          {/if}

          <div class="gc-settings-actions">
            <button type="button" class="gc-primary-action" on:click={onGenerate} disabled={disabled}>
              Generate Collage
            </button>
            <button
              type="button"
              class="gc-secondary-action"
              on:click={onDownload}
              disabled={disabled || (!previewUrl && !outputUrl)}
            >
              Save Collage
            </button>
            <button
              type="button"
              class="gc-secondary-action"
              on:click={onOpenOutput}
              disabled={disabled || (!previewUrl && !outputUrl)}
            >
              Open Collage
            </button>
          </div>
        </section>
      </div>

      {#if statusMessage}
        <p class="gc-modal-note">{statusMessage}</p>
      {/if}
    </div>
  </div>
{/if}
