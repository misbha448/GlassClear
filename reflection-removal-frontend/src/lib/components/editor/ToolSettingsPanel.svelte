<svelte:options runes={false} />

<script>
  export let selectedTool = null;
  export let toolList = [];
  export let showToolPicker = false;
  export let panelMode = 'tool';
  export let strength = 'balanced';
  export let detailPreservation = true;
  export let reflectionType = 'auto-detect';
  export let reflectionTypes = [];
  export let selectiveCleanupMode = false;
  export let brightness = 100;
  export let contrast = 100;
  export let sharpness = 100;
  export let applying = false;
  export let hasProcessedImage = false;
  export let clarityPreviewEnabled = false;
  export let colorRestorePreviewEnabled = false;
  export let resizeWidth = '';
  export let resizeHeight = '';
  export let formatValue = 'PNG';
  export let toolMessage = '';
  export let onSelectTool = () => {};
  export let onStrengthChange = () => {};
  export let onToggleDetail = () => {};
  export let onReflectionTypeChange = () => {};
  export let onToggleSelective = () => {};
  export let onBrightnessChange = () => {};
  export let onContrastChange = () => {};
  export let onSharpnessChange = () => {};
  export let onResizeWidthChange = () => {};
  export let onResizeHeightChange = () => {};
  export let onFormatChange = () => {};
  export let onApply = () => {};
  export let onReset = () => {};
</script>

