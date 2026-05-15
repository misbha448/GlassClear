<script>
  import { t } from '$lib/state.svelte.js';
  let { currentVersion = $bindable('Original') } = $props();
  const versions = ['Original', 'Fidelity', 'Quality'];
</script>

<div class="version-timeline">
  <div class="timeline-track">
    <div 
      class="track-fill" 
      style="width: {versions.indexOf(currentVersion) * 50}%"
    ></div>
  </div>
  <div class="steps">
    {#each versions as version}
      <button 
        class="step-btn" 
        class:active={currentVersion === version}
        onclick={() => currentVersion = version}
      >
        <div class="dot"></div>
        <span class="label">{t('mode_' + version.toLowerCase())}</span>
      </button>
    {/each}
  </div>
</div>

<style>
  .version-timeline {
    position: relative;
    width: 100%;
    max-width: 320px;
    padding: 10px 0;
  }

  .timeline-track {
    position: absolute;
    top: 16px;
    left: 25px;
    right: 25px;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
    z-index: 1;
  }

  .track-fill {
    height: 100%;
    background: #6366f1;
    transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .steps {
    display: flex;
    justify-content: space-between;
    position: relative;
    z-index: 2;
  }

  .step-btn {
    background: none;
    border: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 0;
    transition: all 0.3s ease;
    width: 50px;
  }

  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #0a0a0c;
    border: 2px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
  }

  :global([data-bs-theme='light']) .dot {
    background: #fcfcfd;
    border-color: rgba(0, 0, 0, 0.2);
  }

  .label {
    font-size: 0.6rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
  }

  :global([data-bs-theme='light']) .label { color: rgba(0, 0, 0, 0.4); }
  .step-btn:hover .label { color: rgba(255, 255, 255, 0.8); } /* Dark mode hover */
  :global([data-bs-theme='light']) .step-btn:hover .label { color: rgba(0, 0, 0, 0.8); } /* Light mode hover */

  .step-btn.active .dot {
    background: #6366f1;
    border-color: #6366f1;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
  }

  .step-btn.active .label {
    color: white;
  }
</style>