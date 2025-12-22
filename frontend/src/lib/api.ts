import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export interface TaskStep {
  step: string;
  minutes: number;
}

export interface TaskBreakdown {
  steps: TaskStep[];
}

export interface NextAction {
  task: string;
  step: string;
  minutes: number;
}

export interface TaskAnalysisResponse {
  priorities: {
    must: string[];
    should: string[];
    optional: string[];
  };
  breakdown: Record<string, TaskBreakdown>;
  next_action: NextAction;
}

export interface TaskAnalysisRequest {
  tasks: string;
}

export async function analyzeTasks(tasks: string): Promise<TaskAnalysisResponse> {
  try {
    const response = await axios.post<TaskAnalysisResponse>(
      `${API_BASE_URL}/api/analyze`,
      { tasks },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.detail || error.message || 'Failed to analyze tasks';
      throw new Error(message);
    }
    throw error;
  }
}

