<script>
  import { onMount } from 'svelte';

  let errorMessage = $state('');

  onMount(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    const tokenType = params.get('token_type') || 'bearer';
    const role = params.get('role') || 'user';
    const userName = params.get('user_name');

    if (!token) {
      errorMessage = 'Google sign-in could not be completed.';
      setTimeout(() => {
        window.location.href = '/login?error=' + encodeURIComponent(errorMessage);
      }, 1200);
      return;
    }

    localStorage.setItem('token', token);
    localStorage.setItem('token_type', tokenType);
    localStorage.setItem('role', role);
    if (userName) {
      localStorage.setItem('user_name', userName);
    }

    window.location.href = role === 'admin' ? '/admin/dashboard' : '/dashboard';
  });
</script>

<div class="gc-auth-callback">
  <div class="gc-auth-callback__card">
    <h1>Signing you in...</h1>
    <p>{errorMessage || 'Finalizing your GlassClear workspace.'}</p>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    min-height: 100vh;
    background: #05050a;
    color: #f4f7ff;
    font-family: 'DM Sans', 'Sora', sans-serif;
  }

  .gc-auth-callback {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 24px;
  }

  .gc-auth-callback__card {
    width: min(420px, 100%);
    padding: 32px;
    border-radius: 20px;
    background: rgba(20, 20, 32, 0.92);
    border: 1px solid rgba(124, 58, 237, 0.24);
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.35);
    text-align: center;
  }

  h1 {
    margin: 0 0 12px;
    font-size: 28px;
  }

  p {
    margin: 0;
    color: rgba(226, 224, 234, 0.7);
    line-height: 1.6;
  }
</style>
