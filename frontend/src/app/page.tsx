import React from 'react';
import { HomeClientView } from '../components/HomeClientView';
import { fetchProducts, fetchReviews } from '../lib/api';
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-dynamic';

export default async function HomePage() {
  let products = await fetchProducts();
  let reviews = await fetchReviews();

  if (!products || products.length === 0) {
    try {
      const dataPath = path.join(process.cwd(), '..', 'backend', 'data', 'products.json');
      if (fs.existsSync(dataPath)) {
        products = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
      }
    } catch {}
  }

  return <HomeClientView products={products || []} reviews={reviews || []} />;
}
