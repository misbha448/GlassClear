<svelte:options runes={false} />

<script>
  import SharePanel from './SharePanel.svelte';
  import ProjectsPanel from './ProjectsPanel.svelte';

  export let activeTool = 'remove-reflection';
  export let strength = 'balanced';
  export let detailPreservation = true;
  export let reflectionType = 'auto_detect';
  export let reflectionTypes = [];
  export let brightness = 100;
  export let contrast = 100;
  export let sharpness = 100;
  export let saturation = 100;
  export let isProcessing = false;
  export let historyItems = [];
  export let selectedHistoryId = '';
  export let projects = [];
  export let shareLink = '';
  export let shareStatus = '';
  export let projectStatus = '';
  export let isSavingProject = false;
  export let hasProcessedImage = false;
  export let onStrengthChange = () => {};
  export let onDetailToggle = () => {};
  export let onReflectionTypeChange = () => {};
  export let onApplyReflection = () => {};
  export let onAdjustmentChange = () => {};
  export let onResetAdjustments = () => {};
  export let onSelectHistory = () => {};
  export let onCreateProject = () => {};
  export let onSaveCurrentResult = () => {};
  export let onSelectProject = () => {};
  export let onCopyShareLink = () => {};
  export let onDownloadComparison = () => {};
  export let onOpenClientPreview = () => {};

  const strengthOptions = ['soft', 'balanced', 'strong'];
</script>

<section class="gc-settings">
  {#if activeTool === 'remove-reflection'}
    <div class="gc-setting-card">
      <div class="gc-setting-card__header">
        <div>
          <strong>Remove Reflection</strong>
          <p>Configure the GlassClear AI cleanup pass.</p>
        </div>
      </div>

      <div class="gc-field">
        <span>Strength</span>
        <div class="gc-segmented">
          {#each strengthOptions as option}
            <button type="button" class:gc-segmented__active={strength === option} onclick={() => onStrengthChange(option)}>
              {option === 'soft' ? 'Soft' : option === 'balanced' ? 'Balanced' : 'Strong'}
            </button>
          {/each}
        </div>
      </div>

      <div class="gc-field">
        <span>Detail Preservation</span>
        <button type="button" class:gc-toggle--active={detailPreservation} class="gc-toggle" onclick={onDetailToggle}>
          <span></span>
          <strong>{detailPreservation ? 'On' : 'Off'}</strong>
        </button>
      </div>

      <div class="gc-field">
        <label for="reflection-type">Reflection Type</label>
        <select id="reflection-type" value={reflectionType} onchange={(event) => onReflectionTypeChange(event.currentTarget.value)}>
          {#each reflectionTypes as type}
            <option value={type.value}>{type.label}</option>
          {/each}
        </select>
      </div>

      <button type="button" class="gc-button gc-button--primary gc-button--full" disabled={isProcessing} onclick={onApplyReflection}>
        {isProcessing ? 'Applying...' : 'Apply Reflection Removal'}
      </button>
    </div>
  {:else if activeTool === 'adjust-image'}
    <div class="gc-setting-card">
      <div class="gc-setting-card__header">
        <div>
          <strong>Adjust Image</strong>
          <p>Preview frontend-only tonal refinement.</p>
        </div>
      </div>

      {#each [
        ['brightness', 'Brightness', brightness],
        ['contrast', 'Contrast', contrast],
        ['sharpness', 'Sharpness', sharpness],
        ['saturation', 'Saturation', saturation]
      ] as [key, label, value]}
        <div class="gc-field">
          <div class="gc-field__row">
            <label for={key}>{label}</label>
            <span>{value}%</span>
          </div>
          <input
            id={key}
            type="range"
            min="0"
            max="200"
            value={value}
            oninput={(event) => onAdjustmentChange(key, Number(event.currentTarget.value))}
          />
        </div>
      {/each}

      <button type="button" class="gc-button gc-button--ghost gc-button--full" onclick={onResetAdjustments}>Reset</button>
    </div>
  {:else if activeTool === 'history'}
    <div class="gc-setting-card">
      <div class="gc-setting-card__header">
        <div>
          <strong>History</strong>
          <p>Recent versions from this session or backend workspace.</p>
        </div>
      </div>

      <div class="gc-history-list">
        {#each historyItems as item}
          <button
            type="button"
            class:gc-history-list__item--active={selectedHistoryId === item.id}
            class="gc-history-list__item"
            onclick={() => onSelectHistory(item)}
          >
            <img src={item.thumbnail} alt={item.label} />
            <span>
              <strong>{item.label}</strong>
              <small>{item.filename}</small>
            </span>
          </button>
        {/each}
      </div>
    </div>
  {:else if activeTool === 'projects'}
    <ProjectsPanel
      {projects}
      {projectStatus}
      {isSavingProject}
      onCreateProject={onCreateProject}
      onSaveCurrentResult={onSaveCurrentResult}
      onSelectProject={onSelectProject}
    />
  {:else if activeTool === 'share'}
    <SharePanel
      {shareLink}
      {shareStatus}
      {hasProcessedImage}
      onCopyShareLink={onCopyShareLink}
      onDownloadComparison={onDownloadComparison}
      onOpenClientPreview={onOpenClientPreview}
    />
  {/if}
</section>
