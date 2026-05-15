<script>
  import { t } from '$lib/state.svelte.js';
  let { original = "", result = "" } = $props();
</script>

<div class="row mt-4">

<div class="col-md-6">

<h5>{t('res_original')}</h5>

<img src={original} class="img-fluid">

</div>

<div class="col-md-6">

<h5>{t('res_removed')}</h5>

<img src={result} class="img-fluid">

</div>

</div>