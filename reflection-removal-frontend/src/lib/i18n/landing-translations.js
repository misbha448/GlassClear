export const landingTranslations = {
  en: {
    common: { expand: 'Expand', collapse: 'Collapse' },
    navbar: { pro: 'Pro' },
    navbarMenu: {
      features: {
        coreTools: 'Core Tools',
        workflow: 'Workflow',
        removeReflection: { title: 'Remove Reflection', description: 'Clean glare and glass reflections from architectural photos.' },
        batch: { title: 'Batch Processing', description: 'Process multiple images safely in one queue.' },
        albums: { title: 'Smart Albums', description: 'Auto-organize restored results into useful collections.' },
        history: { title: 'History', description: 'Review every processed result from your workspace.' },
        cta: { title: 'Start a New Upload', description: 'Open the GlassClear uploader and restore your next image.' }
      },
      products: {
        workspace: 'Workspace',
        collections: 'Collections',
        dashboard: { title: 'Dashboard', description: 'Manage processing, previews, and saved results in one place.' },
        upload: { title: 'Upload Image', description: 'Start reflection removal with a fresh architectural image.' },
        albums: { title: 'Smart Albums', description: 'Browse your organized image collections.' },
        history: { title: 'Results History', description: 'Revisit completed restorations and exports.' },
        cta: { title: 'Open Dashboard', description: 'Jump into your GlassClear workspace and continue editing.' }
      },
      resources: {
        learn: 'Learn',
        help: 'Help',
        how: { title: 'How It Works', description: 'Understand the reflection removal workflow.' },
        demo: { title: 'See It in Action', description: 'View before-after restoration examples.' },
        faq: { title: 'FAQ', description: 'Common questions about GlassClear.' },
        guide: { title: 'Upload Guide', description: 'Go straight to the uploader and start a new restoration.' },
        cta: { title: 'Try the Demo Flow', description: 'Scroll to the live showcase and preview the restoration experience.' }
      }
    },
    dashboardUi: {
      zoomOut: 'Zoom -',
      zoomIn: 'Zoom +',
      fit: 'Fit',
      loadingWorkspace: 'Loading workspace...',
      preparingWorkspace: 'Preparing your editor state.',
      noOutput: 'No output yet',
      noImage: 'No image available',
      openImage: 'Open an image to start editing.',
      processedPreview: 'Processed preview for',
      originalPreview: 'Original preview for',
      projects: 'Projects',
      projectsHelp: 'Save your current result or attach it to an existing project.',
      saving: 'Saving...',
      saveCurrentResult: 'Save Current Result',
      createProject: 'Create Project',
      recentProjects: 'Recent Projects',
      recentProjectsHelp: 'Reuse your existing delivery spaces.',
      noProjects: 'No projects yet. Create your first project to save dashboard results.'
    },
    adminUi: {
      dashboard: 'Admin Dashboard',
      toggleSidebar: 'Toggle sidebar',
      sections: 'Admin sections'
    },
    landing: {
      hero: {
        badge: 'AI-Powered · Real-Time · No Signup',
        titleLine1: 'Automated Glare &',
        titleLine2: 'Reflection Elimination',
        titleLine3: 'For Architectural Photography',
        subtitleLine1: 'AI-powered glare and reflection removal designed for architectural photography.',
        subtitleLine2: 'Clean, sharp, and professional results. No Photoshop required.',
        cta: 'Remove Reflections Now'
      },
      upload: { drop: 'Drop your image here', browse: 'browse from device', hint: 'JPG, PNG, WEBP up to 50MB' },
      how: {
        label: 'HOW IT WORKS',
        title: 'Simple, Fast, Reflection-Free',
        subtitle: 'Upload an architectural image, let GlassClear remove reflections, then compare and export a clean professional result.',
        step1: { title: 'Upload Image', desc: 'Choose a glass facade, interior, or window reflection photo from your device.', note: 'Supports JPG, PNG, WEBP, and high-resolution image files.' },
        step2: { title: 'AI Restoration', desc: 'GlassClear detects glare and reflection artifacts, then reconstructs a cleaner architectural image.', note: 'Smart processing preserves structure, edges, and natural lighting balance.' },
        step3: { title: 'Compare, Save & Export', desc: 'Preview the before-after result, save it to history, share it, or export in high quality.', note: 'Available in PNG, JPG, and HD export quality.' }
      },
      showcase: {
        workspace: {
          label: 'GlassClear Workspace',
          titleLine1: 'Process reflection-heavy images in one',
          titleEmphasis: 'clean',
          titleLine2: 'workspace',
          body: 'Upload architectural photos, track restoration progress, and manage every GlassClear output from a simple AI-powered workspace.',
          cta: 'Explore Workspace',
          statusDone: 'Reflection removed',
          statusProcessing: 'Processing',
          statusQueued: 'In queue',
          badgeQueued: 'Queued',
          statusReady: 'Ready to export',
          badgeReady: 'Output ready'
        },
        albums: {
          label: 'Smart Organization',
          titleLine1: 'Organize every restored result with',
          titleEmphasis: 'smart albums',
          body: 'GlassClear groups processed images into indoor, outdoor, glass facade, and high-glare collections so your project history stays clean and easy to review.',
          cta: 'View Smart Albums',
          panelTitle: 'Smart Albums',
          latest: 'Latest',
          images: 'images'
        }
      },
      carousel: {
        label: 'SEE IT IN ACTION',
        title: 'Clarity you can see',
        subtitle: 'From storefront glass to office interiors, our AI handles every reflection scenario.',
        previous: 'Previous slide',
        next: 'Next slide',
        slide1: { title: 'Glass Building Reflection Removal', subtitle: 'Architectural Photography' },
        slide2: { title: 'Window Glare Correction', subtitle: 'Real Estate Imaging' },
        slide3: { title: 'Screen Clarity Enhancement', subtitle: 'Product Photography' },
        slide4: { title: 'Skylight Transparency Restore', subtitle: 'Interior Design Shoots' },
        slide5: { title: 'Facade Haze Removal', subtitle: 'Urban Architecture' },
        slide6: { title: 'Office Glass Deglare', subtitle: 'Corporate Interiors' }
      },
      features: {
        eyebrow: 'GlassClear Features',
        titleLine1: 'Designed to Make',
        titleLine2: 'Restoration Effortless',
        subtitle: 'A cleaner, smarter workspace for processing, organizing, and sharing reflection-free architectural images.',
        panelEyebrow: 'AI-Powered Glass Restoration',
        headlineLine1: 'Professional',
        headlineEmphasis: 'clarity',
        headlineLine2: 'for',
        headlineLine3: 'architectural',
        headlineLine4: 'visuals',
        body: 'GlassClear helps architects, real-estate teams, and visual creators restore reflection-heavy images into clean, client-ready results without manual editing.',
        start: 'Start Restoring',
        workflow: 'View Workflow',
        queueTitle: 'Project Queue',
        summaryTitle: 'Restoration Summary',
        queue1: { title: 'Facade Cleanup', sub: 'Uploading output · 3 assets' },
        queue2: { title: 'Interior Glass Shot', sub: 'Queued · 2 assets' },
        queue3: { title: 'Client Preview', sub: 'Queued · 5 assets' },
        summary1: { label: 'Reflection Reduced' },
        summary2: { label: 'Export Ready' },
        summary3: { label: 'Before / After' },
        summaryChip: 'Avg cleanup time',
        trustedLabel: 'Trusted across industries',
        industry1: 'Architects',
        industry2: 'Real Estate',
        industry3: 'Interior Studios',
        industry4: 'Visual Creators',
        industry5: 'Client Delivery'
      },
      testimonials: {
        label: 'What people are saying',
        title: 'Trusted by Creators Who Demand Clarity',
        subtitle: 'From photographers to real estate teams, GlassClear transforms reflections into crystal-clear visuals.',
        proofPrefix: 'Loved by',
        proofSuffix: 'creators worldwide',
        1: { quote: 'GlassClear literally saved my architectural shots. Reflections were ruining everything, and this fixed it in seconds.', role: 'Architectural Photographer' },
        2: { quote: 'The AI is insanely accurate. It removes reflections without touching the original details. That is rare.', role: 'Visual Designer' },
        3: { quote: 'I used to spend hours in Photoshop. Now it is literally one click. Game changer.', role: 'Real Estate Editor' },
        4: { quote: 'What impressed me most is how natural the output looks. No artifacts, no weird patches.', role: 'Content Creator' },
        5: { quote: 'The reflection removal is not just good, it is smart. It understands the scene.', role: 'AI Research Student' },
        6: { quote: 'Clean UI, fast processing, and crazy accurate results. This feels like a premium tool.', role: 'Product Designer' },
        7: { quote: 'Tried multiple tools, but GlassClear gives the most consistent results across different lighting conditions.', role: 'Freelance Photographer' },
        8: { quote: 'The confidence score and AI insights actually make me trust the output more.', role: 'UX Researcher' },
        9: { quote: 'It does not just remove reflections, it restores the image. That is the difference.', role: 'Media Editor' },
        10: { quote: 'I love how fast everything is. Upload, process, done. No friction at all.', role: 'Digital Marketer' },
        11: { quote: 'The AI story feature is surprisingly useful. It explains what actually happened in the image.', role: 'Student Developer' },
        12: { quote: 'Feels like something Apple would build if they worked on image clarity tools.', role: 'Creative Director' }
      },
      faq: {
        ariaLabel: 'Frequently Asked Questions',
        label: 'FAQ',
        titleLine1: 'Frequently Asked',
        titleLine2: 'Questions',
        1: { question: 'What is GlassClear?', answer: 'GlassClear is an AI-powered reflection removal system designed for architectural photography. It removes glare, window reflections, and glass artifacts while preserving building details and visual clarity.' },
        2: { question: 'Do I need technical skills to use it?', answer: 'No. Just upload an image, let the AI process it, and download the restored result. Logged-in users also get history, sharing, batch processing, and smart albums.' },
        3: { question: 'What type of images work best?', answer: 'GlassClear works best with architectural photos, glass facades, windows, interiors, real estate images, and outdoor building shots affected by glare or reflection.' },
        4: { question: 'Can I process multiple images at once?', answer: 'Yes. Logged-in users can use batch processing to upload multiple images together, and GlassClear handles them safely one by one.' },
        5: { question: 'Will image quality improve after removal?', answer: 'GlassClear focuses on reducing reflections while keeping lines, textures, and details natural. Extra quality enhancement can be added after reflection removal.' },
        6: { question: 'Is my data secure?', answer: 'Uploaded images stay linked to the user account and can only be accessed by the logged-in user. Shared links are created only when the user chooses to share a result.' }
      },
      cta: {
        ariaLabel: 'Try GlassClear',
        label: 'Try GlassClear',
        titleLine1: 'Ready to remove',
        titleEmphasis: 'reflections',
        titleLine2: 'from your architectural photos?',
        subtitle: 'Upload a glass, window, or facade image and let GlassClear generate a cleaner, reflection-reduced result in seconds.',
        primary: 'Upload Your Image',
        secondary: 'View Sample Result',
        card1: { title: 'AI Reflection Removal', text: 'Remove glare, window reflections, and glass artifacts from architectural images with precision AI restoration.' },
        card2: { title: 'Batch Processing', text: 'Process multiple building photos safely with controlled queue-based restoration in one workflow.' },
        card3: { title: 'Smart Albums', text: 'Organize restored results into indoor, outdoor, facade, and high-glare collections automatically.' }
      }
    }
  },
  hi: {
    common: { expand: 'खोलें', collapse: 'समेटें' },
    navbar: { pro: 'प्रो' },
    adminUi: { dashboard: 'एडमिन डैशबोर्ड', toggleSidebar: 'साइडबार बदलें', sections: 'एडमिन सेक्शन' },
    dashboardUi: { zoomOut: 'ज़ूम -', zoomIn: 'ज़ूम +', fit: 'फिट', loadingWorkspace: 'वर्कस्पेस लोड हो रहा है...', preparingWorkspace: 'आपका एडिटर तैयार किया जा रहा है।', noOutput: 'अभी आउटपुट नहीं है', noImage: 'कोई इमेज उपलब्ध नहीं है', openImage: 'एडिट शुरू करने के लिए इमेज खोलें।', processedPreview: 'प्रोसेस्ड प्रीव्यू', originalPreview: 'ओरिजिनल प्रीव्यू', projects: 'प्रोजेक्ट्स', projectsHelp: 'अपना मौजूदा रिजल्ट सेव करें या किसी प्रोजेक्ट में जोड़ें।', saving: 'सेव हो रहा है...', saveCurrentResult: 'मौजूदा रिजल्ट सेव करें', createProject: 'प्रोजेक्ट बनाएं', recentProjects: 'हाल के प्रोजेक्ट्स', recentProjectsHelp: 'अपने मौजूदा डिलीवरी स्पेस दोबारा इस्तेमाल करें।', noProjects: 'अभी कोई प्रोजेक्ट नहीं है।' },
    landing: {
      hero: { badge: 'AI-संचालित · रियल-टाइम · बिना साइनअप', titleLine1: 'ऑटोमेटेड ग्लेयर और', titleLine2: 'रिफ्लेक्शन हटाना', titleLine3: 'आर्किटेक्चरल फोटोग्राफी के लिए', subtitleLine1: 'आर्किटेक्चरल फोटोग्राफी के लिए AI-संचालित ग्लेयर और रिफ्लेक्शन रिमूवल।', subtitleLine2: 'साफ, शार्प और प्रोफेशनल रिजल्ट। Photoshop की जरूरत नहीं।', cta: 'अभी रिफ्लेक्शन हटाएँ' },
      upload: { drop: 'अपनी इमेज यहाँ छोड़ें', browse: 'डिवाइस से चुनें', hint: 'JPG, PNG, WEBP, अधिकतम 50MB' },
      how: { label: 'यह कैसे काम करता है', title: 'सरल, तेज और रिफ्लेक्शन-फ्री', subtitle: 'आर्किटेक्चरल इमेज अपलोड करें, GlassClear से रिफ्लेक्शन हटवाएँ, फिर साफ रिजल्ट को तुलना करके एक्सपोर्ट करें।', step1: { title: 'इमेज अपलोड करें', desc: 'अपने डिवाइस से ग्लास फेसाड, इंटीरियर या विंडो रिफ्लेक्शन फोटो चुनें।', note: 'JPG, PNG, WEBP और हाई-रिजॉल्यूशन इमेज फाइलें सपोर्टेड हैं।' }, step2: { title: 'AI रिस्टोरेशन', desc: 'GlassClear ग्लेयर और रिफ्लेक्शन आर्टिफैक्ट्स पहचानकर साफ आर्किटेक्चरल इमेज बनाता है।', note: 'स्मार्ट प्रोसेसिंग स्ट्रक्चर, एज और नेचुरल लाइट बैलेंस को सुरक्षित रखती है।' }, step3: { title: 'तुलना, सेव और एक्सपोर्ट', desc: 'पहले और बाद का रिजल्ट देखें, हिस्ट्री में सेव करें, शेयर करें या हाई क्वालिटी में एक्सपोर्ट करें।', note: 'PNG, JPG और HD क्वालिटी में उपलब्ध।' } },
      showcase: { workspace: { label: 'GlassClear वर्कस्पेस', titleLine1: 'रिफ्लेक्शन वाली इमेज को एक', titleEmphasis: 'साफ', titleLine2: 'वर्कस्पेस में प्रोसेस करें', body: 'आर्किटेक्चरल फोटो अपलोड करें, रिस्टोरेशन प्रोग्रेस ट्रैक करें और हर GlassClear आउटपुट को एक आसान AI वर्कस्पेस में मैनेज करें।', cta: 'वर्कस्पेस देखें', statusDone: 'रिफ्लेक्शन हट गया', statusProcessing: 'प्रोसेस हो रहा है', statusQueued: 'क्यू में', badgeQueued: 'क्यू में', statusReady: 'एक्सपोर्ट के लिए तैयार', badgeReady: 'आउटपुट तैयार' }, albums: { label: 'स्मार्ट ऑर्गनाइजेशन', titleLine1: 'हर रिस्टोर किए गए रिजल्ट को', titleEmphasis: 'स्मार्ट एल्बम्स के साथ', body: 'GlassClear प्रोसेस की गई इमेज को इंडोर, आउटडोर, ग्लास फेसाड और हाई-ग्लेयर कलेक्शन में रखता है।', cta: 'स्मार्ट एल्बम देखें', panelTitle: 'स्मार्ट एल्बम', latest: 'नवीनतम', images: 'इमेज' } },
      carousel: { label: 'इसे काम करते देखें', title: 'स्पष्टता जो आप देख सकें', subtitle: 'स्टोरफ्रंट ग्लास से ऑफिस इंटीरियर तक, हमारा AI हर रिफ्लेक्शन सीन संभालता है।', previous: 'पिछली स्लाइड', next: 'अगली स्लाइड', slide1: { title: 'ग्लास बिल्डिंग रिफ्लेक्शन रिमूवल', subtitle: 'आर्किटेक्चरल फोटोग्राफी' }, slide2: { title: 'विंडो ग्लेयर करेक्शन', subtitle: 'रियल एस्टेट इमेजिंग' }, slide3: { title: 'स्क्रीन क्लैरिटी एन्हांसमेंट', subtitle: 'प्रोडक्ट फोटोग्राफी' }, slide4: { title: 'स्कायलाइट ट्रांसपेरेंसी रिस्टोर', subtitle: 'इंटीरियर डिजाइन शूट्स' }, slide5: { title: 'फेसाड हेज रिमूवल', subtitle: 'अर्बन आर्किटेक्चर' }, slide6: { title: 'ऑफिस ग्लास डीग्लेयर', subtitle: 'कॉर्पोरेट इंटीरियर्स' } },
      features: { eyebrow: 'GlassClear फीचर्स', titleLine1: 'रिस्टोरेशन को बनाए', titleLine2: 'बिलकुल आसान', subtitle: 'रिफ्लेक्शन-फ्री आर्किटेक्चरल इमेज को प्रोसेस, व्यवस्थित और शेयर करने के लिए साफ वर्कस्पेस।', panelEyebrow: 'AI-संचालित ग्लास रिस्टोरेशन', headlineLine1: 'प्रोफेशनल', headlineEmphasis: 'क्लैरिटी', headlineLine2: 'के लिए', headlineLine3: 'आर्किटेक्चरल', headlineLine4: 'विजुअल्स', body: 'GlassClear आर्किटेक्ट्स, रियल एस्टेट टीम्स और विजुअल क्रिएटर्स को बिना मैनुअल एडिटिंग के क्लाइंट-रेडी रिजल्ट देता है।', start: 'रिस्टोर शुरू करें', workflow: 'वर्कफ्लो देखें', queueTitle: 'प्रोजेक्ट क्यू', summaryTitle: 'रिस्टोरेशन सारांश', queue1: { title: 'फेसाड क्लीनअप', sub: 'आउटपुट अपलोड हो रहा है · 3 एसेट्स' }, queue2: { title: 'इंटीरियर ग्लास शॉट', sub: 'क्यू में · 2 एसेट्स' }, queue3: { title: 'क्लाइंट प्रीव्यू', sub: 'क्यू में · 5 एसेट्स' }, summary1: { label: 'रिफ्लेक्शन कम हुआ' }, summary2: { label: 'एक्सपोर्ट तैयार' }, summary3: { label: 'पहले / बाद में' }, summaryChip: 'औसत क्लीनअप समय', trustedLabel: 'कई इंडस्ट्री में भरोसेमंद', industry1: 'आर्किटेक्ट्स', industry2: 'रियल एस्टेट', industry3: 'इंटीरियर स्टूडियो', industry4: 'विजुअल क्रिएटर्स', industry5: 'क्लाइंट डिलीवरी' },
      testimonials: { label: 'लोग क्या कह रहे हैं', title: 'स्पष्टता चाहने वाले क्रिएटर्स का भरोसा', subtitle: 'फोटोग्राफर से रियल एस्टेट टीम्स तक, GlassClear रिफ्लेक्शन को साफ विजुअल्स में बदल देता है।', proofPrefix: 'पसंद किया गया', proofSuffix: 'क्रिएटर्स द्वारा दुनिया भर में', 1: { quote: 'GlassClear ने सच में मेरी आर्किटेक्चरल फोटो बचा लीं।', role: 'आर्किटेक्चरल फोटोग्राफर' }, 2: { quote: 'AI बहुत सटीक है। यह डिटेल्स को छुए बिना रिफ्लेक्शन हटाता है।', role: 'विजुअल डिजाइनर' }, 3: { quote: 'मैं पहले Photoshop में घंटों लगाता था। अब बस एक क्लिक।', role: 'रियल एस्टेट एडिटर' }, 4: { quote: 'आउटपुट बहुत नेचुरल लगता है।', role: 'कंटेंट क्रिएटर' }, 5: { quote: 'यह सिर्फ अच्छा नहीं, स्मार्ट भी है।', role: 'AI रिसर्च स्टूडेंट' }, 6: { quote: 'साफ UI, तेज प्रोसेसिंग और शानदार सटीकता।', role: 'प्रोडक्ट डिजाइनर' }, 7: { quote: 'GlassClear अलग-अलग लाइटिंग में स्थिर रिजल्ट देता है।', role: 'फ्रीलांस फोटोग्राफर' }, 8: { quote: 'कॉन्फिडेंस स्कोर आउटपुट पर भरोसा बढ़ाता है।', role: 'UX रिसर्चर' }, 9: { quote: 'यह इमेज को रिस्टोर करता है।', role: 'मीडिया एडिटर' }, 10: { quote: 'सब कुछ बहुत तेज है।', role: 'डिजिटल मार्केटर' }, 11: { quote: 'AI स्टोरी फीचर सच में काम का है।', role: 'स्टूडेंट डेवलपर' }, 12: { quote: 'यह बहुत प्रीमियम लगता है।', role: 'क्रिएटिव डायरेक्टर' } },
      faq: { ariaLabel: 'अक्सर पूछे जाने वाले सवाल', label: 'FAQ', titleLine1: 'अक्सर पूछे जाने वाले', titleLine2: 'सवाल', 1: { question: 'GlassClear क्या है?', answer: 'GlassClear आर्किटेक्चरल फोटोग्राफी के लिए AI-संचालित रिफ्लेक्शन रिमूवल सिस्टम है।' }, 2: { question: 'क्या तकनीकी स्किल चाहिए?', answer: 'नहीं। बस इमेज अपलोड करें और रिजल्ट डाउनलोड करें।' }, 3: { question: 'किस तरह की इमेज काम करती हैं?', answer: 'आर्किटेक्चरल, ग्लास फेसाड, विंडो और रियल एस्टेट इमेज अच्छी तरह काम करती हैं।' }, 4: { question: 'क्या कई इमेज साथ में प्रोसेस कर सकता हूँ?', answer: 'हाँ, लॉग-इन यूजर बैच प्रोसेसिंग इस्तेमाल कर सकते हैं।' }, 5: { question: 'क्या क्वालिटी बेहतर होगी?', answer: 'यह रिफ्लेक्शन कम करते हुए डिटेल्स को नेचुरल रखता है।' }, 6: { question: 'क्या डेटा सुरक्षित है?', answer: 'अपलोड की गई इमेज आपके अकाउंट से जुड़ी रहती हैं।' } },
      cta: { ariaLabel: 'GlassClear आज़माएँ', label: 'GlassClear आज़माएँ', titleLine1: 'क्या आप', titleEmphasis: 'रिफ्लेक्शन', titleLine2: 'अपनी आर्किटेक्चरल फोटो से हटाना चाहते हैं?', subtitle: 'ग्लास, विंडो या फेसाड इमेज अपलोड करें और GlassClear से सेकंड्स में साफ रिजल्ट पाएँ।', primary: 'अपनी इमेज अपलोड करें', secondary: 'सैंपल रिजल्ट देखें', card1: { title: 'AI रिफ्लेक्शन रिमूवल', text: 'आर्किटेक्चरल इमेज से ग्लेयर, विंडो रिफ्लेक्शन और ग्लास आर्टिफैक्ट्स हटाएँ।' }, card2: { title: 'बैच प्रोसेसिंग', text: 'कई बिल्डिंग फोटो को सुरक्षित वर्कफ्लो में प्रोसेस करें।' }, card3: { title: 'स्मार्ट एल्बम', text: 'रिस्टोर किए गए रिजल्ट को उपयोगी कलेक्शन में रखें।' } }
    }
  },
  kn: {
    common: { expand: 'ತೆರೆಯಿರಿ', collapse: 'ಮುಚ್ಚಿರಿ' },
    navbar: { pro: 'ಪ್ರೋ' },
    adminUi: { dashboard: 'ಅಡ್ಮಿನ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್', toggleSidebar: 'ಸೈಡ್‌ಬಾರ್ ಬದಲಿಸಿ', sections: 'ಅಡ್ಮಿನ್ ವಿಭಾಗಗಳು' },
    dashboardUi: { zoomOut: 'ಜೂಮ್ -', zoomIn: 'ಜೂಮ್ +', fit: 'ಫಿಟ್', loadingWorkspace: 'ಕಾರ್ಯಕ್ಷೇತ್ರ ಲೋಡ್ ಆಗುತ್ತಿದೆ...', preparingWorkspace: 'ನಿಮ್ಮ ಎಡಿಟರ್ ಸಿದ್ಧವಾಗುತ್ತಿದೆ.', noOutput: 'ಇನ್ನೂ ಔಟ್‌ಪುಟ್ ಇಲ್ಲ', noImage: 'ಚಿತ್ರ ಲಭ್ಯವಿಲ್ಲ', openImage: 'ಎಡಿಟ್ ಮಾಡಲು ಚಿತ್ರ ತೆರೆಯಿರಿ.', processedPreview: 'ಪ್ರೊಸೆಸ್ಡ್ ಪ್ರಿವ್ಯೂ', originalPreview: 'ಮೂಲ ಪ್ರಿವ್ಯೂ', projects: 'ಪ್ರಾಜೆಕ್ಟ್‌ಗಳು', projectsHelp: 'ನಿಮ್ಮ ಇತ್ತೀಚಿನ ಫಲಿತಾಂಶವನ್ನು ಉಳಿಸಿ ಅಥವಾ ಪ್ರಾಜೆಕ್ಟ್‌ಗೆ ಸೇರಿಸಿ.', saving: 'ಉಳಿಸಲಾಗುತ್ತಿದೆ...', saveCurrentResult: 'ಪ್ರಸ್ತುತ ಫಲಿತಾಂಶ ಉಳಿಸಿ', createProject: 'ಪ್ರಾಜೆಕ್ಟ್ ರಚಿಸಿ', recentProjects: 'ಇತ್ತೀಚಿನ ಪ್ರಾಜೆಕ್ಟ್‌ಗಳು', recentProjectsHelp: 'ಈಗಿರುವ ಡೆಲಿವರಿ ಸ್ಪೇಸ್‌ಗಳನ್ನು ಮರುಬಳಸಿ.', noProjects: 'ಇನ್ನೂ ಯಾವುದೇ ಪ್ರಾಜೆಕ್ಟ್ ಇಲ್ಲ.' },
    landing: {
      hero: { badge: 'AI ಆಧಾರಿತ · ರಿಯಲ್-ಟೈಮ್ · ಸೈನ್‌ಅಪ್ ಬೇಡ', titleLine1: 'ಸ್ವಯಂಚಾಲಿತ ಗ್ಲೇರ್ ಮತ್ತು', titleLine2: 'ಪ್ರತಿಫಲನ ತೆಗೆದುಹಾಕುವುದು', titleLine3: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಫೋಟೋಗ್ರಫಿಗಾಗಿ', subtitleLine1: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಫೋಟೋಗ್ರಫಿಗಾಗಿ AI ಆಧಾರಿತ ಗ್ಲೇರ್ ಮತ್ತು ಪ್ರತಿಫಲನ ನಿವಾರಣೆ.', subtitleLine2: 'ಸ್ವಚ್ಛ, ಶಾರ್ಪ್ ಮತ್ತು ಪ್ರೊಫೆಷನಲ್ ಫಲಿತಾಂಶಗಳು. Photoshop ಬೇಕಾಗಿಲ್ಲ.', cta: 'ಈಗ ಪ್ರತಿಫಲನ ತೆಗೆದುಹಾಕಿ' },
      upload: { drop: 'ನಿಮ್ಮ ಚಿತ್ರವನ್ನು ಇಲ್ಲಿ ಬಿಡಿ', browse: 'ಡಿವೈಸ್‌ನಿಂದ ಆಯ್ಕೆಮಾಡಿ', hint: 'JPG, PNG, WEBP, ಗರಿಷ್ಠ 50MB' },
      how: { label: 'ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ', title: 'ಸರಳ, ವೇಗವಾದ, ಪ್ರತಿಫಲನರಹಿತ', subtitle: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಚಿತ್ರವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ, GlassClear ಪ್ರತಿಫಲನ ತೆಗೆದುಹಾಕಲಿ, ನಂತರ ಸ್ವಚ್ಛ ಫಲಿತಾಂಶವನ್ನು ಹೋಲಿಸಿ ಎಕ್ಸ್ಪೋರ್ಟ್ ಮಾಡಿ.', step1: { title: 'ಚಿತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ', desc: 'ನಿಮ್ಮ ಡಿವೈಸ್‌ನಿಂದ ಗ್ಲಾಸ್ ಫಸಾಡ್, ಇಂಟೀರಿಯರ್ ಅಥವಾ ವಿಂಡೋ ಪ್ರತಿಫಲನ ಫೋಟೋ ಆಯ್ಕೆಮಾಡಿ.', note: 'JPG, PNG, WEBP ಮತ್ತು ಹೈ-ರೆಸಲ್ಯೂಷನ್ ಫೈಲ್‌ಗಳು ಬೆಂಬಲಿತ.' }, step2: { title: 'AI ರಿಸ್ಟೋರೇಶನ್', desc: 'GlassClear ಗ್ಲೇರ್ ಮತ್ತು ಪ್ರತಿಫಲನ ದೋಷಗಳನ್ನು ಗುರುತಿಸಿ ಸ್ವಚ್ಛ ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಚಿತ್ರವನ್ನು ಸೃಷ್ಟಿಸುತ್ತದೆ.', note: 'ಸ್ಮಾರ್ಟ್ ಪ್ರೊಸೆಸಿಂಗ್ ರಚನೆ, ಅಂಚು ಮತ್ತು ಬೆಳಕು ಸಮತೋಲನವನ್ನು ಉಳಿಸುತ್ತದೆ.' }, step3: { title: 'ಹೋಲಿಸಿ, ಉಳಿಸಿ ಮತ್ತು ಎಕ್ಸ್ಪೋರ್ಟ್ ಮಾಡಿ', desc: 'ಮೊದಲು ಮತ್ತು ನಂತರದ ಫಲಿತಾಂಶ ನೋಡಿ, ಇತಿಹಾಸದಲ್ಲಿ ಉಳಿಸಿ, ಹಂಚಿಕೊಳ್ಳಿ ಅಥವಾ ಹೈ ಕ್ವಾಲಿಟಿಯಲ್ಲಿ ಎಕ್ಸ್ಪೋರ್ಟ್ ಮಾಡಿ.', note: 'PNG, JPG ಮತ್ತು HD ಗುಣಮಟ್ಟದಲ್ಲಿ ಲಭ್ಯ.' } },
      showcase: { workspace: { label: 'GlassClear ಕಾರ್ಯಕ್ಷೇತ್ರ', titleLine1: 'ಪ್ರತಿಫಲನ ಇರುವ ಚಿತ್ರಗಳನ್ನು ಒಂದು', titleEmphasis: 'ಸ್ವಚ್ಛ', titleLine2: 'ಕಾರ್ಯಕ್ಷೇತ್ರದಲ್ಲಿ ಪ್ರೊಸೆಸ್ ಮಾಡಿ', body: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಫೋಟೋಗಳನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ, ಪ್ರಗತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ ಮತ್ತು ಪ್ರತಿಯೊಂದು GlassClear ಔಟ್‌ಪುಟ್ ಅನ್ನು AI ಕಾರ್ಯಕ್ಷೇತ್ರದಲ್ಲಿ ನಿರ್ವಹಿಸಿ.', cta: 'ಕಾರ್ಯಕ್ಷೇತ್ರ ನೋಡಿ', statusDone: 'ಪ್ರತಿಫಲನ ತೆಗೆದಿದೆ', statusProcessing: 'ಪ್ರೊಸೆಸಿಂಗ್', statusQueued: 'ಕ್ಯೂನಲ್ಲಿ', badgeQueued: 'ಕ್ಯೂನಲ್ಲಿ', statusReady: 'ಎಕ್ಸ್ಪೋರ್ಟ್‌ಗೆ ಸಿದ್ಧ', badgeReady: 'ಔಟ್‌ಪುಟ್ ಸಿದ್ಧ' }, albums: { label: 'ಸ್ಮಾರ್ಟ್ ಸಂಘಟನೆ', titleLine1: 'ಪ್ರತಿಯೊಂದು ರಿಸ್ಟೋರ್ ಮಾಡಿದ ಫಲಿತಾಂಶವನ್ನು', titleEmphasis: 'ಸ್ಮಾರ್ಟ್ ಆಲ್ಬಮ್‌ಗಳೊಂದಿಗೆ', body: 'GlassClear ಪ್ರೊಸೆಸಾದ ಚಿತ್ರಗಳನ್ನು ಉಪಯುಕ್ತ ಕಲೆಕ್ಷನ್‌ಗಳಲ್ಲಿ ಇಡುತ್ತದೆ.', cta: 'ಸ್ಮಾರ್ಟ್ ಆಲ್ಬಮ್ ನೋಡಿ', panelTitle: 'ಸ್ಮಾರ್ಟ್ ಆಲ್ಬಮ್‌ಗಳು', latest: 'ಇತ್ತೀಚಿನದು', images: 'ಚಿತ್ರಗಳು' } },
      carousel: { label: 'ಕಾರ್ಯದಲ್ಲಿ ನೋಡಿ', title: 'ನೀವು ನೋಡಬಹುದಾದ ಸ್ಪಷ್ಟತೆ', subtitle: 'ಸ್ಟೋರ್‌ಫ್ರಂಟ್ ಗ್ಲಾಸ್‌ನಿಂದ ಆಫೀಸ್ ಇಂಟೀರಿಯರ್‌ವರೆಗೆ ನಮ್ಮ AI ಎಲ್ಲವನ್ನೂ ನಿಭಾಯಿಸುತ್ತದೆ.', previous: 'ಹಿಂದಿನ ಸ್ಲೈಡ್', next: 'ಮುಂದಿನ ಸ್ಲೈಡ್', slide1: { title: 'ಗ್ಲಾಸ್ ಬಿಲ್ಡಿಂಗ್ ಪ್ರತಿಫಲನ ನಿವಾರಣೆ', subtitle: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಫೋಟೋಗ್ರಫಿ' }, slide2: { title: 'ವಿಂಡೋ ಗ್ಲೇರ್ ಸರಿಪಡింపు', subtitle: 'ರಿಯಲ್ ಎಸ್ಟೇಟ್ ಇಮೇಜಿಂಗ್' }, slide3: { title: 'ಸ್ಕ್ರೀನ್ ಕ್ಲಾರಿಟಿ ಹೆಚ್ಚింపు', subtitle: 'ಪ್ರೊಡಕ್ಟ್ ಫೋಟೋಗ್ರಫಿ' }, slide4: { title: 'ಸ್ಕೈಲೈಟ್ ಪಾರದರ್ಶಕತೆ ಪುನಃಸ್ಥಾಪನೆ', subtitle: 'ಇಂಟೀರಿಯರ್ ಡಿಸೈನ್ ಶೂಟ್ಸ್' }, slide5: { title: 'ಫಸಾಡ್ ಹೇಸ್ ನಿವಾರಣೆ', subtitle: 'ನಗರ ಆರ್ಕಿಟೆಕ್ಚರ್' }, slide6: { title: 'ಆಫೀಸ್ ಗ್ಲಾಸ್ ಡಿಗ್ಲೇರ್', subtitle: 'ಕಾರ್ಪೊರೇಟ್ ಇಂಟೀರಿಯರ್ಸ್' } },
      features: { eyebrow: 'GlassClear ವೈಶಿಷ್ಟ್ಯಗಳು', titleLine1: 'ರಿಸ್ಟೋರೇಶನ್ ಅನ್ನು ಮಾಡಿ', titleLine2: 'ಸುಲಭ ಮತ್ತು ಸರಳ', subtitle: 'ಪ್ರತಿಫಲನರಹಿತ ಚಿತ್ರಗಳನ್ನು ಪ್ರೊಸೆಸ್, ಆಯೋಜನೆ ಮತ್ತು ಹಂಚಿಕೆಗೆ ಸ್ವಚ್ಛ ಕಾರ್ಯಕ್ಷೇತ್ರ.', panelEyebrow: 'AI ಆಧಾರಿತ ಗ್ಲಾಸ್ ರಿಸ್ಟೋರೇಶನ್', headlineLine1: 'ಪ್ರೊಫೆಷನಲ್', headlineEmphasis: 'ಸ್ಪಷ್ಟತೆ', headlineLine2: 'ಗಾಗಿ', headlineLine3: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್', headlineLine4: 'ವಿಜುವಲ್ಸ್', body: 'GlassClear ತಂಡಗಳಿಗೆ ಮ್ಯಾನುಯಲ್ ಎಡಿಟಿಂಗ್ ಇಲ್ಲದೆ ಕ್ಲೈಯಂಟ್-ರೆಡಿ ಫಲಿತಾಂಶಗಳನ್ನು ನೀಡುತ್ತದೆ.', start: 'ರಿಸ್ಟೋರ್ ಪ್ರಾರಂಭಿಸಿ', workflow: 'ವರ್ಕ್‌ಫ್ಲೋ ನೋಡಿ', queueTitle: 'ಪ್ರಾಜೆಕ್ಟ್ ಕ್ಯೂ', summaryTitle: 'ರಿಸ್ಟೋರೇಶನ್ ಸಾರಾಂಶ', queue1: { title: 'ಫಸಾಡ್ ಕ್ಲೀನ್‌ಅಪ್', sub: 'ಔಟ್‌ಪುಟ್ ಅಪ್ಲೋಡ್ ಆಗುತ್ತಿದೆ · 3 ಅಸೆಟ್‌ಗಳು' }, queue2: { title: 'ಇಂಟೀರಿಯರ್ ಗ್ಲಾಸ್ ಶಾಟ್', sub: 'ಕ್ಯೂನಲ್ಲಿ · 2 ಅಸೆಟ್‌ಗಳು' }, queue3: { title: 'ಕ್ಲೈಯಂಟ್ ಪ್ರಿವ್ಯೂ', sub: 'ಕ್ಯೂನಲ್ಲಿ · 5 ಅಸೆಟ್‌ಗಳು' }, summary1: { label: 'ಪ್ರತಿಫಲನ ಕಡಿಮೆಯಾಗಿದೆ' }, summary2: { label: 'ಎಕ್ಸ್ಪೋರ್ಟ್ ಸಿದ್ಧ' }, summary3: { label: 'ಮೊದಲು / ನಂತರ' }, summaryChip: 'ಸರಾಸರಿ ಕ್ಲೀನ್‌ಅಪ್ ಸಮಯ', trustedLabel: 'ಹೆಚ್ಚು ಕ್ಷೇತ್ರಗಳಲ್ಲಿ ನಂಬಿಕೆ', industry1: 'ಆರ್ಕಿಟೆಕ್ಟ್‌ಗಳು', industry2: 'ರಿಯಲ್ ಎಸ್ಟೇಟ್', industry3: 'ಇಂಟೀರಿಯರ್ ಸ್ಟುಡಿಯೋಗಳು', industry4: 'ವಿಜುವಲ್ ಕ್ರಿಯೇಟರ್‌ಗಳು', industry5: 'ಕ್ಲೈಯಂಟ್ ಡೆಲಿವರಿ' },
      testimonials: { label: 'ಜನರು ಏನು ಹೇಳುತ್ತಾರೆ', title: 'ಸ್ಪಷ್ಟತೆಯನ್ನು ಬೇಡುವ ಕ್ರಿಯೇಟರ್‌ಗಳ ನಂಬಿಕೆ', subtitle: 'ಫೋಟೋಗ್ರಾಫರ್‌ಗಳಿಂದ ರಿಯಲ್ ಎಸ್ಟೇಟ್ ತಂಡಗಳವರೆಗೆ GlassClear ಸ್ವಚ್ಛ ದೃಶ್ಯ ನೀಡುತ್ತದೆ.', proofPrefix: 'ಇಷ್ಟಪಟ್ಟಿದ್ದಾರೆ', proofSuffix: 'ಕ್ರಿಯೇಟರ್‌ಗಳು ಜಗತ್ತಿನಾದ್ಯಂತ', 1: { quote: 'GlassClear ನನ್ನ ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಶಾಟ್‌ಗಳನ್ನು ಉಳಿಸಿತು.', role: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಫೋಟೋಗ್ರಾಫರ್' }, 2: { quote: 'AI ತುಂಬಾ ನಿಖರವಾಗಿದೆ.', role: 'ವಿಜುವಲ್ ಡಿಸೈನರ್' }, 3: { quote: 'ಇದು ಒಂದೇ ಕ್ಲಿಕ್ ಕೆಲಸವಾಗಿದೆ.', role: 'ರಿಯಲ್ ಎಸ್ಟೇಟ್ ಎಡಿಟರ್' }, 4: { quote: 'ಔಟ್‌ಪುಟ್ ನೈಸರ್ಗಿಕವಾಗಿ ಕಾಣುತ್ತದೆ.', role: 'ಕಂಟೆಂಟ್ ಕ್ರಿಯೇಟರ್' }, 5: { quote: 'ಇದು ಚತುರವಾದ ಉಪಕರಣ.', role: 'AI ಸಂಶೋಧನಾ ವಿದ್ಯಾರ್ಥಿ' }, 6: { quote: 'ಸ್ವಚ್ಛ UI ಮತ್ತು ವೇಗದ ಫಲಿತಾಂಶಗಳು.', role: 'ಪ್ರೊಡಕ್ಟ್ ಡಿಸೈನರ್' }, 7: { quote: 'GlassClear ಸ್ಥಿರ ಫಲಿತಾಂಶ ನೀಡುತ್ತದೆ.', role: 'ಫ್ರೀಲಾನ್ಸ್ ಫೋಟೋಗ್ರಾಫರ್' }, 8: { quote: 'AI ಇನ್ಸೈಟ್ಸ್ ವಿಶ್ವಾಸ ಹೆಚ್ಚಿಸುತ್ತವೆ.', role: 'UX ರಿಸರ್ಚರ್' }, 9: { quote: 'ಇದು ಚಿತ್ರವನ್ನು ಮರುಸ್ಥಾಪಿಸುತ್ತದೆ.', role: 'ಮೀಡಿಯಾ ಎಡಿಟರ್' }, 10: { quote: 'ಅತ್ಯಂತ ವೇಗದ ಅನುಭವ.', role: 'ಡಿಜಿಟಲ್ ಮಾರ್ಕೆಟರ್' }, 11: { quote: 'AI ಸ್ಟೋರಿ ಉಪಯುಕ್ತವಾಗಿದೆ.', role: 'ವಿದ್ಯಾರ್ಥಿ ಡೆವಲಪರ್' }, 12: { quote: 'ಇದು ಪ್ರೀಮಿಯಂ ಅನುಭವ ಕೊಡುತ್ತದೆ.', role: 'ಕ್ರಿಯೇಟಿವ್ ಡೈರೆಕ್ಟರ್' } },
      faq: { ariaLabel: 'ಹೆಚ್ಚಾಗಿ ಕೇಳುವ ಪ್ರಶ್ನೆಗಳು', label: 'FAQ', titleLine1: 'ಹೆಚ್ಚಾಗಿ ಕೇಳುವ', titleLine2: 'ಪ್ರಶ್ನೆಗಳು', 1: { question: 'GlassClear ಎಂದರೇನು?', answer: 'GlassClear ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಫೋಟೋಗ್ರಫಿಗಾಗಿ AI ಆಧಾರಿತ ಪ್ರತಿಫಲನ ನಿವಾರಣಾ ವ್ಯವಸ್ಥೆ.' }, 2: { question: 'ತಾಂತ್ರಿಕ ಜ್ಞಾನ ಬೇಕೇ?', answer: 'ಬೇಡ. ಚಿತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ಫಲಿತಾಂಶ ಪಡೆಯಿರಿ.' }, 3: { question: 'ಯಾವ ಚಿತ್ರಗಳು ಉತ್ತಮ?', answer: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್, ವಿಂಡೋ, ಫಸಾಡ್ ಮತ್ತು ರಿಯಲ್ ಎಸ್ಟೇಟ್ ಚಿತ್ರಗಳು ಉತ್ತಮ.' }, 4: { question: 'ಒಮ್ಮೆ ಹಲವಾರು ಚಿತ್ರಗಳನ್ನು ಪ್ರೊಸೆಸ್ ಮಾಡಬಹುದೇ?', answer: 'ಹೌದು, ಬ್ಯಾಚ್ ಪ್ರೊಸೆಸಿಂಗ್ ಲಭ್ಯ.' }, 5: { question: 'ಗುಣಮಟ್ಟ ಸುಧಾರಣೆಯಾಗುತ್ತದೆಯೇ?', answer: 'ಇದು ವಿವರಗಳನ್ನು ಉಳಿಸಿಕೊಂಡೇ ಪ್ರತಿಫಲನ ಕಡಿಮೆ ಮಾಡುತ್ತದೆ.' }, 6: { question: 'ನನ್ನ ಡೇಟಾ ಸುರಕ್ಷಿತವೇ?', answer: 'ಚಿತ್ರಗಳು ನಿಮ್ಮ ಖಾತೆಗೆ ಮಾತ್ರ ಸಂಪರ್ಕಿತವಾಗಿರುತ್ತವೆ.' } },
      cta: { ariaLabel: 'GlassClear ಪ್ರಯತ್ನಿಸಿ', label: 'GlassClear ಪ್ರಯತ್ನಿಸಿ', titleLine1: 'ನಿಮ್ಮ ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಫೋಟೋಗಳಿಂದ', titleEmphasis: 'ಪ್ರತಿಫಲನ', titleLine2: 'ತೆಗೆದುಹಾಕಲು ಸಿದ್ಧವೇ?', subtitle: 'ಗ್ಲಾಸ್, ವಿಂಡೋ ಅಥವಾ ಫಸಾಡ್ ಚಿತ್ರವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ಕ್ಷಣಗಳಲ್ಲಿ ಸ್ವಚ್ಛ ಫಲಿತಾಂಶ ಪಡೆಯಿರಿ.', primary: 'ನಿಮ್ಮ ಚಿತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ', secondary: 'ಸ್ಯಾಂಪಲ್ ಫಲಿತಾಂಶ ನೋಡಿ', card1: { title: 'AI ಪ್ರತಿಫಲನ ನಿವಾರಣೆ', text: 'ಆರ್ಕಿಟೆಕ್ಚರಲ್ ಚಿತ್ರಗಳಿಂದ ಗ್ಲೇರ್ ಮತ್ತು ಪ್ರತಿಫಲನ ತೆಗೆದುಹಾಕಿ.' }, card2: { title: 'ಬ್ಯಾಚ್ ಪ್ರೊಸೆಸಿಂಗ್', text: 'ಹಲವಾರು ಕಟ್ಟಡ ಫೋಟೋಗಳನ್ನು ಸುರಕ್ಷಿತ ವರ್ಕ್‌ಫ್ಲೋದಲ್ಲಿ ಪ್ರೊಸೆಸ್ ಮಾಡಿ.' }, card3: { title: 'ಸ್ಮಾರ್ಟ್ ಆಲ್ಬಮ್‌ಗಳು', text: 'ರಿಸ್ಟೋರ್ ಮಾಡಿದ ಫಲಿತಾಂಶಗಳನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಆಯೋಜಿಸಿ.' } }
    }
  }
};
