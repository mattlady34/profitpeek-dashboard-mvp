// Analytics utility for tracking user events

declare global {
  interface Window {
    gtag: (...args: any[]) => void;
    mixpanel: any;
  }
}

// Google Analytics tracking
export const trackGA = (action: string, category: string, label?: string, value?: number) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }
};

// Mixpanel tracking
export const trackMixpanel = (event: string, properties?: Record<string, any>) => {
  if (typeof window !== 'undefined' && window.mixpanel) {
    window.mixpanel.track(event, properties);
  }
};

// Combined tracking function
export const trackEvent = (event: string, properties?: Record<string, any>) => {
  // Track in Google Analytics
  trackGA(event, 'User Interaction', properties?.category || 'App');
  
  // Track in Mixpanel
  trackMixpanel(event, properties);
};

// Specific event tracking functions
export const trackAppLoaded = () => {
  trackEvent('app_loaded', {
    timestamp: new Date().toISOString(),
    url: window.location.href,
  });
};

export const trackDemoModeStarted = () => {
  trackEvent('demo_mode_started', {
    timestamp: new Date().toISOString(),
    source: 'landing_page',
  });
};

export const trackStoreConnected = (shop: string) => {
  trackEvent('store_connected', {
    shop: shop,
    timestamp: new Date().toISOString(),
  });
};

export const trackDashboardViewed = () => {
  trackEvent('dashboard_viewed', {
    timestamp: new Date().toISOString(),
    page: 'dashboard',
  });
};

export const trackOrdersViewed = () => {
  trackEvent('orders_viewed', {
    timestamp: new Date().toISOString(),
    page: 'orders',
  });
};

export const trackSettingsUpdated = (settings: Record<string, any>) => {
  trackEvent('settings_updated', {
    settings: settings,
    timestamp: new Date().toISOString(),
  });
};

export const trackError = (error: string, context?: string) => {
  trackEvent('error_occurred', {
    error: error,
    context: context,
    timestamp: new Date().toISOString(),
    url: window.location.href,
  });
};

export const trackPageView = (page: string) => {
  trackEvent('page_viewed', {
    page: page,
    timestamp: new Date().toISOString(),
    url: window.location.href,
  });
};

// User identification
export const identifyUser = (userId: string, properties?: Record<string, any>) => {
  if (typeof window !== 'undefined' && window.mixpanel) {
    window.mixpanel.identify(userId);
    if (properties) {
      window.mixpanel.people.set(properties);
    }
  }
};

// Set user properties
export const setUserProperties = (properties: Record<string, any>) => {
  if (typeof window !== 'undefined' && window.mixpanel) {
    window.mixpanel.people.set(properties);
  }
};
