<svelte:options runes={false} />

<script>
  import { onDestroy, onMount } from 'svelte';

  export let beforeImage = '';
  export let afterImage = '';
  export let imageFilter = '';

  let slider = 52;
  let dragging = false;
  let container;

  function updateSlider(event) {
    if (!container) return;
    const rect = container.getBoundingClientRect();
    const clientX = event.touches ? event.touches[0].clientX : event.clientX;
    slider = Math.max(0, Math.min(100, ((clientX - rect.left) / rect.width) * 100));
  }

  function startDrag(event) {
    dragging = true;
    updateSlider(event);
  }

  function moveDrag(event) {
    if (!dragging) return;
    updateSlider(event);
  }

  function stopDrag() {
    dragging = false;
  }

  onMount(() => {
    window.addEventListener('pointermove', moveDrag);
    window.addEventListener('pointerup', stopDrag);
  });

  onDestroy(() => {
    window.removeEventListener('pointermove', moveDrag);
    window.removeEventListener('pointerup', stopDrag);
  });
</script>

<div bind:this={container} class="gc-compare-editor" on:pointerdown={startDrag} role="presentation">
  <img src={beforeImage} alt="Original" class="gc-compare-editor__image" style={`filter: ${imageFilter || 'none'};`} />

  <div class="gc-compare-editor__after" style={`clip-path: inset(0 ${100 - slider}% 0 0);`}>
    <img src={afterImage} alt="Processed" class="gc-compare-editor__image" style={`filter: ${imageFilter || 'none'};`} />
  </div>

  <div class="gc-compare-editor__labels">
    <span>Original</span>
    <span>GlassClear Output</span>
  </div>

  <div class="gc-compare-editor__divider" style={`left:${slider}%;`}>
    <span class="gc-compare-editor__handle"></span>
  </div>
</div>
