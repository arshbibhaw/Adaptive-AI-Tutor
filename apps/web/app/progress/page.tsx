"use client";

import Link from "next/link";

/**
 * Progress Dashboard page.
 *
 * Learning history, topic progress, scores, strong/weak concepts, learning path.
 */
export default function ProgressPage() {
  // Placeholder data — in production, fetches from GET /progress
  const progress = {
    topics_studied: ["Ohm's Law", "Photosynthesis"],
    total_sessions: 3,
    average_score: 0.75,
    strong_concepts: ["Voltage", "Current"],
    weak_concepts: ["Resistance"],
    current_learning_path: ["Review: Resistance", "Advanced Ohm's Law"],
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-8">
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">My Progress</h1>
          <Link
            href="/learn"
            className="px-6 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-xl text-sm font-semibold transition-colors"
          >
            Learn More
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-6 text-center">
            <p className="text-3xl font-bold text-indigo-400">{progress.total_sessions}</p>
            <p className="text-sm text-slate-400 mt-1">Sessions</p>
          </div>
          <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-6 text-center">
            <p className="text-3xl font-bold text-green-400">
              {Math.round(progress.average_score * 100)}%
            </p>
            <p className="text-sm text-slate-400 mt-1">Average Score</p>
          </div>
          <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-6 text-center">
            <p className="text-3xl font-bold text-cyan-400">{progress.topics_studied.length}</p>
            <p className="text-sm text-slate-400 mt-1">Topics</p>
          </div>
        </div>

        {/* Strong Concepts */}
        <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-green-400 mb-3">✅ Strong Concepts</h2>
          <div className="flex flex-wrap gap-2">
            {progress.strong_concepts.map((c) => (
              <span key={c} className="px-3 py-1 bg-green-900/30 border border-green-700 text-green-300 rounded-full text-sm">
                {c}
              </span>
            ))}
          </div>
        </div>

        {/* Weak Concepts */}
        <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-amber-400 mb-3">⚠️ Needs Revision</h2>
          <div className="flex flex-wrap gap-2">
            {progress.weak_concepts.map((c) => (
              <span key={c} className="px-3 py-1 bg-amber-900/30 border border-amber-700 text-amber-300 rounded-full text-sm">
                {c}
              </span>
            ))}
          </div>
        </div>

        {/* Learning Path */}
        <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-indigo-400 mb-3">🗺️ Learning Path</h2>
          <div className="space-y-2">
            {progress.current_learning_path.map((step, i) => (
              <div key={i} className="flex items-center gap-3">
                <div className="w-6 h-6 bg-indigo-600 rounded-full flex items-center justify-center text-xs shrink-0">
                  {i + 1}
                </div>
                <p className="text-slate-300">{step}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Topics Studied */}
        <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-slate-300 mb-3">📚 Topics Studied</h2>
          <div className="space-y-2">
            {progress.topics_studied.map((t) => (
              <div key={t} className="flex items-center justify-between p-3 bg-slate-900 rounded-lg">
                <span>{t}</span>
                <span className="text-xs text-slate-500">Completed</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
