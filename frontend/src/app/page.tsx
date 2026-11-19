import React from 'react';
import { HomeClientView } from '../components/HomeClientView';
import { fetchProducts, fetchReviews } from '../lib/api';

export const runtime = 'edge';
export const dynamic = 'force-dynamic';

export default async function HomePage() {
  const products = await fetchProducts();
  const reviews = await fetchReviews();

  return <HomeClientView products={products || []} reviews={reviews || []} />;
}
