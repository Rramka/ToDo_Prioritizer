'use client';

interface PriorityListProps {
  priorities: {
    must: string[];
    should: string[];
    optional: string[];
  };
}

export default function PriorityList({ priorities }: PriorityListProps) {
  const sections = [
    {
      title: 'Must Do',
      tasks: priorities.must,
      color: 'red',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-300',
      textColor: 'text-red-900',
      icon: '🔴',
    },
    {
      title: 'Should Do',
      tasks: priorities.should,
      color: 'yellow',
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-300',
      textColor: 'text-yellow-900',
      icon: '🟡',
    },
    {
      title: 'Optional',
      tasks: priorities.optional,
      color: 'gray',
      bgColor: 'bg-gray-50',
      borderColor: 'border-gray-300',
      textColor: 'text-gray-900',
      icon: '⚪',
    },
  ];

  return (
    <div className="space-y-6">
      {sections.map((section) => (
        <div
          key={section.title}
          className={`${section.bgColor} border-2 ${section.borderColor} rounded-lg p-4`}
        >
          <h3 className={`text-lg font-bold ${section.textColor} mb-3 flex items-center gap-2`}>
            <span>{section.icon}</span>
            {section.title} ({section.tasks.length})
          </h3>
          {section.tasks.length > 0 ? (
            <ul className="space-y-2">
              {section.tasks.map((task, index) => (
                <li
                  key={index}
                  className={`${section.textColor} pl-4 border-l-2 ${section.borderColor}`}
                >
                  {task}
                </li>
              ))}
            </ul>
          ) : (
            <p className={`${section.textColor} opacity-50 italic`}>No tasks in this category</p>
          )}
        </div>
      ))}
    </div>
  );
}

