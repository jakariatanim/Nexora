import React from 'react';
import { fetchReviews } from '../../lib/api';
import { ReviewsClient } from './ReviewsClient';

export const runtime = 'edge';
export const dynamic = 'force-dynamic';

export const metadata = {
  title: 'Community Reviews & Ratings | NEXORA',
  description: 'Read authentic verified customer reviews and ratings on flagship hardware from NEXORA.',
};

export default async function ReviewsPage() {
  const reviews = await fetchReviews();

  return <ReviewsClient initialReviews={reviews} />;
}
