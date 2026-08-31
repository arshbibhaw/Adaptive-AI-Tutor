"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import Link from "next/link";

/**
 * Lesson Plan page.
 *
 * Displays the generated lesson plan with concepts, time allocation, and start button.
 */
function LessonContent() {
  const params = useSearchParams();
  const topic = params.get("topic") || "Lesson";
  const level = params.get("level") || "beginner";
  const language = params.get("language") || "en";
  const duration = parseInt(params.get("duration") || "20");

  // Placeholder lesson plan segments
  const segments = [
    { id: "s1", concept: `Introduction to ${topic}`, minutes: Math.floor(duration * 0.2), visual_type: "diagram", checkpoint: false },
    { id: "s2", concept: `Core Principles of ${topic}`, minutes: Math.floor(duration * 0.3), visual_type: "diagram", checkpoint: true },
    { id: "s3", concept: `Applications of ${topic}`, minutes: Math.floor(duration * 0.3), visual_type: "code", checkpoint: true },
    { id: "s4", concept: `Summary & Assessment`, minutes: Math.floor(duration * 0.2), visual_type: "none", checkpoint: true },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-8">
      <div className="max-w-2xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold">{topic}</h1>

        <div className="flex gap-4 text-sm text-slate-400">
          <span className="px-3 py-1 bg-slate-800 rounded-full capitalize">{level}</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">{language.toUpperCase()}</span>
          <span className="px-3 py-1 bg-slate-800 rounded-full">{duration} min</span>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-slate-300">Lesson Plan</h2>
          {segments.map((seg, i) => (
            <div
              key={seg.id}
              className="flex items-center gap-4 p-4 bg-slate-800/60 border border-slate-700 rounded-xl"
            >
              <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-sm font-bold shrink-0">
                {i + 1}
              </div>
              <div className="flex-1">
                <p className="font-medium">{seg.concept}</p>
                <p className="text-xs text-slate-500">
                  {seg.minutes} min • {seg.visual_type} {seg.checkpoint ? "• checkpoint" : ""}
                </p>
              </div>
            </div>
          ))}
        </div>

        <Link
          href={`/lesson/teach?topic=${encodeURIComponent(topic)}&level=${level}&language=${language}&duration=${duration}`}
          className="block w-full text-center py-4 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold text-lg transition-colors"
        >
          Start Teaching
        </Link>
      </div>
    </main>
  );
}

export default function LessonPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">Loading...</div>}>
      <LessonContent />
    </Suspense>
  );
}
