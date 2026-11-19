'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Review } from '../../lib/types';
import { Star, CheckCircle, MessageSquarePlus, X, ChevronLeft, Search } from 'lucide-react';
import { submitReview } from '../../lib/api';

export const ReviewsClient: React.FC<{ initialReviews: Review[] }> = ({ initialReviews }) => {
  const [reviews, setReviews] = useState<Review[]>(initialReviews);
  const [selectedRating, setSelectedRating] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [author, setAuthor] = useState('');
  const [productName, setProductName] = useState('Apple iPhone 18 Pro Max');
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);

  const filteredReviews = reviews.filter((rev) => {
    const matchesRating = selectedRating === null || rev.rating === selectedRating;
    const matchesSearch =
      rev.comment.toLowerCase().includes(searchQuery.toLowerCase()) ||
      rev.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      rev.author.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesRating && matchesSearch;
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const newRev = await submitReview({
      author,
      productName,
      rating,
      comment,
    });
    if (newRev && newRev.id) {
      setReviews([newRev, ...reviews]);
      setIsModalOpen(false);
      setComment('');
      setAuthor('');
    }
    setLoading(false);
  };

  const averageRating = (
    reviews.reduce((acc, r) => acc + r.rating, 0) / (reviews.length || 1)
  ).toFixed(1);

  return (
    <div className="min-h-screen bg-[#F7F4EE] dark:bg-[#080E1E] pt-28 pb-20 px-4 sm:px-6 transition-colors">
      <div className="max-w-6xl mx-auto space-y-10">
        
        {/* Navigation Breadcrumb (High contrast in light & dark mode) */}
        <div>
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white dark:bg-[#121624] border border-black/10 dark:border-white/15 text-[#0071E3] dark:text-[#38BDF8] hover:bg-[#0071E3] hover:text-white dark:hover:bg-[#0071E3] dark:hover:text-white transition-all shadow-sm text-sm font-semibold"
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Back to Store Home</span>
          </Link>
        </div>

        {/* Header Banner - Responsive spacing & layout */}
        <div className="p-5 sm:p-12 rounded-2xl sm:rounded-3xl bg-white dark:bg-[#121624] border border-black/[0.08] dark:border-white/10 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6 sm:gap-8">
          <div className="space-y-2 sm:space-y-3 text-center md:text-left">
            <span className="text-xs font-mono uppercase tracking-widest text-[#0071E3] dark:text-[#38BDF8] font-semibold block">
              Authentic Feedback &amp; Verification
            </span>
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-semibold text-[#1D1D1F] dark:text-white tracking-tight">
              Community Reviews
            </h1>
            <p className="text-sm sm:text-base text-[#555558] dark:text-[#CBD5E1] max-w-xl leading-relaxed">
              Transparent experiences and honest ratings from verified creators, developers, and hardware enthusiasts across Bangladesh.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-6 w-full md:w-auto">
            <div className="p-4 sm:p-5 rounded-2xl bg-[#F5F5F7] dark:bg-white/5 border border-black/[0.06] dark:border-white/10 text-center min-w-[130px] w-full sm:w-auto">
              <div className="text-3xl sm:text-4xl font-bold text-[#1D1D1F] dark:text-white font-mono">{averageRating}</div>
              <div className="flex justify-center gap-0.5 text-amber-500 my-1">
                {[1, 2, 3, 4, 5].map((s) => (
                  <Star key={s} className="w-4 h-4 fill-amber-400 text-amber-400" />
                ))}
              </div>
              <div className="text-[11px] sm:text-xs text-[#6E6E73] dark:text-[#A1A1A6] font-mono">{reviews.length} Total Reviews</div>
            </div>

            <button
              onClick={() => setIsModalOpen(true)}
              className="w-full sm:w-auto px-6 py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-medium text-sm tracking-wide transition-all shadow-sm flex items-center justify-center gap-2 active:scale-95"
            >
              <MessageSquarePlus className="w-4 h-4" />
              <span>Write a Review</span>
            </button>
          </div>
        </div>

        {/* Search & Rating Filter Controls */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 sm:gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#86868B]" />
            <input
              type="text"
              placeholder="Search reviews by keyword, device, or user..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-full bg-white dark:bg-[#121624] border border-black/10 dark:border-white/15 text-base sm:text-sm focus:outline-none focus:border-[#0071E3] shadow-sm text-[#1D1D1F] dark:text-white placeholder-[#86868B]"
            />
          </div>

          <div className="flex items-center gap-1.5 sm:gap-2 overflow-x-auto no-scrollbar pb-1 max-w-full touch-pan-x">
            <button
              onClick={() => setSelectedRating(null)}
              className={`flex-shrink-0 px-3.5 sm:px-4 py-2 rounded-full text-xs font-semibold tracking-wide transition-all min-h-[34px] ${
                selectedRating === null
                  ? 'bg-[#1D1D1F] dark:bg-white text-white dark:text-[#1D1D1F] shadow-sm'
                  : 'bg-white dark:bg-[#121624] border border-black/10 dark:border-white/15 text-[#6E6E73] dark:text-[#A1A1A6] hover:bg-[#F5F5F7] dark:hover:bg-white/5'
              }`}
            >
              All ({reviews.length})
            </button>
            {[5, 4, 3, 2, 1].map((r) => {
              const count = reviews.filter((x) => x.rating === r).length;
              return (
                <button
                  key={r}
                  onClick={() => setSelectedRating(selectedRating === r ? null : r)}
                  className={`flex-shrink-0 px-3 py-2 rounded-full text-xs font-semibold tracking-wide transition-all min-h-[34px] flex items-center gap-1 ${
                    selectedRating === r
                      ? 'bg-[#0071E3] text-white shadow-sm'
                      : 'bg-white dark:bg-[#121624] border border-black/10 dark:border-white/15 text-[#6E6E73] dark:text-[#A1A1A6] hover:bg-[#F5F5F7] dark:hover:bg-white/5'
                  }`}
                >
                  <span>{r}★</span>
                  <span className="opacity-70">({count})</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Reviews Grid */}
        {filteredReviews.length === 0 ? (
          <div className="p-10 sm:p-16 text-center rounded-2xl sm:rounded-3xl bg-white dark:bg-[#121624] border border-black/[0.08] dark:border-white/10">
            <p className="text-[#6E6E73] dark:text-[#A1A1A6] text-sm sm:text-base">No reviews match your current search criteria.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-8">
            {filteredReviews.map((rev) => (
              <div
                key={rev.id}
                className="p-5 sm:p-8 rounded-2xl sm:rounded-3xl bg-white dark:bg-[#121624] border border-black/[0.08] dark:border-white/10 shadow-[0_2px_16px_rgba(0,0,0,0.03)] flex flex-col justify-between hover:shadow-md transition-shadow"
              >
                <div className="space-y-3.5">
                  <div className="flex items-center justify-between">
                    <div className="flex gap-1 text-amber-500">
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Star
                          key={i}
                          className={`w-4 h-4 ${
                            i < rev.rating
                              ? 'fill-amber-400 text-amber-400'
                              : 'text-gray-300 dark:text-white/20'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-xs font-mono text-[#6E6E73] dark:text-[#A1A1A6]">{rev.date}</span>
                  </div>
                  <p className="text-sm font-semibold text-[#0071E3] dark:text-[#38BDF8]">{rev.productName}</p>
                  <p className="text-base text-[#333336] dark:text-[#E2E8F0] font-normal leading-relaxed">
                    &ldquo;{rev.comment}&rdquo;
                  </p>
                </div>

                <div className="pt-6 mt-6 border-t border-black/[0.08] dark:border-white/10 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-emerald-600 dark:text-emerald-400 flex-shrink-0" />
                  <span className="text-sm font-medium text-[#1D1D1F] dark:text-white truncate">{rev.author}</span>
                  <span className="text-xs text-[#6E6E73] dark:text-[#A1A1A6] font-mono ml-auto">Verified Buyer</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Review Submission Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm"
            onClick={() => setIsModalOpen(false)}
          />
          <div className="relative w-full max-w-md p-6 sm:p-8 rounded-3xl bg-white dark:bg-[#141A2E] border border-black/10 dark:border-white/15 shadow-2xl z-10 text-[#1D1D1F] dark:text-white">
            <button
              onClick={() => setIsModalOpen(false)}
              className="absolute top-5 right-5 p-1.5 text-[#86868B] hover:text-[#1D1D1F] dark:hover:text-white rounded-full bg-black/5 dark:bg-white/10"
            >
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-xl font-bold mb-1">Share Your Experience</h3>
            <p className="text-xs text-[#6E6E73] dark:text-[#A1A1A6] mb-5">
              Submit your genuine rating and feedback for the NEXORA community.
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-[#555558] dark:text-[#CBD5E1] mb-1">
                  Your Full Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Tanvir Ahmed"
                  value={author}
                  onChange={(e) => setAuthor(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 dark:border-white/15 text-sm focus:outline-none focus:border-[#0071E3] bg-[#F5F5F7] dark:bg-white/5 text-[#1D1D1F] dark:text-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#555558] dark:text-[#CBD5E1] mb-1">
                  Product Purchased
                </label>
                <select
                  value={productName}
                  onChange={(e) => setProductName(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 dark:border-white/15 text-sm focus:outline-none focus:border-[#0071E3] bg-[#F5F5F7] dark:bg-white/5 text-[#1D1D1F] dark:text-white"
                >
                  <option value="Apple iPhone 18 Pro Max" className="text-black">Apple iPhone 18 Pro Max</option>
                  <option value="Samsung Galaxy S24 Ultra" className="text-black">Samsung Galaxy S24 Ultra</option>
                  <option value="Apple Watch Ultra 2" className="text-black">Apple Watch Ultra 2</option>
                  <option value="Apple MacBook Pro 16-inch" className="text-black">Apple MacBook Pro 16-inch</option>
                  <option value="Apple iPad Pro 13-inch" className="text-black">Apple iPad Pro 13-inch</option>
                  <option value="Sony WH-1000XM5" className="text-black">Sony WH-1000XM5</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#555558] dark:text-[#CBD5E1] mb-1">
                  Rating
                </label>
                <div className="flex items-center gap-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setRating(star)}
                      className="p-1 text-amber-500 hover:scale-110 transition-transform"
                    >
                      <Star
                        className={`w-6 h-6 ${
                          star <= rating
                            ? 'fill-amber-400 text-amber-400'
                            : 'text-gray-300 dark:text-white/20'
                        }`}
                      />
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#555558] dark:text-[#CBD5E1] mb-1">
                  Your Review &amp; Impressions
                </label>
                <textarea
                  required
                  rows={4}
                  placeholder="Tell others about the build quality, display, battery, or tactile experience..."
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 dark:border-white/15 text-sm focus:outline-none focus:border-[#0071E3] bg-[#F5F5F7] dark:bg-white/5 text-[#1D1D1F] dark:text-white"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-full bg-[#0071E3] hover:bg-[#0077ED] text-white font-semibold text-sm shadow-md transition-all active:scale-95 disabled:opacity-50"
              >
                {loading ? 'Submitting...' : 'Post Verified Review'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