<aside class="gc-settings-panel">
  {#if showToolPicker && toolList.length}
    <section class="gc-settings-card">
      <div class="gc-settings-card__head">
        <strong>AI Tools</strong>
        <span>{toolList.length} available</span>
      </div>

      <div class="gc-tool-selector">
        {#each toolList as tool}
          <button
            type="button"
            class:gc-active={selectedTool?.id === tool.id}
            class="gc-choice-chip"
            on:click={() => onSelectTool(tool.id)}
          >
            {tool.title}
          </button>
        {/each}
      </div>
    </section>
  {/if}

  {#if panelMode === 'adjustments'}
    <div class="gc-settings-panel__header">
      <span>Adjustments</span>
      <h2>Image adjustments</h2>
      <p>Use the sliders below for a clean frontend preview during your demo.</p>
    </div>

    <section class="gc-settings-card">
      <div class="gc-settings-card__head">
        <strong>Brightness</strong>
        <span>{brightness}%</span>
      </div>
      <input type="range" min="60" max="140" step="1" value={brightness} on:input={(event) => onBrightnessChange(Number(event.currentTarget.value))} />
    </section>

    <section class="gc-settings-card">
      <div class="gc-settings-card__head">
        <strong>Contrast</strong>
        <span>{contrast}%</span>
      </div>
      <input type="range" min="60" max="140" step="1" value={contrast} on:input={(event) => onContrastChange(Number(event.currentTarget.value))} />
    </section>

    <section class="gc-settings-card">
      <div class="gc-settings-card__head">
        <strong>Sharpness</strong>
        <span>{sharpness}%</span>
      </div>
      <input type="range" min="60" max="140" step="1" value={sharpness} on:input={(event) => onSharpnessChange(Number(event.currentTarget.value))} />
    </section>

    <div class="gc-settings-actions">
      <button class="gc-secondary-action" type="button" on:click={onReset}>Reset Panel</button>
    </div>
  {:else if selectedTool?.id === 'remove_reflection' || selectedTool?.id === 'remove_glare' || selectedTool?.id === 'preserve_details'}
    <div class="gc-settings-panel__header">
      <span>Tool Settings</span>
      <h2>{selectedTool?.title}</h2>
      <p>{selectedTool?.description}</p>
    </div>

    <section class="gc-settings-card">
      <div class="gc-settings-card__head">
        <strong>Strength</strong>
        <span>{selectedTool?.id === 'remove_glare' ? 'balanced' : strength}</span>
      </div>

      <div class="gc-strength-editor">
        <input
          type="range"
          min="0"
          max="2"
          step="1"
          disabled={selectedTool?.id === 'remove_glare'}
          value={strength === 'soft' ? 0 : strength === 'balanced' ? 1 : 2}
          on:input={(event) =>
            onStrengthChange(['soft', 'balanced', 'strong'][Number(event.currentTarget.value)])}
        />

        <div class="gc-strength-editor__labels">
          <span class:gc-active={strength === 'soft'}>Soft</span>
          <span class:gc-active={strength === 'balanced' || selectedTool?.id === 'remove_glare'}>Balanced</span>
          <span class:gc-active={strength === 'strong'}>Strong</span>
        </div>
      </div>
    </section>

    <section class="gc-settings-card">
      <div class="gc-settings-card__toggle">
        <div>
          <strong>Detail Preservation</strong>
          <p>{selectedTool?.id === 'preserve_details' ? 'Enabled for the next reflection removal run.' : 'Keep facade edges and material textures natural.'}</p>
        </div>

        <button
          type="button"
          aria-label="Toggle detail preservation"
          class:gc-active={detailPreservation || selectedTool?.id === 'preserve_details'}
          class="gc-toggle-button"
          on:click={onToggleDetail}
        >
          <span></span>
        </button>
      </div>
    </section>

    <section class="gc-settings-card">
      <div class="gc-settings-card__head">
        <strong>Reflection Type</strong>
      </div>

      <div class="gc-reflection-types">
        {#each reflectionTypes as option}
          <button
            type="button"
            class:gc-active={(selectedTool?.id === 'remove_glare' && option.id === 'window_glare') || reflectionType === option.id}
            class="gc-choice-chip"
            on:click={() => onReflectionTypeChange(option.id)}
            disabled={selectedTool?.id === 'remove_glare' && option.id !== 'window_glare'}
          >
            {option.label}
          </button>
        {/each}
      </div>
    </section>

    <section class="gc-settings-card">
      <div class="gc-settings-card__head">
        <strong>Selective Cleanup</strong>
        <p>Click on the image to prioritize cleanup regions.</p>
      </div>

      <button
        type="button"
        class:gc-active={selectiveCleanupMode}
        class="gc-secondary-action"
        on:click={onToggleSelective}
      >
        {selectiveCleanupMode ? 'Marking Active' : 'Mark Reflection Areas'}
      </button>
    </section>

    <div class="gc-settings-actions">
      <button class="gc-primary-action" type="button" on:click={onApply} disabled={applying}>
        {applying
          ? 'Applying AI restoration...'
          : selectedTool?.id === 'remove_glare'
            ? 'Apply Glare Removal'
            : selectedTool?.id === 'preserve_details'
              ? 'Apply With Detail Preservation'
              : 'Apply Reflection Removal'}
      </button>
      <button class="gc-secondary-action" type="button" on:click={onReset}>Reset Panel</button>
    </div>
  {:else if selectedTool?.id === 'enhance_clarity' || selectedTool?.id === 'color_restore'}
    <div class="gc-settings-panel__header">
      <span>Tool Settings</span>
      <h2>{selectedTool.title}</h2>
      <p>{selectedTool.description}</p>
    </div>

    <section class="gc-settings-card">
      <strong>{selectedTool.id === 'enhance_clarity' ? 'Clarity preview' : 'Color restore preview'}</strong>
      <p>
        {selectedTool.id === 'enhance_clarity'
          ? 'Applies a frontend-only display filter so users can inspect a sharper preview instantly.'
          : 'Applies a frontend-only display filter to lift muted color and contrast.'}
      </p>
      <p>
        {selectedTool.id === 'enhance_clarity'
          ? clarityPreviewEnabled ? 'Preview is active.' : 'Preview is not active yet.'
          : colorRestorePreviewEnabled ? 'Preview is active.' : 'Preview is not active yet.'}
      </p>
    </section>

    <div class="gc-settings-actions">
      <button class="gc-primary-action" type="button" on:click={onApply}>
        Apply Preview
      </button>
      <button class="gc-secondary-action" type="button" on:click={onReset}>Reset Preview</button>
    </div>
  {:else if selectedTool?.id === 'before_after_poster' || selectedTool?.id === 'collage_maker' || selectedTool?.id === 'client_showcase'}
    <div class="gc-settings-panel__header">
      <span>Tool Settings</span>
      <h2>{selectedTool.title}</h2>
      <p>{selectedTool.description}</p>
    </div>

    <section class="gc-settings-card">
      <strong>{selectedTool.id === 'client_showcase' ? 'Presentation tools' : 'Collage generation'}</strong>
      <p>
        {selectedTool.id === 'before_after_poster'
          ? 'Opens Collage Maker with Before/After Split preselected.'
          : selectedTool.id === 'collage_maker'
            ? 'Select images, generate a polished board, then download it.'
            : 'Open the Share Center to create a client-facing link or share poster.'}
      </p>
    </section>

    <div class="gc-settings-actions">
      <button class="gc-primary-action" type="button" on:click={onApply}>
        {selectedTool.id === 'client_showcase' ? 'Open Share Center' : 'Open Collage Builder'}
      </button>
      <button class="gc-secondary-action" type="button" on:click={onReset}>Reset Panel</button>
    </div>
  {:else if selectedTool?.id === 'crop'}
    <div class="gc-settings-panel__header">
      <span>Tool Settings</span>
      <h2>Crop</h2>
      <p>Crop tool UI is staged so the dashboard does not feel broken while backend save is still disconnected.</p>
    </div>

    <section class="gc-settings-card">
      <strong>Crop placeholder</strong>
      <p>Crop tool UI ready. Backend save not connected yet.</p>
    </section>

    <div class="gc-settings-actions">
      <button class="gc-primary-action" type="button" on:click={onApply}>Show Crop Status</button>
      <button class="gc-secondary-action" type="button" on:click={onReset}>Reset Panel</button>
    </div>
  {:else if selectedTool?.id === 'resize'}
    <div class="gc-settings-panel__header">
      <span>Tool Settings</span>
      <h2>Resize</h2>
      <p>Width and height controls are ready, but saving resized output still needs backend support.</p>
    </div>

    <section class="gc-settings-card">
      <div class="gc-resize-grid">
        <label>
          <strong>Width</strong>
          <input type="number" min="1" value={resizeWidth} on:input={(event) => onResizeWidthChange(event.currentTarget.value)} placeholder="1920" />
        </label>
        <label>
          <strong>Height</strong>
          <input type="number" min="1" value={resizeHeight} on:input={(event) => onResizeHeightChange(event.currentTarget.value)} placeholder="1080" />
        </label>
      </div>
      <p>Resize backend not connected yet. The dimensions above are stored only in the current panel.</p>
    </section>

    <div class="gc-settings-actions">
      <button class="gc-primary-action" type="button" disabled>Apply Resize</button>
      <button class="gc-secondary-action" type="button" on:click={onReset}>Reset Panel</button>
    </div>
  {:else if selectedTool?.id === 'format_converter'}
    <div class="gc-settings-panel__header">
      <span>Tool Settings</span>
      <h2>Format Converter</h2>
      <p>Select a target format without leaving the dashboard. Real conversion stays disabled until backend support is wired.</p>
    </div>

    <section class="gc-settings-card">
      <div class="gc-settings-card__head">
        <strong>Target format</strong>
      </div>
      <select value={formatValue} on:change={(event) => onFormatChange(event.currentTarget.value)}>
        <option value="PNG">PNG</option>
        <option value="JPG">JPG</option>
        <option value="WEBP">WEBP</option>
      </select>
      <p>{hasProcessedImage ? 'Format conversion backend not connected yet.' : 'Process an image first to prepare a downloadable output.'}</p>
    </section>

    <div class="gc-settings-actions">
      <button class="gc-primary-action" type="button" on:click={onApply}>
        Check Conversion Support
      </button>
      <button class="gc-secondary-action" type="button" on:click={onReset}>Reset Panel</button>
    </div>
  {:else if selectedTool}
    <div class="gc-settings-panel__header">
      <span>Tool Settings</span>
      <h2>{selectedTool.title}</h2>
      <p>{selectedTool.description}</p>
    </div>

    <section class="gc-settings-card">
      <strong>Editor Note</strong>
      <p>This tool has a safe placeholder state so the dashboard never leaves the user with a dead action.</p>
    </section>

    <div class="gc-settings-actions">
      <button class="gc-primary-action" type="button" on:click={onApply}>Open Tool</button>
      <button class="gc-secondary-action" type="button" on:click={onReset}>Reset Panel</button>
    </div>
  {/if}

  {#if toolMessage}
    <p class="gc-modal-note">{toolMessage}</p>
  {/if}
</aside>
