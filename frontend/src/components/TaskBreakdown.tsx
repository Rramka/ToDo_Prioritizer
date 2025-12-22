'use client';

import { TaskBreakdown as TaskBreakdownType } from '@/lib/api';

interface TaskBreakdownProps {
  taskName: string;
  breakdown: TaskBreakdownType;
}

export default function TaskBreakdown({ taskName, breakdown }: TaskBreakdownProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
      <h4 className="font-semibold text-gray-900 mb-3">{taskName}</h4>
      <ol className="space-y-2">
        {breakdown.steps.map((step, index) => (
          <li key={index} className="flex items-start gap-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-sm font-semibold">
              {index + 1}
            </span>
            <div className="flex-1">
              <p className="text-gray-900">{step.step}</p>
              <p className="text-sm text-gray-500 mt-1">⏱️ {step.minutes} minutes</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}

