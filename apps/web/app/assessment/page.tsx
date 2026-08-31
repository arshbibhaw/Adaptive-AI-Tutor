"use client";

import { useState } from "react";
import Link from "next/link";

/**
 * Assessment page.
 *
 * Displays final quiz questions, accepts answers, shows feedback and score.
 */
export default function AssessmentPage() {
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [submitted, setSubmitted] = useState(false);

  // Placeholder quiz questions
  const questions = [
    {
      id: "q1",
      text: "Which of the following best describes the core concept?",
      type: "mcq",
      options: ["A correct description", "A common misconception", "An unrelated concept", "A partial description"],
      correct: 0,
    },
    {
      id: "q2",
      text: "Explain the key principle in your own words.",
      type: "short_answer",
      options: null,
      correct: null,
    },
    {
      id: "q3",
      text: "What happens when you increase the input variable?",
      type: "mcq",
      options: ["Output increases proportionally", "Output decreases", "No change", "Output becomes zero"],
      correct: 0,
    },
  ];

  const handleAnswer = (answer: string) => {
    const newAnswers = [...answers];
    newAnswers[currentQ] = answer;
    setAnswers(newAnswers);
  };

  const handleSubmit = () => {
    setSubmitted(true);
  };

  const score = submitted
    ? questions.reduce((acc, q, i) => {
        if (q.correct !== null && q.options) {
          return acc + (answers[i] === q.options[q.correct] ? 1 : 0);
        }
        return acc + (answers[i] ? 0.5 : 0); // Partial credit for open-ended
      }, 0)
    : 0;

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-8">
      <div className="max-w-2xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold">Final Assessment</h1>

        {!submitted ? (
          <>
            {/* Question Card */}
            <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-6 space-y-4">
              <p className="text-sm text-slate-500">
                Question {currentQ + 1} of {questions.length}
              </p>
              <p className="text-lg font-medium">{questions[currentQ].text}</p>

              {questions[currentQ].options ? (
                <div className="space-y-2">
                  {questions[currentQ].options.map((opt, i) => (
                    <button
                      key={i}
                      onClick={() => handleAnswer(opt)}
                      className={`w-full text-left px-4 py-3 rounded-xl border transition-colors ${
                        answers[currentQ] === opt
                          ? "border-indigo-500 bg-indigo-600/20"
                          : "border-slate-700 bg-slate-800 hover:border-slate-600"
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              ) : (
                <textarea
                  value={answers[currentQ] || ""}
                  onChange={(e) => handleAnswer(e.target.value)}
                  placeholder="Type your answer..."
                  className="w-full h-24 px-4 py-3 bg-slate-900 border border-slate-700 rounded-xl focus:border-indigo-500 focus:outline-none resize-none"
                />
              )}
            </div>

            {/* Navigation */}
            <div className="flex gap-4">
              <button
                onClick={() => setCurrentQ(Math.max(0, currentQ - 1))}
                disabled={currentQ === 0}
                className="flex-1 py-3 border border-slate-700 hover:border-indigo-500 disabled:opacity-50 rounded-xl transition-colors"
              >
                Previous
              </button>
              {currentQ < questions.length - 1 ? (
                <button
                  onClick={() => setCurrentQ(currentQ + 1)}
                  className="flex-1 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold transition-colors"
                >
                  Next
                </button>
              ) : (
                <button
                  onClick={handleSubmit}
                  className="flex-1 py-3 bg-green-600 hover:bg-green-500 rounded-xl font-semibold transition-colors"
                >
                  Submit Assessment
                </button>
              )}
            </div>
          </>
        ) : (
          /* Results */
          <div className="space-y-6">
            <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-8 text-center space-y-4">
              <p className="text-6xl font-bold text-indigo-400">
                {Math.round((score / questions.length) * 100)}%
              </p>
              <p className="text-xl text-slate-300">
                {score.toFixed(1)} / {questions.length} correct
              </p>
            </div>

            <div className="flex gap-4">
              <Link
                href="/progress"
                className="flex-1 text-center py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold transition-colors"
              >
                View Learning Report
              </Link>
              <Link
                href="/learn"
                className="flex-1 text-center py-3 border border-slate-700 hover:border-indigo-500 rounded-xl transition-colors"
              >
                Learn Something New
              </Link>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
