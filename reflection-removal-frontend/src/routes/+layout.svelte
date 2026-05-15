<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { initializeLanguage } from '$lib/stores/language.js';

  import 'bootstrap/dist/css/bootstrap.min.css';
  import 'bootstrap-icons/font/bootstrap-icons.css';

  // Dynamically import Bootstrap's JS only on the client-side
  onMount(async () => {
    if (browser) {
      initializeLanguage();
      await import('bootstrap/dist/js/bootstrap.bundle.min.js');
    }
  });
  // Svelte 5 way to handle layout content
  let { children } = $props();
</script>

{@render children()}
