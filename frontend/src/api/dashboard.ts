import client from './client';
import type { DashboardOverview, PipelineStage } from '../types/dashboard';

export const getOverview = async (): Promise<DashboardOverview> => {
    const response = await client.get<DashboardOverview>('/dashboard/overview');
    return response.data;
};

export const getPipeline = async (): Promise<PipelineStage[]> => {
    const response = await client.get<PipelineStage[]>('/dashboard/pipeline');
    return response.data;
};
