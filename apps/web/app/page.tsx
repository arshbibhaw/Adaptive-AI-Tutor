import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl text-center space-y-8">
        <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">
          AI Teacher
        </h1>
        <p className="text-xl text-slate-300">
          Your Personalized, Intelligent Teaching Companion
        </p>
        <p className="text-slate-400">
          Upload a document or enter a topic. The AI Teacher will create a
          personalized lesson, teach through avatar and voice, ask questions,
          detect misconceptions, and adapt to help you truly understand.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/learn"
            className="px-8 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold transition-colors"
          >
            Start Learning
          </Link>
          <Link
            href="/progress"
            className="px-8 py-3 border border-slate-600 hover:border-indigo-500 rounded-xl font-semibold transition-colors"
          >
            My Progress
          </Link>
        </div>
      </div>
    </main>
  );
}
