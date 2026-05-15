<script>
  import { t } from '$lib/state.svelte.js';
  import ResultDisplay from './ResultDisplay.svelte';
  import ProcessingScreen from './ProcessingScreen.svelte';
  import { fade } from 'svelte/transition';
  import { apiFetch, API_BASE } from '$lib/api/api.js';
  import { savePendingGuestImage } from '$lib/utils/pendingGuestImage.js';

  let selectedFile = $state(null);
  let previewImage = $state(null);
  let processing = $state(false);
  let error = $state(null);

  // State for the processed results
  let originalProcessedImage = $state(null); // The original image URL from the server after upload
  let finalProcessedImage = $state(null); // The final processed image URL from the server
  let predictionId = $state(null);
  let aiMode = $state({ selected_mode: "fidelity", reason: "No specific reason." });
  let confidenceMap = $state(null);
  let ssim = $state(0.0);
  let edgeScore = $state(0.0);
  let intermediateOutputs = $state([]);
  let processingSteps = $state([]);

  function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
      selectedFile = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImage = e.target.result;
      };
      reader.readAsDataURL(file);
      // Reset results when a new file is selected
      resetResults();
    }
  }

  function resetResults() {
    originalProcessedImage = null;
    finalProcessedImage = null;
    predictionId = null;
    aiMode = { selected_mode: "fidelity", reason: "No specific reason." };
    confidenceMap = null;
    ssim = 0.0;
    edgeScore = 0.0;
    intermediateOutputs = [];
    processingSteps = [];
    error = null;
  }

  async function processImage() {
    if (!selectedFile) {
      error = "Please select an image first.";
      return;
    }

    if (!selectedFile.type?.startsWith('image/')) {
      error = 'Please upload a valid image.';
      return;
    }

    processing = true;
    error = null;

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('mode', 'Quality');

      const response = await apiFetch(`/process-image`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.detail || data?.message || 'Processing failed');
      }
      if (data.processing_required === false) {
        resetResults();
        error = data.message || 'No reflection detected. Processing not required.';
        return;
      }

      if (data.guest_image_token) {
        savePendingGuestImage({
          guest_image_id: data.prediction_id,
          guest_filename: selectedFile?.name,
          guest_original_url: data.original_image_url,
          guest_processed_url: data.processed_image_url,
          guest_image_token: data.guest_image_token
        });
      }

      finalProcessedImage = `${API_BASE}${data.processed_image_url}`;
      originalProcessedImage = `${API_BASE}${data.original_image_url}`;
      predictionId = data.prediction_id;
      aiMode = { selected_mode: data.selected_mode, reason: data.reason };
      confidenceMap = `${API_BASE}${data.confidence_map_url}`;
      ssim = data.ssim;
      edgeScore = data.edge_score;
      intermediateOutputs = (data.intermediate_outputs || []).map(p => `${API_BASE}${p}`);
      processingSteps = data.processing_steps || [];

    } catch (err) {
      error = err.message?.startsWith('Processing failed:')
        ? err.message
        : err.message || 'Please upload a valid image.';
      console.error(err);
    } finally {
      processing = false;
    }
  }
</script>

{#if !finalProcessedImage}
  <div class="image-upload-container glass-card p-4" in:fade>
    <h2 class="text-center text-neon mb-4">{t('upload_title')}</h2>

    <div class="input-group mb-3">
      <input type="file" class="form-control glass-card-nested" id="imageUpload" accept="image/*" onchange={handleFileChange}>
      <button class="btn btn-primary glass-btn" onclick={processImage} disabled={!selectedFile || processing}>
        {#if processing}
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          Processing...
        {:else}
          {t('process_button')}
        {/if}
      </button>
    </div>

    {#if error}
      <div class="alert alert-danger" role="alert" in:fade>{error}</div>
    {/if}

    {#if previewImage}
      <div class="preview-area text-center mt-4" in:fade>
        <h5>{t('preview_title')}</h5>
        {#if processing}
          <ProcessingScreen
            originalSrc={previewImage}
            processedSrc={finalProcessedImage}
            title="Premium AI Reflection Removal"
            subtitle="The uploaded image is being scanned for glare, reflection hotspots, and clean-surface reconstruction."
          />
        {:else}
          <img src={previewImage} alt="Preview" class="img-fluid rounded-3 shadow-premium" style="max-height: 400px;">
        {/if}
      </div>
    {/if}
  </div>
{:else}
  <div class="results-dashboard-wrapper" in:fade>
    <button class="btn btn-outline-secondary mb-3" onclick={() => finalProcessedImage = null}>
      <i class="bi bi-arrow-left me-2"></i> {t('btn_reprocess') || 'Process Another'}
    </button>
    <ResultDisplay
      originalImage={originalProcessedImage}
      processedImage={finalProcessedImage}
      {predictionId}
      {aiMode}
      {confidenceMap}
      {ssim}
      {edgeScore}
      {intermediateOutputs}
      {processingSteps}
    />
  </div>
{/if}

<style>
  .image-upload-container {
    max-width: 900px;
    margin: 50px auto;
  }
  .glass-card-nested {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: #fff;
  }
  .glass-btn {
    background: linear-gradient(45deg, #00d2ff, #7367f0);
    border: none;
    color: white;
    font-weight: bold;
    transition: all 0.3s ease;
  }
  .glass-btn:hover {
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 210, 255, 0.3);
  }
  .text-neon {
    color: #00d2ff;
    text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
  }
</style>
