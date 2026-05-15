<svelte:options runes={false} />

<script>
  export let settings = {};
  export let saving = false;
  export let error = '';
  export let onSave = () => {};

  let form = {
    max_upload_size_mb: 15,
    max_batch_size: 50,
    default_share_expiry_days: 7,
    demo_image_url: '',
    welcome_email_subject: ''
  };

  $: form = {
    max_upload_size_mb: settings.max_upload_size_mb ?? 15,
    max_batch_size: settings.max_batch_size ?? 50,
    default_share_expiry_days: settings.default_share_expiry_days ?? 7,
    demo_image_url: settings.demo_image_url ?? '',
    welcome_email_subject: settings.welcome_email_subject ?? ''
  };
</script>

<section class="gc-admin-settings-grid">
  <article class="gc-admin-panel">
    <div class="gc-admin-panel__header">
      <div>
        <span class="gc-admin-section-kicker">Demo Sample Image</span>
        <h2>Presentation Asset</h2>
      </div>
    </div>
    <img class="gc-admin-settings-preview" src={settings.demo_image_url} alt="Demo preview" />
    <div class="gc-admin-settings-meta">
      <strong>{settings.demo_image_url || 'No demo image configured'}</strong>
    </div>
  </article>

  <article class="gc-admin-panel">
    <div class="gc-admin-panel__header">
      <div>
        <span class="gc-admin-section-kicker">Upload Limits</span>
        <h2>Ingestion Rules</h2>
      </div>
    </div>
    <div class="gc-admin-settings-list">
      <label>
        <span>Max upload size (MB)</span>
        <input type="number" min="1" bind:value={form.max_upload_size_mb} />
      </label>
      <label>
        <span>Max batch size</span>
        <input type="number" min="1" bind:value={form.max_batch_size} />
      </label>
    </div>
  </article>

  <article class="gc-admin-panel">
    <div class="gc-admin-panel__header">
      <div>
        <span class="gc-admin-section-kicker">Share Settings</span>
        <h2>Delivery Defaults</h2>
      </div>
    </div>
    <div class="gc-admin-settings-list">
      <label>
        <span>Default share expiry (days)</span>
        <input type="number" min="1" bind:value={form.default_share_expiry_days} />
      </label>
    </div>
  </article>

  <article class="gc-admin-panel">
    <div class="gc-admin-panel__header">
      <div>
        <span class="gc-admin-section-kicker">Welcome Email Preview</span>
        <h2>Messaging Check</h2>
      </div>
    </div>
    <div class="gc-admin-email-preview">
      <span>Subject</span>
      <input type="text" bind:value={form.welcome_email_subject} />
    </div>
    {#if error}
      <p>{error}</p>
    {/if}
    <button
      type="button"
      class="gc-admin-button gc-admin-button--primary"
      on:click={() => onSave(form)}
      disabled={saving}
    >
      {saving ? 'Saving...' : 'Save Settings'}
    </button>
  </article>
</section>
