import client from './client';
import type { Deal, DealCreate, DealUpdate } from '../types/deal';

export const getDeals = async (): Promise<Deal[]> => {
    const response = await client.get<Deal[]>('/deals');
    return response.data;
};

export const createDeal = async (deal: DealCreate): Promise<Deal> => {
    const response = await client.post<Deal>('/deals', deal);
    return response.data;
};

export const updateDeal = async (id: string, deal: DealUpdate): Promise<Deal> => {
    const response = await client.put<Deal>(`/deals/${id}`, deal);
    return response.data;
};

export const updateDealStage = async (id: string, stage: string): Promise<Deal> => {
    const response = await client.put<Deal>(`/deals/${id}/stage`, { stage });
    return response.data;
};

export const deleteDeal = async (id: string): Promise<void> => {
    await client.delete(`/deals/${id}`);
};
