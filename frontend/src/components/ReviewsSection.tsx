'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Review } from '../lib/types';
import { Star, CheckCircle, MessageSquarePlus, X, ArrowRight } from 'lucide-react';
import { submitReview } from '../lib/api';

export const ReviewsSection: React.FC<{ initialReviews: Review[] }> = ({ initialReviews }) => {
  const [reviews, setReviews] = useState<Review[]>(initialReviews);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [author, setAuthor] = useState('');
  const [productName, setProductName] = useState('Apple iPhone 18 Pro Max');
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);

  // Exactly 2 featured reviews in 1 row as requested
  const displayedReviews = reviews.slice(0, 2);

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

  return (
    <section className="py-16 px-4 max-w-6xl mx-auto">
      {/* Clean Centered Header */}
      <div className="text-center mb-10">
        <h2 className="text-3xl sm:text-4xl font-semibold text-[#1D1D1F] dark:text-white tracking-tight">
          Customer Experience
        </h2>
      </div>

      {/* Spacious 2-Review Row Layout (Centered & Compact on Mobile) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 sm:gap-8 max-w-xl mx-auto md:max-w-none">
        {displayedReviews.map(rev => (
          <div
            key={rev.id}
            className="p-5 sm:p-8 rounded-2xl sm:rounded-3xl bg-white dark:bg-[#121624] border border-black/[0.06] dark:border-white/10 shadow-[0_2px_16px_rgba(0,0,0,0.03)] flex flex-col justify-between hover:shadow-md transition-shadow text-center sm:text-left"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex gap-1 text-amber-500">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star
                      key={i}
                      className={`w-3.5 h-3.5 sm:w-4 sm:h-4 ${
                        i < rev.rating
                          ? 'fill-amber-400 text-amber-400'
                          : 'text-gray-300 dark:text-white/20'
                      }`}
                    />
                  ))}
                </div>
                <span className="text-xs font-mono text-[#6E6E73] dark:text-[#A1A1A6]">{rev.date}</span>
              </div>
              <p className="text-xs sm:text-sm font-semibold text-[#0071E3] dark:text-[#38BDF8]">{rev.productName}</p>
              <p className="text-sm sm:text-base text-[#333336] dark:text-[#E2E8F0] font-normal leading-relaxed">
                &ldquo;{rev.comment}&rdquo;
              </p>
            </div>

            <div className="pt-4 sm:pt-6 mt-4 sm:mt-6 border-t border-black/[0.06] dark:border-white/10 flex items-center justify-between sm:justify-start gap-2">
              <div className="flex items-center gap-1.5 truncate">
                <CheckCircle className="w-4 h-4 text-emerald-600 dark:text-emerald-400 flex-shrink-0" />
                <span className="text-xs sm:text-sm font-medium text-[#1D1D1F] dark:text-white truncate">{rev.author}</span>
              </div>
              <span className="text-[10px] sm:text-xs text-[#6E6E73] dark:text-[#A1A1A6] font-mono sm:ml-auto flex-shrink-0">Verified Buyer</span>
            </div>
          </div>
        ))}
      </div>

      {/* Buttons: Write a Review placed directly above Browse All Verified Reviews */}
      <div className="mt-10 flex flex-col items-center gap-3.5 text-center">
        <button
          onClick={() => setIsModalOpen(true)}
          className="inline-flex items-center gap-2 px-7 py-3 rounded-full bg-[#1D1D1F] hover:bg-[#0071E3] dark:bg-white/10 dark:hover:bg-[#0071E3] border border-transparent dark:border-white/15 text-white text-sm font-semibold tracking-wide transition-all shadow-sm active:scale-95"
        >
          <MessageSquarePlus className="w-4 h-4" />
          <span>Write a Review</span>
        </button>

        <Link
          href="/reviews"
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-full bg-white dark:bg-[#121624] border border-black/15 dark:border-white/20 hover:border-[#0071E3] dark:hover:border-[#0071E3] hover:text-[#0071E3] dark:hover:text-[#38BDF8] text-[#1D1D1F] dark:text-white text-sm font-semibold transition-all shadow-sm active:scale-95 group"
        >
          <span className="group-hover:text-[#0071E3] dark:group-hover:text-[#38BDF8] transition-colors">Browse All Verified Reviews &amp; Ratings</span>
          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 group-hover:text-[#0071E3] dark:group-hover:text-[#38BDF8] transition-all" />
        </Link>
      </div>

      {/* Review Submission Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="fixed inset-0 bg-black/40 backdrop-blur-sm"
            onClick={() => setIsModalOpen(false)}
          />
          <div className="relative w-full max-w-md p-6 rounded-3xl bg-white border border-black/10 shadow-2xl z-10 text-[#1D1D1F]">
            <button
              onClick={() => setIsModalOpen(false)}
              className="absolute top-5 right-5 p-1 text-[#86868B] hover:text-[#1D1D1F] rounded-full"
            >
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-xl font-bold mb-1">Share Your Experience</h3>
            <p className="text-xs text-[#6E6E73] mb-5">
              Submit your genuine rating and feedback for the NEXORA community.
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-[#6E6E73] mb-1">
                  Your Full Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Tanvir Ahmed"
                  value={author}
                  onChange={e => setAuthor(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-black/10 text-sm focus:outline-none focus:border-[#0071E3] bg-[#F5F5F7]"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-[#6E6E73] mb-1">
                  Product Purchased
                </label>
                <select
                  value={productName}
                  onChange={e => setProductName(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-black/10 text-sm focus:outline-none focus:border-[#0071E3] bg-[#F5F5F7]"
                >
                  <option value="Apple iPhone 18 Pro Max">Apple iPhone 18 Pro Max</option>
                  <option value="Samsung Galaxy S24 Ultra">Samsung Galaxy S24 Ultra</option>
                  <option value="NEXORA Cyber Earbuds Pro">NEXORA Cyber Earbuds Pro</option>
                  <option value="Apple Watch Ultra 2">Apple Watch Ultra 2</option>
                  <option value="NEXORA Aero 8K Drone">NEXORA Aero 8K Drone</option>
                  <option value="Apple MacBook Pro 16-inch">Apple MacBook Pro 16-inch</option>
                  <option value="Apple iPad Pro 13-inch">Apple iPad Pro 13-inch</option>
                  <option value="Sony WH-1000XM5">Sony WH-1000XM5</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-[#6E6E73] mb-1">
                  Rating
                </label>
                <div className="flex items-center gap-2">
                  {[1, 2, 3, 4, 5].map(star => (
                    <button
                      type="button"
                      key={star}
                      onClick={() => setRating(star)}
                      className="p-1 text-amber-500 hover:scale-110 transition-transform"
                    >
                      <Star
                        className={`w-6 h-6 ${
                          star <= rating
                            ? 'fill-amber-400 text-amber-400'
                            : 'text-gray-300'
                        }`}
                      />
                    </button>
                  ))}
                  <span className="text-xs font-mono text-[#6E6E73] ml-2 font-medium">
                    {rating} of 5 Stars
                  </span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-[#6E6E73] mb-1">
                  Your Review
                </label>
                <textarea
                  required
                  rows={3}
                  placeholder="Tell us what you loved about this device..."
                  value={comment}
                  onChange={e => setComment(e.target.value)}
                  className="w-full px-3.5 py-2 rounded-xl border border-black/10 text-sm focus:outline-none focus:border-[#0071E3] bg-[#F5F5F7]"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-sm text-[#6E6E73] hover:text-[#1D1D1F]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-5 py-2 rounded-full bg-[#0071E3] text-white text-sm font-medium hover:bg-[#0077ED] transition-colors disabled:opacity-50 shadow-sm"
                >
                  {loading ? 'Submitting...' : 'Post Review'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </section>
  );
};
