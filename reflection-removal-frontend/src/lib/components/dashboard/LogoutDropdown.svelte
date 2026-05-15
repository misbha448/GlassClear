<svelte:options runes={false} />

<script>
  export let userName = 'User';
  export let userInitial = 'U';
  export let logoutLabel = 'Logout';
  export let onLogout = () => {};

  let open = false;

  function toggle() {
    open = !open;
  }

  function handleOutside(event) {
    if (!event.currentTarget.contains(event.relatedTarget)) {
      open = false;
    }
  }
</script>

<div class="gc-logout" onfocusout={handleOutside}>
  <button type="button" class="gc-logout__trigger" onclick={toggle} aria-expanded={open}>
    <span class="gc-logout__avatar">{userInitial}</span>
    <span class="gc-logout__name">{userName}</span>
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="m7 10 5 5 5-5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
  </button>

  {#if open}
    <div class="gc-logout__menu">
      <button
        type="button"
        class="gc-logout__action"
        onclick={() => {
          open = false;
          onLogout();
        }}
      >
        {logoutLabel}
      </button>
    </div>
  {/if}
</div>
