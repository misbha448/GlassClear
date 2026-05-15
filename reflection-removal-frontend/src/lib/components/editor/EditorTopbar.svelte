<svelte:options runes={false} />

<script>
  export let currentFileName = 'Sample Architectural Image';
  export let userName = 'Misbha';
  export let userInitial = 'M';
  export let userMode = 'Architect Mode';
  export let searchQuery = '';
  export let allToolsOpen = false;
  export let flatTools = [];
  export let aiStatus = 'online';
  export let onToggleSidebar = () => {};
  export let onSearchChange = () => {};
  export let onToggleAllTools = () => {};
  export let onSelectTool = () => {};
  export let onProjects = () => {};
  export let onOpenImage = () => {};
  export let onShare = () => {};
  export let onCollage = () => {};
  export let onExport = () => {};
</script>

<header class="gc-topbar-editor">
  <div class="gc-topbar-editor__left">
    <button class="gc-mobile-menu" type="button" aria-label="Open tools sidebar" on:click={onToggleSidebar}>
      <span></span><span></span><span></span>
    </button>

    <div class="gc-brand">
      <span class="gc-brand__mark">G</span>
      <div>
        <strong>GlassClear</strong>
        <span>AI Editor Workspace</span>
      </div>
    </div>

    <button class="gc-topbar-button" type="button" on:click={onProjects}>My Projects</button>
    <button class="gc-topbar-button gc-topbar-button--accent" type="button" on:click={onOpenImage}>
      Open Image
    </button>

    <div class="gc-topbar-dropdown">
      <button class="gc-topbar-button" type="button" on:click={onToggleAllTools}>
        All Tools
      </button>

      {#if allToolsOpen}
        <div class="gc-topbar-menu">
          {#each flatTools as tool}
            <button type="button" class="gc-topbar-menu__item" on:click={() => onSelectTool(tool.id)}>
              <strong>{tool.title}</strong>
              <span>{tool.description}</span>
            </button>
          {/each}
        </div>
      {/if}
    </div>

    <label class="gc-tool-search">
      <input
        type="text"
        value={searchQuery}
        placeholder="Search tools"
        on:input={(event) => onSearchChange(event.currentTarget.value)}
      />
    </label>
  </div>

  <div class="gc-topbar-editor__center">
    <strong title={currentFileName}>{currentFileName}</strong>
    <span class="gc-status-pill-editor">AI Engine {aiStatus}</span>
  </div>

  <div class="gc-topbar-editor__right">
    <button class="gc-icon-button" type="button" on:click={onShare}>Share</button>
    <button class="gc-icon-button" type="button" on:click={onCollage}>Collage</button>
    <button class="gc-icon-button gc-icon-button--accent" type="button" on:click={onExport}>Export</button>

    <div class="gc-user-chip">
      <span class="gc-user-chip__avatar">{userInitial}</span>
      <div>
        <strong>{userName}</strong>
        <span>{userMode}</span>
      </div>
    </div>
  </div>
</header>
