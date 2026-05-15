<script>
  import { t } from '$lib/state.svelte.js';
</script>

<div class="text-center mt-4">
  <div class="spinner-border text-primary" role="status"></div>
  <p class="mt-2">{t('loader_processing')}</p>
</div>