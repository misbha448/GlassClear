<script>
  let {
    steps = [],
    activeStep = 0
  } = $props();
</script>

<div class="steps" aria-label="Processing steps">
  {#each steps as step, index}
    <div
      class="step-card {index < activeStep ? 'is-complete' : ''} {index === activeStep ? 'is-active' : ''}"
      aria-current={index === activeStep ? 'step' : undefined}
    >
      <div class="step-index">{index + 1}</div>
      <div class="step-copy">
        <span class="step-title">{step}</span>
        <span class="step-state">
          {#if index < activeStep}
            Completed
          {:else if index === activeStep}
            In Progress
          {:else}
            Pending
          {/if}
        </span>
      </div>
    </div>
  {/each}
</div>

<style>
  .steps {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.9rem;
    width: 100%;
  }

  .step-card {
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    min-height: 84px;
    padding: 1rem 1.05rem;
    border-radius: 20px;
    border: 1px solid rgba(226, 232, 240, 0.92);
    background: rgba(255, 255, 255, 0.82);
    box-shadow: 0 16px 34px rgba(79, 70, 229, 0.08);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    transition:
      transform 0.35s ease-in-out,
      border-color 0.35s ease-in-out,
      box-shadow 0.35s ease-in-out,
      background 0.35s ease-in-out;
  }

  .step-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(224, 231, 255, 0.6), transparent 75%);
    opacity: 0;
    transition: opacity 0.35s ease-in-out;
    pointer-events: none;
  }

  .step-index {
    position: relative;
    z-index: 1;
    display: grid;
    place-items: center;
    width: 2.5rem;
    height: 2.5rem;
    flex-shrink: 0;
    border-radius: 999px;
    border: 1px solid rgba(99, 102, 241, 0.12);
    background: #eef2ff;
    color: #4f46e5;
    font-size: 0.9rem;
    font-weight: 700;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
  }

  .step-copy {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    min-width: 0;
  }

  .step-title {
    color: #111827;
    font-size: 0.92rem;
    font-weight: 600;
    line-height: 1.25;
  }

  .step-state {
    color: #64748b;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .step-card.is-active {
    transform: translateY(-3px);
    border-color: rgba(99, 102, 241, 0.28);
    box-shadow:
      0 0 0 1px rgba(99, 102, 241, 0.12),
      0 18px 40px rgba(99, 102, 241, 0.14);
  }

  .step-card.is-active::before {
    opacity: 1;
  }

  .step-card.is-active .step-index {
    border-color: rgba(99, 102, 241, 0.24);
    background: linear-gradient(135deg, #6366f1, #818cf8);
    color: white;
  }

  .step-card.is-complete {
    border-color: rgba(34, 197, 94, 0.2);
    background: rgba(240, 253, 244, 0.92);
  }

  .step-card.is-complete .step-index {
    background: linear-gradient(135deg, #22c55e, #4ade80);
    border-color: rgba(34, 197, 94, 0.26);
    color: white;
  }

  .step-card.is-complete .step-state {
    color: #166534;
  }

  @media (max-width: 960px) {
    .steps {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 640px) {
    .steps {
      grid-template-columns: 1fr;
    }

    .step-card {
      min-height: 72px;
      padding: 0.9rem 1rem;
    }
  }
</style>
