import React from 'react';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { fetchProductById } from '../../../lib/api';
import { ProductDetailClient } from './ProductDetailClient';

export const runtime = 'edge';
export const dynamic = 'force-dynamic';

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const product = await fetchProductById(params.id);
  if (!product) {
    return {
      title: 'Product Not Found | NEXORA',
      description: 'The requested gadget is not available in NEXORA catalog.',
    };
  }

  return {
    title: `${product.name} | NEXORA Flagship Hardware`,
    description: product.tagline || product.description,
    openGraph: {
      title: `${product.name} — ৳${product.priceBDT.toLocaleString()} | NEXORA`,
      description: product.description,
      images: [
        {
          url: product.image,
          width: 1200,
          height: 630,
          alt: product.name,
        },
      ],
      siteName: 'NEXORA',
    },
    twitter: {
      card: 'summary_large_image',
      title: product.name,
      description: product.tagline,
      images: [product.image],
    },
  };
}

export default async function ProductDetailPage({ params }: { params: { id: string } }) {
  const product = await fetchProductById(params.id);

  if (!product) {
    notFound();
  }

  // Schema.org Structured JSON-LD
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: product.image,
    description: product.description,
    brand: {
      '@type': 'Brand',
      name: product.brand || 'NEXORA',
    },
    offers: {
      '@type': 'Offer',
      priceCurrency: 'BDT',
      price: product.priceBDT,
      availability: product.inStock ? 'https://schema.org/InStock' : 'https://schema.org/PreOrder',
      itemCondition: 'https://schema.org/NewCondition',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: product.rating || 5,
      reviewCount: product.reviewCount || 10,
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <ProductDetailClient product={product} />
    </>
  );
}
