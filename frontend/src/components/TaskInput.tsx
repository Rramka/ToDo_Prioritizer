'use client';

import { useState } from 'react';

interface TaskInputProps {
  onAnalyze: (tasks: string) => void;
  isLoading: boolean;
}

export default function TaskInput({ onAnalyze, isLoading }: TaskInputProps) {
  const [tasks, setTasks] = useState('');
  const MAX_LENGTH = 2000;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedTasks = tasks.trim();
    if (trimmedTasks && !isLoading) {
      onAnalyze(trimmedTasks);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    if (newValue.length <= MAX_LENGTH) {
      setTasks(newValue);
      // Force state update
      console.log('Tasks updated:', newValue.trim().length > 0 ? 'Has tasks' : 'Empty');
    }
  };

  const remainingChars = MAX_LENGTH - tasks.length;
  const isNearLimit = remainingChars < 100;
  const hasTasks = tasks.trim().length > 0;
  const isDisabled = !hasTasks || isLoading;

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <textarea
          value={tasks}
          onChange={handleChange}
          onInput={handleChange}
          placeholder="Paste your tasks here...&#10;&#10;Example:&#10;Write quarterly report&#10;Call client about project&#10;Buy groceries&#10;Review code changes"
          className="w-full h-64 p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none resize-none text-gray-900 placeholder-gray-400"
          disabled={isLoading}
        />
        <div className="absolute bottom-2 right-2 flex items-center gap-2">
          <span
            className={`text-sm ${
              isNearLimit ? 'text-red-500' : 'text-gray-500'
            }`}
          >
            {remainingChars} / {MAX_LENGTH}
          </span>
        </div>
      </div>
      <button
        type="submit"
        disabled={isDisabled}
        className={`mt-4 w-full py-3 px-6 rounded-lg font-semibold transition-colors ${
          isDisabled
            ? 'bg-gray-400 text-white cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700 cursor-pointer'
        }`}
        aria-label={hasTasks ? 'Analyze tasks' : 'Enter tasks to enable'}
      >
        {isLoading ? 'Analyzing...' : 'Get Clarity'}
      </button>
      {!hasTasks && !isLoading && (
        <p className="mt-2 text-sm text-gray-500 text-center">
          Enter at least one task to enable the button
        </p>
      )}
      {hasTasks && !isLoading && (
        <p className="mt-2 text-sm text-green-600 text-center">
          ✓ Ready to analyze {tasks.split('\n').filter(t => t.trim()).length} task(s)
        </p>
      )}
    </form>
  );
}

