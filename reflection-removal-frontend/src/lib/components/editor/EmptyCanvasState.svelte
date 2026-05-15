<svelte:options runes={false} />

<script>
  export let sampleImage = '';
  export let onTrySample = () => {};
  export let onUploadImage = () => {};
</script>

<div class="gc-empty-canvas">
  <div class="gc-empty-canvas__card">
    <img src={sampleImage} alt="Sample architectural scene" />
    <div>
      <h2>Start editing with GlassClear</h2>
      <p>Upload an architectural image or try a sample image to access AI editor tools.</p>
    </div>
    <div class="gc-empty-canvas__actions">
      <button type="button" class="gc-primary-action" on:click={onUploadImage}>Upload Image</button>
      <button type="button" class="gc-secondary-action" on:click={onTrySample}>Try Sample</button>
    </div>
  </div>
</div>
