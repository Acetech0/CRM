import client from './client';
import type { Deal } from '../types/deal';

export const getDeals = async (): Promise<Deal[]> => {
    const response = await client.get<Deal[]>('/deals');
    return response.data;
};

export const updateDealStage = async (id: number, stage: string): Promise<Deal> => {
    const response = await client.put<Deal>(`/deals/${id}/stage`, { stage });
    return response.data;
};
