<script>
  let {
    canCrop = true,
    isCropping = false,
    hasEdits = false,
    onRotateLeft = () => {},
    onRotateRight = () => {},
    onToggleCrop = () => {},
    onApplyCrop = () => {},
    onReset = () => {}
  } = $props();
</script>

<div class="editor-toolbar" aria-label="Image editing tools">
  <button class="tool-btn" type="button" onclick={onRotateLeft} title="Rotate Left" aria-label="Rotate Left">
    <i class="bi bi-arrow-counterclockwise"></i>
  </button>

  <button class="tool-btn" type="button" onclick={onRotateRight} title="Rotate Right" aria-label="Rotate Right">
    <i class="bi bi-arrow-clockwise"></i>
  </button>

  <button
    class="tool-btn {isCropping ? 'is-active' : ''}"
    type="button"
    onclick={onToggleCrop}
    title={isCropping ? 'Cancel Crop' : 'Crop'}
    aria-label={isCropping ? 'Cancel Crop' : 'Crop'}
    disabled={!canCrop}
  >
    <i class="bi bi-bounding-box-circles"></i>
  </button>

  {#if isCropping}
    <button class="tool-btn is-accent" type="button" onclick={onApplyCrop} title="Apply Crop" aria-label="Apply Crop">
      <i class="bi bi-check2"></i>
    </button>
  {/if}

  <button
    class="tool-btn"
    type="button"
    onclick={onReset}
    title="Reset Edits"
    aria-label="Reset Edits"
    disabled={!hasEdits && !isCropping}
  >
    <i class="bi bi-arrow-repeat"></i>
  </button>
</div>

<style>
  .editor-toolbar {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.55rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
  }

  .tool-btn {
    width: 2.6rem;
    height: 2.6rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.03);
    color: rgba(255, 255, 255, 0.82);
    transition: all 0.22s ease-in-out;
  }

  .tool-btn:hover:enabled,
  .tool-btn.is-active {
    color: #fff;
    border-color: rgba(115, 103, 240, 0.42);
    background: rgba(115, 103, 240, 0.12);
    box-shadow: 0 0 18px rgba(115, 103, 240, 0.16);
  }

  .tool-btn.is-accent {
    border-color: rgba(16, 185, 129, 0.28);
    background: rgba(16, 185, 129, 0.12);
    color: #86efac;
  }

  .tool-btn:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
</style>
