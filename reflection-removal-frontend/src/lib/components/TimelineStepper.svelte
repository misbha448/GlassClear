<script>
  import { t } from '$lib/state.svelte.js';
  import { fade } from 'svelte/transition';

  let { processingSteps = [] } = $props(); // Array of { name: string, status: 'pending' | 'completed' | 'failed' }
</script>

<div class="timeline-stepper" transition:fade>
  <h6 class="panel-label">PROCESSING FLOW</h6>

  <div class="stepper-container">
    {#each processingSteps as step, i}
      <div class="stepper-item {step.status}">
        <div class="stepper-circle">
          {#if step.status === 'completed'}
            <i class="bi bi-check-lg"></i>
          {:else if step.status === 'failed'}
            <i class="bi bi-x-lg"></i>
          {:else}
            {i + 1}
          {/if}
        </div>
        <div class="stepper-label small text-muted">{step.name}</div>
      </div>
      {#if i < processingSteps.length - 1}
        <div class="stepper-line {step.status === 'completed' ? 'completed' : ''}"></div>
      {/if}
    {/each}
  </div>
</div>

<style>
  .panel-label {
    font-size: 0.65rem;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.3);
    letter-spacing: 2px;
    margin-bottom: 1.5rem;
  }

  .stepper-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }

  .stepper-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
    position: relative;
  }

  .stepper-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.5);
    margin-bottom: 5px;
    transition: all 0.3s ease;
  }

  .stepper-item.completed .stepper-circle {
    background: linear-gradient(135deg, #7367f0, #00d2ff);
    color: white;
    box-shadow: 0 0 15px rgba(115, 103, 240, 0.4);
  }

  .stepper-item.failed .stepper-circle {
    background: #dc3545;
    color: white;
    box-shadow: 0 0 10px rgba(220, 53, 69, 0.5);
  }

  .stepper-line {
    flex-grow: 1;
    height: 2px;
    background: rgba(255, 255, 255, 0.05);
    margin-top: -20px; /* Align with circles */
    transition: background 0.6s ease;
  }

  .stepper-line.completed {
    background: linear-gradient(to right, #7367f0, #00d2ff);
  }

  .stepper-label {
    font-size: 0.65rem;
    text-align: center;
    max-width: 60px;
    margin-top: 4px;
  }
</style>