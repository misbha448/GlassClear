<svelte:options runes={false} />

<script>
  import { getDisplayName } from '$lib/utils/displayName.js';

  export let open = false;
  export let item = null;
  export let busy = false;
  export let labels = {};
  export let onClose = () => {};
  export let onJpg = async () => {};
  export let onPng = async () => {};
  export let onHd = async () => {};
  export let onComparison = async () => {};
</script>

{#if open && item}
  <div class="gc-modal-backdrop" role="presentation" onclick={onClose}>
    <div class="gc-modal-card" role="dialog" aria-modal="true" aria-label={labels.title} tabindex="-1" onclick={(event) => event.stopPropagation()} onkeydown={(event) => event.stopPropagation()}>
      <div class="gc-modal-header">
        <div>
          <p class="gc-modal-kicker">{labels.kicker}</p>
          <h2>{labels.title}</h2>
          <p>{getDisplayName(item)}</p>
        </div>
        <button type="button" class="gc-button gc-button--ghost gc-button--small" onclick={onClose}>{labels.close}</button>
      </div>

      <div class="gc-action-grid gc-action-grid--compact">
        <button type="button" class="gc-action-card" onclick={onJpg} disabled={busy}>
          <strong>{labels.jpg}</strong>
          <p>{labels.jpgHelp}</p>
        </button>
        <button type="button" class="gc-action-card" onclick={onPng} disabled={busy}>
          <strong>{labels.png}</strong>
          <p>{labels.pngHelp}</p>
        </button>
        <button type="button" class="gc-action-card" onclick={onHd} disabled={busy}>
          <strong>{labels.hd}</strong>
          <p>{labels.hdHelp}</p>
        </button>
        <button type="button" class="gc-action-card" onclick={onComparison} disabled={busy}>
          <strong>{labels.comparison}</strong>
          <p>{labels.comparisonHelp}</p>
        </button>
      </div>
    </div>
  </div>
{/if}
