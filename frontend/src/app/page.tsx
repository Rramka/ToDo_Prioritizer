'use client';

import { useState } from 'react';
import TaskInput from '@/components/TaskInput';
import ResultsDisplay from '@/components/ResultsDisplay';
import { analyzeTasks, TaskAnalysisResponse } from '@/lib/api';

export default function Home() {
  const [results, setResults] = useState<TaskAnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (tasks: string) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const analysis = await analyzeTasks(tasks);
      setResults(analysis);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to analyze tasks';
      setError(errorMessage);
      console.error('Analysis error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            ToDo Prioritizer
          </h1>
          <p className="text-xl text-gray-600">
            Break down your to-do list into actionable micro-steps and identify what to do next
          </p>
        </div>

        {/* Task Input */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <TaskInput onAnalyze={handleAnalyze} isLoading={isLoading} />
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border-2 border-red-300 rounded-lg p-4 mb-8">
            <h3 className="text-red-900 font-semibold mb-2">Error</h3>
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Analyzing your tasks...</p>
          </div>
        )}

        {/* Results Display */}
        {results && !isLoading && <ResultsDisplay results={results} />}
      </div>
    </main>
  );
}
