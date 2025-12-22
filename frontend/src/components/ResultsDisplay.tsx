'use client';

import { TaskAnalysisResponse } from '@/lib/api';
import NextAction from './NextAction';
import PriorityList from './PriorityList';
import TaskBreakdown from './TaskBreakdown';

interface ResultsDisplayProps {
  results: TaskAnalysisResponse;
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  return (
    <div className="mt-8 space-y-8">
      {/* Next Action - Highlighted */}
      <NextAction nextAction={results.next_action} />

      {/* Priorities */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Prioritized Tasks</h2>
        <PriorityList priorities={results.priorities} />
      </section>

      {/* Task Breakdowns */}
      <section>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Task Breakdowns</h2>
        <div className="space-y-4">
          {Object.entries(results.breakdown).map(([taskName, breakdown]) => (
            <TaskBreakdown key={taskName} taskName={taskName} breakdown={breakdown} />
          ))}
        </div>
      </section>
    </div>
  );
}

