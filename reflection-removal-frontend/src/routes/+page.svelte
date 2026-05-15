<script>
  import { onMount } from 'svelte';
  import Navbar from '$lib/components/Navbar.svelte';
  import ImageCompare from '$lib/components/ImageCompare.svelte';
  import Chatbot from '$lib/components/Chatbot.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import ProcessingScreen from '$lib/components/ProcessingScreen.svelte';
  import ResultDisplay from '$lib/components/ResultDisplay.svelte';
  import UnlockResultModal from '$lib/components/UnlockResultModal.svelte';
  import { t } from '$lib/state.svelte.js';
  import { savePendingGuestImage } from '$lib/utils/pendingGuestImage.js';
  import { API_BASE, apiFetch, getStoredToken } from '$lib/api/api.js';

  let selectedFile = $state(null);
  let previewUrl = $state(null);
  let resultUrl = $state(null);
  let processing = $state(false);
  let progress = $state(0);
  let showResults = $state(false);
  let error = $state("");
  let fileInput = $state(null);
  let selectedMode = $state("Quality");
  let selectedFormat = $state("PNG");
  let downloadFilename = $state("");
  let imageMeta = $state({ resolution: "---", size: "---" });
  let isDragging = $state(false);

  let predictionId = $state(null);
  let guestOriginalUrl = $state(null);
  let guestToken = $state(null);
  let unlockModalOpen = $state(false);
  let aiMode = $state({ selected_mode: "fidelity", reason: "Analyzing..." });
  let confidenceMap = $state(null);
  let ssim = $state(0.0);
  let edgeScore = $state(0.0);
  let intermediateOutputs = $state([]);
  let processingSteps = $state([]);
  let activeCarouselIndex = $state(0);

  function reset() {
    selectedFile = null;
    previewUrl = null;
    showResults = false;
    predictionId = null;
    error = "";
  }

  function triggerChange() {
    if (fileInput) {
      fileInput.value = "";
      fileInput.click();
    }
  }

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (file) {
      selectedFile = file;
      previewUrl = URL.createObjectURL(file);
      resultUrl = null;
      showResults = false;
      error = "";
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    isDragging = false;
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      selectedFile = file;
      previewUrl = URL.createObjectURL(file);
      resultUrl = null;
      showResults = false;
      error = "";
    }
  }

  function handleDragOver(e) {
    e.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  $effect(() => {
    if (resultUrl && showResults) {
      const img = new Image();
      img.onload = () => { imageMeta.resolution = `${img.width}x${img.height}`; };
      img.src = resultUrl;
      fetch(resultUrl, { method: 'HEAD' }).then(res => {
        const bytes = res.headers.get('content-length');
        if (bytes) imageMeta.size = (bytes / (1024 * 1024)).toFixed(2) + " MB";
      });
    }
  });

  async function uploadAndProcess() {
    if (!selectedFile) return;
    processing = true;
    error = "";
    progress = 20;

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('mode', selectedMode === 'Quality' ? 'enhanced' : 'clean');
    formData.append('output_format', selectedFormat.toLowerCase());

    try {
      const response = await apiFetch(`/process-image`, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.detail || data?.message || t('upload_error_engine'));
      }
      if (data.processing_required === false) {
        resultUrl = null;
        showResults = false;
        predictionId = null;
        guestOriginalUrl = null;
        guestToken = null;
        confidenceMap = null;
        aiMode = { selected_mode: "fidelity", reason: "Analyzing..." };
        ssim = 0.0;
        edgeScore = 0.0;
        intermediateOutputs = [];
        processingSteps = [];
        progress = 0;
        error = data.message || 'No reflection detected. Processing not required.';
        processing = false;
        return;
      }
      predictionId = data.prediction_id;
      guestOriginalUrl = `${API_BASE}${data.original_image_url}`;
      resultUrl = `${API_BASE}${data.processed_image_url}`;
      downloadFilename = data.download_filename || "";
      guestToken = data.guest_image_token || null;
      confidenceMap = `${API_BASE}${data.confidence_map_url}`;
      aiMode = { selected_mode: data.selected_mode, reason: data.reason };
      ssim = data.ssim;
      edgeScore = data.edge_score;
      intermediateOutputs = (data.intermediate_outputs || []).map(path => `${API_BASE}${path}`);
      processingSteps = data.processing_steps || [];
      progress = 100;
      setTimeout(() => { showResults = true; processing = false; }, 600);
    } catch (err) {
      error = err.message || t('upload_error_engine');
      processing = false;
    }
  }

  function storePendingGuestResult() {
    savePendingGuestImage({
      guest_original_url: guestOriginalUrl || previewUrl,
      guest_processed_url: resultUrl,
      guest_filename: downloadFilename || selectedFile?.name || 'glassclear-result.png',
      guest_image_id: predictionId,
      guest_image_token: guestToken
    });
  }

  async function downloadImage(format = selectedFormat.toLowerCase()) {
    const isAuthenticated = Boolean(getStoredToken());

    if (!isAuthenticated) {
      storePendingGuestResult();
      unlockModalOpen = true;
      return;
    }

    try {
      const response = await fetch(resultUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const fallbackName = `GC_${Date.now()}.${format}`;
      link.setAttribute('download', downloadFilename || fallbackName);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      error = t('upload_error_download');
    }
  }

  function continueToLogin() {
    storePendingGuestResult();
    window.location.href = '/login';
  }

  function continueToSignup() {
    storePendingGuestResult();
    window.location.href = '/signup';
  }

  const carouselSlides = [
    { src: "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=900&q=85", titleKey: 'landing.carousel.slide1.title', subtitleKey: 'landing.carousel.slide1.subtitle' },
    { src: "https://images.unsplash.com/photo-1555099962-4199c345e5dd?w=900&q=85", titleKey: 'landing.carousel.slide2.title', subtitleKey: 'landing.carousel.slide2.subtitle' },
    { src: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=900&q=85", titleKey: 'landing.carousel.slide3.title', subtitleKey: 'landing.carousel.slide3.subtitle' },
    { src: "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?w=900&q=85", titleKey: 'landing.carousel.slide4.title', subtitleKey: 'landing.carousel.slide4.subtitle' },
    { src: "https://images.unsplash.com/photo-1464983953574-0892a716854b?w=900&q=85", titleKey: 'landing.carousel.slide5.title', subtitleKey: 'landing.carousel.slide5.subtitle' },
    { src: "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=900&q=85", titleKey: 'landing.carousel.slide6.title', subtitleKey: 'landing.carousel.slide6.subtitle' },
  ];

  const testimonials = [
    { quote: "GlassClear literally saved my architectural shots. Reflections were ruining everything, and this fixed it in seconds.", name: "Arjun Mehta", role: "Architectural Photographer", avatar: "https://randomuser.me/api/portraits/men/32.jpg" },
    { quote: "The AI is insanely accurate. It removes reflections without touching the original details. That's rare.", name: "Sophia Chen", role: "Visual Designer", avatar: "https://randomuser.me/api/portraits/women/44.jpg" },
    { quote: "I used to spend hours in Photoshop. Now it's literally one click. Game changer.", name: "Rohit Sharma", role: "Real Estate Editor", avatar: "https://randomuser.me/api/portraits/men/55.jpg" },
    { quote: "What impressed me most is how natural the output looks. No artifacts, no weird patches.", name: "Emily Carter", role: "Content Creator", avatar: "https://randomuser.me/api/portraits/women/68.jpg" },
    { quote: "The reflection removal is not just good â€” it's smart. It understands the scene.", name: "Daniel Kim", role: "AI Research Student", avatar: "https://randomuser.me/api/portraits/men/12.jpg" },
    { quote: "Clean UI, fast processing, and crazy accurate results. This feels like a premium tool.", name: "Neha Verma", role: "Product Designer", avatar: "https://randomuser.me/api/portraits/women/25.jpg" },
    { quote: "Tried multiple tools, but GlassClear gives the most consistent results across different lighting conditions.", name: "Liam Walker", role: "Freelance Photographer", avatar: "https://randomuser.me/api/portraits/men/41.jpg" },
    { quote: "The confidence score + AI insights actually make me trust the output more.", name: "Aisha Khan", role: "UX Researcher", avatar: "https://randomuser.me/api/portraits/women/36.jpg" },
    { quote: "It doesn't just remove reflections, it restores the image. That's the difference.", name: "Karan Patel", role: "Media Editor", avatar: "https://randomuser.me/api/portraits/men/29.jpg" },
    { quote: "I love how fast everything is. Upload â†’ Process â†’ Done. No friction at all.", name: "Olivia Brown", role: "Digital Marketer", avatar: "https://randomuser.me/api/portraits/women/52.jpg" },
    { quote: "The AI Story feature is surprisingly useful. It explains what actually happened in the image.", name: "Aditya Singh", role: "Student Developer", avatar: "https://randomuser.me/api/portraits/men/23.jpg" },
    { quote: "Feels like something Apple would build if they worked on image clarity tools.", name: "Lucas Martin", role: "Creative Director", avatar: "https://randomuser.me/api/portraits/men/77.jpg" }
  ];

  const localizedTestimonials = [
    { quoteKey: 'landing.testimonials.1.quote', name: "Arjun Mehta", roleKey: 'landing.testimonials.1.role', avatar: "https://randomuser.me/api/portraits/men/32.jpg" },
    { quoteKey: 'landing.testimonials.2.quote', name: "Sophia Chen", roleKey: 'landing.testimonials.2.role', avatar: "https://randomuser.me/api/portraits/women/44.jpg" },
    { quoteKey: 'landing.testimonials.3.quote', name: "Rohit Sharma", roleKey: 'landing.testimonials.3.role', avatar: "https://randomuser.me/api/portraits/men/55.jpg" },
    { quoteKey: 'landing.testimonials.4.quote', name: "Emily Carter", roleKey: 'landing.testimonials.4.role', avatar: "https://randomuser.me/api/portraits/women/68.jpg" },
    { quoteKey: 'landing.testimonials.5.quote', name: "Daniel Kim", roleKey: 'landing.testimonials.5.role', avatar: "https://randomuser.me/api/portraits/men/12.jpg" },
    { quoteKey: 'landing.testimonials.6.quote', name: "Neha Verma", roleKey: 'landing.testimonials.6.role', avatar: "https://randomuser.me/api/portraits/women/25.jpg" },
    { quoteKey: 'landing.testimonials.7.quote', name: "Liam Walker", roleKey: 'landing.testimonials.7.role', avatar: "https://randomuser.me/api/portraits/men/41.jpg" },
    { quoteKey: 'landing.testimonials.8.quote', name: "Aisha Khan", roleKey: 'landing.testimonials.8.role', avatar: "https://randomuser.me/api/portraits/women/36.jpg" },
    { quoteKey: 'landing.testimonials.9.quote', name: "Karan Patel", roleKey: 'landing.testimonials.9.role', avatar: "https://randomuser.me/api/portraits/men/29.jpg" },
    { quoteKey: 'landing.testimonials.10.quote', name: "Olivia Brown", roleKey: 'landing.testimonials.10.role', avatar: "https://randomuser.me/api/portraits/women/52.jpg" },
    { quoteKey: 'landing.testimonials.11.quote', name: "Aditya Singh", roleKey: 'landing.testimonials.11.role', avatar: "https://randomuser.me/api/portraits/men/23.jpg" },
    { quoteKey: 'landing.testimonials.12.quote', name: "Lucas Martin", roleKey: 'landing.testimonials.12.role', avatar: "https://randomuser.me/api/portraits/men/77.jpg" }
  ];

  const tcol1 = localizedTestimonials.slice(0, 4);
  const tcol2 = localizedTestimonials.slice(4, 8);
  const tcol3 = localizedTestimonials.slice(8, 12);

  const faqs = [
    { q: "What is GlassClear?", a: "GlassClear is an AI-powered reflection removal system designed for architectural photography. It helps remove glare, window reflections, and glass surface artifacts from images while preserving building details and visual clarity." },
    { q: "Do I need technical skills to use it?", a: "No. You only need to upload an image, let the AI process it, and download the restored result. The dashboard also provides history, sharing, batch processing, and smart album features for logged-in users." },
    { q: "What type of images work best?", a: "GlassClear works best with architectural photos, glass facades, windows, interiors, real estate images, and outdoor building shots affected by glare or reflection." },
    { q: "Can I process multiple images at once?", a: "Yes. Logged-in users can use batch processing to upload multiple images together. To keep processing stable, the batch limit is controlled and images are processed safely one by one." },
    { q: "Will image quality improve after removal?", a: "GlassClear focuses on reducing reflections while keeping architectural lines, textures, and details natural. Optional quality enhancement can be added after reflection removal for cleaner final output." },
    { q: "Is my data secure?", a: "Uploaded images are connected to the user account and can be accessed only by the logged-in user. Shared links are generated only when the user chooses to share a result." }
  ];

  const localizedFaqs = [
    { qKey: 'landing.faq.1.question', aKey: 'landing.faq.1.answer' },
    { qKey: 'landing.faq.2.question', aKey: 'landing.faq.2.answer' },
    { qKey: 'landing.faq.3.question', aKey: 'landing.faq.3.answer' },
    { qKey: 'landing.faq.4.question', aKey: 'landing.faq.4.answer' },
    { qKey: 'landing.faq.5.question', aKey: 'landing.faq.5.answer' },
    { qKey: 'landing.faq.6.question', aKey: 'landing.faq.6.answer' }
  ];

  let faqActiveIndex = $state(3);

  function toggleFaq(index) {
    faqActiveIndex = faqActiveIndex === index ? null : index;
  }

  let pipelineActiveIdx = $state(2);

  const localizedPipelineSteps = [
    { icon: "Ã°Å¸â€Â", labelKey: 'landing.pipeline.detection' },
    { icon: "Ã°Å¸Å’Â", labelKey: 'landing.pipeline.mapping' },
    { icon: "Ã¢Å¡Â¡", labelKey: 'landing.pipeline.separation' },
    { icon: "Ã°Å¸Â§Â©", labelKey: 'landing.pipeline.recovery' },
    { icon: "Ã¢Å“Â¨", labelKey: 'landing.pipeline.reconstruction' },
  ];

  const pipelineSteps = [
    { icon: "ðŸ”", label: "Reflection Detection" },
    { icon: "ðŸŒ", label: "Glare Mapping" },
    { icon: "âš¡", label: "Layer Separation" },
    { icon: "ðŸ§©", label: "Texture Recovery" },
    { icon: "âœ¨", label: "Final Reconstruction" },
  ];

  onMount(() => {
    // â”€â”€ Carousel logic â”€â”€
    const track       = document.getElementById('carouselTrack');
    const dotsEl      = document.getElementById('carouselDots');
    const progressBar = document.getElementById('progressBar');
    const wrapper     = document.getElementById('carouselWrapper');

    if (!track || !dotsEl) return;

    const N = carouselSlides.length;
    let currentIdx  = 0;
    let isAnimating = false;
    const AUTO_DELAY = 4000;
    const TICK = 50;
    let autoTimer     = null;
    let progressTimer = null;
    let progressVal   = 0;

    const POS_CLASSES = ['pos-center','pos-left','pos-right','pos-far-left','pos-far-right','pos-hidden'];

    const slideEls = carouselSlides.map((data, i) => {
      const el = document.createElement('div');
      el.className = 'slide-gc';
      el.innerHTML = `
        <img src="${data.src}" alt="${data.title}" loading="lazy" draggable="false" />
        <div class="slide-shine-gc"></div>
        <div class="slide-gradient-gc"></div>
        <div class="slide-border-gc"></div>
      `;
      el.addEventListener('click', () => { if (!isAnimating && i !== currentIdx) goTo(i); });
      track.appendChild(el);
      return el;
    });

    const dotEls = carouselSlides.map((_, i) => {
      const d = document.createElement('div');
      d.className = 'dot-gc' + (i === 0 ? ' active' : '');
      d.addEventListener('click', () => { if (!isAnimating) goTo(i); });
      dotsEl.appendChild(d);
      return d;
    });

    function getPositionClass(slideIdx) {
      const diff = ((slideIdx - currentIdx) % N + N) % N;
      if (diff === 0)     return 'pos-center';
      if (diff === 1)     return 'pos-right';
      if (diff === N - 1) return 'pos-left';
      if (diff === 2)     return 'pos-far-right';
      if (diff === N - 2) return 'pos-far-left';
      return 'pos-hidden';
    }

    function render() {
      slideEls.forEach((el, i) => {
        POS_CLASSES.forEach(c => el.classList.remove(c));
        el.classList.add(getPositionClass(i));
      });
      dotEls.forEach((d, i) => d.classList.toggle('active', i === currentIdx));
    }

    function goTo(idx) {
      if (idx === currentIdx) return;
      isAnimating = true;
      currentIdx  = ((idx % N) + N) % N;
      activeCarouselIndex = currentIdx;
      render();
      resetProgress();
      setTimeout(() => { isAnimating = false; }, 560);
    }

    function next() { goTo((currentIdx + 1) % N); }
    function prev() { goTo((currentIdx - 1 + N) % N); }

    document.getElementById('prevBtn').addEventListener('click', () => { if (!isAnimating) prev(); });
    document.getElementById('nextBtn').addEventListener('click', () => { if (!isAnimating) next(); });

    function resetProgress() {
      progressVal = 0;
      if (progressBar) progressBar.style.width = '0%';
    }

    function startAuto() {
      stopAuto();
      resetProgress();
      progressTimer = setInterval(() => {
        progressVal += (TICK / AUTO_DELAY) * 100;
        if (progressBar) progressBar.style.width = Math.min(progressVal, 100) + '%';
      }, TICK);
      autoTimer = setInterval(() => { if (!isAnimating) { next(); resetProgress(); } }, AUTO_DELAY);
    }

    function stopAuto() {
      clearInterval(autoTimer);
      clearInterval(progressTimer);
    }

    wrapper.addEventListener('mouseenter', stopAuto);
    wrapper.addEventListener('mouseleave', startAuto);

    let touchStartX = 0;
    let touchStartTime = 0;
    wrapper.addEventListener('touchstart', e => {
      touchStartX    = e.touches[0].clientX;
      touchStartTime = Date.now();
      stopAuto();
    }, { passive: true });
    wrapper.addEventListener('touchend', e => {
      const dx      = e.changedTouches[0].clientX - touchStartX;
      const elapsed = Date.now() - touchStartTime;
      if (elapsed < 400 && Math.abs(dx) > 40) { if (!isAnimating) { dx < 0 ? next() : prev(); } }
      startAuto();
    }, { passive: true });

    render();
    activeCarouselIndex = currentIdx;
    startAuto();

    // â”€â”€ AI Pipeline cycling â”€â”€
    const pipelineTimer = setInterval(() => {
      pipelineActiveIdx = (pipelineActiveIdx + 1) % 5;
    }, 3200);

    // â”€â”€ How It Works scroll reveal â€” force visible immediately â”€â”€
    const hiwHeader  = document.querySelector('.hiw-header');
    const hiwDivider = document.querySelector('.hiw-divider');
    const hiwSteps   = document.querySelectorAll('.hiw-step');
    const hiwArrows  = document.querySelectorAll('.hiw-arrow-wrap');

    function forceHiwVisible() {
      if (hiwHeader) hiwHeader.classList.add('visible');
      if (hiwDivider) hiwDivider.classList.add('visible');
      hiwSteps.forEach(el => el.classList.add('visible'));
      hiwArrows.forEach(el => el.classList.add('visible'));
    }

    const hiwObserver = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          hiwObserver.unobserve(e.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px 60px 0px' });

    [hiwHeader, hiwDivider, ...hiwSteps, ...hiwArrows].forEach(el => {
      if (el) hiwObserver.observe(el);
    });

    setTimeout(forceHiwVisible, 400);

    // â”€â”€ Feature showcase scroll-reveal â”€â”€
    const showcaseRows = document.querySelectorAll('[data-reveal]');
    const rowObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const row = entry.target;
        row.classList.add('revealed');
        const panel = row.querySelector('[data-panel]');
        if (panel) setTimeout(() => panel.classList.add('panel-in'), 260);
        const rowItems = row.querySelectorAll('[data-item]');
        rowItems.forEach((item, i) => {
          setTimeout(() => item.classList.add('item-in'), 400 + i * 110);
        });
        const rowFills = row.querySelectorAll('.item-progress-fill');
        rowFills.forEach(fill => {
          setTimeout(() => fill.classList.add('fill-in'), 680);
        });
        rowObserver.unobserve(row);
      });
    }, { threshold: 0.15 });
    showcaseRows.forEach(row => rowObserver.observe(row));

    // â”€â”€ NEW: Restoration Summary bar animation â”€â”€
    const summaryBars = document.querySelectorAll('.gc-summary-stat__bar-fill');
    const barObserver = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          setTimeout(() => e.target.classList.add('gc-bar--ready'), 600);
          barObserver.unobserve(e.target);
        }
      });
    }, { threshold: 0.2 });
    summaryBars.forEach(b => barObserver.observe(b));

    // â”€â”€ NEW: Active queue icon pulse â”€â”€
    const activeIcon = document.querySelector('.gc-queue-row--active .gc-queue-row__icon');
    if (activeIcon) {
      let on = false;
      setInterval(() => {
        on = !on;
        activeIcon.style.boxShadow = on
          ? '0 0 0 6px rgba(99,102,241,0.18), 0 4px 12px rgba(99,102,241,0.30)'
          : '0 4px 12px rgba(99,102,241,0.30)';
      }, 900);
    }

    // â”€â”€ Task row stagger for card 1 (kept for any legacy usage) â”€â”€
    const taskRows = ['gc-tr1','gc-tr2','gc-tr3','gc-tr4'];
    function animateGcTasks() {
      taskRows.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('show');
      });
      taskRows.forEach((id, i) => {
        setTimeout(() => {
          const el = document.getElementById(id);
          if (el) el.classList.add('show');
        }, 400 + i * 350);
      });
    }
    setTimeout(animateGcTasks, 800);
    setInterval(animateGcTasks, 6000);

    return () => {
      stopAuto();
      clearInterval(pipelineTimer);
    };
  });
