import { translations as baseTranslations } from './translations.js';
import { landingTranslations } from './landing-translations.js';

const appTranslations = {
  en: {
    common: {
      download: 'Download',
      downloadPng: 'Download PNG',
      downloadJpg: 'Download JPG',
      downloadHd: 'Download HD',
      compare: 'Compare',
      login: 'Login',
      signUp: 'Sign Up',
      email: 'Email',
      password: 'Password',
      continueWithGoogle: 'Continue with Google',
      faq: 'FAQ',
      howItWorks: 'How It Works',
      seeItInAction: 'See It in Action',
      noImagesInAlbumYet: 'No images in this album yet.',
      albumNotFound: 'Album not found',
      searchDashboard: 'Search history, albums, collections, or clients...',
      searchFilenameOrStatus: 'Search by filename or status',
      language: 'Language',
      logout: 'Logout',
      close: 'Close',
      view: 'View',
      export: 'Export',
      delete: 'Delete',
      status: 'Status',
      original: 'Original',
      backToDashboard: 'Back to Dashboard',
      somethingWentWrong: 'Something went wrong.',
      recently: 'Recently',
      updated: 'Updated',
      updatedRecently: 'Updated recently',
      open: 'Open',
      user: 'User',
      remove: 'Remove',
      quality: 'Quality',
      standard: 'Standard',
      high: 'High',
      ultra: 'Ultra'
    },
    auth: {
      togglePassword: 'Toggle password visibility',
      loginBadge: 'AI Reflection Removal',
      loginHeroLine1: 'Clean reflections.',
      loginHeroLine2: 'Keep every detail.',
      loginHeroSubtitle: 'Sign in to restore architectural images, manage exports, and keep every result in one workspace.',
      loginFeatureAccuracy: '98.4% confidence',
      loginFeatureSpeed: 'Fast turnaround',
      loginFeatureOutput: 'Clean output',
      loginFeatureConfidence: 'Trusted results',
      trustedBy: 'Trusted by',
      creators: 'architects, editors, and visual teams',
      signupBadge: 'Create your workspace',
      signupHeroLine1: 'Restore images.',
      signupHeroLine2: 'Deliver faster.',
      signupHeroSubtitle: 'Create your account to process images, build collections, and share polished results with clients.',
      accuracy: 'Accuracy',
      processingLabel: 'Processing',
      resolution: 'Resolution',
      signupQuote: 'GlassClear helps our team clean difficult reflections without slowing down delivery.',
      signupQuoteAuthor: 'Studio Workflow Team',
      accountCreatedLogin: 'Account created. Please log in.'
    },
    dashboard: {
      languageChanged: 'Language changed.',
      exportDownloaded: 'Export downloaded.',
      exportUnavailable: 'Processed output is not available.',
      exportFailed: 'Cannot export a failed result.',
      relogin: 'Please login again to continue.',
      deleteConfirm: 'Delete "{filename}" from history?',
      viewResult: 'View Result',
      uploadImageToView: 'Upload an image to view your latest result.'
    },
    history: {
      title: 'History',
      subtitle: 'All processed GlassClear images for this account.',
      viewAll: 'View All History',
      emptyTitle: 'No history yet',
      emptyMessage: 'Process images to start building your account history.',
      deleteSuccess: 'History item deleted.',
      all: 'All',
      uploaded: 'Uploaded'
    },
    albums: {
      title: 'Smart Albums',
      subtitle: 'Organized collections of your processed GlassClear results.',
      viewAll: 'View All Albums',
      viewAlbum: 'View Album',
      imagesLabel: 'images',
      updatedLabel: 'Updated',
      justNow: 'Updated recently',
      emptyTitle: 'No smart albums yet',
      emptyMessage: 'Processed images will automatically appear in premium albums.',
      emptyAlbumTitle: 'No images in this album yet.',
      emptyAlbumMessage: 'Process more images and GlassClear will place them here automatically.',
      notFoundTitle: 'Album not found',
      notFoundMessage: 'This album slug is invalid or is not available for your account.',
      fallbackName: 'Miscellaneous',
      routeUnavailable: 'Album route is unavailable right now.',
      noMatchingImages: 'No matching images found.',
      searchHelp: 'Try a different search term for this album.',
      smartAlbumLabel: 'Smart Album'
    },
    batch: {
      completed: 'Completed',
      failed: 'Failed'
    },
    collections: {
      title: 'Collections',
      subtitle: 'Save important results into curated folders for teams and clients.',
      fallbackName: 'Collection',
      newCollection: 'New Collection',
      createCollection: 'Create Collection',
      createNew: 'Create New Collection',
      creating: 'Creating...',
      viewAll: 'View All Collections',
      addLatest: 'Add Latest Result',
      addLatestShort: 'Add Result',
      addingLatest: 'Adding latest...',
      adding: 'Adding...',
      addToCollection: 'Add to Collection',
      processBeforeAdd: 'Process an image before adding it to a collection.',
      selectFirst: 'Select a collection first.',
      created: 'Collection created.',
      createFailed: 'Could not create collection.',
      latestAdded: 'Latest result added to collection.',
      addFailed: 'Could not add result to collection.',
      cardDescription: 'Organize your cleaned outputs for quick access and delivery.',
      emptyMessage: 'Create a collection to start organizing your results.',
      name: 'Collection Name',
      placeholder: 'Enter collection name',
      chooseSaveLocation: 'Choose where to save this result.',
      createPersonal: 'Create a new collection for this image.',
      detailSubtitle: 'Your saved results in this collection.',
      removeConfirm: 'Remove {filename} from this collection?',
      removed: 'Item removed from collection.',
      removeFailed: 'Could not remove item.',
      loadFailed: 'Could not load collection.',
      emptyDetailTitle: 'No images in this collection yet.',
      emptyDetailMessage: 'Add results from the dashboard to start organizing this collection.',
      viewAllShort: 'View All Collections'
    },
    delivery: {
      title: 'Client Delivery Pack',
      subtitle: 'Prepare a neat handoff package for your latest restored image.',
      latestCompleted: 'Latest completed result',
      generate: 'Generate Pack',
      generating: 'Generating...',
      download: 'Download Pack',
      downloading: 'Downloading...',
      emptyMessage: 'Process an image to prepare a delivery pack.',
      ready: 'Delivery pack ready.',
      generateFailed: 'Could not generate delivery pack.',
      generateFirst: 'Generate the delivery pack first.',
      downloaded: 'Delivery pack downloaded.',
      downloadFailed: 'Could not download delivery pack.',
      latestReady: 'Latest result is ready for delivery.',
      historyGenerate: 'Generate a delivery pack from your history after processing.'
    },
    processing: {
      title: 'GlassClear Processing',
      subtitle: 'Removing reflections, balancing glare, and preparing a clean architectural result.',
      badge: 'Processing',
      aiProcessing: 'AI Processing',
      aiStatus: 'AI Status',
      uploaded: 'Uploaded',
      processing: 'Processing',
      finalizing: 'Finalizing',
      preparingPreview: 'Preparing preview...',
      changeImage: 'Change Image',
      statusUploadComplete: 'Upload complete.',
      statusScanning: 'Scanning reflective regions...',
      statusRemoving: 'Removing reflections...',
      statusFinalizing: 'Finalizing your output...'
    },
    resultDetail: {
      title: 'GlassClear Result',
      kicker: 'New result ready',
      subtitle: 'Review the cleaned output, compare it against the original capture, and export the version you need.',
      summary: 'Result Summary',
      statusReady: 'Result Ready',
      fileName: 'File name',
      resolution: 'Resolution',
      format: 'Format',
      mode: 'Mode',
      processedOn: 'Processed Date',
      exportTitle: 'Export Output',
      exportOptions: 'Export options',
      exportHelp: 'Select your format and download instantly.',
      exportNote: 'Free export. Clean output. No weird extra steps.',
      back: 'New result ready',
      changeImage: 'Change Image',
      aiStatus: 'AI Status',
      uploadComplete: 'Uploaded',
      processed: 'Processed',
      exportReady: 'Export Ready',
      readyForExport: '{status} and ready for export.',
      downloading: 'Downloading...'
    },
    result: {
      feedback: 'Reflection artifacts were reduced while preserving structure, lighting, and scene details.'
    },
    footer: {
      social: 'Social',
      email: 'Email',
      support: 'Support',
      links: 'Links',
      socials: 'Socials',
      newsletter: 'Newsletter',
      home: 'Home',
      dashboard: 'Dashboard',
      heading: 'Stay updated with GlassClear',
      body: 'Get updates on AI restoration, reflection removal, and architectural imaging workflows.',
      inputPlaceholder: 'Enter email address',
      subscribe: 'Subscribe',
      subscribed: 'Subscribed!',
      taglineLine1: 'Beyond Reflections.',
      taglineLine2: 'Built for Clarity.',
      copyright: '© 2026 GlassClear AI. All rights reserved.',
      privacy: 'Privacy Policy',
      terms: 'Terms of Service'
    },
    navbar: {
      features: 'Features',
      products: 'Products',
      resources: 'Resources',
      dashboard: 'Dashboard',
      uploadImage: 'Upload Image',
      smartAlbums: 'Smart Albums',
      history: 'History',
      howItWorks: 'How It Works',
      seeItInAction: 'See It in Action',
      faq: 'FAQ',
      toggleNavigation: 'Toggle navigation',
      primaryNavigation: 'Primary navigation',
      userMenu: 'User profile menu',
      quickStart: 'Quick Start',
      newUpload: 'New Upload'
    }
  },
  hi: {
    navbarMenu: {
      features: {
        coreTools: '\u0915\u094b\u0930 \u091f\u0942\u0932',
        workflow: '\u0935\u0930\u094d\u0915\u092b\u094d\u0932\u094b',
        removeReflection: { title: '\u0930\u093f\u092b\u094d\u0932\u0947\u0915\u094d\u0936\u0928 \u0939\u091f\u093e\u090f\u0901', description: '\u0906\u0930\u094d\u0915\u093f\u091f\u0947\u0915\u094d\u091a\u0930\u0932 \u092b\u094b\u091f\u094b \u0938\u0947 \u0917\u094d\u0932\u0947\u092f\u0930 \u0914\u0930 \u0917\u094d\u0932\u093e\u0938 \u0930\u093f\u092b\u094d\u0932\u0947\u0915\u094d\u0936\u0928 \u0938\u093e\u092b \u0915\u0930\u0947\u0902\u0964' },
        batch: { title: '\u092c\u0948\u091a \u092a\u094d\u0930\u094b\u0938\u0947\u0938\u093f\u0902\u0917', description: '\u090f\u0915 \u0915\u094d\u092f\u0942 \u092e\u0947\u0902 \u0915\u0908 \u0907\u092e\u0947\u091c \u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924 \u0924\u0930\u0940\u0915\u0947 \u0938\u0947 \u092a\u094d\u0930\u094b\u0938\u0947\u0938 \u0915\u0930\u0947\u0902\u0964' },
        albums: { title: '\u0938\u094d\u092e\u093e\u0930\u094d\u091f \u0906\u0932\u094d\u092c\u092e', description: '\u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0915\u093f\u090f \u0917\u090f \u0930\u093f\u091c\u0932\u094d\u091f\u094d\u0938 \u0915\u094b \u0909\u092a\u092f\u094b\u0917\u0940 \u0915\u0932\u0947\u0915\u094d\u0936\u0928 \u092e\u0947\u0902 \u0911\u091f\u094b-\u0911\u0930\u094d\u0917\u0928\u093e\u0907\u091c \u0915\u0930\u0947\u0902\u0964' },
        history: { title: '\u0939\u093f\u0938\u094d\u091f\u094d\u0930\u0940', description: '\u0905\u092a\u0928\u0947 \u0935\u0930\u094d\u0915\u0938\u094d\u092a\u0947\u0938 \u0915\u093e \u0939\u0930 \u092a\u094d\u0930\u094b\u0938\u0947\u0938\u094d\u0921 \u0930\u093f\u091c\u0932\u094d\u091f \u092b\u093f\u0930 \u0938\u0947 \u0926\u0947\u0916\u0947\u0902\u0964' },
        cta: { title: '\u0928\u092f\u093e \u0905\u092a\u0932\u094b\u0921 \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902', description: 'GlassClear \u0905\u092a\u0932\u094b\u0921\u0930 \u0916\u094b\u0932\u0947\u0902 \u0914\u0930 \u0905\u0917\u0932\u0940 \u0907\u092e\u0947\u091c \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0915\u0930\u0947\u0902\u0964' }
      },
      products: {
        workspace: '\u0935\u0930\u094d\u0915\u0938\u094d\u092a\u0947\u0938',
        collections: '\u0915\u0932\u0947\u0915\u094d\u0936\u0928',
        dashboard: { title: '\u0921\u0948\u0936\u092c\u094b\u0930\u094d\u0921', description: '\u092a\u094d\u0930\u094b\u0938\u0947\u0938\u093f\u0902\u0917, \u092a\u094d\u0930\u0940\u0935\u094d\u092f\u0942 \u0914\u0930 \u0938\u0947\u0935 \u0930\u093f\u091c\u0932\u094d\u091f\u094d\u0938 \u090f\u0915 \u091c\u0917\u0939 \u092e\u0947\u0902 \u092e\u0948\u0928\u0947\u091c \u0915\u0930\u0947\u0902\u0964' },
        upload: { title: '\u0907\u092e\u0947\u091c \u0905\u092a\u0932\u094b\u0921 \u0915\u0930\u0947\u0902', description: '\u090f\u0915 \u0928\u0908 \u0906\u0930\u094d\u0915\u093f\u091f\u0947\u0915\u094d\u091a\u0930\u0932 \u0907\u092e\u0947\u091c \u0915\u0947 \u0938\u093e\u0925 \u0930\u093f\u092b\u094d\u0932\u0947\u0915\u094d\u0936\u0928 \u0930\u093f\u092e\u0942\u0935\u0932 \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902\u0964' },
        albums: { title: '\u0938\u094d\u092e\u093e\u0930\u094d\u091f \u0906\u0932\u094d\u092c\u092e', description: '\u0905\u092a\u0928\u0947 \u0911\u0930\u094d\u0917\u0928\u093e\u0907\u091c\u094d\u0921 \u0907\u092e\u0947\u091c \u0915\u0932\u0947\u0915\u094d\u0936\u0928 \u092c\u094d\u0930\u093e\u0909\u091c \u0915\u0930\u0947\u0902\u0964' },
        history: { title: '\u0930\u093f\u091c\u0932\u094d\u091f \u0939\u093f\u0938\u094d\u091f\u094d\u0930\u0940', description: '\u092a\u0942\u0930\u0940 \u0939\u0941\u0908 \u0930\u093f\u0938\u094d\u091f\u094b\u0930\u0947\u0936\u0928 \u0914\u0930 \u090f\u0915\u094d\u0938\u092a\u094b\u0930\u094d\u091f \u092b\u093f\u0930 \u0938\u0947 \u0926\u0947\u0916\u0947\u0902\u0964' },
        cta: { title: '\u0921\u0948\u0936\u092c\u094b\u0930\u094d\u0921 \u0916\u094b\u0932\u0947\u0902', description: '\u0905\u092a\u0928\u0947 GlassClear \u0935\u0930\u094d\u0915\u0938\u094d\u092a\u0947\u0938 \u092e\u0947\u0902 \u091c\u093e\u090f\u0901 \u0914\u0930 \u090f\u0921\u093f\u091f\u093f\u0902\u0917 \u091c\u093e\u0930\u0940 \u0930\u0916\u0947\u0902\u0964' }
      },
      resources: {
        learn: '\u0938\u0940\u0916\u0947\u0902',
        help: '\u092e\u0926\u0926',
        how: { title: '\u092f\u0939 \u0915\u0948\u0938\u0947 \u0915\u093e\u092e \u0915\u0930\u0924\u093e \u0939\u0948', description: '\u0930\u093f\u092b\u094d\u0932\u0947\u0915\u094d\u0936\u0928 \u0930\u093f\u092e\u0942\u0935\u0932 \u0935\u0930\u094d\u0915\u092b\u094d\u0932\u094b \u0915\u094b \u0938\u092e\u091d\u0947\u0902\u0964' },
        demo: { title: '\u090f\u0915\u094d\u0936\u0928 \u092e\u0947\u0902 \u0926\u0947\u0916\u0947\u0902', description: '\u092c\u093f\u092b\u094b\u0930-\u0906\u092b\u094d\u091f\u0930 \u0930\u093f\u0938\u094d\u091f\u094b\u0930\u0947\u0936\u0928 \u0909\u0926\u093e\u0939\u0930\u0923 \u0926\u0947\u0916\u0947\u0902\u0964' },
        faq: { title: 'FAQ', description: 'GlassClear \u0915\u0947 \u092c\u093e\u0930\u0947 \u092e\u0947\u0902 \u0938\u093e\u092e\u093e\u0928\u094d\u092f \u092a\u094d\u0930\u0936\u094d\u0928\u0964' },
        guide: { title: '\u0905\u092a\u0932\u094b\u0921 \u0917\u093e\u0907\u0921', description: '\u0938\u0940\u0927\u0947 \u0905\u092a\u0932\u094b\u0921\u0930 \u092a\u0930 \u091c\u093e\u090f\u0901 \u0914\u0930 \u0928\u0908 \u0930\u093f\u0938\u094d\u091f\u094b\u0930\u0947\u0936\u0928 \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902\u0964' },
        cta: { title: '\u0921\u0947\u092e\u094b \u092b\u094d\u0932\u094b \u0906\u091c\u092e\u093e\u090f\u0901', description: '\u0932\u093e\u0907\u0935 \u0936\u094b\u0915\u0947\u0938 \u0924\u0915 \u0938\u094d\u0915\u094d\u0930\u0949\u0932 \u0915\u0930\u0947\u0902 \u0914\u0930 \u0930\u093f\u0938\u094d\u091f\u094b\u0930\u0947\u0936\u0928 \u0905\u0928\u0941\u092d\u0935 \u092a\u094d\u0930\u0940\u0935\u094d\u092f\u0942 \u0915\u0930\u0947\u0902\u0964' }
      }
    },
    common: {
      download: 'डाउनलोड',
      downloadPng: 'PNG डाउनलोड',
      downloadJpg: 'JPG डाउनलोड',
      downloadHd: 'HD डाउनलोड',
      compare: 'तुलना',
      login: 'लॉगिन',
      signUp: 'साइन अप',
      email: 'ईमेल',
      password: 'पासवर्ड',
      continueWithGoogle: 'Google के साथ जारी रखें',
      faq: 'सामान्य प्रश्न',
      howItWorks: 'यह कैसे काम करता है',
      seeItInAction: 'इसे काम करते देखें',
      noImagesInAlbumYet: 'इस एल्बम में अभी कोई इमेज नहीं है।',
      albumNotFound: 'एल्बम नहीं मिला',
      searchDashboard: 'हिस्ट्री, एल्बम, कलेक्शन या क्लाइंट खोजें...',
      searchFilenameOrStatus: 'फ़ाइल नाम या स्थिति से खोजें',
      language: 'भाषा',
      logout: 'लॉग आउट',
      close: 'बंद करें',
      view: 'देखें',
      export: 'एक्सपोर्ट',
      delete: 'हटाएँ',
      status: 'स्थिति',
      original: 'ओरिजिनल',
      backToDashboard: 'डैशबोर्ड पर वापस जाएँ',
      somethingWentWrong: 'कुछ गलत हो गया।',
      recently: 'अभी हाल में',
      updated: 'अपडेट',
      updatedRecently: 'हाल ही में अपडेट किया गया',
      open: 'खोलें',
      user: 'उपयोगकर्ता',
      remove: 'हटाएँ',
      quality: 'क्वालिटी',
      standard: 'स्टैंडर्ड',
      high: 'हाई',
      ultra: 'अल्ट्रा'
    },
    auth: {
      togglePassword: 'पासवर्ड दिखाएँ या छिपाएँ',
      loginBadge: 'AI रिफ्लेक्शन रिमूवल',
      loginHeroLine1: 'रिफ्लेक्शन हटाएँ।',
      loginHeroLine2: 'हर डिटेल बचाएँ।',
      loginHeroSubtitle: 'साइन इन करें और आर्किटेक्चरल इमेज साफ करें, एक्सपोर्ट संभालें, और सभी रिजल्ट एक जगह रखें।',
      loginFeatureAccuracy: '98.4% कॉन्फिडेंस',
      loginFeatureSpeed: 'तेज़ प्रोसेसिंग',
      loginFeatureOutput: 'साफ आउटपुट',
      loginFeatureConfidence: 'विश्वसनीय रिजल्ट',
      trustedBy: 'इनके द्वारा भरोसेमंद',
      creators: 'आर्किटेक्ट, एडिटर और विज़ुअल टीमें',
      signupBadge: 'अपना वर्कस्पेस बनाएँ',
      signupHeroLine1: 'इमेज साफ करें।',
      signupHeroLine2: 'डिलीवरी तेज़ करें।',
      signupHeroSubtitle: 'अकाउंट बनाकर इमेज प्रोसेस करें, कलेक्शन बनाएँ और क्लाइंट्स के साथ पॉलिश्ड रिजल्ट शेयर करें।',
      accuracy: 'सटीकता',
      processingLabel: 'प्रोसेसिंग',
      resolution: 'रिज़ॉल्यूशन',
      signupQuote: 'GlassClear हमारी टीम को कठिन रिफ्लेक्शन साफ करने में मदद करता है बिना डिलीवरी धीमी किए।',
      signupQuoteAuthor: 'स्टूडियो वर्कफ़्लो टीम',
      accountCreatedLogin: 'अकाउंट बन गया। कृपया लॉगिन करें।'
    },
    dashboard: {
      languageChanged: 'भाषा बदल गई।',
      exportDownloaded: 'एक्सपोर्ट डाउनलोड हो गया।',
      exportUnavailable: 'प्रोसेस्ड आउटपुट उपलब्ध नहीं है।',
      exportFailed: 'विफल परिणाम को एक्सपोर्ट नहीं किया जा सकता।',
      relogin: 'जारी रखने के लिए फिर से लॉगिन करें।',
      deleteConfirm: 'क्या हिस्ट्री से "{filename}" हटाएँ?',
      viewResult: 'रिजल्ट देखें',
      uploadImageToView: 'अपना नवीनतम रिजल्ट देखने के लिए इमेज अपलोड करें।'
    },
    history: {
      title: 'हिस्ट्री',
      subtitle: 'इस अकाउंट की सभी प्रोसेस की गई GlassClear इमेज।',
      viewAll: 'पूरी हिस्ट्री देखें',
      emptyTitle: 'अभी कोई हिस्ट्री नहीं है',
      emptyMessage: 'अपनी हिस्ट्री बनाने के लिए इमेज प्रोसेस करें।',
      deleteSuccess: 'हिस्ट्री आइटम हट गया।',
      all: 'सभी',
      uploaded: 'अपलोड किया गया'
    },
    albums: {
      title: 'स्मार्ट एल्बम',
      subtitle: 'आपके प्रोसेस किए गए GlassClear रिजल्ट्स के व्यवस्थित कलेक्शन।',
      viewAll: 'सभी एल्बम देखें',
      viewAlbum: 'एल्बम देखें',
      imagesLabel: 'इमेज',
      updatedLabel: 'अपडेट',
      justNow: 'हाल ही में अपडेट किया गया',
      emptyTitle: 'अभी कोई स्मार्ट एल्बम नहीं है',
      emptyMessage: 'प्रोसेस्ड इमेज अपने-आप प्रीमियम एल्बम में दिखेंगी।',
      emptyAlbumTitle: 'इस एल्बम में अभी कोई इमेज नहीं है।',
      emptyAlbumMessage: 'और इमेज प्रोसेस करें, GlassClear उन्हें यहाँ अपने-आप रख देगा।',
      notFoundTitle: 'एल्बम नहीं मिला',
      notFoundMessage: 'यह एल्बम स्लग अमान्य है या आपके अकाउंट के लिए उपलब्ध नहीं है।',
      fallbackName: 'विविध',
      routeUnavailable: 'एल्बम रूट अभी उपलब्ध नहीं है।',
      noMatchingImages: 'कोई मिलती हुई इमेज नहीं मिली।',
      searchHelp: 'इस एल्बम के लिए कोई दूसरा खोज शब्द आज़माएँ।',
      smartAlbumLabel: 'स्मार्ट एल्बम'
    },
    batch: {
      completed: 'पूर्ण',
      failed: 'विफल'
    },
    collections: {
      title: 'कलेक्शन',
      subtitle: 'टीम और क्लाइंट के लिए महत्वपूर्ण रिजल्ट चुने हुए फ़ोल्डर में रखें।',
      fallbackName: 'कलेक्शन',
      newCollection: 'नया कलेक्शन',
      createCollection: 'कलेक्शन बनाएँ',
      createNew: 'नया कलेक्शन बनाएँ',
      creating: 'बनाया जा रहा है...',
      viewAll: 'सभी कलेक्शन देखें',
      addLatest: 'नवीनतम रिजल्ट जोड़ें',
      addLatestShort: 'रिजल्ट जोड़ें',
      addingLatest: 'नवीनतम जोड़ा जा रहा है...',
      adding: 'जोड़ा जा रहा है...',
      addToCollection: 'कलेक्शन में जोड़ें',
      processBeforeAdd: 'कलेक्शन में जोड़ने से पहले इमेज प्रोसेस करें।',
      selectFirst: 'पहले एक कलेक्शन चुनें।',
      created: 'कलेक्शन बन गया।',
      createFailed: 'कलेक्शन नहीं बन सका।',
      latestAdded: 'नवीनतम रिजल्ट कलेक्शन में जोड़ दिया गया।',
      addFailed: 'रिजल्ट नहीं जोड़ा जा सका।',
      cardDescription: 'तेज़ एक्सेस और डिलीवरी के लिए अपने साफ किए गए आउटपुट व्यवस्थित करें।',
      emptyMessage: 'अपने रिजल्ट व्यवस्थित करने के लिए एक कलेक्शन बनाएँ।',
      name: 'कलेक्शन नाम',
      placeholder: 'कलेक्शन नाम दर्ज करें',
      chooseSaveLocation: 'यह रिजल्ट कहाँ सेव करना है चुनें।',
      createPersonal: 'इस इमेज के लिए नया कलेक्शन बनाएँ।',
      detailSubtitle: 'इस कलेक्शन में आपके सेव किए गए रिजल्ट।',
      removeConfirm: 'क्या {filename} को इस कलेक्शन से हटाएँ?',
      removed: 'आइटम कलेक्शन से हट गया।',
      removeFailed: 'आइटम हटाया नहीं जा सका।',
      loadFailed: 'कलेक्शन लोड नहीं हो सका।',
      emptyDetailTitle: 'इस कलेक्शन में अभी कोई इमेज नहीं है।',
      emptyDetailMessage: 'इस कलेक्शन को व्यवस्थित करना शुरू करने के लिए डैशबोर्ड से रिजल्ट जोड़ें।',
      viewAllShort: 'सभी कलेक्शन देखें'
    },
    delivery: {
      title: 'क्लाइंट डिलीवरी पैक',
      subtitle: 'अपने नवीनतम साफ किए गए रिजल्ट के लिए साफ-सुथरा हैंडऑफ़ पैक तैयार करें।',
      latestCompleted: 'नवीनतम पूरा हुआ रिजल्ट',
      generate: 'पैक बनाएँ',
      generating: 'बनाया जा रहा है...',
      download: 'पैक डाउनलोड करें',
      downloading: 'डाउनलोड हो रहा है...',
      emptyMessage: 'डिलीवरी पैक तैयार करने के लिए एक इमेज प्रोसेस करें।',
      ready: 'डिलीवरी पैक तैयार है।',
      generateFailed: 'डिलीवरी पैक नहीं बन सका।',
      generateFirst: 'पहले डिलीवरी पैक बनाएँ।',
      downloaded: 'डिलीवरी पैक डाउनलोड हो गया।',
      downloadFailed: 'डिलीवरी पैक डाउनलोड नहीं हो सका।',
      latestReady: 'नवीनतम रिजल्ट डिलीवरी के लिए तैयार है।',
      historyGenerate: 'प्रोसेसिंग के बाद हिस्ट्री से डिलीवरी पैक बनाएँ।'
    },
    processing: {
      title: 'GlassClear प्रोसेसिंग',
      subtitle: 'रिफ्लेक्शन हटाए जा रहे हैं, ग्लेयर संतुलित हो रहा है, और साफ आर्किटेक्चरल रिजल्ट तैयार किया जा रहा है।',
      badge: 'प्रोसेसिंग',
      aiProcessing: 'AI प्रोसेसिंग',
      aiStatus: 'AI स्थिति',
      uploaded: 'अपलोड हो गया',
      processing: 'प्रोसेसिंग',
      finalizing: 'अंतिम रूप दिया जा रहा है',
      preparingPreview: 'प्रीव्यू तैयार हो रहा है...',
      changeImage: 'इमेज बदलें',
      statusUploadComplete: 'अपलोड पूरा हुआ।',
      statusScanning: 'रिफ्लेक्टिव हिस्सों को स्कैन किया जा रहा है...',
      statusRemoving: 'रिफ्लेक्शन हटाए जा रहे हैं...',
      statusFinalizing: 'आउटपुट को अंतिम रूप दिया जा रहा है...'
    },
    resultDetail: {
      title: 'GlassClear रिजल्ट',
      kicker: 'नया रिजल्ट तैयार है',
      subtitle: 'साफ आउटपुट देखें, उसे ओरिजिनल कैप्चर से तुलना करें, और अपनी ज़रूरत वाला वर्ज़न एक्सपोर्ट करें।',
      summary: 'रिजल्ट सारांश',
      statusReady: 'रिजल्ट तैयार',
      fileName: 'फ़ाइल नाम',
      resolution: 'रिज़ॉल्यूशन',
      format: 'फ़ॉर्मेट',
      mode: 'मोड',
      processedOn: 'प्रोसेस की तारीख',
      exportTitle: 'एक्सपोर्ट आउटपुट',
      exportOptions: 'एक्सपोर्ट विकल्प',
      exportHelp: 'अपना फ़ॉर्मेट चुनें और तुरंत डाउनलोड करें।',
      exportNote: 'मुफ़्त एक्सपोर्ट। साफ आउटपुट। बिना अतिरिक्त स्टेप्स के।',
      back: 'नया रिजल्ट तैयार है',
      changeImage: 'इमेज बदलें',
      aiStatus: 'AI स्थिति',
      uploadComplete: 'अपलोड हुआ',
      processed: 'प्रोसेस हुआ',
      exportReady: 'एक्सपोर्ट तैयार',
      readyForExport: '{status} और एक्सपोर्ट के लिए तैयार।',
      downloading: 'डाउनलोड हो रहा है...'
    },
    result: {
      feedback: 'रिफ्लेक्शन आर्टिफैक्ट कम किए गए हैं, जबकि संरचना, रोशनी और दृश्य विवरण सुरक्षित रखे गए हैं।'
    },
    footer: {
      social: 'सोशल',
      email: 'ईमेल',
      support: 'सपोर्ट',
      links: 'लिंक',
      socials: 'सोशल्स',
      newsletter: 'न्यूज़लेटर',
      home: 'होम',
      dashboard: 'डैशबोर्ड',
      heading: 'GlassClear के साथ अपडेट रहें',
      body: 'AI रिस्टोरेशन, रिफ्लेक्शन रिमूवल और आर्किटेक्चरल इमेजिंग वर्कफ़्लो के अपडेट पाएँ।',
      inputPlaceholder: 'ईमेल पता दर्ज करें',
      subscribe: 'सब्सक्राइब करें',
      subscribed: 'सब्सक्राइब हो गया!',
      taglineLine1: 'रिफ्लेक्शन से आगे।',
      taglineLine2: 'स्पष्टता के लिए बनाया गया।',
      copyright: '© 2026 GlassClear AI. सर्वाधिकार सुरक्षित।',
      privacy: 'प्राइवेसी पॉलिसी',
      terms: 'सेवा की शर्तें'
    },
    navbar: {
      features: 'फ़ीचर्स',
      products: 'प्रोडक्ट्स',
      resources: 'संसाधन',
      dashboard: 'डैशबोर्ड',
      uploadImage: 'इमेज अपलोड करें',
      smartAlbums: 'स्मार्ट एल्बम',
      history: 'हिस्ट्री',
      howItWorks: 'यह कैसे काम करता है',
      seeItInAction: 'इसे काम करते देखें',
      faq: 'सामान्य प्रश्न',
      toggleNavigation: 'नेविगेशन टॉगल करें',
      primaryNavigation: 'मुख्य नेविगेशन',
      userMenu: 'यूज़र प्रोफ़ाइल मेन्यू',
      quickStart: 'क्विक स्टार्ट',
      newUpload: 'नई अपलोड'
    }
  },
  kn: {
    navbarMenu: {
      features: {
        coreTools: '\u0c95\u0cca\u0cb0\u0ccd \u0c9f\u0cc2\u0cb2\u0ccd\u0c97\u0cb3\u0cc1',
        workflow: '\u0cb5\u0cb0\u0ccd\u0c95\u0ccd\u0cab\u0ccd\u0cb2\u0ccb',
        removeReflection: { title: '\u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0cab\u0cb2\u0ca8 \u0ca4\u0cc6\u0c97\u0cc6\u0ca6\u0cc1\u0cb9\u0cbe\u0c95\u0cbf', description: '\u0c86\u0cb0\u0ccd\u0c95\u0cbf\u0c9f\u0cc6\u0c95\u0ccd\u0c9a\u0cb0\u0cb2\u0ccd \u0cab\u0ccb\u0c9f\u0ccb\u0c97\u0cb3\u0cbf\u0c82\u0ca6 \u0c97\u0ccd\u0cb2\u0cc7\u0cb0\u0ccd \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0c97\u0ccd\u0cb2\u0cbe\u0cb8\u0ccd \u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0cab\u0cb2\u0ca8\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb8\u0ccd\u0cb5\u0c9a\u0ccd\u0c9b\u0c97\u0cca\u0cb3\u0cbf\u0cb8\u0cbf\u002e' },
        batch: { title: '\u0cac\u0ccd\u0caf\u0cbe\u0c9a\u0ccd \u0caa\u0ccd\u0cb0\u0ccb\u0cb8\u0cc6\u0cb8\u0cbf\u0c82\u0c97\u0ccd', description: '\u0c92\u0c82\u0ca6\u0cc1 \u0c95\u0ccd\u0caf\u0cc2\u0ca8\u0cb2\u0ccd\u0cb2\u0cbf \u0c85\u0ca8\u0cc7\u0c95 \u0c9a\u0cbf\u0ca4\u0ccd\u0cb0\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb8\u0cc1\u0cb0\u0c95\u0ccd\u0cb7\u0cbf\u0ca4\u0cb5\u0cbe\u0c97\u0cbf \u0caa\u0ccd\u0cb0\u0ccb\u0cb8\u0cc6\u0cb8\u0ccd \u0cae\u0cbe\u0ca1\u0cbf\u002e' },
        albums: { title: '\u0cb8\u0ccd\u0cae\u0cbe\u0cb0\u0ccd\u0c9f\u0ccd \u0c86\u0cb2\u0ccd\u0cac\u0cae\u0ccd\u0c97\u0cb3\u0cc1', description: '\u0cb0\u0cbf\u0cb8\u0ccd\u0c9f\u0ccb\u0cb0\u0ccd \u0cae\u0cbe\u0ca1\u0cbf\u0ca6 \u0cab\u0cb2\u0cbf\u0ca4\u0cbe\u0c82\u0cb6\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0c89\u0caa\u0caf\u0cc1\u0c95\u0ccd\u0ca4 \u0c95\u0cb2\u0cc6\u0c95\u0ccd\u0cb7\u0ca8\u0ccd\u0c97\u0cb3\u0cb2\u0ccd\u0cb2\u0cbf \u0cb8\u0ccd\u0cb5\u0caf\u0c82\u0c9a\u0cbe\u0cb2\u0cbf\u0ca4\u0cb5\u0cbe\u0c97\u0cbf \u0c86\u0caf\u0ccb\u0c9c\u0cbf\u0cb8\u0cbf\u002e' },
        history: { title: '\u0c87\u0ca4\u0cbf\u0cb9\u0cbe\u0cb8', description: '\u0ca8\u0cbf\u0cae\u0ccd\u0cae \u0cb5\u0cb0\u0ccd\u0c95\u0ccd\u0cb8\u0ccd\u0caa\u0cc7\u0cb8\u0ccd\u0ca8\u0cb2\u0ccd\u0cb2\u0cbf \u0caa\u0ccd\u0cb0\u0ccb\u0cb8\u0cc6\u0cb8\u0ccd\u0ca1\u0ccd \u0c86\u0ca6 \u0caa\u0ccd\u0cb0\u0ca4\u0cbf \u0cab\u0cb2\u0cbf\u0ca4\u0cbe\u0c82\u0cb6\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cae\u0ca4\u0ccd\u0ca4\u0cc6 \u0ca8\u0ccb\u0ca1\u0cbf\u002e' },
        cta: { title: '\u0cb9\u0cca\u0cb8 \u0c85\u0caa\u0ccd\u0cb2\u0ccb\u0ca1\u0ccd \u0cb6\u0cc1\u0cb0\u0cc1 \u0cae\u0cbe\u0ca1\u0cbf', description: 'GlassClear \u0c85\u0caa\u0ccd\u0cb2\u0ccb\u0ca1\u0cb0\u0ccd \u0ca4\u0cc6\u0cb0\u0cc6\u0caf\u0cbf\u0cb0\u0cbf \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0cae\u0cc1\u0c82\u0ca6\u0cbf\u0ca8 \u0c9a\u0cbf\u0ca4\u0ccd\u0cb0\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb0\u0cbf\u0cb8\u0ccd\u0c9f\u0ccb\u0cb0\u0ccd \u0cae\u0cbe\u0ca1\u0cbf\u002e' }
      },
      products: {
        workspace: '\u0c95\u0cbe\u0cb0\u0ccd\u0caf\u0c95\u0ccd\u0cb7\u0cc7\u0ca4\u0ccd\u0cb0',
        collections: '\u0c95\u0cb2\u0cc6\u0c95\u0ccd\u0cb7\u0ca8\u0ccd\u0c97\u0cb3\u0cc1',
        dashboard: { title: '\u0ca1\u0ccd\u0caf\u0cbe\u0cb7\u0ccd\u0cac\u0ccb\u0cb0\u0ccd\u0ca1\u0ccd', description: '\u0caa\u0ccd\u0cb0\u0ccb\u0cb8\u0cc6\u0cb8\u0cbf\u0c82\u0c97\u0ccd, \u0caa\u0ccd\u0cb0\u0cc0\u0cb5\u0ccd\u0caf\u0cc2 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0c89\u0cb3\u0cbf\u0cb8\u0cbf\u0ca6 \u0cab\u0cb2\u0cbf\u0ca4\u0cbe\u0c82\u0cb6\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0c92\u0c82\u0ca6\u0cc7 \u0c9c\u0c97\u0cb9\u0ca6\u0cb2\u0ccd\u0cb2\u0cbf \u0ca8\u0cbf\u0cb0\u0ccd\u0cb5\u0cb9\u0cbf\u0cb8\u0cbf\u002e' },
        upload: { title: '\u0c9a\u0cbf\u0ca4\u0ccd\u0cb0 \u0c85\u0caa\u0ccd\u0cb2\u0ccb\u0ca1\u0ccd \u0cae\u0cbe\u0ca1\u0cbf', description: '\u0cb9\u0cca\u0cb8 \u0c86\u0cb0\u0ccd\u0c95\u0cbf\u0c9f\u0cc6\u0c95\u0ccd\u0c9a\u0cb0\u0cb2\u0ccd \u0c9a\u0cbf\u0ca4\u0ccd\u0cb0\u0ca6 \u0c9c\u0cca\u0ca4\u0cc6 \u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0cab\u0cb2\u0ca8 \u0ca4\u0cc6\u0c97\u0cc6\u0ca6\u0cc1\u0cb9\u0cbe\u0c95\u0cc1\u0cb5\u0c81\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb6\u0cc1\u0cb0\u0cc1 \u0cae\u0cbe\u0ca1\u0cbf\u002e' },
        albums: { title: '\u0cb8\u0ccd\u0cae\u0cbe\u0cb0\u0ccd\u0c9f\u0ccd \u0c86\u0cb2\u0ccd\u0cac\u0cae\u0ccd\u0c97\u0cb3\u0cc1', description: '\u0ca8\u0cbf\u0cae\u0ccd\u0cae \u0c86\u0caf\u0ccb\u0c9c\u0cbf\u0ca4 \u0c9a\u0cbf\u0ca4\u0ccd\u0cb0 \u0c95\u0cb2\u0cc6\u0c95\u0ccd\u0cb7\u0ca8\u0ccd\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0cac\u0ccd\u0cb0\u0ccd\u0caf\u0cbe\u0c89\u0c9c\u0ccd \u0cae\u0cbe\u0ca1\u0cbf\u002e' },
        history: { title: '\u0cab\u0cb2\u0cbf\u0ca4\u0cbe\u0c82\u0cb6 \u0c87\u0ca4\u0cbf\u0cb9\u0cbe\u0cb8', description: '\u0caa\u0cc2\u0cb0\u0ccd\u0ca3\u0c97\u0cca\u0c82\u0ca1 \u0cb0\u0cbf\u0cb8\u0ccd\u0c9f\u0ccb\u0cb0\u0cc7\u0cb6\u0ca8\u0ccd\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0c8e\u0c95\u0ccd\u0cb8\u0ccd\u0caa\u0ccb\u0cb0\u0ccd\u0c9f\u0ccd\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0cae\u0ca4\u0ccd\u0ca4\u0cc6 \u0ca8\u0ccb\u0ca1\u0cbf\u002e' },
        cta: { title: '\u0ca1\u0ccd\u0caf\u0cbe\u0cb7\u0ccd\u0cac\u0ccb\u0cb0\u0ccd\u0ca1\u0ccd \u0ca4\u0cc6\u0cb0\u0cc6\u0caf\u0cbf\u0cb0\u0cbf', description: '\u0ca8\u0cbf\u0cae\u0ccd\u0cae GlassClear \u0c95\u0cbe\u0cb0\u0ccd\u0caf\u0c95\u0ccd\u0cb7\u0cc7\u0ca4\u0ccd\u0cb0\u0c95\u0ccd\u0c95\u0cc6 \u0cb9\u0ccb\u0c97\u0cbf \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0c8e\u0ca1\u0cbf\u0c9f\u0cbf\u0c82\u0c97\u0ccd \u0cae\u0c82\u0ca6\u0cc1\u0cb5\u0cb0\u0cbf\u0cb8\u0cbf\u002e' }
      },
      resources: {
        learn: '\u0c95\u0cb2\u0cbf\u0caf\u0cbf\u0cb0\u0cbf',
        help: '\u0cb8\u0cb9\u0cbe\u0caf',
        how: { title: '\u0c87\u0ca6\u0cc1 \u0cb9\u0cc7\u0c97\u0cc6 \u0c95\u0cc6\u0cb2\u0cb8 \u0cae\u0cbe\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0ca6\u0cc6', description: '\u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0cab\u0cb2\u0ca8 \u0ca4\u0cc6\u0c97\u0cc6\u0ca6\u0cc1\u0cb9\u0cbe\u0c95\u0cc1\u0cb5 \u0cb5\u0cb0\u0ccd\u0c95\u0ccd\u0cab\u0ccd\u0cb2\u0ccb\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0c85\u0cb0\u0cbf\u0ca4\u0cc1\u0c95\u0cca\u0cb3\u0ccd\u0cb3\u0cbf\u002e' },
        demo: { title: '\u0c95\u0ccd\u0cb0\u0cbf\u0caf\u0cc6\u0caf\u0cb2\u0ccd\u0cb2\u0cbf \u0ca8\u0ccb\u0ca1\u0cbf', description: '\u0cae\u0cc1\u0c82\u0c9a\u0cc6-\u0ca8\u0c82\u0ca4\u0cb0 \u0cb0\u0cbf\u0cb8\u0ccd\u0c9f\u0ccb\u0cb0\u0cc7\u0cb6\u0ca8\u0ccd \u0c89\u0ca6\u0cbe\u0cb9\u0cb0\u0ca3\u0cc6\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0ca8\u0ccb\u0ca1\u0cbf\u002e' },
        faq: { title: 'FAQ', description: 'GlassClear \u0cac\u0c97\u0ccd\u0c97\u0cc6 \u0cb8\u0cbe\u0cae\u0cbe\u0ca8\u0ccd\u0caf \u0caa\u0ccd\u0cb0\u0cb6\u0ccd\u0ca8\u0cc6\u0c97\u0cb3\u0cc1\u002e' },
        guide: { title: '\u0c85\u0caa\u0ccd\u0cb2\u0ccb\u0ca1\u0ccd \u0c97\u0cc8\u0ca1\u0ccd', description: '\u0ca8\u0cc7\u0cb0\u0cb5\u0cbe\u0c97\u0cbf \u0c85\u0caa\u0ccd\u0cb2\u0ccb\u0ca1\u0cb0\u0ccd\u0c97\u0cc6 \u0cb9\u0ccb\u0c97\u0cbf \u0cb9\u0cca\u0cb8 \u0cb0\u0cbf\u0cb8\u0ccd\u0c9f\u0ccb\u0cb0\u0cc7\u0cb6\u0ca8\u0ccd \u0cb6\u0cc1\u0cb0\u0cc1 \u0cae\u0cbe\u0ca1\u0cbf\u002e' },
        cta: { title: '\u0ca1\u0cc6\u0cae\u0cca \u0cab\u0ccd\u0cb2\u0ccb \u0caa\u0ccd\u0cb0\u0caf\u0ca4\u0ccd\u0ca8\u0cbf\u0cb8\u0cbf', description: '\u0cb2\u0cc8\u0cb5\u0ccd \u0cb6\u0ccb\u0c95\u0cc7\u0cb8\u0ccd\u0c97\u0cc6 \u0cb8\u0ccd\u0c95\u0ccd\u0cb0\u0ccd\u0cb0\u0ccb\u0cb2\u0ccd \u0cae\u0cbe\u0ca1\u0cbf \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0cb0\u0cbf\u0cb8\u0ccd\u0c9f\u0ccb\u0cb0\u0cc7\u0cb6\u0ca8\u0ccd \u0c85\u0ca8\u0cc1\u0cad\u0cb5\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0caa\u0ccd\u0cb0\u0cc0\u0cb5\u0ccd\u0caf\u0cc2 \u0cae\u0cbe\u0ca1\u0cbf\u002e' }
      }
    },
    common: {
      download: 'ಡೌನ್‌ಲೋಡ್',
      downloadPng: 'PNG ಡೌನ್‌ಲೋಡ್',
      downloadJpg: 'JPG ಡೌನ್‌ಲೋಡ್',
      downloadHd: 'HD ಡೌನ್‌ಲೋಡ್',
      compare: 'ಹೋಲಿಕೆ',
      login: 'ಲಾಗಿನ್',
      signUp: 'ಸೈನ್ ಅಪ್',
      email: 'ಇಮೇಲ್',
      password: 'ಪಾಸ್ವರ್ಡ್',
      continueWithGoogle: 'Google ಜೊತೆಗೆ ಮುಂದುವರಿಸಿ',
      faq: 'FAQ',
      howItWorks: 'ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
      seeItInAction: 'ಇದನ್ನು ಕೆಲಸದಲ್ಲಿ ನೋಡಿ',
      noImagesInAlbumYet: 'ಈ ಆಲ್ಬಮ್‌ನಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ಚಿತ್ರಗಳಿಲ್ಲ.',
      albumNotFound: 'ಆಲ್ಬಮ್ ಸಿಗಲಿಲ್ಲ',
      searchDashboard: 'ಇತಿಹಾಸ, ಆಲ್ಬಮ್, ಕಲೆಕ್ಷನ್ ಅಥವಾ ಕ್ಲೈಂಟ್ ಹುಡುಕಿ...',
      searchFilenameOrStatus: 'ಫೈಲ್ ಹೆಸರು ಅಥವಾ ಸ್ಥಿತಿಯಿಂದ ಹುಡುಕಿ',
      language: 'ಭಾಷೆ',
      logout: 'ಲಾಗ್ ಔಟ್',
      close: 'ಮುಚ್ಚಿ',
      view: 'ನೋಡಿ',
      export: 'ಎಕ್ಸ್‌ಪೋರ್ಟ್',
      delete: 'ಅಳಿಸಿ',
      status: 'ಸ್ಥಿತಿ',
      original: 'ಮೂಲ',
      backToDashboard: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹಿಂತಿರುಗಿ',
      somethingWentWrong: 'ಏನೋ ತಪ್ಪಾಗಿದೆ.',
      recently: 'ಇತ್ತೀಚೆಗೆ',
      updated: 'ಅಪ್ಡೇಟ್',
      updatedRecently: 'ಇತ್ತೀಚೆಗೆ ಅಪ್ಡೇಟ್ ಮಾಡಲಾಗಿದೆ',
      open: 'ತೆರೆಯಿರಿ',
      user: 'ಬಳಕೆದಾರ',
      remove: 'ತೆಗೆದುಹಾಕಿ',
      quality: 'ಗುಣಮಟ್ಟ',
      standard: 'ಸ್ಟ್ಯಾಂಡರ್ಡ್',
      high: 'ಹೈ',
      ultra: 'ಅಲ್ಟ್ರಾ'
    },
    auth: {
      togglePassword: 'ಪಾಸ್ವರ್ಡ್ ತೋರಿಸಿ ಅಥವಾ ಮರೆಮಾಡಿ',
      loginBadge: 'AI ಪ್ರತಿಫಲನ ನಿವಾರಣೆ',
      loginHeroLine1: 'ಪ್ರತಿಫಲನ ತೆಗೆದುಹಾಕಿ.',
      loginHeroLine2: 'ಎಲ್ಲ ವಿವರ ಉಳಿಸಿ.',
      loginHeroSubtitle: 'ಲಾಗಿನ್ ಮಾಡಿ, ವಾಸ್ತುಶೈಲಿಯ ಚಿತ್ರಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ, ಎಕ್ಸ್‌ಪೋರ್ಟ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಿ ಮತ್ತು ಎಲ್ಲ ಫಲಿತಾಂಶಗಳನ್ನು ಒಂದೇ ಜಾಗದಲ್ಲಿ ಇಡಿ.',
      loginFeatureAccuracy: '98.4% ವಿಶ್ವಾಸ',
      loginFeatureSpeed: 'ವೇಗವಾದ ಪ್ರೊಸೆಸಿಂಗ್',
      loginFeatureOutput: 'ಸ್ವಚ್ಛ ಔಟ್‌ಪುಟ್',
      loginFeatureConfidence: 'ನಂಬಲರ್ಹ ಫಲಿತಾಂಶಗಳು',
      trustedBy: 'ಇವರಿಂದ ವಿಶ್ವಾಸಾರ್ಹ',
      creators: 'ವಾಸ್ತುಶಿಲ್ಪಿಗಳು, ಸಂಪಾದಕರು ಮತ್ತು ದೃಶ್ಯ ತಂಡಗಳು',
      signupBadge: 'ನಿಮ್ಮ ವರ್ಕ್‌ಸ್ಪೇಸ್ ರಚಿಸಿ',
      signupHeroLine1: 'ಚಿತ್ರಗಳನ್ನು ಸರಿಪಡಿಸಿ.',
      signupHeroLine2: 'ವಿತರಣೆಯನ್ನು ವೇಗಗೊಳಿಸಿ.',
      signupHeroSubtitle: 'ಖಾತೆ ರಚಿಸಿ, ಚಿತ್ರಗಳನ್ನು ಪ್ರೊಸೆಸ್ ಮಾಡಿ, ಕಲೆಕ್ಷನ್ ನಿರ್ಮಿಸಿ ಮತ್ತು ಕ್ಲೈಂಟ್‌ಗಳಿಗೆ ಪಾಳಿಷ್ಡ್ ಫಲಿತಾಂಶ ಹಂಚಿ.',
      accuracy: 'ಖಚಿತತೆ',
      processingLabel: 'ಪ್ರೊಸೆಸಿಂಗ್',
      resolution: 'ರೆಸಲ್ಯೂಶನ್',
      signupQuote: 'GlassClear ನಮ್ಮ ತಂಡಕ್ಕೆ ಕಠಿಣ ಪ್ರತಿಫಲನಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ, ಡಿಲಿವರಿ ನಿಧಾನಗೊಳಿಸದೆ.',
      signupQuoteAuthor: 'ಸ್ಟುಡಿಯೊ ವರ್ಕ್‌ಫ್ಲೋ ತಂಡ',
      accountCreatedLogin: 'ಖಾತೆ ಸಿದ್ಧವಾಗಿದೆ. ದಯವಿಟ್ಟು ಲಾಗಿನ್ ಮಾಡಿ.'
    },
    dashboard: {
      languageChanged: 'ಭಾಷೆ ಬದಲಾಗಿದೆ.',
      exportDownloaded: 'ಎಕ್ಸ್‌ಪೋರ್ಟ್ ಡೌನ್‌ಲೋಡ್ ಆಯಿತು.',
      exportUnavailable: 'ಪ್ರೊಸೆಸ್ ಮಾಡಿದ ಔಟ್‌ಪುಟ್ ಲಭ್ಯವಿಲ್ಲ.',
      exportFailed: 'ವಿಫಲವಾದ ಫಲಿತಾಂಶವನ್ನು ಎಕ್ಸ್‌ಪೋರ್ಟ್ ಮಾಡಲಾಗುವುದಿಲ್ಲ.',
      relogin: 'ಮುಂದುವರಿಸಲು ಮತ್ತೆ ಲಾಗಿನ್ ಮಾಡಿ.',
      deleteConfirm: 'ಇತಿಹಾಸದಿಂದ "{filename}" ಅಳಿಸಬೇಕೇ?',
      viewResult: 'ಫಲಿತಾಂಶ ನೋಡಿ',
      uploadImageToView: 'ನಿಮ್ಮ ಹೊಸ ಫಲಿತಾಂಶ ನೋಡಲು ಚಿತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ.'
    },
    history: {
      title: 'ಇತಿಹಾಸ',
      subtitle: 'ಈ ಖಾತೆಯ ಎಲ್ಲಾ ಪ್ರೊಸೆಸ್ ಆದ GlassClear ಚಿತ್ರಗಳು.',
      viewAll: 'ಪೂರ್ಣ ಇತಿಹಾಸ ನೋಡಿ',
      emptyTitle: 'ಇನ್ನೂ ಇತಿಹಾಸ ಇಲ್ಲ',
      emptyMessage: 'ನಿಮ್ಮ ಇತಿಹಾಸ ನಿರ್ಮಿಸಲು ಚಿತ್ರಗಳನ್ನು ಪ್ರೊಸೆಸ್ ಮಾಡಿ.',
      deleteSuccess: 'ಇತಿಹಾಸ ಐಟಂ ಅಳಿಸಲಾಗಿದೆ.',
      all: 'ಎಲ್ಲಾ',
      uploaded: 'ಅಪ್ಲೋಡ್ ಮಾಡಲಾಗಿದೆ'
    },
    albums: {
      title: 'ಸ್ಮಾರ್ಟ್ ಆಲ್ಬಮ್‌ಗಳು',
      subtitle: 'ನಿಮ್ಮ ಪ್ರೊಸೆಸ್ ಆದ GlassClear ಫಲಿತಾಂಶಗಳ ಸರಿಯಾದ ಸಂಗ್ರಹಗಳು.',
      viewAll: 'ಎಲ್ಲಾ ಆಲ್ಬಮ್‌ಗಳನ್ನು ನೋಡಿ',
      viewAlbum: 'ಆಲ್ಬಮ್ ನೋಡಿ',
      imagesLabel: 'ಚಿತ್ರಗಳು',
      updatedLabel: 'ಅಪ್ಡೇಟ್',
      justNow: 'ಇತ್ತೀಚೆಗೆ ಅಪ್ಡೇಟ್ ಮಾಡಲಾಗಿದೆ',
      emptyTitle: 'ಇನ್ನೂ ಸ್ಮಾರ್ಟ್ ಆಲ್ಬಮ್‌ಗಳಿಲ್ಲ',
      emptyMessage: 'ಪ್ರೊಸೆಸ್ ಆದ ಚಿತ್ರಗಳು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಪ್ರೀಮಿಯಂ ಆಲ್ಬಮ್‌ಗಳಲ್ಲಿ ಕಾಣಿಸುತ್ತವೆ.',
      emptyAlbumTitle: 'ಈ ಆಲ್ಬಮ್‌ನಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ಚಿತ್ರಗಳಿಲ್ಲ.',
      emptyAlbumMessage: 'ಇನ್ನಷ್ಟು ಚಿತ್ರಗಳನ್ನು ಪ್ರೊಸೆಸ್ ಮಾಡಿದರೆ GlassClear ಅವನ್ನು ಇಲ್ಲಿ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಇಡುತ್ತದೆ.',
      notFoundTitle: 'ಆಲ್ಬಮ್ ಸಿಗಲಿಲ್ಲ',
      notFoundMessage: 'ಈ ಆಲ್ಬಮ್ ಸ್ಲಗ್ ಅಮಾನ್ಯವಾಗಿದೆ ಅಥವಾ ನಿಮ್ಮ ಖಾತೆಗೆ ಲಭ್ಯವಿಲ್ಲ.',
      fallbackName: 'ವಿವಿಧ',
      routeUnavailable: 'ಆಲ್ಬಮ್ ಮಾರ್ಗ ಈಗ ಲಭ್ಯವಿಲ್ಲ.',
      noMatchingImages: 'ಹೊಂದುವ ಚಿತ್ರಗಳು ಸಿಗಲಿಲ್ಲ.',
      searchHelp: 'ಈ ಆಲ್ಬಮ್‌ಗೆ ಬೇರೆ ಹುಡುಕಾಟ ಪದ ಪ್ರಯತ್ನಿಸಿ.',
      smartAlbumLabel: 'ಸ್ಮಾರ್ಟ್ ಆಲ್ಬಮ್'
    },
    batch: {
      completed: 'ಪೂರ್ಣ',
      failed: 'ವಿಫಲ'
    },
    collections: {
      title: 'ಕಲೆಕ್ಷನ್‌ಗಳು',
      subtitle: 'ತಂಡ ಮತ್ತು ಕ್ಲೈಂಟ್‌ಗಳಿಗಾಗಿ ಮುಖ್ಯ ಫಲಿತಾಂಶಗಳನ್ನು ಆರಿಸಿದ ಫೋಲ್ಡರ್‌ಗಳಲ್ಲಿ ಉಳಿಸಿ.',
      fallbackName: 'ಕಲೆಕ್ಷನ್',
      newCollection: 'ಹೊಸ ಕಲೆಕ್ಷನ್',
      createCollection: 'ಕಲೆಕ್ಷನ್ ರಚಿಸಿ',
      createNew: 'ಹೊಸ ಕಲೆಕ್ಷನ್ ರಚಿಸಿ',
      creating: 'ರಚಿಸಲಾಗುತ್ತಿದೆ...',
      viewAll: 'ಎಲ್ಲಾ ಕಲೆಕ್ಷನ್‌ಗಳನ್ನು ನೋಡಿ',
      addLatest: 'ಹೊಸ ಫಲಿತಾಂಶ ಸೇರಿಸಿ',
      addLatestShort: 'ಫಲಿತಾಂಶ ಸೇರಿಸಿ',
      addingLatest: 'ಹೊಸದು ಸೇರಿಸಲಾಗುತ್ತಿದೆ...',
      adding: 'ಸೇರಿಸಲಾಗುತ್ತಿದೆ...',
      addToCollection: 'ಕಲೆಕ್ಷನ್‌ಗೆ ಸೇರಿಸಿ',
      processBeforeAdd: 'ಕಲೆಕ್ಷನ್‌ಗೆ ಸೇರಿಸುವ ಮೊದಲು ಒಂದು ಚಿತ್ರವನ್ನು ಪ್ರೊಸೆಸ್ ಮಾಡಿ.',
      selectFirst: 'ಮೊದಲು ಒಂದು ಕಲೆಕ್ಷನ್ ಆಯ್ಕೆಮಾಡಿ.',
      created: 'ಕಲೆಕ್ಷನ್ ರಚಿಸಲಾಗಿದೆ.',
      createFailed: 'ಕಲೆಕ್ಷನ್ ರಚಿಸಲಾಗಲಿಲ್ಲ.',
      latestAdded: 'ಹೊಸ ಫಲಿತಾಂಶ ಕಲೆಕ್ಷನ್‌ಗೆ ಸೇರಿಸಲಾಗಿದೆ.',
      addFailed: 'ಫಲಿತಾಂಶ ಸೇರಿಸಲಾಗಲಿಲ್ಲ.',
      cardDescription: 'ವೇಗವಾದ ಪ್ರವೇಶ ಮತ್ತು ವಿತರಣೆಗೆ ನಿಮ್ಮ ಸ್ವಚ್ಛ ಔಟ್‌ಪುಟ್‌ಗಳನ್ನು ವ್ಯವಸ್ಥೆಗೊಳಿಸಿ.',
      emptyMessage: 'ನಿಮ್ಮ ಫಲಿತಾಂಶಗಳನ್ನು ವ್ಯವಸ್ಥೆಗೊಳಿಸಲು ಒಂದು ಕಲೆಕ್ಷನ್ ರಚಿಸಿ.',
      name: 'ಕಲೆಕ್ಷನ್ ಹೆಸರು',
      placeholder: 'ಕಲೆಕ್ಷನ್ ಹೆಸರು ನಮೂದಿಸಿ',
      chooseSaveLocation: 'ಈ ಫಲಿತಾಂಶವನ್ನು ಎಲ್ಲಿಗೆ ಉಳಿಸಬೇಕು ಆಯ್ಕೆಮಾಡಿ.',
      createPersonal: 'ಈ ಚಿತ್ರಕ್ಕಾಗಿ ಹೊಸ ಕಲೆಕ್ಷನ್ ರಚಿಸಿ.',
      detailSubtitle: 'ಈ ಕಲೆಕ್ಷನ್‌ನಲ್ಲಿ ನಿಮ್ಮ ಉಳಿಸಿದ ಫಲಿತಾಂಶಗಳು.',
      removeConfirm: '{filename} ಅನ್ನು ಈ ಕಲೆಕ್ಷನ್‌ನಿಂದ ತೆಗೆದುಹಾಕಬೇಕೇ?',
      removed: 'ಐಟಂ ಕಲೆಕ್ಷನ್‌ನಿಂದ ತೆಗೆದುಹಾಕಲಾಗಿದೆ.',
      removeFailed: 'ಐಟಂ ತೆಗೆದುಹಾಕಲಾಗಲಿಲ್ಲ.',
      loadFailed: 'ಕಲೆಕ್ಷನ್ ಲೋಡ್ ಆಗಲಿಲ್ಲ.',
      emptyDetailTitle: 'ಈ ಕಲೆಕ್ಷನ್‌ನಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ಚಿತ್ರಗಳಿಲ್ಲ.',
      emptyDetailMessage: 'ಈ ಕಲೆಕ್ಷನ್ ಅನ್ನು ವ್ಯವಸ್ಥೆಗೊಳಿಸಲು ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಿಂದ ಫಲಿತಾಂಶಗಳನ್ನು ಸೇರಿಸಿ.',
      viewAllShort: 'ಎಲ್ಲಾ ಕಲೆಕ್ಷನ್‌ಗಳನ್ನು ನೋಡಿ'
    },
    delivery: {
      title: 'ಕ್ಲೈಂಟ್ ಡಿಲಿವರಿ ಪ್ಯಾಕ್',
      subtitle: 'ನಿಮ್ಮ ಇತ್ತೀಚಿನ ಸ್ವಚ್ಛಗೊಳಿಸಿದ ಫಲಿತಾಂಶಕ್ಕೆ ಸುವ್ಯವಸ್ಥಿತ ಹ್ಯಾಂಡ್ಆಫ್ ಪ್ಯಾಕ್ ತಯಾರಿಸಿ.',
      latestCompleted: 'ಇತ್ತೀಚಿನ ಪೂರ್ಣಗೊಂಡ ಫಲಿತಾಂಶ',
      generate: 'ಪ್ಯಾಕ್ ರಚಿಸಿ',
      generating: 'ರಚಿಸಲಾಗುತ್ತಿದೆ...',
      download: 'ಪ್ಯಾಕ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ',
      downloading: 'ಡೌನ್‌ಲೋಡ್ ಆಗುತ್ತಿದೆ...',
      emptyMessage: 'ಡಿಲಿವರಿ ಪ್ಯಾಕ್ ತಯಾರಿಸಲು ಒಂದು ಚಿತ್ರವನ್ನು ಪ್ರೊಸೆಸ್ ಮಾಡಿ.',
      ready: 'ಡಿಲಿವರಿ ಪ್ಯಾಕ್ ಸಿದ್ಧವಾಗಿದೆ.',
      generateFailed: 'ಡಿಲಿವರಿ ಪ್ಯಾಕ್ ರಚಿಸಲಾಗಲಿಲ್ಲ.',
      generateFirst: 'ಮೊದಲು ಡಿಲಿವರಿ ಪ್ಯಾಕ್ ರಚಿಸಿ.',
      downloaded: 'ಡಿಲಿವರಿ ಪ್ಯಾಕ್ ಡೌನ್‌ಲೋಡ್ ಆಯಿತು.',
      downloadFailed: 'ಡಿಲಿವರಿ ಪ್ಯಾಕ್ ಡೌನ್‌ಲೋಡ್ ಆಗಲಿಲ್ಲ.',
      latestReady: 'ಇತ್ತೀಚಿನ ಫಲಿತಾಂಶ ಡಿಲಿವರಿಗೆ ಸಿದ್ಧವಾಗಿದೆ.',
      historyGenerate: 'ಪ್ರೊಸೆಸಿಂಗ್ ನಂತರ ಇತಿಹಾಸದಿಂದ ಡಿಲಿವರಿ ಪ್ಯಾಕ್ ರಚಿಸಿ.'
    },
    processing: {
      title: 'GlassClear ಪ್ರೊಸೆಸಿಂಗ್',
      subtitle: 'ಪ್ರತಿಫಲನ ತೆಗೆದುಹಾಕಲಾಗುತ್ತಿದೆ, glare ಸಮತೋಲನಗೊಳಿಸಲಾಗುತ್ತಿದೆ, ಮತ್ತು ಸ್ವಚ್ಛ ವಾಸ್ತುಶೈಲಿಯ ಫಲಿತಾಂಶ ತಯಾರಾಗುತ್ತಿದೆ.',
      badge: 'ಪ್ರೊಸೆಸಿಂಗ್',
      aiProcessing: 'AI ಪ್ರೊಸೆಸಿಂಗ್',
      aiStatus: 'AI ಸ್ಥಿತಿ',
      uploaded: 'ಅಪ್ಲೋಡ್ ಆಯಿತು',
      processing: 'ಪ್ರೊಸೆಸಿಂಗ್',
      finalizing: 'ಅಂತಿಮಗೊಳಿಸಲಾಗುತ್ತಿದೆ',
      preparingPreview: 'ಪ್ರೀವ್ಯೂ ತಯಾರಾಗುತ್ತಿದೆ...',
      changeImage: 'ಚಿತ್ರ ಬದಲಿಸಿ',
      statusUploadComplete: 'ಅಪ್ಲೋಡ್ ಪೂರ್ಣಗೊಂಡಿದೆ.',
      statusScanning: 'ಪ್ರತಿಫಲನ ಪ್ರದೇಶಗಳನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಲಾಗುತ್ತಿದೆ...',
      statusRemoving: 'ಪ್ರತಿಫಲನಗಳನ್ನು ತೆಗೆದುಹಾಕಲಾಗುತ್ತಿದೆ...',
      statusFinalizing: 'ಔಟ್‌ಪುಟ್ ಅಂತಿಮಗೊಳಿಸಲಾಗುತ್ತಿದೆ...'
    },
    resultDetail: {
      title: 'GlassClear ಫಲಿತಾಂಶ',
      kicker: 'ಹೊಸ ಫಲಿತಾಂಶ ಸಿದ್ಧವಾಗಿದೆ',
      subtitle: 'ಸ್ವಚ್ಛ ಔಟ್‌ಪುಟ್ ಪರಿಶೀಲಿಸಿ, ಅದನ್ನು ಮೂಲ ಕ್ಯಾಪ್ಚರ್ ಜೊತೆ ಹೋಲಿಸಿ, ಮತ್ತು ಬೇಕಾದ ಆವೃತ್ತಿಯನ್ನು ಎಕ್ಸ್‌ಪೋರ್ಟ್ ಮಾಡಿ.',
      summary: 'ಫಲಿತಾಂಶ ಸಾರಾಂಶ',
      statusReady: 'ಫಲಿತಾಂಶ ಸಿದ್ಧ',
      fileName: 'ಫೈಲ್ ಹೆಸರು',
      resolution: 'ರೆಸಲ್ಯೂಶನ್',
      format: 'ಫಾರ್ಮಾಟ್',
      mode: 'ಮೋಡ್',
      processedOn: 'ಪ್ರೊಸೆಸ್ಡ್ ದಿನಾಂಕ',
      exportTitle: 'ಎಕ್ಸ್‌ಪೋರ್ಟ್ ಔಟ್‌ಪುಟ್',
      exportOptions: 'ಎಕ್ಸ್‌ಪೋರ್ಟ್ ಆಯ್ಕೆಗಳು',
      exportHelp: 'ನಿಮ್ಮ ಫಾರ್ಮಾಟ್ ಆಯ್ಕೆ ಮಾಡಿ ಮತ್ತು ತಕ್ಷಣ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.',
      exportNote: 'ಉಚಿತ ಎಕ್ಸ್‌ಪೋರ್ಟ್. ಸ್ವಚ್ಛ ಔಟ್‌ಪುಟ್. ಹೆಚ್ಚುವರಿ ಹಂತಗಳಿಲ್ಲ.',
      back: 'ಹೊಸ ಫಲಿತಾಂಶ ಸಿದ್ಧವಾಗಿದೆ',
      changeImage: 'ಚಿತ್ರ ಬದಲಿಸಿ',
      aiStatus: 'AI ಸ್ಥಿತಿ',
      uploadComplete: 'ಅಪ್ಲೋಡ್ ಆಯಿತು',
      processed: 'ಪ್ರೊಸೆಸ್ ಆಯಿತು',
      exportReady: 'ಎಕ್ಸ್‌ಪೋರ್ಟ್ ಸಿದ್ಧ',
      readyForExport: '{status} ಮತ್ತು ಎಕ್ಸ್‌ಪೋರ್ಟ್‌ಗೆ ಸಿದ್ಧ.',
      downloading: 'ಡೌನ್‌ಲೋಡ್ ಆಗುತ್ತಿದೆ...'
    },
    result: {
      feedback: 'ರಚನೆ, ಬೆಳಕು ಮತ್ತು ದೃಶ್ಯದ ವಿವರಗಳನ್ನು ಉಳಿಸಿಕೊಂಡೇ ಪ್ರತಿಫಲನದ ಕಲೆಗಳು ಕಡಿತಗೊಳಿಸಲ್ಪಟ್ಟಿವೆ.'
    },
    footer: {
      social: 'ಸೋಶಿಯಲ್',
      email: 'ಇಮೇಲ್',
      support: 'ಸಪೋರ್ಟ್',
      links: 'ಲಿಂಕ್‌ಗಳು',
      socials: 'ಸೋಶಿಯಲ್ಸ್',
      newsletter: 'ನ್ಯೂಸ್‌ಲೆಟರ್',
      home: 'ಮುಖಪುಟ',
      dashboard: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
      heading: 'GlassClear ಜೊತೆ ಅಪ್ಡೇಟ್ ಆಗಿ ಇರಿ',
      body: 'AI ರಿಸ್ಟೋರೇಶನ್, ಪ್ರತಿಫಲನ ನಿವಾರಣೆ ಮತ್ತು ವಾಸ್ತುಶೈಲಿಯ ಚಿತ್ರಣ ವರ್ಕ್‌ಫ್ಲೋ ಅಪ್ಡೇಟ್‌ಗಳನ್ನು ಪಡೆಯಿರಿ.',
      inputPlaceholder: 'ಇಮೇಲ್ ವಿಳಾಸ ನಮೂದಿಸಿ',
      subscribe: 'ಚಂದಾದಾರರಾಗಿ',
      subscribed: 'ಚಂದಾದಾರರಾಗಿದ್ದೀರಿ!',
      taglineLine1: 'ಪ್ರತಿಫಲನದಾಚೆ.',
      taglineLine2: 'ಸ್ಪಷ್ಟತೆಗೆ ನಿರ್ಮಿತ.',
      copyright: '© 2026 GlassClear AI. ಎಲ್ಲಾ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ.',
      privacy: 'ಗೌಪ್ಯತಾ ನೀತಿ',
      terms: 'ಸೇವಾ ನಿಯಮಗಳು'
    },
    navbar: {
      features: 'ವೈಶಿಷ್ಟ್ಯಗಳು',
      products: 'ಉತ್ಪನ್ನಗಳು',
      resources: 'ಸಂಪನ್ಮೂಲಗಳು',
      dashboard: 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
      uploadImage: 'ಚಿತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ',
      smartAlbums: 'ಸ್ಮಾರ್ಟ್ ಆಲ್ಬಮ್‌ಗಳು',
      history: 'ಇತಿಹಾಸ',
      howItWorks: 'ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
      seeItInAction: 'ಇದನ್ನು ಕೆಲಸದಲ್ಲಿ ನೋಡಿ',
      faq: 'FAQ',
      toggleNavigation: 'ನಾವಿಗೇಶನ್ ಟಾಗಲ್ ಮಾಡಿ',
      primaryNavigation: 'ಮುಖ್ಯ ನಾವಿಗೇಶನ್',
      userMenu: 'ಬಳಕೆದಾರ ಪ್ರೊಫೈಲ್ ಮೆನು',
      quickStart: 'ಕ್ವಿಕ್ ಸ್ಟಾರ್ಟ್',
      newUpload: 'ಹೊಸ ಅಪ್ಲೋಡ್'
    }
  }
};

