<script>
  import { onMount } from 'svelte';

  let coords = { x: 0, y: 0 };
  let innerCoords = { x: 0, y: 0 };
  let outerCoords = { x: 0, y: 0 };
  
  let isHovering = false;
  let isResizing = false;
  let isVisible = false;
  let isMobile = false;

  // Smoothness factor (lerp)
  const lagAmount = 0.15;

  function updatePosition() {
    if (isMobile) return;

    // Inner cursor follows mouse exactly
    innerCoords.x = coords.x;
    innerCoords.y = coords.y;

    // Outer cursor lags behind (Linear Interpolation)
    outerCoords.x += (coords.x - outerCoords.x) * lagAmount;
    outerCoords.y += (coords.y - outerCoords.y) * lagAmount;

    requestAnimationFrame(updatePosition);
  }

  onMount(() => {
    // Disable on mobile/touch devices
    isMobile = window.matchMedia("(pointer: coarse)").matches;
    if (isMobile) return;

    const handleMouseMove = (e) => {
      coords.x = e.clientX;
      coords.y = e.clientY;
      if (!isVisible) isVisible = true;
    };

    const handleMouseOver = (e) => {
      const target = e.target;
      
      // Check for buttons/links
      const isClickable = target.closest('button, a, [role="button"]');
      isHovering = !!isClickable;

      // Check for image comparison slider (assuming class .comparison-slider or similar)
      const isSlider = target.closest('.comparison-slider, [data-cursor="resize"]');
      isResizing = !!isSlider;
    };

    const handleMouseLeaveWindow = () => isVisible = false;
    const handleMouseEnterWindow = () => isVisible = true;

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseover', handleMouseOver);
    document.addEventListener('mouseleave', handleMouseLeaveWindow);
    document.addEventListener('mouseenter', handleMouseEnterWindow);
    
    const animationId = requestAnimationFrame(updatePosition);

    // Hide native cursor globally when component is active
    document.body.style.cursor = 'none';

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseover', handleMouseOver);
      document.removeEventListener('mouseleave', handleMouseLeaveWindow);
      document.removeEventListener('mouseenter', handleMouseEnterWindow);
      cancelAnimationFrame(animationId);
      document.body.style.cursor = 'auto';
    };
  });
</script>

{#if !isMobile && isVisible}
  <!-- Outer Ring -->
  <div 
    class="cursor-outer" 
    class:hovering={isHovering}
    class:resizing={isResizing}
    style="transform: translate3d({outerCoords.x}px, {outerCoords.y}px, 0) translate(-50%, -50%)"
  ></div>

  <!-- Inner Dot -->
  <div 
    class="cursor-inner" 
    class:hovering={isHovering}
    class:resizing={isResizing}
    style="transform: translate3d({innerCoords.x}px, {innerCoords.y}px, 0) translate(-50%, -50%)"
  >
    {#if isResizing}
      <div class="resize-arrows"></div>
    {/if}
  </div>
{/if}

<style>
  :global(body) {
    /* Ensure fallback cursor if JS fails or on mobile */
    cursor: auto;
  }

  .cursor-inner, .cursor-outer {
    position: fixed;
    top: 0;
    left: 0;
    pointer-events: none; /* Crucial: clicks pass through */
    z-index: 9999;
    border-radius: 50%;
    transition: width 0.3s ease, height 0.3s ease, background-color 0.3s ease, border 0.3s ease, opacity 0.2s ease;
    will-change: transform;
  }

  /* Inner Dot Styling */
  .cursor-inner {
    width: 10px;
    height: 10px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
  }

  /* Outer Ring Styling */
  .cursor-outer {
    width: 28px;
    height: 28px;
    border: 1px solid rgba(99, 102, 241, 0.4);
    background: transparent;
  }

  /* Hover States (Buttons/Links) */
  .cursor-inner.hovering {
    transform: scale(1.5);
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.8);
    opacity: 0.8;
  }

  .cursor-outer.hovering {
    width: 48px;
    height: 48px;
    border: 1px solid rgba(99, 102, 241, 0.2);
    background: rgba(99, 102, 241, 0.05);
  }

  /* Image Comparison Slider State */
  .cursor-inner.resizing {
    width: 4px;
    height: 24px;
    border-radius: 2px;
    background: #fff;
  }

  .cursor-outer.resizing {
    width: 40px;
    height: 40px;
    border: 2px solid #fff;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(2px);
  }

  :global(a, button, [role="button"]) {
    cursor: none !important;
  }
</style>
