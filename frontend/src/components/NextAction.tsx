'use client';

import { NextAction as NextActionType } from '@/lib/api';

interface NextActionProps {
  nextAction: NextActionType;
}

export default function NextAction({ nextAction }: NextActionProps) {
  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-lg p-6 mb-8">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
        <h2 className="text-xl font-bold text-gray-900">What to do in the next 10 minutes</h2>
      </div>
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <p className="text-sm text-gray-600 mb-2">Task: <span className="font-semibold text-gray-900">{nextAction.task}</span></p>
        <p className="text-lg font-semibold text-gray-900 mb-2">{nextAction.step}</p>
        <p className="text-sm text-gray-500">⏱️ Estimated time: {nextAction.minutes} minutes</p>
      </div>
    </div>
  );
}

