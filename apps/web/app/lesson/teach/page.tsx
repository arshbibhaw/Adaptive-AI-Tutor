"use client";

import { useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";

/**
 * Teaching Room page.
 *
 * AI video player, visuals, Q&A interaction, adaptation feedback.
 * This is the core teaching experience page.
 */
function TeachContent() {
  const params = useSearchParams();
  const topic = params.get("topic") || "Lesson";

  const [phase, setPhase] = useState<string>("explanation");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<string | null>(null);
  const [isAdapting, setIsAdapting] = useState(false);
  const [questionIndex, setQuestionIndex] = useState(0);

  const handleSubmitAnswer = () => {
    if (!answer.trim()) return;

    // Simulate evaluation — in production, calls POST /sessions/{id}/answer
    if (questionIndex === 0) {
      // First answer: simulate WRONG (demo the adaptive flow)
      setPhase("adaptation");
      setIsAdapting(true);
      setFeedback(
        "Not quite right. It seems like you might be confusing the relationship between the variables. " +
        "Let me try explaining it differently using an analogy."
      );
    } else {
      // Subsequent answers: simulate CORRECT
      setPhase("continue");
      setIsAdapting(false);
      setFeedback("Correct! Great job. Let's continue.");
    }
    setQuestionIndex((prev) => prev + 1);
    setAnswer("");
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto p-8 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">{topic}</h1>
          <div className="flex gap-2 text-xs">
            <span className={`px-3 py-1 rounded-full ${
              phase === "adaptation" ? "bg-amber-600" : "bg-indigo-600"
            }`}>
              {phase === "adaptation" ? "⚡ Adapting" : "📖 Teaching"}
            </span>
          </div>
        </div>

        {/* Video / Avatar Area */}
        <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-8 text-center space-y-4">
          <div className="w-32 h-32 mx-auto bg-slate-700 rounded-full flex items-center justify-center text-4xl">
            🧑‍🏫
          </div>
          <p className="text-slate-400 text-sm">
            AI Avatar will appear here when TTS and Avatar APIs are configured.
          </p>
          <div className="bg-slate-900 rounded-xl p-4 text-left max-h-48 overflow-y-auto">
            {phase === "explanation" && (
              <p>
                Let me explain the core concept of <strong>{topic}</strong>.
                This is a fundamental topic that builds the foundation for more advanced understanding...
              </p>
            )}
            {phase === "adaptation" && (
              <p className="text-amber-300">
                {feedback}
              </p>
            )}
            {phase === "continue" && (
              <p className="text-green-300">
                {feedback}
              </p>
            )}
          </div>
        </div>

        {/* Visual Area */}
        <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-6">
          <p className="text-xs text-slate-500 mb-2">Educational Visual</p>
          <div className="h-48 bg-slate-900 rounded-lg flex items-center justify-center text-slate-600">
            [Subject-aware visual will appear here]
          </div>
        </div>

        {/* Question & Answer */}
        <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-6 space-y-4">
          <p className="font-medium">
            {isAdapting
              ? `Let's try again: Can you explain ${topic} in your own words?`
              : `Question: What is the key principle behind ${topic}?`
            }
          </p>
          <div className="flex gap-3">
            <input
              type="text"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer..."
              className="flex-1 px-4 py-3 bg-slate-900 border border-slate-700 rounded-xl focus:border-indigo-500 focus:outline-none"
              onKeyDown={(e) => e.key === "Enter" && handleSubmitAnswer()}
            />
            <button
              onClick={handleSubmitAnswer}
              className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold transition-colors"
            >
              Submit
            </button>
          </div>
        </div>

        {/* Feedback / Adaptation indicator */}
        {feedback && (
          <div className={`p-4 rounded-xl border ${
            isAdapting
              ? "bg-amber-900/30 border-amber-600 text-amber-300"
              : "bg-green-900/30 border-green-600 text-green-300"
          }`}>
            <p className="text-sm font-medium mb-1">
              {isAdapting ? "⚡ Misconception Detected — Adapting" : "✅ Correct"}
            </p>
            <p className="text-sm">{feedback}</p>
          </div>
        )}

        {/* Navigation */}
        <div className="flex gap-4">
          <Link
            href="/assessment"
            className="flex-1 text-center py-3 border border-slate-700 hover:border-indigo-500 rounded-xl transition-colors"
          >
            Skip to Assessment
          </Link>
          <Link
            href="/lesson"
            className="flex-1 text-center py-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors"
          >
            Back to Plan
          </Link>
        </div>
      </div>
    </main>
  );
}

export default function TeachPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">Loading...</div>}>
      <TeachContent />
    </Suspense>
  );
}
