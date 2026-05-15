<svelte:options runes={false} />

<script>
  import { t } from '$lib/state.svelte.js';

  export let open = false;
  export let collections = [];
  export let creating = false;
  export let adding = false;
  export let latestResultAvailable = false;
  export let newCollectionName = '';
  export let selectedCollectionId = null;
  export let mode = 'add';
  export let onClose = () => {};
  export let onChoose = () => {};
  export let onAdd = () => {};
  export let onCreate = () => {};

  function formatUpdated(value) {
    if (!value) return t('common.updatedRecently');
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return t('common.updatedRecently');
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }
</script>

{#if open}
  <div class="gc-modal-backdrop" role="presentation" onclick={onClose}>
    <div
      class="gc-preview-modal gc-collection-modal"
      role="dialog"
      aria-modal="true"
      tabindex="-1"
      onclick={(event) => event.stopPropagation()}
      onkeydown={(event) => {
        if (event.key === 'Escape') {
          onClose();
        }
      }}
    >
      <div class="gc-modal-header gc-card__header--compact">
        <div>
          <p class="gc-delivery-pack__eyebrow">{mode === 'add' ? t('collections.addToCollection') : t('collections.newCollection')}</p>
          <h3>{mode === 'add' ? t('collections.addToCollection') : t('collections.createCollection')}</h3>
          <p>
            {#if mode === 'add'}
              {t('collections.chooseSaveLocation')}
            {:else}
              {t('collections.createPersonal')}
            {/if}
          </p>
        </div>
        <button type="button" class="gc-button gc-button--ghost gc-button--small" onclick={onClose}>{t('common.close')}</button>
      </div>

      {#if mode === 'add'}
        {#if collections.length}
          <div class="gc-collection-modal__list">
            {#each collections as collection}
              <button
                type="button"
                class:selected={selectedCollectionId === collection.id}
                class="gc-collection-modal__item"
                onclick={() => onChoose(collection.id)}
              >
                <strong>{collection.name}</strong>
                <span>{t('common.imagesCount', { count: collection.count })}</span>
                <span>{formatUpdated(collection.updated_at)}</span>
              </button>
            {/each}
          </div>
        {:else}
          <div class="gc-collection-modal__empty">
            <p>{t('collections.emptyMessage')}</p>
          </div>
        {/if}
      {/if}

      <div class="gc-collection-modal__create">
        <label for="collection-name-input">{t('collections.name')}</label>
        <div class="gc-collection-modal__create-row">
          <input
            id="collection-name-input"
            class="gc-collection-modal__input"
            type="text"
            placeholder={t('collections.placeholder')}
            bind:value={newCollectionName}
          />
          <button type="button" class="gc-button gc-button--primary" onclick={onCreate} disabled={creating || !newCollectionName.trim()}>
            {creating ? t('collections.creating') : t('collections.createNew')}
          </button>
        </div>
      </div>

      {#if mode === 'add'}
        <div class="gc-collection-modal__actions">
          <button
            type="button"
            class="gc-button gc-button--soft"
            onclick={() => onAdd(selectedCollectionId)}
            disabled={!latestResultAvailable || !selectedCollectionId || adding}
          >
            {adding ? t('collections.adding') : t('collections.addToCollection')}
          </button>
          {#if !latestResultAvailable}
            <p class="gc-helper-message">{t('collections.processBeforeAdd')}</p>
          {/if}
        </div>
      {/if}
    </div>
  </div>
{/if}
