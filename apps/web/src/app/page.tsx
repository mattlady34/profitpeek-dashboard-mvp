'use client';

import { useEffect } from 'react';
import { trackPageView } from './utils/analytics';

export default function Home() {
  useEffect(() => {
    trackPageView('home');
    // Redirect to marketing page
    window.location.href = '/marketing';
  }, []);

  return (
    <div>
      <h1>Redirecting to ProfitPeek...</h1>
      <p>Please wait while we redirect you to our marketing page.</p>
    </div>
  );
}