</script>

<div class="page-wrapper">
  <Navbar />

  <div class="content-area">
    {#if !showResults}

      <!-- â•â•â•â•â•â•â•â•â•â• HERO â•â•â•â•â•â•â•â•â•â• -->
      <section class="gc-hero" id="upload">
        <!-- Background effects -->
        <div class="gc-hero-bg" aria-hidden="true">
          <div class="gc-orb gc-orb-1"></div>
          <div class="gc-orb gc-orb-2"></div>
          <div class="gc-orb gc-orb-3"></div>
          <div class="gc-grid-overlay"></div>
          <div class="gc-hero-beam"></div>
          <div class="gc-hero-particles">
            <span class="gc-particle p1"></span>
            <span class="gc-particle p2"></span>
            <span class="gc-particle p3"></span>
            <span class="gc-particle p4"></span>
            <span class="gc-particle p5"></span>
            <span class="gc-particle p6"></span>
          </div>
        </div>

        <div class="gc-hero-inner">
          <!-- Pill badge -->
          <div class="gc-hero-pill">
            <span class="gc-pill-dot"></span>
            {t('landing.hero.badge')}
          </div>

          <!-- â”€â”€ UPDATED HERO TITLE â”€â”€ -->
          <h1 class="gc-hero-title">
            <span class="gc-title-reveal gc-line-1">
              <span class="gc-title-text">{t('landing.hero.titleLine1')}</span>
            </span>
            <span class="gc-title-reveal gc-line-2">
              <span class="gc-title-text gc-gradient-text">{t('landing.hero.titleLine2')}</span>
            </span>
            <span class="gc-title-reveal gc-line-sub">
              <span class="gc-title-text gc-title-sub-text">{t('landing.hero.titleLine3')}</span>
            </span>
          </h1>

          <!-- Description -->
          <p class="gc-hero-desc">
            {t('landing.hero.subtitleLine1')}<br />
            {t('landing.hero.subtitleLine2')}
          </p>

          <!-- Upload zone -->
          <div
            class="gc-upload-card {isDragging ? 'gc-dragging' : ''} {selectedFile ? 'gc-has-file' : ''}"
            ondrop={handleDrop}
            ondragover={handleDragOver}
            ondragleave={handleDragLeave}
            role="button"
            tabindex="0"
          >
            <input
              type="file"
              bind:this={fileInput}
              accept="image/*"
              class="gc-file-input"
              onchange={handleFileChange}
            />

            {#if !selectedFile}
              <div class="gc-upload-idle">
                <div class="gc-upload-icon-wrap">
                  <div class="gc-upload-icon-ring gc-ring-outer"></div>
                  <div class="gc-upload-icon-ring gc-ring-inner"></div>
                  <div class="gc-upload-icon-badge">
                    <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
                      <path d="M24 32V18M17 25l7-7 7 7" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M15 36h18" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                  </div>
                </div>
                <p class="gc-upload-title">{t('landing.upload.drop')}</p>
                <p class="gc-upload-hint">
                  or <button class="gc-browse-btn" onclick={triggerChange}>{t('landing.upload.browse')}</button>
                  &middot; {t('landing.upload.hint')}
                </p>
                <div class="gc-fmt-chips">
                  <span class="gc-fmt-chip">JPG</span>
                  <span class="gc-fmt-chip">PNG</span>
                  <span class="gc-fmt-chip">WEBP</span>
                  <span class="gc-fmt-chip">up to 50 MB</span>
                </div>
              </div>
            {:else if !processing}
              <div class="gc-upload-preview">
                <img src={previewUrl} alt="Preview" class="gc-preview-img" />
                <button class="gc-change-btn" onclick={triggerChange}>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  {t('processing.changeImage')}
                </button>
              </div>
            {/if}

            <!-- Corner accents -->
            <span class="gc-corner gc-tl"></span>
            <span class="gc-corner gc-tr"></span>
            <span class="gc-corner gc-bl"></span>
            <span class="gc-corner gc-br"></span>
          </div>

          <!-- CTA button -->
          {#if selectedFile && !processing}
            <button class="gc-cta-btn" onclick={uploadAndProcess}>
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              {t('landing.hero.cta')}
            </button>
          {/if}

          {#if processing}
            <ProcessingScreen
              originalSrc={previewUrl}
              processedSrc={resultUrl}
              title={t('processing.title')}
              subtitle={t('processing.subtitle')}
              onChangeImage={triggerChange}
            />
          {/if}

          {#if error}
            <div class="gc-error-msg">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {error}
            </div>
          {/if}
        </div>
      </section>

      <!-- â•â•â•â•â•â•â•â•â•â• HOW IT WORKS â•â•â•â•â•â•â•â•â•â• -->
      <section class="how-it-works" id="how-it-works">
        <div class="hiw-container">

          <div class="hiw-header visible">
            <span class="hiw-label">{t('landing.how.label')}</span>
            <h2 class="hiw-heading">{t('landing.how.title')}</h2>
            <div class="hiw-divider visible"></div>
            <p class="hiw-sub">{t('landing.how.subtitle')}</p>
          </div>

          <div class="hiw-steps">

            <div class="hiw-step visible">
              <div class="hiw-step-inner">
                <span class="hiw-number">1</span>
                <h3 class="hiw-step-title">{t('landing.how.step1.title')}</h3>
                <p class="hiw-step-desc">{t('landing.how.step1.desc')}</p>
                <p class="hiw-step-note">{t('landing.how.step1.note')}</p>
              </div>
            </div>

            <div class="hiw-arrow-wrap visible">
              <svg class="hiw-arrow" viewBox="0 0 200 90" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path class="hiw-arrow-path" d="M 12 58 C 28 18, 68 10, 78 42 C 88 72, 50 74, 62 48 C 74 22, 118 14, 160 38" stroke="#6366f1" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                <path class="hiw-arrow-head" d="M 148 22 L 164 40 L 144 48" stroke="#6366f1" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
              </svg>
            </div>

            <div class="hiw-step visible">
              <div class="hiw-step-inner">
                <span class="hiw-number">2</span>
                <h3 class="hiw-step-title">{t('landing.how.step2.title')}</h3>
                <p class="hiw-step-desc">{t('landing.how.step2.desc')}</p>
                <p class="hiw-step-note">{t('landing.how.step2.note')}</p>
              </div>
            </div>

            <div class="hiw-arrow-wrap visible">
              <svg class="hiw-arrow" viewBox="0 0 200 90" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path class="hiw-arrow-path" d="M 12 58 C 28 18, 68 10, 78 42 C 88 72, 50 74, 62 48 C 74 22, 118 14, 160 38" stroke="#6366f1" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                <path class="hiw-arrow-head" d="M 148 22 L 164 40 L 144 48" stroke="#6366f1" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
              </svg>
            </div>

            <div class="hiw-step visible">
              <div class="hiw-step-inner">
                <span class="hiw-number">3</span>
                <h3 class="hiw-step-title">{t('landing.how.step3.title')}</h3>
                <p class="hiw-step-desc">{t('landing.how.step3.desc')}</p>
                <p class="hiw-step-note">{t('landing.how.step3.note')}</p>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
           FEATURE SHOWCASE
      â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
      <section class="gc-showcase-section">
        <div class="gc-showcase-container">

          <div class="gc-row row-a" data-reveal>
            <div class="gc-visual">
              <img class="gc-img" src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80" alt="Modern glass building facade" loading="lazy" />
              <div class="gc-img-overlay"></div>
              <div class="gc-panel panel-bottom-left" data-panel>
                <div class="panel-header">
                  <div class="panel-title-wrap">
                    <div class="panel-accent-bar"></div>
                    <span class="panel-title">{t('landing.showcase.workspace.panelTitle')}</span>
                  </div>
                  <div class="panel-icon">
                    <svg fill="none" viewBox="0 0 16 16" stroke="currentColor" stroke-width="1.8" color="#6366f1">
                      <circle cx="7" cy="7" r="5.25"/><path d="M12.5 12.5l2 2" stroke-linecap="round"/>
                    </svg>
                  </div>
                </div>
                <div class="panel-item" data-item>
                  <div class="item-icon icon-purple">ðŸ¢</div>
                  <div class="item-body">
                    <div class="item-name">{t('landing.showcase.workspace.item1Name')}</div>
                    <div class="item-sub">{t('landing.showcase.workspace.statusDone')}</div>
                  </div>
                  <span class="item-status status-done">96%</span>
                </div>
                <div class="panel-item" data-item>
                  <div class="item-icon icon-blue">ðŸªŸ</div>
                  <div class="item-body">
                    <div class="item-name">{t('landing.showcase.workspace.item2Name')}</div>
                    <div class="item-sub">{t('landing.showcase.workspace.statusProcessing')}</div>
                  </div>
                  <div class="item-progress-wrap">
                    <div class="item-progress-bar">
                      <div class="item-progress-fill" style="--fill-w:64%"></div>
                    </div>
                    <span class="item-progress-pct">64%</span>
                  </div>
                </div>
                <div class="panel-item" data-item>
                  <div class="item-icon icon-sky">ðŸ™</div>
                  <div class="item-body">
                    <div class="item-name">{t('landing.showcase.workspace.item3Name')}</div>
                    <div class="item-sub">{t('landing.showcase.workspace.statusQueued')}</div>
                  </div>
                    <span class="item-status status-queued">{t('landing.showcase.workspace.badgeQueued')}</span>
                </div>
                <div class="panel-item" data-item>
                  <div class="item-icon icon-amber">âœ¨</div>
                  <div class="item-body">
                    <div class="item-name">{t('landing.showcase.workspace.item4Name')}</div>
                    <div class="item-sub">{t('landing.showcase.workspace.statusReady')}</div>
                  </div>
                    <span class="item-status status-ready">{t('landing.showcase.workspace.badgeReady')}</span>
                </div>
              </div>
            </div>
            <div class="gc-text">
              <span class="text-label"><span class="label-dot"></span>{t('landing.showcase.workspace.label')}</span>
              <h2 class="gc-heading">{t('landing.showcase.workspace.titleLine1')} <em>{t('landing.showcase.workspace.titleEmphasis')}</em> {t('landing.showcase.workspace.titleLine2')}</h2>
              <p class="gc-para">{t('landing.showcase.workspace.body')}</p>
              <a class="gc-btn" href="#upload">
                {t('landing.showcase.workspace.cta')}
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
              </a>
            </div>
          </div>

          <div class="gc-row row-b" data-reveal>
            <div class="gc-text">
              <span class="text-label"><span class="label-dot"></span>{t('landing.showcase.albums.label')}</span>
              <h2 class="gc-heading">{t('landing.showcase.albums.titleLine1')} <em>{t('landing.showcase.albums.titleEmphasis')}</em></h2>
              <p class="gc-para">{t('landing.showcase.albums.body')}</p>
              <a class="gc-btn" href="#smart-albums">
                {t('landing.showcase.albums.cta')}
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
              </a>
            </div>
            <div class="gc-visual">
              <img class="gc-img" src="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=80" alt="Luxury architectural interior" loading="lazy" />
              <div class="gc-img-overlay"></div>
              <div class="gc-panel panel-bottom-right" data-panel>
                <div class="panel-header">
                  <div class="panel-title-wrap">
                    <div class="panel-accent-bar"></div>
                    <span class="panel-title">{t('landing.showcase.albums.panelTitle')}</span>
                  </div>
                  <div class="panel-icon">
                    <svg fill="none" viewBox="0 0 16 16" stroke="currentColor" stroke-width="1.8" color="#6366f1">
                      <rect x="1.5" y="3.5" width="13" height="10" rx="2"/>
                      <path d="M5 3.5V2M11 3.5V2" stroke-linecap="round"/>
                    </svg>
                  </div>
                </div>
                <div class="panel-item" data-item>
                  <div class="item-icon icon-blue">ðŸ›</div>
                  <div class="item-body">
                    <div class="item-name">{t('landing.showcase.albums.item1Name')}</div>
                    <div class="item-sub">{t('landing.showcase.albums.latestPrefix')}: facade-glass-01.jpg</div>
                  </div>
                  <span class="item-count">12 {t('landing.showcase.albums.images')}</span>
                </div>
                <div class="panel-item" data-item>
                  <div class="item-icon icon-purple">ðŸªž</div>
                  <div class="item-body">
                    <div class="item-name">{t('landing.showcase.albums.item2Name')}</div>
                    <div class="item-sub">{t('landing.showcase.albums.latestPrefix')}: lobby-window-02.jpg</div>
                  </div>
                  <span class="item-count">8 {t('landing.showcase.albums.images')}</span>
                </div>
                <div class="panel-item" data-item>
                  <div class="item-icon icon-green">ðŸŒ¿</div>
                  <div class="item-body">
                    <div class="item-name">{t('landing.showcase.albums.item3Name')}</div>
                    <div class="item-sub">{t('landing.showcase.albums.latestPrefix')}: tower-exterior-03.jpg</div>
                  </div>
                  <span class="item-count">15 {t('landing.showcase.albums.images')}</span>
                </div>
                <div class="panel-item" data-item>
                  <div class="item-icon icon-amber">â˜€ï¸</div>
                  <div class="item-body">
                    <div class="item-name">{t('landing.showcase.albums.item4Name')}</div>
                    <div class="item-sub">{t('landing.showcase.albums.latestPrefix')}: interior-glass-04.jpg</div>
                  </div>
                  <span class="item-count">5 {t('landing.showcase.albums.images')}</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- â•â•â•â•â•â•â•â•â•â• CAROUSEL â•â•â•â•â•â•â•â•â•â• -->
      <section class="section carousel-section" id="demo">
        <div class="container">
          <div class="section-label">{t('landing.carousel.label')}</div>
          <h2 class="section-title">{t('landing.carousel.title')}</h2>
          <p class="section-desc">{t('landing.carousel.subtitle')}</p>
        </div>

        <div class="carousel-wrapper-gc" id="carouselWrapper">
          <div class="carousel-stage-gc">
            <div class="carousel-track-gc" id="carouselTrack"></div>
            <button class="nav-btn-gc nav-prev-gc" id="prevBtn" aria-label={t('landing.carousel.previous')}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <button class="nav-btn-gc nav-next-gc" id="nextBtn" aria-label={t('landing.carousel.next')}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
          <div class="carousel-caption-gc">
            <div class="caption-title-gc" id="captionTitle">{t(carouselSlides[activeCarouselIndex].titleKey)}</div>
            <div class="caption-sub-gc" id="captionSub">{t(carouselSlides[activeCarouselIndex].subtitleKey)}</div>
          </div>
          <div class="carousel-dots-gc" id="carouselDots"></div>
          <div class="progress-track-gc">
            <div class="progress-bar-gc" id="progressBar"></div>
          </div>
        </div>
      </section>

      <!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
           "DESIGNED TO MAKE RESTORATION EFFORTLESS"
           â€” Replaced with integrated HTML UI component
      â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->
      <section class="gc-feat-section">

          <div class="gc-feat-header" id="gcSectionHeader">
            <div class="gc-feat-eyebrow">
              <span class="gc-feat-eyebrow-dot"></span>
              {t('landing.features.eyebrow')}
            </div>
            <h2 class="gc-feat-heading">
              {t('landing.features.titleLine1')}<br>
              <em>{t('landing.features.titleLine2')}</em>
            </h2>
            <p class="gc-feat-sub">{t('landing.features.subtitle')}</p>
          </div>

        <!-- â•â• Integrated Hero Component: Two-card layout â•â• -->
        <div class="gc-hero-cards__container">

          <!-- LEFT copy -->
          <div class="gc-hero-cards__left">
            <span class="gc-hero-cards__eyebrow">
              <span class="gc-hero-cards__eyebrow-dot"></span>
              {t('landing.features.panelEyebrow')}
            </span>
            <h3 class="gc-hero-cards__headline">
              {t('landing.features.headlineLine1')}<br/>
              <em>{t('landing.features.headlineEmphasis')}</em> {t('landing.features.headlineLine2')}<br/>
              {t('landing.features.headlineLine3')}<br/>
              {t('landing.features.headlineLine4')}
            </h3>
            <p class="gc-hero-cards__body">
              {t('landing.features.body')}
            </p>
            <div class="gc-hero-cards__actions">
              <a href="#upload" class="gc-hc-btn-primary">
                {t('landing.features.start')}
                <span class="gc-hc-btn-primary__arrow">
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 8h10M9 4l4 4-4 4"/>
                  </svg>
                </span>
              </a>
              <a href="#how-it-works" class="gc-hc-btn-secondary">{t('landing.features.workflow')}</a>
            </div>
          </div>

          <!-- RIGHT: stacked cards -->
          <div class="gc-hero-cards__right">

            <!-- Card 1: Project Queue -->
            <div class="gc-hc-card gc-hc-card--queue">
              <div class="gc-hc-card__title">{t('landing.features.queueTitle')}</div>

              <div class="gc-queue-row gc-queue-row--active">
                <span class="gc-queue-row__icon">FC</span>
                <div class="gc-queue-row__meta">
                  <span class="gc-queue-row__label">{t('landing.features.queue1.title')}</span>
                  <span class="gc-queue-row__sub">{t('landing.features.queue1.sub')}</span>
                </div>
                <span class="gc-queue-row__badge">{t('common.ready')}</span>
              </div>

              <div class="gc-queue-row">
                <span class="gc-queue-row__icon">IG</span>
                <div class="gc-queue-row__meta">
                  <span class="gc-queue-row__label">{t('landing.features.queue2.title')}</span>
                  <span class="gc-queue-row__sub">{t('landing.features.queue2.sub')}</span>
                </div>
                <span class="gc-queue-row__dot"></span>
              </div>

              <div class="gc-queue-row">
                <span class="gc-queue-row__icon">CP</span>
                <div class="gc-queue-row__meta">
                  <span class="gc-queue-row__label">{t('landing.features.queue3.title')}</span>
                  <span class="gc-queue-row__sub">{t('landing.features.queue3.sub')}</span>
                </div>
                <span class="gc-queue-row__dot"></span>
              </div>
            </div>

            <!-- Card 2: Restoration Summary -->
            <div class="gc-hc-card gc-hc-card--summary">
              <div class="gc-hc-card__title">{t('landing.features.summaryTitle')}</div>

              <div class="gc-summary-stat">
                <div class="gc-summary-stat__label">
                  {t('landing.features.summary1.label')}
                  <span class="gc-summary-stat__pct">94%</span>
                </div>
                <div class="gc-summary-stat__bar-track">
                  <div class="gc-summary-stat__bar-fill" style="--bar-target:94%"></div>
                </div>
              </div>

              <div class="gc-summary-stat">
                <div class="gc-summary-stat__label">
                  {t('landing.features.summary2.label')}
                  <span class="gc-summary-stat__pct">81%</span>
                </div>
                <div class="gc-summary-stat__bar-track">
                  <div class="gc-summary-stat__bar-fill" style="--bar-target:81%"></div>
                </div>
              </div>

              <div class="gc-summary-stat">
                <div class="gc-summary-stat__label">
                  {t('landing.features.summary3.label')}
                  <span class="gc-summary-stat__pct">100%</span>
                </div>
                <div class="gc-summary-stat__bar-track">
                  <div class="gc-summary-stat__bar-fill" style="--bar-target:100%"></div>
                </div>
              </div>

              <div class="gc-summary-chip">
                <span class="gc-summary-chip__label">{t('landing.features.summaryChip')}</span>
                <span class="gc-summary-chip__value">2m 20s</span>
              </div>
            </div>

          </div>
        </div>

        <!-- Bottom strip -->
        <div class="gc-hero-cards__strip">
          <div class="gc-hero-cards__strip-label">{t('landing.features.trustedLabel')}</div>
          <div class="gc-hero-cards__strip-row">
            <div class="gc-strip-item"><span class="gc-strip-item__name">{t('landing.features.industry1')}</span></div>
            <div class="gc-strip-item"><span class="gc-strip-item__name">{t('landing.features.industry2')}</span></div>
            <div class="gc-strip-item"><span class="gc-strip-item__name">{t('landing.features.industry3')}</span></div>
            <div class="gc-strip-item"><span class="gc-strip-item__name">{t('landing.features.industry4')}</span></div>
            <div class="gc-strip-item"><span class="gc-strip-item__name">{t('landing.features.industry5')}</span></div>
          </div>
        </div>

      </section>

      <!-- â•â•â•â•â•â•â•â•â•â• TESTIMONIALS â•â•â•â•â•â•â•â•â•â• -->
      <section class="section testimonials-section">
        <div class="container">
          <div class="section-label">{t('landing.testimonials.label')}</div>
          <h2 class="section-title">{t('landing.testimonials.title')}</h2>
          <p class="section-desc">From photographers to real estate teams â€” GlassClear transforms reflections into crystal-clear visuals.</p>
          <div class="testimonial-top">
            <div class="testi-avatars">
              <img src="https://randomuser.me/api/portraits/women/1.jpg" alt="User" />
              <img src="https://randomuser.me/api/portraits/men/2.jpg" alt="User" />
              <img src="https://randomuser.me/api/portraits/women/3.jpg" alt="User" />
              <img src="https://randomuser.me/api/portraits/men/4.jpg" alt="User" />
            </div>
            <div class="testi-proof-text">
              <div class="testi-stars">â˜…â˜…â˜…â˜…â˜…</div>
              <p>{t('landing.testimonials.proofPrefix')} <strong>4,000+</strong> {t('landing.testimonials.proofSuffix')}</p>
            </div>
          </div>
        </div>
        <div class="testi-outer">
          <div class="testi-fade-top"></div>
          <div class="testi-cols" aria-hidden="true">
            <div class="testi-col testi-col-up testi-col-slow">
              {#each [...tcol1, ...tcol1] as card}
                <div class="testi-card">
                  <span class="testi-quote-icon">"</span>
                  <div class="testi-stars-sm">â˜…â˜…â˜…â˜…â˜…</div>
                  <p class="testi-text">{t(card.quoteKey)}</p>
                  <div class="testi-footer">
                    <img src={card.avatar} alt={card.name} class="testi-avatar" />
                    <div class="testi-info">
                      <span class="testi-name">{card.name}</span>
                      <span class="testi-role">{t(card.roleKey)}</span>
                    </div>
                  </div>
                </div>
              {/each}
            </div>
            <div class="testi-col testi-col-down testi-col-medium">
              {#each [...tcol2, ...tcol2] as card}
                <div class="testi-card">
                  <span class="testi-quote-icon">"</span>
                  <div class="testi-stars-sm">â˜…â˜…â˜…â˜…â˜…</div>
                  <p class="testi-text">{t(card.quoteKey)}</p>
                  <div class="testi-footer">
                    <img src={card.avatar} alt={card.name} class="testi-avatar" />
                    <div class="testi-info">
                      <span class="testi-name">{card.name}</span>
                      <span class="testi-role">{t(card.roleKey)}</span>
                    </div>
                  </div>
                </div>
              {/each}
            </div>
            <div class="testi-col testi-col-up testi-col-fast">
              {#each [...tcol3, ...tcol3] as card}
                <div class="testi-card">
                  <span class="testi-quote-icon">"</span>
                  <div class="testi-stars-sm">â˜…â˜…â˜…â˜…â˜…</div>
                  <p class="testi-text">{t(card.quoteKey)}</p>
                  <div class="testi-footer">
                    <img src={card.avatar} alt={card.name} class="testi-avatar" />
                    <div class="testi-info">
                      <span class="testi-name">{card.name}</span>
                      <span class="testi-role">{t(card.roleKey)}</span>
                    </div>
                  </div>
                </div>
              {/each}
            </div>
          </div>
          <div class="testi-fade-bot"></div>
        </div>
      </section>

      <!-- â•â•â•â•â•â•â•â•â•â• FAQ â•â•â•â•â•â•â•â•â•â• -->
      <section class="lp-faq-section" id="faq" aria-label={t('landing.faq.ariaLabel')}>
        <div class="lp-faq-inner">
          <div class="lp-faq-header">
            <div class="lp-faq-pill">{t('landing.faq.label')}</div>
            <h2 class="lp-faq-title">
              {t('landing.faq.titleLine1')}<br />
              <em>{t('landing.faq.titleLine2')}</em>
            </h2>
          </div>
          <div class="lp-faq-grid">
            {#each localizedFaqs as item, i}
              <div
                class="lp-faq-card {faqActiveIndex === i ? 'active' : ''}"
                role="button"
                aria-expanded={faqActiveIndex === i}
                tabindex="0"
                onclick={() => toggleFaq(i)}
                onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleFaq(i); } }}
              >
                <div class="lp-faq-question">
                  <span class="lp-faq-question-text">{t(item.qKey)}</span>
                  <button class="lp-faq-btn" aria-label={faqActiveIndex === i ? t('common.collapse') : t('common.expand')} tabindex="-1"></button>
                </div>
                <div class="lp-faq-divider"></div>
                <div class="lp-faq-answer-wrap">
                  <div class="lp-faq-answer-inner">
                    <p class="lp-faq-answer">{t(item.aKey)}</p>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </section>

      <!-- â•â•â•â•â•â•â•â•â•â• CTA â•â•â•â•â•â•â•â•â•â• -->
      <section class="lp-cta-section" aria-label={t('landing.cta.ariaLabel')}>
        <div class="lp-cta-orb" aria-hidden="true"></div>
        <div class="lp-cta-content">
          <span class="lp-cta-label">{t('landing.cta.label')}</span>
          <h2 class="lp-cta-heading">
            {t('landing.cta.titleLine1')} <em>{t('landing.cta.titleEmphasis')}</em><br />{t('landing.cta.titleLine2')}
          </h2>
          <p class="lp-cta-subtitle">
            Upload a glass, window, or facade image and let GlassClear generate a cleaner, reflection-reduced result in seconds.
          </p>
          <div class="lp-cta-buttons">
            <a href="#upload" class="lp-cta-btn lp-cta-btn-primary" onclick={(e) => { const t = document.getElementById('upload'); if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth'});} }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              {t('landing.cta.primary')}
            </a>
            <a href="#demo" class="lp-cta-btn lp-cta-btn-secondary" onclick={(e) => { const t = document.getElementById('demo'); if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth'});} }}>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polygon points="10 8 16 12 10 16 10 8"/></svg>
              {t('landing.cta.secondary')}
            </a>
          </div>
          <div class="lp-cta-divider"></div>
          <div class="lp-cta-cards">
            <div class="lp-cta-card">
              <div class="lp-cta-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z"/>
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M4.5 4.5l15 15" stroke="#a5b4fc" stroke-width="1.4"/>
                </svg>
              </div>
              <div class="lp-cta-card-title">{t('landing.cta.card1.title')}</div>
              <div class="lp-cta-card-text">{t('landing.cta.card1.text')}</div>
            </div>
            <div class="lp-cta-card">
              <div class="lp-cta-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="7" width="9" height="10" rx="2"/>
                  <rect x="13" y="7" width="9" height="10" rx="2"/>
                  <path d="M6 7V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2"/>
                </svg>
              </div>
              <div class="lp-cta-card-title">{t('landing.cta.card2.title')}</div>
              <div class="lp-cta-card-text">{t('landing.cta.card2.text')}</div>
            </div>
            <div class="lp-cta-card">
              <div class="lp-cta-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="3" width="7" height="7" rx="1.5"/>
                  <rect x="14" y="3" width="7" height="7" rx="1.5"/>
                  <rect x="3" y="14" width="7" height="7" rx="1.5"/>
                  <path d="M17.5 14v7M14 17.5h7"/>
                </svg>
              </div>
              <div class="lp-cta-card-title">{t('landing.cta.card3.title')}</div>
              <div class="lp-cta-card-text">{t('landing.cta.card3.text')}</div>
            </div>
          </div>
        </div>
      </section>

    {:else}

      <!-- â•â•â•â•â•â•â•â•â•â• RESULTS VIEW â•â•â•â•â•â•â•â•â•â• -->
      <section class="result-section container-fluid px-lg-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <button class="back-btn glass-card p-2 px-3" onclick={() => showResults = false}>
            <i class="bi bi-arrow-left me-2"></i> {t('res_new')}
          </button>
          <div class="d-flex gap-2">
            <select bind:value={selectedFormat} class="form-select glass-input w-auto">
               <option value="PNG">PNG</option>
               <option value="JPG">JPG</option>
            </select>
            <button class="btn btn-primary rounded-pill px-4" onclick={() => downloadImage(selectedFormat.toLowerCase())}>
              <i class="bi bi-download me-2"></i> {t('exp_free')}
            </button>
          </div>
        </div>
        <ResultDisplay
          originalImage={previewUrl}
          processedImage={resultUrl}
          {downloadFilename}
          {predictionId}
          downloadHandler={downloadImage}
          {aiMode}
          {confidenceMap}
          {ssim}
          {edgeScore}
          {intermediateOutputs}
          {processingSteps}
        />
      </section>

    {/if}

    <Footer />
  </div>

  <Chatbot />
  <UnlockResultModal
    open={unlockModalOpen}
    onLogin={continueToLogin}
    onSignup={continueToSignup}
    onClose={() => (unlockModalOpen = false)}
  />
</div>

<style>
  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     GOOGLE FONT IMPORT â€” Space Grotesk + DM Serif Display + DM Sans + DM Mono
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800;900&family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Mono:wght@400;500&display=swap');

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     GLOBAL BASE
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  :global(html) { scroll-behavior: smooth; }
  :global(body) {
    margin: 0;
    font-family: Inter, system-ui, sans-serif;
    background: #ffffff;
    color: #111827;
    overflow-x: hidden;
  }

  .page-wrapper {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    font-family: Inter, system-ui, sans-serif;
    background: radial-gradient(125% 125% at 50% 10%, #fff 40%, #6366f1 100%);
    background-attachment: fixed;
  }
  .content-area { flex: 1; }
  .container { max-width: 1180px; margin: 0 auto; padding: 0 1.5rem; }

  .glass-card {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 20px;
  }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     HERO SECTION
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .gc-hero {
    position: relative;
    display: flex;
    align-items: center;
    overflow: hidden;
    padding: 90px 24px 56px;
  }

  .gc-hero-bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
  }

  .gc-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(110px);
    animation: gc-float 13s ease-in-out infinite;
  }
  .gc-orb-1 {
    width: 680px; height: 680px;
    background: radial-gradient(circle, rgba(99,102,241,0.17) 0%, rgba(99,102,241,0.05) 50%, transparent 75%);
    top: -240px; left: -180px;
    animation-duration: 14s;
  }
  .gc-orb-2 {
    width: 520px; height: 520px;
    background: radial-gradient(circle, rgba(129,140,248,0.13) 0%, transparent 70%);
    top: -40px; right: -140px;
    animation-delay: 5s; animation-duration: 16s;
  }
  .gc-orb-3 {
    width: 380px; height: 280px;
    background: radial-gradient(ellipse, rgba(99,102,241,0.07) 0%, transparent 70%);
    bottom: 60px; left: 50%; transform: translateX(-50%);
    animation-delay: 2s; animation-duration: 10s;
    filter: blur(70px);
  }
  @keyframes gc-float {
    0%, 100% { transform: translateY(0px) scale(1); }
    50%       { transform: translateY(-28px) scale(1.04); }
  }

  .gc-grid-overlay {
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(99,102,241,0.045) 1px, transparent 1px),
      linear-gradient(90deg, rgba(99,102,241,0.045) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 85% 75% at 50% 0%, black 30%, transparent 100%);
  }

  .gc-hero-beam {
    position: absolute;
    top: -10%; left: 50%; transform: translateX(-50%);
    width: 2px; height: 65%;
    background: linear-gradient(to bottom, transparent 0%, rgba(99,102,241,0.28) 35%, rgba(129,140,248,0.16) 65%, transparent 100%);
    filter: blur(3px);
    animation: gc-beam-pulse 4s ease-in-out infinite;
  }
  @keyframes gc-beam-pulse {
    0%, 100% { opacity: 0.6; transform: translateX(-50%) scaleX(1); }
    50%       { opacity: 1;   transform: translateX(-50%) scaleX(2.2); }
  }

  .gc-hero-particles { position: absolute; inset: 0; }
  .gc-particle {
    position: absolute;
    border-radius: 50%;
    background: rgba(99,102,241,0.4);
    animation: gc-particle-float linear infinite;
  }
  .gc-particle.p1 { width:3px; height:3px; left:12%; top:30%; animation-duration:8s;  }
  .gc-particle.p2 { width:2px; height:2px; left:25%; top:65%; animation-duration:12s; animation-delay:2s; }
  .gc-particle.p3 { width:4px; height:4px; left:72%; top:22%; animation-duration:9s;  animation-delay:1s; }
  .gc-particle.p4 { width:2px; height:2px; left:85%; top:58%; animation-duration:11s; animation-delay:3s; }
  .gc-particle.p5 { width:3px; height:3px; left:48%; top:80%; animation-duration:7s;  animation-delay:0.5s; }
  .gc-particle.p6 { width:2px; height:2px; left:60%; top:40%; animation-duration:14s; animation-delay:4s; }
  @keyframes gc-particle-float {
    0%   { transform: translateY(0) scale(1);   opacity: 0; }
    10%  { opacity: 0.6; }
    90%  { opacity: 0.3; }
    100% { transform: translateY(-110px) scale(0.4); opacity: 0; }
  }

  .gc-hero-inner {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
    max-width: 1180px;
    margin: 0 auto;
  }

  .gc-hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 999px;
    padding: 0.38rem 1.15rem;
    font-size: 0.74rem;
    font-weight: 600;
    color: #4f46e5;
    letter-spacing: 0.05em;
    margin-bottom: 2.2rem;
    position: relative;
    overflow: hidden;
    opacity: 0;
    animation: gc-fadeUp 0.7s cubic-bezier(.22,1,.36,1) 0.1s forwards;
  }
  .gc-hero-pill::after {
    content: '';
    position: absolute; top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.08), transparent);
    animation: gc-badge-shimmer 3.5s ease-in-out infinite;
  }
  @keyframes gc-badge-shimmer {
    0%   { left: -100%; }
    60%  { left: 160%; }
    100% { left: 160%; }
  }

  .gc-pill-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #6366f1;
    box-shadow: 0 0 10px rgba(99,102,241,0.6), 0 0 18px rgba(99,102,241,0.2);
    animation: gc-pulse 2s ease-in-out infinite;
    flex-shrink: 0;
  }
  @keyframes gc-pulse {
    0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 10px rgba(99,102,241,0.6); }
    50%       { opacity: 0.5; transform: scale(0.72); box-shadow: 0 0 4px rgba(99,102,241,0.3); }
  }

  .gc-hero-title {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
    margin: 0 0 1.4rem;
    padding: 0;
    overflow: hidden;
  }

  .gc-title-reveal {
    display: block;
    overflow: hidden;
    line-height: 1;
  }

  .gc-title-text {
    display: block;
    font-family: 'Space Grotesk', 'Inter', system-ui, sans-serif;
    font-size: clamp(54px, 8vw, 120px);
    font-weight: 900;
    letter-spacing: -0.075em;
    line-height: 0.9;
    color: #0f172a;
    opacity: 0;
    transform: translateY(110%);
  }

  .gc-line-1 { padding-bottom: 0.08em; }
  .gc-line-1 .gc-title-text {
    animation: gc-title-reveal 1.1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
  }

  .gc-line-2 { padding-bottom: 0.08em; }
  .gc-line-2 .gc-title-text {
    animation: gc-title-reveal 1.1s cubic-bezier(0.16, 1, 0.3, 1) 0.55s forwards;
  }

  .gc-line-sub { margin-top: 0.7em; }
  .gc-line-sub .gc-title-text {
    font-family: 'Space Grotesk', 'Inter', system-ui, sans-serif;
    font-size: clamp(10px, 1.1vw, 15px);
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(15,23,42,0.38);
    line-height: 1;
    animation: gc-title-reveal 0.9s cubic-bezier(0.16, 1, 0.3, 1) 1.0s forwards;
  }

  .gc-gradient-text {
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #4f46e5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    background-size: 200% auto;
    animation: gc-title-reveal 1.1s cubic-bezier(0.16, 1, 0.3, 1) 0.55s forwards,
               gc-text-shimmer 5s linear 1.8s infinite;
  }
  @keyframes gc-text-shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
  }

  @keyframes gc-title-reveal {
    0%   { opacity: 0; transform: translateY(110%); }
    1%   { opacity: 1; }
    100% { opacity: 1; transform: translateY(0%); }
  }

  .gc-hero-desc {
    font-size: clamp(16px, 1.7vw, 19px);
    color: #475569;
    line-height: 1.68;
    max-width: 620px;
    margin: 0 0 2.4rem;
    font-weight: 450;
    opacity: 0;
    animation: gc-fadeUp 0.7s cubic-bezier(.22,1,.36,1) 1.15s forwards;
  }

  @keyframes gc-fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .gc-upload-card {
    position: relative;
    width: 100%;
    max-width: 800px;
    border-radius: 28px;
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1.5px dashed rgba(99,102,241,0.28);
    box-shadow:
      0 24px 80px rgba(99,102,241,0.11),
      0 4px 16px rgba(31,41,55,0.06),
      inset 0 1px 0 rgba(255,255,255,0.9);
    cursor: pointer;
    transition:
      border-color 0.32s ease,
      background 0.32s ease,
      box-shadow 0.32s ease,
      transform 0.32s ease;
    overflow: hidden;
    opacity: 0;
    animation: gc-fadeUp 0.75s cubic-bezier(.22,1,.36,1) 1.3s forwards;
  }

  .gc-upload-card::before {
    content: '';
    position: absolute; left: 0; right: 0; top: 0;
    height: 1.5px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.55), rgba(129,140,248,0.75), rgba(99,102,241,0.55), transparent);
    z-index: 2; pointer-events: none;
    animation: gc-uz-scan 3.2s ease-in-out infinite; opacity: 0;
  }
  @keyframes gc-uz-scan {
    0%   { top: 0%;   opacity: 0; }
    6%   { opacity: 0.7; }
    88%  { opacity: 0.45; }
    100% { top: 100%; opacity: 0; }
  }

  .gc-upload-card:hover,
  .gc-upload-card.gc-dragging {
    border-color: rgba(99,102,241,0.52);
    border-style: solid;
    background: rgba(255,255,255,0.9);
    box-shadow:
      0 0 0 1px rgba(99,102,241,0.1) inset,
      0 0 60px rgba(99,102,241,0.12),
      0 28px 72px rgba(99,102,241,0.1);
    transform: translateY(-3px);
  }
  .gc-upload-card.gc-dragging {
    border-color: rgba(99,102,241,0.72);
    background: rgba(255,255,255,0.95);
    box-shadow: 0 0 80px rgba(99,102,241,0.18), 0 0 0 2px rgba(99,102,241,0.22) inset;
  }

  .gc-corner {
    position: absolute; width: 18px; height: 18px; pointer-events: none; z-index: 3;
    transition: opacity 0.3s;
  }
  .gc-tl { top: 14px; left: 14px;  border-top: 1.5px solid rgba(99,102,241,0.38); border-left:  1.5px solid rgba(99,102,241,0.38); }
  .gc-tr { top: 14px; right: 14px; border-top: 1.5px solid rgba(99,102,241,0.38); border-right: 1.5px solid rgba(99,102,241,0.38); }
  .gc-bl { bottom: 14px; left: 14px;  border-bottom: 1.5px solid rgba(99,102,241,0.38); border-left:  1.5px solid rgba(99,102,241,0.38); }
  .gc-br { bottom: 14px; right: 14px; border-bottom: 1.5px solid rgba(99,102,241,0.38); border-right: 1.5px solid rgba(99,102,241,0.38); }

  .gc-file-input {
    position: absolute; inset: 0; width: 100%; height: 100%;
    opacity: 0; cursor: pointer; z-index: 10;
  }

  .gc-upload-idle {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3.5rem 2rem 3rem;
  }

  .gc-upload-icon-wrap {
    position: relative;
    width: 80px; height: 80px;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; justify-content: center;
  }
  .gc-upload-icon-badge {
    width: 72px; height: 72px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(99,102,241,0.06));
    border: 1.5px solid rgba(99,102,241,0.2);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 20px rgba(99,102,241,0.15);
    position: relative; z-index: 2;
  }
  .gc-upload-icon-ring {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(99,102,241,0.14);
  }
  .gc-ring-outer { inset: -12px; animation: gc-ring-spin 6s linear infinite; }
  .gc-ring-inner { inset: -22px; border-color: rgba(99,102,241,0.07); border-style: dashed; animation: gc-ring-spin-rev 9s linear infinite; }
  @keyframes gc-ring-spin     { from { transform: rotate(0deg); }   to { transform: rotate(360deg); } }
  @keyframes gc-ring-spin-rev { from { transform: rotate(0deg); }   to { transform: rotate(-360deg); } }

  .gc-upload-title {
    font-size: 1.1rem; font-weight: 700; color: #1f2937; margin: 0 0 0.45rem;
    letter-spacing: -0.02em;
  }
  .gc-upload-hint {
    font-size: 0.85rem; color: #6b7280; margin: 0 0 1.2rem;
  }

  .gc-browse-btn {
    background: none; border: none; color: #6366f1; cursor: pointer; padding: 0;
    font-size: inherit; text-decoration: underline; text-underline-offset: 3px;
    position: relative; z-index: 20; transition: color 0.2s;
  }
  .gc-browse-btn:hover { color: #4f46e5; }

  .gc-fmt-chips { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; justify-content: center; }
  .gc-fmt-chip {
    font-size: 10.5px; font-weight: 600; letter-spacing: 0.06em;
    color: #6366f1; background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.16); border-radius: 6px; padding: 3px 10px;
  }

  .gc-upload-preview {
    padding: 1.6rem;
    display: flex; flex-direction: column; align-items: center; gap: 1rem;
  }
  .gc-preview-img {
    max-height: 360px; max-width: 100%;
    border-radius: 18px; object-fit: contain;
    box-shadow: 0 20px 60px rgba(99,102,241,0.14), 0 0 0 1px rgba(99,102,241,0.1);
    animation: gc-fadeUp 0.4s ease both;
  }
  .gc-change-btn {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.16);
    border-radius: 999px; padding: 0.4rem 1rem;
    color: #6b7280; font-size: 0.8rem; cursor: pointer;
    transition: all 0.22s; position: relative; z-index: 20;
  }
  .gc-change-btn:hover { background: rgba(99,102,241,0.12); color: #1f2937; border-color: rgba(99,102,241,0.35); }

  .gc-cta-btn {
    display: inline-flex; align-items: center; gap: 0.6rem;
    margin-top: 1.6rem; padding: 1rem 2.8rem;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none; border-radius: 16px; color: white;
    font-size: 1rem; font-weight: 700; cursor: pointer;
    position: relative; overflow: hidden;
    transition: transform 0.26s ease, box-shadow 0.26s ease, filter 0.26s ease;
    box-shadow: 0 8px 32px rgba(99,102,241,0.35), 0 0 0 1px rgba(255,255,255,0.15) inset;
    opacity: 0;
    animation: gc-fadeUp 0.7s cubic-bezier(.22,1,.36,1) 1.1s forwards;
  }
  .gc-cta-btn::before {
    content: '';
    position: absolute; top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
    animation: gc-cta-shimmer 3s ease-in-out infinite;
  }
  @keyframes gc-cta-shimmer {
    0%  { left: -100%; }
    55% { left: 160%; }
    100%{ left: 160%; }
  }
  .gc-cta-btn:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 20px 56px rgba(99,102,241,0.44), 0 0 0 1px rgba(255,255,255,0.2) inset;
    filter: brightness(1.06);
  }
  .gc-cta-btn:active { transform: scale(0.97); }

  .gc-error-msg {
    display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem;
    padding: 0.75rem 1.25rem;
    background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.15);
    border-radius: 12px; color: #dc2626; font-size: 0.875rem;
  }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     HOW IT WORKS
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .how-it-works {
    position: relative;
    width: 100%;
    padding: 72px 24px 78px;
    background: rgba(255,255,255,0.32);
    backdrop-filter: blur(8px);
    border-top: 1px solid rgba(99,102,241,0.08);
    border-bottom: 1px solid rgba(99,102,241,0.08);
    overflow: hidden;
  }

  .how-it-works::before {
    content: '';
    position: absolute;
    width: 700px; height: 500px;
    top: -120px; left: 50%; transform: translateX(-50%);
    background: radial-gradient(ellipse, rgba(99,102,241,0.06) 0%, transparent 70%);
    pointer-events: none;
    filter: blur(40px);
  }

  .hiw-container {
    max-width: 1180px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }

  .hiw-header {
    text-align: center;
    opacity: 1;
    transform: none;
  }
  .hiw-header.visible { opacity: 1; transform: none; }

  .hiw-label {
    display: inline-block;
    font-size: 0.76rem; font-weight: 800; letter-spacing: 0.18em;
    text-transform: uppercase; color: #6366f1; margin-bottom: 16px; opacity: 0.85;
  }

  .hiw-heading {
    font-family: 'Space Grotesk', 'Inter', system-ui, sans-serif;
    font-size: clamp(34px, 4.8vw, 68px);
    font-weight: 800; color: #111827;
    line-height: 1.06; letter-spacing: -0.04em;
    margin-bottom: 16px;
  }

  .hiw-divider {
    width: 40px; height: 1px;
    background: linear-gradient(90deg, transparent, #6366f1, transparent);
    margin: 0 auto 18px;
    opacity: 1;
  }
  .hiw-divider.visible { opacity: 1; }

  .hiw-sub {
    font-size: clamp(16px, 1.6vw, 18.5px);
    color: #475569; font-weight: 500;
    max-width: 680px; margin: 0 auto; line-height: 1.65;
  }

  .hiw-steps {
    display: grid;
    grid-template-columns: 1fr 180px 1fr 180px 1fr;
    align-items: start;
    column-gap: 12px;
    margin: 56px auto 0;
  }

  .hiw-step {
    text-align: center;
    opacity: 1;
    transform: none;
  }
  .hiw-step.visible { opacity: 1; transform: none; }

  .hiw-step-inner {
    max-width: 300px; margin: 0 auto;
    transition: transform 0.42s cubic-bezier(.16,1,.3,1);
  }
  .hiw-step:hover .hiw-step-inner { transform: translateY(-5px); }

  .hiw-number {
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    font-size: 80px; font-weight: 900;
    background: linear-gradient(135deg, #4338ca, #6366f1, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1; margin-bottom: 24px; display: block;
    opacity: 1; transform: none;
  }

  .hiw-step-title {
    font-size: 1.15rem; font-weight: 800; color: #111827;
    margin-bottom: 12px; letter-spacing: -0.025em;
  }
  .hiw-step-desc {
    font-size: 0.96rem; color: #475569; font-weight: 500;
    line-height: 1.68; max-width: 300px; margin: 0 auto;
  }
  .hiw-step-note {
    margin-top: 12px; font-size: 0.8rem; color: #64748b;
    font-weight: 600; letter-spacing: 0.01em;
    line-height: 1.6; font-style: italic;
  }

  .hiw-arrow-wrap {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 22px;
    opacity: 1;
  }
  .hiw-arrow-wrap.visible { opacity: 1; }

  .hiw-arrow {
    width: 160px; height: 78px;
    display: block; overflow: visible;
    filter: drop-shadow(0 0 6px rgba(99,102,241,0.2));
  }

  .hiw-arrow-path {
    fill: none;
    stroke: #6366f1;
    stroke-width: 2.8;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-dasharray: 340;
    stroke-dashoffset: 0;
  }
  .hiw-arrow-head {
    fill: none;
    stroke: #6366f1;
    stroke-width: 2.8;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-dasharray: 42;
    stroke-dashoffset: 0;
  }

  @media (max-width: 900px) {
    .hiw-steps { grid-template-columns: 1fr; margin-top: 48px; }
    .hiw-step  { margin-bottom: 28px; }
    .hiw-arrow-wrap {
      padding-top: 0; margin: -4px auto 28px;
      transform: rotate(90deg);
    }
    .hiw-arrow { width: 100px; height: 52px; }
  }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     GENERIC SECTION
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .section { padding: 72px 24px; }
  .section-label {
    display: inline-block; font-size: 0.78rem; font-weight: 800;
    letter-spacing: 0.12em; text-transform: uppercase; color: #6366f1; margin-bottom: 1rem;
  }
  .section-title {
    font-family: 'Space Grotesk', Inter, system-ui, sans-serif;
    font-size: clamp(34px, 4.8vw, 68px);
    font-weight: 800; letter-spacing: -0.04em; line-height: 1.06;
    margin: 0 0 1rem; color: #111827;
  }
  .section-desc {
    font-size: clamp(16px, 1.65vw, 18.5px); color: #475569;
    max-width: 720px; line-height: 1.65; margin: 0 0 2.5rem;
  }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     FEATURE SHOWCASE SECTION
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .gc-showcase-section {
    position: relative; width: 100%;
    padding: 56px 24px 72px;
  }
  .gc-showcase-container {
    max-width: 1240px; margin: 0 auto;
    display: flex; flex-direction: column; gap: 56px;
  }

  :global(.gc-row) {
    display: grid; grid-template-columns: 1fr 1fr; gap: 56px; align-items: center;
    opacity: 1; transform: translateY(0);
    transition: opacity 0.85s cubic-bezier(.22,1,.36,1), transform 0.85s cubic-bezier(.22,1,.36,1);
  }
  :global(.gc-row.revealed) { opacity: 1; transform: translateY(0); }

  .gc-visual {
    position: relative; width: 100%; min-height: 420px;
    border-radius: 32px; overflow: hidden;
    border: 1px solid rgba(255,255,255,0.8);
    box-shadow: 0 32px 80px rgba(99,102,241,0.12), 0 4px 24px rgba(31,41,55,0.08);
    transition: box-shadow 0.4s ease;
  }
  .gc-visual:hover .gc-img { transform: scale(1.045); }

  .gc-img {
    position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
    transition: transform 6s cubic-bezier(.25,.46,.45,.94);
  }
  .gc-img-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(99,102,241,0.1));
    z-index: 1;
  }

  .gc-panel {
    position: absolute; z-index: 2;
    width: 68%; max-width: 390px;
    background: rgba(255,255,255,0.92); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    border-radius: 24px; padding: 24px;
    box-shadow: 0 24px 70px rgba(31,41,55,0.12), 0 2px 8px rgba(99,102,241,0.08);
    border: 1px solid rgba(255,255,255,0.9);
    transition: opacity 0.9s 0.25s, transform 0.9s 0.25s cubic-bezier(.22,1,.36,1);
    opacity: 1; transform: translateY(0);
  }
  :global(.gc-panel.panel-in) {
    opacity: 1; transform: translateY(0);
    animation: panelFloat 5s ease-in-out infinite;
  }
  @keyframes panelFloat {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-9px); }
  }
  .panel-bottom-left  { bottom: 28px; left: 28px; }
  .panel-bottom-right { bottom: 28px; right: 28px; }

  .panel-header {
    display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px;
  }
  .panel-title-wrap { display: flex; align-items: center; gap: 10px; }
  .panel-accent-bar {
    width: 4px; height: 20px; border-radius: 4px;
    background: linear-gradient(180deg, #6366f1, #4f46e5); flex-shrink: 0;
  }
  .panel-title { font-size: 0.875rem; font-weight: 600; color: #111827; letter-spacing: -0.01em; }
  .panel-icon {
    width: 30px; height: 30px; border-radius: 8px; background: #eef2ff;
    border: 1px solid rgba(99,102,241,0.14);
    display: flex; align-items: center; justify-content: center;
  }
  .panel-icon svg { width: 14px; height: 14px; }

  .panel-item {
    background: #ffffff; border-radius: 14px; padding: 12px 14px; margin-bottom: 10px;
    display: flex; align-items: center; gap: 12px;
    border: 1px solid rgba(99,102,241,0.09);
    box-shadow: 0 2px 8px rgba(31,41,55,0.04);
    cursor: default;
    transition: transform 0.22s ease, box-shadow 0.22s ease;
    opacity: 1; transform: translateX(0);
  }
  .panel-item:last-child { margin-bottom: 0; }
  :global(.panel-item.item-in) { opacity: 1; transform: translateX(0); }
  .panel-item:hover { transform: translateX(4px); box-shadow: 0 4px 18px rgba(99,102,241,0.1); }

  .item-icon {
    width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 14px;
  }
  .icon-purple { background: #ede9fe; }
  .icon-blue   { background: #e0e7ff; }
  .icon-green  { background: #dcfce7; }
  .icon-amber  { background: #fef3c7; }
  .icon-sky    { background: #e0f2fe; }

  .item-body { flex: 1; min-width: 0; }
  .item-name { font-size: 0.78rem; font-weight: 600; color: #111827; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 2px; }
  .item-sub  { font-size: 0.7rem;  color: #6b7280;  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  .item-status {
    flex-shrink: 0; font-size: 0.68rem; font-weight: 600;
    padding: 4px 9px; border-radius: 999px; letter-spacing: 0.01em;
  }
  .status-done   { background: #d1fae5; color: #065f46; }
  .status-queued { background: #f3f4f6; color: #6b7280; }
  .status-ready  { background: #fef3c7; color: #92400e; }

  .item-progress-wrap { display: flex; align-items: center; gap: 7px; }
  .item-progress-bar  { width: 52px; height: 5px; background: #e0e7ff; border-radius: 99px; overflow: hidden; flex-shrink: 0; }
  .item-progress-fill {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, #6366f1, #4f46e5);
    width: 0%; transition: width 1.5s 0.6s cubic-bezier(.22,1,.36,1);
  }
  :global(.item-progress-fill.fill-in) { width: var(--fill-w, 64%); }
  .item-progress-pct { font-size: 0.68rem; font-weight: 600; color: #6366f1; }
  .item-count {
    flex-shrink: 0; font-size: 0.7rem; font-weight: 600; color: #6b7280;
    background: #f3f4f6; border-radius: 999px; padding: 3px 9px;
  }

  .gc-text { display: flex; flex-direction: column; gap: 20px; }
  .text-label {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #6366f1;
  }
  .label-dot { width: 6px; height: 6px; border-radius: 50%; background: #6366f1; flex-shrink: 0; }

  .gc-heading {
    font-family: 'Space Grotesk', Inter, system-ui, sans-serif;
    font-size: clamp(34px, 4.8vw, 60px);
    line-height: 1.08; letter-spacing: -0.04em; color: #111827;
  }
  .gc-heading em { font-style: normal; color: #6366f1; }

  .gc-para {
    font-size: clamp(16px, 1.65vw, 18.5px); line-height: 1.65;
    color: #475569; max-width: 560px; font-weight: 500;
  }

  .gc-btn {
    display: inline-flex; align-items: center; gap: 8px;
    background: #111827; color: #fff;
    font-size: 0.9rem; font-weight: 500; padding: 14px 26px;
    border-radius: 999px; text-decoration: none; border: none; cursor: pointer;
    align-self: flex-start;
    box-shadow: 0 4px 20px rgba(17,24,39,0.16);
    transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.22s ease;
  }
  .gc-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(17,24,39,0.2); background: #1f2937; }
  .gc-btn svg { width: 14px; height: 14px; opacity: 0.75; }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     CAROUSEL
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .carousel-section { overflow: hidden; padding-top: 56px; padding-bottom: 72px; }

  .carousel-wrapper-gc {
    position: relative; width: 100%; max-width: 1100px; margin: 0 auto;
    display: flex; flex-direction: column; align-items: center;
  }
  .carousel-stage-gc {
    position: relative; width: 100%; height: 320px;
    display: flex; align-items: center; justify-content: center; overflow: hidden;
  }
  .carousel-track-gc {
    position: relative; width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
  }

  :global(.slide-gc) {
    position: absolute; width: 440px; height: 300px; border-radius: 20px; overflow: hidden; cursor: pointer;
    transition: transform 0.52s cubic-bezier(0.4,0,0.2,1), opacity 0.52s cubic-bezier(0.4,0,0.2,1), filter 0.52s cubic-bezier(0.4,0,0.2,1), box-shadow 0.52s cubic-bezier(0.4,0,0.2,1);
    will-change: transform, opacity, filter; backface-visibility: hidden;
  }
  :global(.slide-gc img) { width: 100%; height: 100%; object-fit: cover; display: block; border-radius: 20px; transition: transform 0.4s cubic-bezier(0.4,0,0.2,1); }
  :global(.slide-shine-gc)    { position: absolute; inset: 0; border-radius: 20px; background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.04) 35%, transparent 60%); pointer-events: none; z-index: 2; }
  :global(.slide-gradient-gc) { position: absolute; inset: 0; border-radius: 20px; background: linear-gradient(to bottom, transparent 40%, rgba(17,24,39,0.55) 100%); pointer-events: none; z-index: 3; }
  :global(.slide-border-gc)   { position: absolute; inset: 0; border-radius: 20px; border: 1px solid transparent; pointer-events: none; z-index: 4; transition: border-color 0.52s cubic-bezier(0.4,0,0.2,1); }

  :global(.slide-gc.pos-center) { transform: translateX(0) scale(1.05) rotateY(0deg); opacity: 1; filter: none; z-index: 10; box-shadow: 0 0 0 1px rgba(99,102,241,0.3), 0 32px 72px rgba(99,102,241,0.18), 0 8px 24px rgba(0,0,0,0.12); }
  :global(.slide-gc.pos-center .slide-border-gc) { border-color: rgba(99,102,241,0.35); }
  :global(.slide-gc.pos-center:hover img)         { transform: scale(1.04); }
  :global(.slide-gc.pos-left)      { transform: translateX(-380px) scale(0.8) rotateY(18deg) perspective(900px); opacity: 0.35; filter: blur(2px); z-index: 6; }
  :global(.slide-gc.pos-right)     { transform: translateX(380px)  scale(0.8) rotateY(-18deg) perspective(900px); opacity: 0.35; filter: blur(2px); z-index: 6; }
  :global(.slide-gc.pos-far-left)  { transform: translateX(-660px) scale(0.65) rotateY(28deg) perspective(900px); opacity: 0; filter: blur(6px); z-index: 2; pointer-events: none; }
  :global(.slide-gc.pos-far-right) { transform: translateX(660px)  scale(0.65) rotateY(-28deg) perspective(900px); opacity: 0; filter: blur(6px); z-index: 2; pointer-events: none; }
  :global(.slide-gc.pos-hidden)    { transform: translateX(0) scale(0.5); opacity: 0; z-index: 1; pointer-events: none; }

  .nav-btn-gc {
    position: absolute; top: 50%; transform: translateY(-50%); z-index: 20;
    width: 48px; height: 48px; border-radius: 50%;
    border: 1px solid rgba(99,102,241,0.18);
    background: rgba(255,255,255,0.8); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    color: #6366f1; display: flex; align-items: center; justify-content: center;
    cursor: pointer; outline: none;
    transition: background 0.25s, border-color 0.25s, box-shadow 0.25s, transform 0.2s;
    box-shadow: 0 2px 12px rgba(99,102,241,0.1);
  }
  .nav-btn-gc svg { width: 20px; height: 20px; flex-shrink: 0; }
  .nav-btn-gc:hover { background: rgba(255,255,255,0.95); border-color: rgba(99,102,241,0.45); box-shadow: 0 0 20px rgba(99,102,241,0.2), inset 0 0 12px rgba(99,102,241,0.05); transform: translateY(-50%) scale(1.1); color: #4f46e5; }
  .nav-btn-gc:active { transform: translateY(-50%) scale(0.96); }
  .nav-prev-gc { left:  clamp(8px, 3vw, 40px); }
  .nav-next-gc { right: clamp(8px, 3vw, 40px); }

  .carousel-caption-gc { margin-top: 24px; text-align: center; min-height: 58px; }
  .caption-title-gc { font-family: 'Space Grotesk', Inter, system-ui, sans-serif; font-size: 22px; font-weight: 800; color: #111827; letter-spacing: -0.02em; margin-bottom: 5px; transition: opacity 0.28s, transform 0.28s; }
  .caption-sub-gc   { font-size: 12px; font-weight: 700; color: #64748b; letter-spacing: 0.18em; text-transform: uppercase; transition: opacity 0.28s, transform 0.28s; }
  :global(.caption-fade-gc) { opacity: 0; transform: translateY(6px); }

  .carousel-dots-gc { display: flex; align-items: center; gap: 8px; margin-top: 24px; }
  :global(.dot-gc) { height: 6px; width: 6px; border-radius: 3px; background: rgba(99,102,241,0.18); cursor: pointer; transition: width 0.35s cubic-bezier(0.4,0,0.2,1), background 0.35s, box-shadow 0.35s; }
  :global(.dot-gc.active) { width: 24px; background: linear-gradient(90deg, #6366f1, #4f46e5); box-shadow: 0 0 10px rgba(99,102,241,0.4); }

  .progress-track-gc { width: 180px; height: 2px; background: rgba(99,102,241,0.1); border-radius: 1px; margin-top: 20px; overflow: hidden; }
  .progress-bar-gc   { height: 100%; width: 0%; border-radius: 1px; background: linear-gradient(90deg, #6366f1, #4f46e5); transition: width 0.05s linear; box-shadow: 0 0 6px rgba(99,102,241,0.4); }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     FEATURES SECTION â€” with integrated hero card component
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .gc-feat-section {
    position: relative; z-index: 1;
    max-width: 1280px; margin: 0 auto;
    padding: 64px 32px 80px;
    border-top: 1px solid rgba(99,102,241,0.08);
  }

  .gc-feat-header {
    text-align: center; margin-bottom: 64px;
    opacity: 1; transform: translateY(0);
  }
  .gc-feat-header.gc-visible { opacity: 1; transform: translateY(0); }

  .gc-feat-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 12px; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase;
    color: #6366f1; background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.18);
    border-radius: 100px; padding: 6px 16px; margin-bottom: 28px;
  }
  .gc-feat-eyebrow-dot { width: 6px; height: 6px; border-radius: 50%; background: #6366f1; animation: gc-feat-pulse 2s ease-in-out infinite; }
  @keyframes gc-feat-pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.7)} }

  .gc-feat-heading {
    font-family: 'Space Grotesk', Inter, system-ui, sans-serif;
    font-size: clamp(34px, 4.8vw, 68px); font-weight: 800; color: #111827;
    line-height: 1.06; letter-spacing: -0.04em;
    margin-bottom: 14px; max-width: 680px; margin-left: auto; margin-right: auto;
  }
  .gc-feat-heading em { font-style: normal; color: #6366f1; }

  .gc-feat-sub {
    font-size: clamp(16px, 1.65vw, 18.5px); font-weight: 500; color: #475569;
    line-height: 1.65; max-width: 700px; margin: 0 auto;
  }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     INTEGRATED HERO CARDS COMPONENT
     (Ported from the HTML UI component â€” two-column layout)
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */

  /* CSS variables scoped to this component */
  .gc-hero-cards__container {
    --hc-bg: #f4f3ee;
    --hc-ink: #111827;
    --hc-ink-soft: #475569;
    --hc-ink-muted: #94a3b8;
    --hc-indigo: #6366f1;
    --hc-violet: #8b5cf6;
    --hc-card-bg: rgba(255,255,255,0.92);
    --hc-card-border: rgba(148,163,184,0.18);
    --hc-shadow-card: 0 30px 80px rgba(15,23,42,0.12), 0 4px 16px rgba(15,23,42,0.06);
    --hc-shadow-hover: 0 40px 100px rgba(15,23,42,0.16), 0 8px 24px rgba(15,23,42,0.08);

    display: grid;
    grid-template-columns: 42fr 58fr;
    align-items: center;
    gap: 48px;
    padding: 0 0 56px;
    position: relative;
    /* Subtle grid background behind cards */
    background-image: repeating-linear-gradient(
      90deg,
      rgba(99,102,241,0.03) 0px,
      rgba(99,102,241,0.03) 1px,
      transparent 1px,
      transparent 72px
    );
    background-size: 72px 100%;
    border-radius: 32px;
  }

  /* â”€â”€ Left copy column â”€â”€ */
  .gc-hero-cards__left {
    display: flex;
    flex-direction: column;
    gap: 26px;
    padding: 8px 0;
  }

  .gc-hero-cards__eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px 6px 8px;
    background: rgba(99,102,241,0.09);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--hc-indigo);
    width: fit-content;
  }

  .gc-hero-cards__eyebrow-dot {
    width: 6px; height: 6px;
    background: var(--hc-indigo);
    border-radius: 50%;
    animation: gc-pulse 2s ease-in-out infinite;
    flex-shrink: 0;
  }

  .gc-hero-cards__headline {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: clamp(40px, 5vw, 76px);
    font-weight: 400;
    letter-spacing: -0.03em;
    line-height: 0.95;
    color: var(--hc-ink);
    margin: 0;
  }

  .gc-hero-cards__headline em {
    font-style: italic;
    color: var(--hc-indigo);
  }

  .gc-hero-cards__body {
    font-family: 'DM Sans', system-ui, sans-serif;
    font-size: 17px;
    line-height: 1.65;
    color: var(--hc-ink-soft);
    font-weight: 300;
    max-width: 480px;
    margin: 0;
  }

  .gc-hero-cards__actions {
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
  }

  /* Primary CTA button */
  .gc-hc-btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 14px 20px 14px 28px;
    background: #111827;
    color: #fff;
    border: none;
    border-radius: 999px;
    font-family: 'DM Sans', system-ui, sans-serif;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: -0.01em;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
    box-shadow: 0 2px 12px rgba(15,23,42,0.22);
  }
  .gc-hc-btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(15,23,42,0.28);
    background: #1e293b;
  }

  .gc-hc-btn-primary__arrow {
    width: 32px; height: 32px;
    background: #fff;
    border-radius: 50%;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    transition: transform 0.18s ease;
  }
  .gc-hc-btn-primary:hover .gc-hc-btn-primary__arrow { transform: translateX(2px); }
  .gc-hc-btn-primary__arrow svg { color: #111827; width: 16px; height: 16px; }

  /* Secondary CTA button */
  .gc-hc-btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 14px 28px;
    background: transparent;
    color: #111827;
    border: 1.5px solid rgba(17,24,39,0.25);
    border-radius: 999px;
    font-family: 'DM Sans', system-ui, sans-serif;
    font-size: 15px;
    font-weight: 500;
    letter-spacing: -0.01em;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
  }
  .gc-hc-btn-secondary:hover {
    transform: translateY(-2px);
    border-color: #111827;
    background: rgba(17,24,39,0.04);
  }

  /* â”€â”€ Right cards column â”€â”€ */
  .gc-hero-cards__right {
    position: relative;
    height: 500px;
  }

  /* Base card style */
  .gc-hc-card {
    position: absolute;
    background: var(--hc-card-bg);
    backdrop-filter: blur(20px) saturate(1.6);
    -webkit-backdrop-filter: blur(20px) saturate(1.6);
    border: 1px solid var(--hc-card-border);
    box-shadow: var(--hc-shadow-card);
    border-radius: 28px;
    padding: 28px 30px;
    transition: box-shadow 0.25s ease;
  }
  .gc-hc-card:hover { box-shadow: var(--hc-shadow-hover); }

  /* Card 1 â€” Project Queue: large, behind, tilted left */
  .gc-hc-card--queue {
    width: 520px;
    top: 0; left: 0;
    z-index: 1;
    transform: rotate(-2deg);
    animation:
      hcQueueReveal 0.85s cubic-bezier(0.34,1.2,0.64,1) 0.4s both,
      hcFloatA 7s ease-in-out 1.4s infinite;
  }
  @keyframes hcQueueReveal {
    from { opacity: 0; transform: rotate(-2deg) translateY(32px) scale(0.96); }
    to   { opacity: 1; transform: rotate(-2deg) translateY(0)    scale(1); }
  }
  @keyframes hcFloatA {
    0%,100% { transform: rotate(-2deg) translateY(0px); }
    50%      { transform: rotate(-2deg) translateY(-7px); }
  }

  /* Card 2 â€” Restoration Summary: smaller, front, tilted right, overlaps bottom-right */
  .gc-hc-card--summary {
    width: 380px;
    top: 220px; left: 175px;
    z-index: 2;
    transform: rotate(1.5deg);
    animation:
      hcSummaryReveal 0.85s cubic-bezier(0.34,1.2,0.64,1) 0.65s both,
      hcFloatB 8s ease-in-out 1.8s infinite;
  }
  @keyframes hcSummaryReveal {
    from { opacity: 0; transform: rotate(1.5deg) translateY(32px) scale(0.96); }
    to   { opacity: 1; transform: rotate(1.5deg) translateY(0)    scale(1); }
  }
  @keyframes hcFloatB {
    0%,100% { transform: rotate(1.5deg) translateY(0px); }
    50%      { transform: rotate(1.5deg) translateY(-6px); }
  }

  /* Card internal title */
  .gc-hc-card__title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: var(--hc-ink-muted);
    margin-bottom: 20px;
    font-family: 'DM Sans', system-ui, sans-serif;
  }

  /* â”€â”€ Queue rows (shared between showcase panel and hero cards) â”€â”€ */
  .gc-queue-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 13px 14px;
    border-radius: 16px;
    margin-bottom: 9px;
  }
  .gc-queue-row:last-child { margin-bottom: 0; }

  .gc-queue-row--active {
    background: rgba(99,102,241,0.09);
    border: 1px solid rgba(99,102,241,0.15);
  }

  .gc-queue-row__icon {
    width: 38px; height: 38px;
    border-radius: 11px;
    flex-shrink: 0;
    display: grid;
    place-items: center;
    font-size: 12px; font-weight: 700;
    color: #fff;
    letter-spacing: 0;
    font-family: 'DM Sans', system-ui, sans-serif;
  }
  .gc-queue-row--active .gc-queue-row__icon {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    box-shadow: 0 4px 12px rgba(99,102,241,0.30);
  }
  .gc-queue-row:not(.gc-queue-row--active) .gc-queue-row__icon {
    background: #e9edf5;
    color: #94a3b8;
  }

  .gc-queue-row__meta {
    flex: 1; min-width: 0;
    display: flex; flex-direction: column; gap: 2px;
  }

  .gc-queue-row__label {
    font-size: 14.5px; font-weight: 600;
    color: #111827; letter-spacing: -0.015em;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    font-family: 'DM Sans', system-ui, sans-serif;
  }
  .gc-queue-row--active .gc-queue-row__label { color: #6366f1; }

  .gc-queue-row__sub {
    font-size: 12px; color: #94a3b8;
    font-family: 'DM Sans', system-ui, sans-serif;
  }

  .gc-queue-row__badge {
    flex-shrink: 0;
    font-size: 11px; font-weight: 700;
    font-family: 'DM Mono', monospace;
    color: #6366f1;
    background: rgba(99,102,241,0.12);
    padding: 4px 10px; border-radius: 999px;
    letter-spacing: 0.02em;
  }

  .gc-queue-row__dot {
    flex-shrink: 0;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #dde2ed;
  }

  /* â”€â”€ Summary stat bars â”€â”€ */
  .gc-summary-stat { margin-bottom: 15px; }
  .gc-summary-stat:last-of-type { margin-bottom: 0; }

  .gc-summary-stat__label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 13px; font-weight: 600;
    color: #111827; letter-spacing: -0.01em;
    font-family: 'DM Sans', system-ui, sans-serif;
  }

  .gc-summary-stat__pct {
    font-family: 'DM Mono', monospace;
    font-size: 12px; color: #94a3b8; font-weight: 400;
  }

  .gc-summary-stat__bar-track {
    height: 8px; background: #eaecf1;
    border-radius: 999px; overflow: hidden;
  }

  .gc-summary-stat__bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    width: 0%;
    transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
  }
  .gc-summary-stat__bar-fill.gc-bar--ready {
    width: var(--bar-target, 0%);
  }

  .gc-summary-chip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 20px;
    padding: 13px 16px;
    background: linear-gradient(135deg, rgba(99,102,241,0.07), rgba(139,92,246,0.07));
    border: 1px solid rgba(99,102,241,0.13);
    border-radius: 16px;
  }

  .gc-summary-chip__label {
    font-size: 12.5px; color: #475569; font-weight: 500;
    font-family: 'DM Sans', system-ui, sans-serif;
  }

  .gc-summary-chip__value {
    font-family: 'DM Mono', monospace;
    font-size: 20px; font-weight: 500;
    color: #6366f1; letter-spacing: -0.02em;
  }

  /* â”€â”€ Bottom industry strip â”€â”€ */
  .gc-hero-cards__strip {
    padding-top: 0;
    border-top: 1px solid rgba(148,163,184,0.2);
    padding-top: 40px;
  }

  .gc-hero-cards__strip-label {
    text-align: center;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #94a3b8; margin-bottom: 20px;
    font-family: 'DM Sans', system-ui, sans-serif;
  }

  .gc-hero-cards__strip-row {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    flex-wrap: wrap;
    gap: 0;
  }

  .gc-strip-item {
    padding: 0 36px;
    border-right: 1px solid rgba(148,163,184,0.25);
  }
  .gc-strip-item:last-child { border-right: none; }

  .gc-strip-item__name {
    font-family: 'DM Sans', system-ui, sans-serif;
    font-size: 15px; font-weight: 600;
    letter-spacing: -0.02em;
    color: #b0b8c8;
    transition: color 0.2s ease;
    white-space: nowrap;
  }
  .gc-strip-item:hover .gc-strip-item__name { color: #6366f1; }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     TESTIMONIALS
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .testimonials-section { padding-top: 7rem; padding-bottom: 0; overflow: hidden; position: relative; }
  .testimonials-section::before { content: ''; position: absolute; width: 700px; height: 700px; background: radial-gradient(circle, rgba(99,102,241,0.07) 0%, transparent 65%); top: -100px; left: -200px; border-radius: 50%; filter: blur(80px); pointer-events: none; }
  .testimonials-section::after  { content: ''; position: absolute; width: 500px; height: 500px; background: radial-gradient(circle, rgba(99,102,241,0.06) 0%, transparent 65%); top: 20%; right: -150px; border-radius: 50%; filter: blur(80px); pointer-events: none; }

  .testimonial-top { display: flex; align-items: center; gap: 14px; margin-bottom: 4rem; }
  .testi-avatars { display: flex; align-items: center; }
  .testi-avatars img { width: 36px; height: 36px; border-radius: 50%; border: 2px solid #fff; object-fit: cover; margin-left: -10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  .testi-avatars img:first-child { margin-left: 0; }
  .testi-proof-text { display: flex; flex-direction: column; gap: 2px; }
  .testi-stars { color: #6366f1; font-size: 13px; letter-spacing: 2px; line-height: 1; }
  .testi-proof-text p { font-size: 0.875rem; color: #9ca3af; margin: 0; }
  .testi-proof-text strong { color: #1f2937; font-weight: 600; }

  .testi-outer { position: relative; width: 100%; height: 640px; overflow: hidden; margin-top: 0; }
  .testi-fade-top { position: absolute; top: 0; left: 0; right: 0; height: 130px; z-index: 10; pointer-events: none; background: linear-gradient(to bottom, #fff 0%, transparent 100%); }
  .testi-fade-bot { position: absolute; bottom: 0; left: 0; right: 0; height: 130px; z-index: 10; pointer-events: none; background: linear-gradient(to top, #fff 0%, transparent 100%); }
  .testi-cols { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; max-width: 1180px; margin: 0 auto; padding: 0 1.5rem; height: 100%; }
  .testi-col { display: flex; flex-direction: column; gap: 14px; will-change: transform; }

  @keyframes testi-scroll-up   { from { transform: translateY(0);   } to { transform: translateY(-50%); } }
  @keyframes testi-scroll-down { from { transform: translateY(-50%); } to { transform: translateY(0);   } }

  .testi-col-up   { animation: testi-scroll-up   linear infinite; }
  .testi-col-down { animation: testi-scroll-down linear infinite; }
  .testi-col-slow   { animation-duration: 42s; }
  .testi-col-medium { animation-duration: 36s; }
  .testi-col-fast   { animation-duration: 30s; }
  .testi-col:hover  { animation-play-state: paused; }

  .testi-card { background: rgba(255,255,255,0.75); border: 1px solid rgba(99,102,241,0.1); border-radius: 18px; padding: 20px 18px 18px; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); flex-shrink: 0; transition: transform 0.32s ease, background 0.32s ease, border-color 0.32s ease, box-shadow 0.32s ease; cursor: default; }
  .testi-card:hover { transform: scale(1.03); background: rgba(255,255,255,0.95); border-color: rgba(99,102,241,0.22); box-shadow: 0 0 28px rgba(99,102,241,0.1), 0 8px 32px rgba(0,0,0,0.07); }
  .testi-quote-icon { display: block; font-family: Georgia, 'Times New Roman', serif; font-size: 34px; line-height: 1; color: rgba(99,102,241,0.35); margin-bottom: 8px; }
  .testi-stars-sm   { color: #6366f1; font-size: 11px; letter-spacing: 1.5px; margin-bottom: 8px; }
  .testi-text       { font-size: 13px; line-height: 1.65; color: #4b5563; margin: 0 0 16px; }
  .testi-footer     { display: flex; align-items: center; gap: 10px; }
  .testi-avatar     { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 1.5px solid rgba(99,102,241,0.18); flex-shrink: 0; }
  .testi-info       { display: flex; flex-direction: column; gap: 2px; }
  .testi-name       { font-size: 12.5px; font-weight: 600; color: #1f2937; line-height: 1.2; }
  .testi-role       { font-size: 11px; color: #9ca3af; }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     FAQ
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .lp-faq-section { background: transparent; padding: 64px 24px 72px; font-family: Inter, system-ui, sans-serif; }
  .lp-faq-inner   { max-width: 1080px; margin: 0 auto; }
  .lp-faq-header  { text-align: center; margin-bottom: 56px; }
  .lp-faq-pill { display: inline-block; font-size: 11px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #6366f1; background: rgba(99,102,241,0.09); border: 1px solid rgba(99,102,241,0.18); border-radius: 100px; padding: 5px 16px; margin-bottom: 22px; }
  .lp-faq-title { font-family: 'Space Grotesk', Inter, system-ui, sans-serif; font-weight: 800; font-size: clamp(34px, 4.8vw, 68px); line-height: 1.08; color: #111827; letter-spacing: -0.04em; margin: 0; }
  .lp-faq-title em { font-style: italic; color: #3b3c8a; }
  .lp-faq-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start; }
  .lp-faq-card { background: rgba(255,255,255,0.72); backdrop-filter: blur(18px) saturate(1.4); -webkit-backdrop-filter: blur(18px) saturate(1.4); border-radius: 18px; border: 1.5px solid rgba(255,255,255,0.7); box-shadow: 0 2px 12px rgba(99,102,241,0.07); overflow: hidden; transition: background 0.38s cubic-bezier(0.4,0,0.2,1), box-shadow 0.38s cubic-bezier(0.4,0,0.2,1), border-color 0.38s cubic-bezier(0.4,0,0.2,1), transform 0.38s cubic-bezier(0.4,0,0.2,1); cursor: pointer; }
  .lp-faq-card:hover { background: rgba(255,255,255,0.88); box-shadow: 0 8px 32px rgba(99,102,241,0.13); transform: translateY(-2px); }
  .lp-faq-card.active { background: rgba(255,255,255,0.92); border-color: #1a1a1a; box-shadow: 0 12px 40px rgba(99,102,241,0.18); transform: translateY(-2px); }
  .lp-faq-question { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 22px 22px; }
  .lp-faq-question-text { font-weight: 600; font-size: 15px; color: #111111; line-height: 1.4; flex: 1; user-select: none; }
  .lp-faq-btn { flex-shrink: 0; width: 36px; height: 36px; border-radius: 50%; background: #1a1a1a; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 3px 10px rgba(0,0,0,0.22); transition: background 0.38s cubic-bezier(0.4,0,0.2,1), transform 0.38s cubic-bezier(0.4,0,0.2,1); position: relative; outline: none; }
  .lp-faq-btn::before, .lp-faq-btn::after { content: ''; position: absolute; background: #ffffff; border-radius: 2px; transition: transform 0.38s cubic-bezier(0.4,0,0.2,1), opacity 0.38s cubic-bezier(0.4,0,0.2,1); }
  .lp-faq-btn::before { width: 14px; height: 2px; }
  .lp-faq-btn::after  { width: 2px; height: 14px; }
  .lp-faq-card.active .lp-faq-btn::after { transform: scaleY(0); opacity: 0; }
  .lp-faq-divider { height: 1px; margin: 0 22px; background: rgba(0,0,0,0.07); transform: scaleX(0); transform-origin: left; transition: transform 0.38s cubic-bezier(0.4,0,0.2,1); }
  .lp-faq-card.active .lp-faq-divider { transform: scaleX(1); }
  .lp-faq-answer-wrap { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.38s cubic-bezier(0.4,0,0.2,1); }
  .lp-faq-card.active .lp-faq-answer-wrap { grid-template-rows: 1fr; }
  .lp-faq-answer-inner { overflow: hidden; }
  .lp-faq-answer { padding: 0 22px 22px; font-size: 14px; font-weight: 400; color: #555563; line-height: 1.7; margin: 0; opacity: 0; transform: translateY(-6px); transition: opacity 0.32s ease 0.04s, transform 0.32s ease 0.04s; }
  .lp-faq-card.active .lp-faq-answer { opacity: 1; transform: translateY(0); }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     CTA
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .lp-cta-section { position: relative; background: transparent; padding: 72px 24px 88px; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: Inter, system-ui, sans-serif; border-top: 1px solid rgba(99,102,241,0.08); }
  .lp-cta-orb { position: absolute; width: 520px; height: 520px; border-radius: 50%; background: radial-gradient(circle, rgba(165,168,255,0.18) 0%, transparent 70%); top: -140px; left: 50%; transform: translateX(-50%); pointer-events: none; filter: blur(40px); }
  .lp-cta-content { position: relative; z-index: 1; width: 100%; max-width: 1100px; display: flex; flex-direction: column; align-items: center; text-align: center; }
  .lp-cta-label { display: inline-flex; align-items: center; gap: 8px; font-size: 10.5px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: #6366f1; background: rgba(99,102,241,0.09); border: 1px solid rgba(99,102,241,0.2); border-radius: 100px; padding: 5px 16px; margin-bottom: 28px; animation: lp-fadeUp 0.65s cubic-bezier(0.4,0,0.2,1) both; }
  .lp-cta-heading { font-family: 'Space Grotesk', Inter, system-ui, sans-serif; font-weight: 800; font-size: clamp(34px, 4.8vw, 68px); line-height: 1.08; letter-spacing: -0.04em; color: #111827; max-width: 800px; margin: 0 0 22px; animation: lp-fadeUp 0.7s cubic-bezier(0.4,0,0.2,1) 0.07s both; }
  .lp-cta-heading em { font-style: normal; background: linear-gradient(120deg, #4f46e5, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  .lp-cta-subtitle { font-size: clamp(16px, 1.75vw, 18.5px); color: #475569; line-height: 1.65; max-width: 600px; margin: 0 0 40px; animation: lp-fadeUp 0.7s cubic-bezier(0.4,0,0.2,1) 0.14s both; }
  .lp-cta-buttons { display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; animation: lp-fadeUp 0.7s cubic-bezier(0.4,0,0.2,1) 0.22s both; }
  .lp-cta-btn { display: inline-flex; align-items: center; gap: 9px; font-family: 'DM Sans', sans-serif; font-size: 14.5px; font-weight: 600; border-radius: 100px; padding: 13px 28px; cursor: pointer; border: none; text-decoration: none; letter-spacing: 0.01em; transition: transform 0.22s cubic-bezier(0.4,0,0.2,1), box-shadow 0.22s cubic-bezier(0.4,0,0.2,1), background 0.22s cubic-bezier(0.4,0,0.2,1); white-space: nowrap; }
  .lp-cta-btn-primary   { background: #1a1a1a; color: #fff; box-shadow: 0 4px 18px rgba(0,0,0,0.2); }
  .lp-cta-btn-primary:hover   { background: #2d2d2d; box-shadow: 0 8px 28px rgba(0,0,0,0.26), 0 0 0 4px rgba(99,102,241,0.12); transform: translateY(-2px); }
  .lp-cta-btn-secondary { background: rgba(255,255,255,0.78); color: #2f3340; border: 1.5px solid rgba(30,30,50,0.18); box-shadow: 0 2px 10px rgba(99,102,241,0.07); backdrop-filter: blur(12px); }
  .lp-cta-btn-secondary:hover { background: rgba(255,255,255,0.96); box-shadow: 0 6px 22px rgba(99,102,241,0.13); transform: translateY(-2px); }
  .lp-cta-btn:active { transform: scale(0.97); }
  .lp-cta-divider { width: 100%; height: 1px; background: linear-gradient(90deg, transparent, rgba(99,102,241,0.15), transparent); margin: 56px 0 48px; }
  .lp-cta-cards { width: 100%; display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; animation: lp-fadeUp 0.7s cubic-bezier(0.4,0,0.2,1) 0.3s both; }
  .lp-cta-card { background: rgba(255,255,255,0.72); border: 1.5px solid rgba(255,255,255,0.7); border-radius: 22px; padding: 30px 26px 26px; box-shadow: 0 2px 14px rgba(99,102,241,0.07); backdrop-filter: blur(18px) saturate(1.4); -webkit-backdrop-filter: blur(18px) saturate(1.4); display: flex; flex-direction: column; gap: 14px; text-align: left; transition: transform 0.3s cubic-bezier(0.4,0,0.2,1), box-shadow 0.3s cubic-bezier(0.4,0,0.2,1), background 0.28s cubic-bezier(0.4,0,0.2,1); }
  .lp-cta-card:hover { transform: translateY(-7px); box-shadow: 0 20px 56px rgba(99,102,241,0.18); background: rgba(255,255,255,0.9); }
  .lp-cta-card-icon { width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, rgba(99,102,241,0.11), rgba(99,102,241,0.05)); border: 1.5px solid rgba(99,102,241,0.16); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(99,102,241,0.1); animation: lp-float 3.6s ease-in-out infinite; flex-shrink: 0; }
  .lp-cta-card:nth-child(2) .lp-cta-card-icon { animation-delay: 0.7s; }
  .lp-cta-card:nth-child(3) .lp-cta-card-icon { animation-delay: 1.4s; }
  .lp-cta-card-icon svg  { width: 22px; height: 22px; }
  .lp-cta-card-title { font-weight: 600; font-size: 15.5px; color: #2f3340; line-height: 1.3; }
  .lp-cta-card-text  { font-size: 13.5px; color: #5f6675; line-height: 1.68; }

  @keyframes lp-fadeUp { from { opacity: 0; transform: translateY(22px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes lp-float  { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     RESULTS PAGE
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  .result-section { padding: 3rem 1.5rem; }
  .back-btn { display: flex; align-items: center; gap: 0.4rem; background: none; border: none; color: #9ca3af; font-size: 0.85rem; cursor: pointer; transition: color 0.2s; }
  .back-btn:hover { color: #1f2937; }

  /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
     RESPONSIVE
  â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
  @media (max-width: 1100px) {
    .gc-hc-card--queue   { width: 460px; }
    .gc-hc-card--summary { width: 340px; left: 150px; top: 215px; }
  }

  @media (max-width: 960px) {
    .gc-hero-cards__container {
      grid-template-columns: 1fr;
      gap: 48px;
    }
    .gc-hero-cards__left { order: 1; }
    .gc-hero-cards__right {
      order: 2;
      height: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    /* Override absolute positioning and rotation on tablet/mobile */
    .gc-hc-card {
      position: static !important;
      transform: none !important;
      width: 100% !important;
      animation: gc-fadeUp 0.7s ease 0.4s both !important;
    }
    .gc-hc-card--summary {
      animation-delay: 0.6s !important;
    }
  }

  @media (max-width: 900px) {
    .gc-hero { padding: 80px 20px 48px; }
    .gc-showcase-container { gap: 80px; }
    :global(.gc-row) { grid-template-columns: 1fr; gap: 40px; }
    :global(.gc-row.row-b .gc-visual) { order: -1; }
    .carousel-stage-gc { height: 260px; }
    :global(.slide-gc)                { width: 280px; height: 200px; }
    :global(.slide-gc.pos-left)       { transform: translateX(-230px) scale(0.8) rotateY(14deg) perspective(600px); }
    :global(.slide-gc.pos-right)      { transform: translateX(230px)  scale(0.8) rotateY(-14deg) perspective(600px); }
    :global(.slide-gc.pos-far-left)   { transform: translateX(-420px) scale(0.65); }
    :global(.slide-gc.pos-far-right)  { transform: translateX(420px)  scale(0.65); }
    .testi-cols { grid-template-columns: 1fr 1fr; }
    .testi-col:nth-child(3) { display: none; }
    .lp-faq-grid  { grid-template-columns: 1fr; }
    .lp-cta-cards { grid-template-columns: 1fr 1fr; }
    .lp-cta-cards .lp-cta-card:last-child { grid-column: 1 / -1; max-width: 380px; margin: 0 auto; width: 100%; }
    .gc-showcase-section { padding: 52px 18px 60px; }
    .gc-visual { min-height: 360px; }
    .gc-panel { width: 88%; }
    .gc-btn { align-self: stretch; justify-content: center; }
    .gc-feat-section { padding: 52px 20px 64px; }
  }

  @media (max-width: 640px) {
    .gc-hero { padding: 80px 18px 44px; }
    .gc-upload-card { max-width: 100%; }
    .how-it-works { padding: 52px 18px 56px; }
    .section { padding: 52px 18px; }
    .carousel-stage-gc { height: 230px; }
    :global(.slide-gc) { width: 240px; height: 170px; }
    :global(.slide-gc.pos-left)  { transform: translateX(-180px) scale(0.78) rotateY(12deg) perspective(500px); }
    :global(.slide-gc.pos-right) { transform: translateX(180px)  scale(0.78) rotateY(-12deg) perspective(500px); }
    :global(.slide-gc.pos-far-left)  { transform: translateX(-340px) scale(0.6); }
    :global(.slide-gc.pos-far-right) { transform: translateX(340px)  scale(0.6); }
    .testi-cols { grid-template-columns: 1fr; }
    .testi-col:nth-child(2), .testi-col:nth-child(3) { display: none; }
    .testi-outer { height: 520px; }
    .lp-faq-section { padding: 52px 18px 68px; }
    .lp-cta-cards { grid-template-columns: 1fr; }
    .lp-cta-cards .lp-cta-card:last-child { grid-column: auto; max-width: none; }
    .lp-cta-buttons { flex-direction: column; width: 100%; max-width: 320px; }
    .lp-cta-btn { justify-content: center; }
    .gc-feat-section { padding: 48px 16px 60px; }
    .gc-hero-cards__container { padding: 0 0 40px; }
    .gc-strip-item { padding: 0 18px; }
    .gc-strip-item__name { font-size: 13px; }
  }
</style>


