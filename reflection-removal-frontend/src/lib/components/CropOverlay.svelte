<script>
  import { onDestroy } from 'svelte';

  let {
    active = false,
    cropRect = { x: 20, y: 15, width: 60, height: 70 },
    onChange = () => {}
  } = $props();

  let overlayEl = $state(null);
  let dragMode = null;
  let startRect = null;
  let startPoint = null;

  function clampRect(rect) {
    const minWidth = 12;
    const minHeight = 12;
    const width = Math.min(Math.max(rect.width, minWidth), 100);
    const height = Math.min(Math.max(rect.height, minHeight), 100);
    const x = Math.min(Math.max(rect.x, 0), 100 - width);
    const y = Math.min(Math.max(rect.y, 0), 100 - height);
    return { x, y, width, height };
  }

  function startInteraction(event, mode) {
    if (!active || !overlayEl) return;

    event.preventDefault();
    event.stopPropagation();
    dragMode = mode;
    startRect = { ...cropRect };
    startPoint = { x: event.clientX, y: event.clientY };

    window.addEventListener('mousemove', handleMove);
    window.addEventListener('mouseup', stopInteraction);
  }

  function handleMove(event) {
    if (!dragMode || !overlayEl || !startRect || !startPoint) return;

    const bounds = overlayEl.getBoundingClientRect();
    const dx = ((event.clientX - startPoint.x) / bounds.width) * 100;
    const dy = ((event.clientY - startPoint.y) / bounds.height) * 100;

    let nextRect = { ...startRect };

    if (dragMode === 'move') {
      nextRect.x = startRect.x + dx;
      nextRect.y = startRect.y + dy;
    } else if (dragMode === 'resize') {
      nextRect.width = startRect.width + dx;
      nextRect.height = startRect.height + dy;
    }

    onChange(clampRect(nextRect));
  }

  function stopInteraction() {
    dragMode = null;
    startRect = null;
    startPoint = null;
    window.removeEventListener('mousemove', handleMove);
    window.removeEventListener('mouseup', stopInteraction);
  }

  onDestroy(() => {
    stopInteraction();
  });
</script>

{#if active}
  <div class="crop-overlay" bind:this={overlayEl}>
    <div
      class="crop-box"
      role="presentation"
      style="left: {cropRect.x}%; top: {cropRect.y}%; width: {cropRect.width}%; height: {cropRect.height}%;"
      onmousedown={(event) => startInteraction(event, 'move')}
    >
      <div class="crop-grid"></div>
      <button
        class="resize-handle"
        type="button"
        aria-label="Resize crop"
        onmousedown={(event) => startInteraction(event, 'resize')}
      ></button>
    </div>
  </div>
{/if}

<style>
  .crop-overlay {
    position: absolute;
    inset: 0;
    z-index: 35;
    background: rgba(2, 6, 23, 0.24);
    pointer-events: auto;
  }

  .crop-box {
    position: absolute;
    border: 1.5px solid rgba(255, 255, 255, 0.92);
    box-shadow: 0 0 0 9999px rgba(2, 6, 23, 0.46);
    cursor: move;
  }

  .crop-grid {
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(to right, rgba(255, 255, 255, 0.25) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.25) 1px, transparent 1px);
    background-size: 33.333% 100%, 100% 33.333%;
  }

  .resize-handle {
    position: absolute;
    right: -0.45rem;
    bottom: -0.45rem;
    width: 1rem;
    height: 1rem;
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.75);
    background: #fff;
    cursor: nwse-resize;
  }
</style>
