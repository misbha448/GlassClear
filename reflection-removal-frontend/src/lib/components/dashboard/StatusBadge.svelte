<svelte:options runes={false} />

<script>
  import { language, t } from '$lib/stores/language.js';

  export let status = 'queued';

  const toneMap = {
    queued: 'muted',
    processing: 'warning',
    completed: 'success',
    failed: 'danger',
    ready: 'success',
    sample: 'muted'
  };

  let label = status;

  $: {
    const activeLanguage = $language;
    activeLanguage;
    label =
      status === 'queued'
        ? t('batch.queued')
        : status === 'processing'
          ? t('batch.processing')
          : status === 'completed'
            ? t('batch.completed')
            : status === 'failed'
              ? t('batch.failed')
              : status === 'partially_failed'
                ? t('batch.partiallyFailed')
                : status === 'sample'
                  ? t('common.sample')
                  : status;
  }
</script>

<span class={`gc-status-badge gc-status-badge--${toneMap[status] || 'muted'}`}>
  {label}
</span>