const supplementalTranslations = {
  en: {
    common: {
      imagesCount: '{count} images',
      notAvailable: 'N/A',
      ready: 'Ready',
      sample: 'Sample'
    },
    dashboard: {
      previewPending: 'The processed preview will appear here as soon as your image is ready.',
      systemHealth: 'System Health',
      online: 'Online',
      modelConfidence: '96% Model Confidence',
      aiReflectionStudio: 'AI Reflection Studio'
    },
    resultDetail: {
      compareSummary: 'Compare the original and GlassClear output.',
      standardMode: 'Standard'
    },
    unlockResult: {
      ariaLabel: 'Unlock your GlassClear result',
      kicker: 'Download Image',
      title: 'Login or signup to download this image',
      body: 'Please login or create an account to download your processed result.',
      noteTitle: 'Download is available after login',
      noteBody: 'Once you login or signup, you can download this image and access your saved results.',
      benefitHd: 'HD download',
      benefitHistory: 'Save to project history',
      benefitWorkspace: 'AI editor workspace',
      benefitShare: 'Share and collage tools',
      continueLogin: 'Login',
      createAccount: 'Signup',
      maybeLater: 'Close'
    },
    landing: {
      showcase: {
        workspace: {
          panelTitle: 'Restoration Queue',
          item1Name: 'facade-glass-01.jpg',
          item2Name: 'lobby-window-02.jpg',
          item3Name: 'tower-exterior-03.jpg',
          item4Name: 'interior-glass-04.jpg'
        },
        albums: {
          item1Name: 'Glass Facade',
          item2Name: 'Interior Reflection',
          item3Name: 'Outdoor Architecture',
          item4Name: 'High Glare',
          latestPrefix: 'Latest'
        }
      }
    }
  },
  hi: {
    common: {
      imagesCount: '{count} इमेज',
      notAvailable: 'उपलब्ध नहीं',
      ready: 'तैयार',
      sample: 'सैंपल'
    },
    dashboard: {
      previewPending: 'जैसे ही आपकी इमेज तैयार होगी, प्रोसेस्ड प्रीव्यू यहां दिखाई देगा।',
      systemHealth: 'सिस्टम हेल्थ',
      online: 'ऑनलाइन',
      modelConfidence: '96% मॉडल कॉन्फिडेंस',
      aiReflectionStudio: 'AI रिफ्लेक्शन स्टूडियो'
    },
    resultDetail: {
      compareSummary: 'ओरिजिनल और GlassClear आउटपुट की तुलना करें।',
      standardMode: 'स्टैंडर्ड'
    },
    unlockResult: {
      ariaLabel: 'अपना GlassClear रिजल्ट अनलॉक करें',
      kicker: 'GlassClear रिजल्ट',
      title: 'आपका GlassClear रिजल्ट तैयार है',
      body: 'डाउनलोड करने, सेव करने और अपनी रिस्टोर की गई इमेज को आगे एडिट करने के लिए मुफ्त अकाउंट बनाएं।',
      benefitHd: 'HD डाउनलोड',
      benefitHistory: 'प्रोजेक्ट हिस्ट्री में सेव करें',
      benefitWorkspace: 'AI एडिटर वर्कस्पेस',
      benefitShare: 'शेयर और कोलाज टूल्स',
      continueLogin: 'लॉगिन के साथ जारी रखें',
      createAccount: 'अकाउंट बनाएं',
      maybeLater: 'बाद में'
    },
    landing: {
      showcase: {
        workspace: {
          panelTitle: 'रिस्टोरेशन क्यू',
          item1Name: 'facade-glass-01.jpg',
          item2Name: 'lobby-window-02.jpg',
          item3Name: 'tower-exterior-03.jpg',
          item4Name: 'interior-glass-04.jpg'
        },
        albums: {
          item1Name: 'ग्लास फसाड',
          item2Name: 'इंटीरियर रिफ्लेक्शन',
          item3Name: 'आउटडोर आर्किटेक्चर',
          item4Name: 'हाई ग्लेयर',
          latestPrefix: 'नवीनतम'
        }
      }
    }
  },
  kn: {
    common: {
      imagesCount: '{count} ಚಿತ್ರಗಳು',
      notAvailable: 'ಲಭ್ಯವಿಲ್ಲ',
      ready: 'ಸಿದ್ಧ',
      sample: 'ಸ್ಯಾಂಪಲ್'
    },
    dashboard: {
      previewPending: 'ನಿಮ್ಮ ಚಿತ್ರ ಸಿದ್ಧವಾದ ತಕ್ಷಣ ಪ್ರೊಸೆಸ್ಡ್ ಪ್ರಿವ್ಯೂ ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತದೆ.',
      systemHealth: 'ಸಿಸ್ಟಮ್ ಆರೋಗ್ಯ',
      online: 'ಆನ್‌ಲೈನ್',
      modelConfidence: '96% ಮಾದರಿ ವಿಶ್ವಾಸ',
      aiReflectionStudio: 'AI ಪ್ರತಿಫಲನ ಸ್ಟುಡಿಯೋ'
    },
    resultDetail: {
      compareSummary: 'ಮೂಲ ಚಿತ್ರ ಮತ್ತು GlassClear ಔಟ್‌ಪುಟ್ ಅನ್ನು ಹೋಲಿಸಿ.',
      standardMode: 'ಸ್ಟಾಂಡರ್ಡ್'
    },
    unlockResult: {
      ariaLabel: 'ನಿಮ್ಮ GlassClear ಫಲಿತಾಂಶವನ್ನು ಅನ್ಲಾಕ್ ಮಾಡಿ',
      kicker: 'GlassClear ಫಲಿತಾಂಶ',
      title: 'ನಿಮ್ಮ GlassClear ಫಲಿತಾಂಶ ಸಿದ್ಧವಾಗಿದೆ',
      body: 'ಡೌನ್‌ಲೋಡ್ ಮಾಡಲು, ಉಳಿಸಲು ಮತ್ತು ಮರುಸ್ಥಾಪಿತ ಚಿತ್ರವನ್ನು ಮುಂದುವರಿಸಿ ಸಂಪಾದಿಸಲು ಉಚಿತ ಖಾತೆ ರಚಿಸಿ.',
      benefitHd: 'HD ಡೌನ್‌ಲೋಡ್',
      benefitHistory: 'ಪ್ರಾಜೆಕ್ಟ್ ಇತಿಹಾಸಕ್ಕೆ ಉಳಿಸಿ',
      benefitWorkspace: 'AI ಎಡಿಟರ್ ಕಾರ್ಯಕ್ಷೇತ್ರ',
      benefitShare: 'ಶೇರ್ ಮತ್ತು ಕೊಲಾಜ್ ಸಾಧನಗಳು',
      continueLogin: 'ಲಾಗಿನ್‌ನೊಂದಿಗೆ ಮುಂದುವರಿಸಿ',
      createAccount: 'ಖಾತೆ ರಚಿಸಿ',
      maybeLater: 'ನಂತರ'
    },
    landing: {
      showcase: {
        workspace: {
          panelTitle: 'ರಿಸ್ಟೋರೇಶನ್ ಕ್ಯೂ',
          item1Name: 'facade-glass-01.jpg',
          item2Name: 'lobby-window-02.jpg',
          item3Name: 'tower-exterior-03.jpg',
          item4Name: 'interior-glass-04.jpg'
        },
        albums: {
          item1Name: 'ಗ್ಲಾಸ್ ಫಸಾಡ್',
          item2Name: 'ಇಂಟೀರಿಯರ್ ಪ್ರತಿಫಲನ',
          item3Name: 'ಔಟ್‌ಡೋರ್ ಆರ್ಕಿಟೆಕ್ಚರ್',
          item4Name: 'ಹೈ ಗ್ಲೇರ್',
          latestPrefix: 'ಇತ್ತೀಚಿನ'
        }
      }
    }
  }
};

function isObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function mergeLocale(base = {}, extra = {}) {
  const merged = { ...base };

  for (const [key, value] of Object.entries(extra)) {
    if (isObject(value) && isObject(base[key])) {
      merged[key] = mergeLocale(base[key], value);
    } else {
      merged[key] = value;
    }
  }

  return merged;
}

export const translations = Object.fromEntries(
  Object.keys(baseTranslations).map((locale) => [
    locale,
    mergeLocale(
      baseTranslations[locale],
      mergeLocale(
        appTranslations[locale] || {},
        mergeLocale(landingTranslations[locale] || {}, supplementalTranslations[locale] || {})
      )
    )
  ])
);

export const SUPPORTED_LOCALES = ['en', 'hi', 'kn'];
