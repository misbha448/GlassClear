<svelte:options runes={false} />

<script>
  import SelectiveRemovalCanvas from './SelectiveRemovalCanvas.svelte';
  import ModeSelector from './ModeSelector.svelte';
  import StrengthControl from './StrengthControl.svelte';

  export let image = '';
  export let points = [];
  export let modes = [];
  export let selectedMode = '';
  export let strengths = [];
  export let selectedStrength = 'balanced';
  export let running = false;
  export let onAddPoint = () => {};
  export let onClearPoints = () => {};
  export let onModeSelect = () => {};
  export let onStrengthChange = () => {};
  export let onRunRestore = async () => {};
</script>

<section class="gc-zone">
  <div class="gc-zone__heading">
    <span class="gc-section-kicker">Precision Reflection Control</span>
    <h2>Choose where, how, and how strongly GlassClear restores architectural surfaces.</h2>
  </div>

  <div class="gc-zone__grid gc-zone__grid--controls">
    <SelectiveRemovalCanvas
      image={image}
      points={points}
      onAddPoint={onAddPoint}
      onClear={onClearPoints}
    />

    <ModeSelector modes={modes} selectedMode={selectedMode} onSelect={onModeSelect} />

    <StrengthControl
      strengths={strengths}
      selectedStrength={selectedStrength}
      onChange={onStrengthChange}
      onRun={onRunRestore}
      running={running}
    />
  </div>
</section>
