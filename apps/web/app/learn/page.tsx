"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

/**
 * Start Learning page.
 *
 * Topic input, file upload, learner level, language, goal, time selection.
 */
export default function LearnPage() {
  const router = useRouter();
  const [topic, setTopic] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [level, setLevel] = useState("beginner");
  const [language, setLanguage] = useState("en");
  const [duration, setDuration] = useState(20);
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleStart = async () => {
    if (!topic && !file) {
      setError("Please enter a topic or upload a document.");
      return;
    }
    setLoading(true);
    setError("");

    try {
      // TODO: Connect to backend API when auth is ready
      // For now, navigate to lesson page with query params
      const params = new URLSearchParams({
        topic: topic || file?.name || "",
        level,
        language,
        duration: duration.toString(),
        goal,
      });
      router.push(`/lesson?${params.toString()}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-8">
      <div className="max-w-xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-center">Start Learning</h1>

        {error && (
          <div className="bg-red-500/20 border border-red-500 text-red-300 rounded-lg p-3 text-sm">
            {error}
          </div>
        )}

        {/* Topic Input */}
        <div className="space-y-2">
          <label className="text-sm text-slate-400">Topic</label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., Ohm's Law, Photosynthesis, Neural Networks"
            className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl focus:border-indigo-500 focus:outline-none"
          />
        </div>

        {/* File Upload */}
        <div className="space-y-2">
          <label className="text-sm text-slate-400">Or upload a document (PDF, DOCX, PPTX)</label>
          <input
            type="file"
            accept=".pdf,.docx,.pptx,.txt,.md"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl file:mr-4 file:bg-indigo-600 file:text-white file:border-0 file:px-4 file:py-2 file:rounded-lg file:cursor-pointer"
          />
          {file && <p className="text-xs text-slate-500">Selected: {file.name}</p>}
        </div>

        {/* Level */}
        <div className="space-y-2">
          <label className="text-sm text-slate-400">Learner Level</label>
          <div className="flex gap-3">
            {["beginner", "intermediate", "advanced"].map((l) => (
              <button
                key={l}
                onClick={() => setLevel(l)}
                className={`flex-1 py-2 rounded-xl capitalize transition-colors ${
                  level === l
                    ? "bg-indigo-600 text-white"
                    : "bg-slate-800 border border-slate-700 text-slate-400 hover:border-indigo-500"
                }`}
              >
                {l}
              </button>
            ))}
          </div>
        </div>

        {/* Language */}
        <div className="space-y-2">
          <label className="text-sm text-slate-400">Language</label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl focus:border-indigo-500 focus:outline-none"
          >
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="hinglish">Hinglish</option>
          </select>
        </div>

        {/* Duration */}
        <div className="space-y-2">
          <label className="text-sm text-slate-400">Duration: {duration} minutes</label>
          <input
            type="range"
            min={5}
            max={60}
            step={5}
            value={duration}
            onChange={(e) => setDuration(parseInt(e.target.value))}
            className="w-full accent-indigo-600"
          />
          <div className="flex justify-between text-xs text-slate-500">
            <span>5 min</span>
            <span>20 min</span>
            <span>60 min</span>
          </div>
        </div>

        {/* Goal */}
        <div className="space-y-2">
          <label className="text-sm text-slate-400">Learning Goal (optional)</label>
          <input
            type="text"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="e.g., Prepare for exam, Quick overview"
            className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl focus:border-indigo-500 focus:outline-none"
          />
        </div>

        {/* Start Button */}
        <button
          onClick={handleStart}
          disabled={loading}
          className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 rounded-xl font-semibold text-lg transition-colors"
        >
          {loading ? "Preparing lesson..." : "Start Lesson"}
        </button>
      </div>
    </main>
  );
}
