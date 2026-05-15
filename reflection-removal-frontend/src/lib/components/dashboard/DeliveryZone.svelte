<svelte:options runes={false} />

<script>
  import BatchRecoveryPanel from './BatchRecoveryPanel.svelte';
  import ProjectVaultPreview from './ProjectVaultPreview.svelte';
  import ExportStudio from './ExportStudio.svelte';

  export let batchQueue = [];
  export let batchHover = false;
  export let projects = [];
  export let exportOptions = [];
  export let selectedExports = [];
  export let generating = false;
  export let onBatchHoverChange = () => {};
  export let onExportToggle = () => {};
  export let onGeneratePackage = async () => {};
</script>

<section class="gc-zone">
  <div class="gc-zone__heading">
    <span class="gc-section-kicker">Professional Delivery Workspace</span>
    <h2>Manage projects, process batches, and export client-ready architectural results.</h2>
  </div>

  <div class="gc-zone__grid gc-zone__grid--delivery">
    <BatchRecoveryPanel queue={batchQueue} hover={batchHover} onHoverChange={onBatchHoverChange} />
    <ProjectVaultPreview projects={projects} />
    <ExportStudio
      options={exportOptions}
      selected={selectedExports}
      onToggle={onExportToggle}
      onGenerate={onGeneratePackage}
      generating={generating}
    />
  </div>
</section>
