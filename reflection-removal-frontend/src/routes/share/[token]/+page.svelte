<svelte:options runes={false} />

<script>
  import { onMount } from 'svelte';
  import { downloadFile, getPublicShare, withBase } from '$lib/api/dashboardApi.js';
  import { language, t } from '$lib/stores/language.js';
  import { getDisplayName, getDownloadName } from '$lib/utils/displayName.js';

  export let data;

  let loading = true;
  let payload = null;
  let errorType = '';
  let activeLanguage = 'en';
  let labels = {};

  $: activeLanguage = $language;
  $: {
    activeLanguage;
    labels = {
      title: t('share.title'),
      loadingPreview: t('share.loadingPreview'),
      invalidTitle: t('share.invalidTitle'),
      invalidMessage: t('share.invalidMessage'),
      expiredTitle: t('share.expiredTitle'),
      expiredMessage: t('share.expiredMessage'),
      genericError: t('share.genericError'),
      publicPreview: t('share.publicPreview'),
      downloadResult: t('share.downloadResult'),
      original: t('common.original'),
      output: t('common.output')
    };
  }

  function normalizeUrl(url) {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return withBase(url) || url;
  }

  async function handleDownload() {
    if (!payload?.processed_url) return;
    await downloadFile(payload.processed_url, getDownloadName(payload));
  }

  onMount(async () => {
    try {
      payload = await getPublicShare(data.token);
    } catch (error) {
      errorType = error?.status === 410 ? 'expired' : error?.status === 404 ? 'invalid' : 'generic';
    } finally {
      loading = false;
    }
  });
</script>

<script context="module">
  export async function load({ params }) {
    return { token: params.token };
  }
</script>

<svelte:head>
  <title>{labels.title}</title>
</svelte:head>

<div class="gc-public-share">
  <div class="gc-public-share__card">
    {#if loading}
      <h1>{labels.loadingPreview}</h1>
    {:else if errorType === 'invalid'}
      <h1>{labels.invalidTitle}</h1>
      <p>{labels.invalidMessage}</p>
    {:else if errorType === 'expired'}
      <h1>{labels.expiredTitle}</h1>
      <p>{labels.expiredMessage}</p>
    {:else if errorType}
      <h1>{labels.invalidTitle}</h1>
      <p>{labels.genericError}</p>
    {:else}
      <p class="gc-public-share__eyebrow">{labels.publicPreview}</p>
      <h1>{getDisplayName(payload)}</h1>
      {#if getDisplayName(payload) !== payload.filename}
        <p>{payload.filename}</p>
      {/if}
      <p class="gc-public-share__date">
        {new Date(payload.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
      </p>

      <div class="gc-public-share__grid">
        <figure>
          <img src={normalizeUrl(payload.original_url)} alt={labels.original} />
          <figcaption>{labels.original}</figcaption>
        </figure>
        <figure>
          <img src={normalizeUrl(payload.processed_url)} alt={labels.output} />
          <figcaption>{labels.output}</figcaption>
        </figure>
      </div>

      {#if payload.allow_download !== false}
        <button type="button" class="gc-public-share__button" onclick={handleDownload}>{labels.downloadResult}</button>
      {/if}
    {/if}
  </div>
</div>

<style>
  .gc-public-share {
    min-height: 100vh;
    padding: 32px 20px;
    background: radial-gradient(125% 125% at 50% 10%, #ffffff 40%, #6366f1 100%);
    color: #172033;
  }

  .gc-public-share__card {
    width: min(1120px, 100%);
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid #e5e7eb;
    border-radius: 28px;
    box-shadow: 0 18px 45px rgba(23, 32, 51, 0.08);
    padding: 28px;
    backdrop-filter: blur(18px);
  }

  .gc-public-share__eyebrow,
  .gc-public-share__date,
  .gc-public-share figcaption,
  .gc-public-share p {
    color: #6b7280;
  }

  .gc-public-share__grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
    margin-top: 24px;
  }

  .gc-public-share figure {
    margin: 0;
  }

  .gc-public-share img {
    width: 100%;
    aspect-ratio: 4 / 3;
    object-fit: cover;
    border-radius: 20px;
    display: block;
  }

  .gc-public-share__button {
    margin-top: 22px;
    border: none;
    border-radius: 14px;
    padding: 12px 18px;
    background: linear-gradient(135deg, #5b6cff, #7c3aed);
    color: #fff;
    font-weight: 700;
    cursor: pointer;
  }

  @media (max-width: 720px) {
    .gc-public-share__grid {
      grid-template-columns: 1fr;
    }
  }
</style>
