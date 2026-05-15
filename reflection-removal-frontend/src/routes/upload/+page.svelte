<script>
import Navbar from "$lib/components/Navbar.svelte"
import ImageUpload from "$lib/components/ImageUpload.svelte"
import { t } from '$lib/state.svelte.js';
</script>

<Navbar/>

<div class="gc-upload-shell">
<div class="container mt-5 gc-upload-card" style="padding-top: var(--navbar-height);">

<h2 class="mb-4">{t('upload.title')}</h2>

<p class="text-muted">
{t('upload.subtitle')}
</p>
<ImageUpload/>

</div>
</div>

<style>
  .gc-upload-shell {
    min-height: 100vh;
    background: radial-gradient(125% 125% at 50% 10%, #ffffff 40%, #6366f1 100%);
    padding: 1.5rem;
  }

  .gc-upload-card {
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(229,231,235,0.9);
    border-radius: 16px;
    box-shadow: 0 18px 45px rgba(23, 32, 51, 0.08);
    backdrop-filter: blur(18px);
    padding: 2rem;
  }

  .gc-upload-card h2 {
    color: #111827;
  }

  .gc-upload-card p {
    color: #6b7280 !important;
  }
</style>
