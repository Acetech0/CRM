import client from './client';
import type { Website, WebsiteCreate } from '../types/website';

export const getWebsites = async (): Promise<Website[]> => {
    const response = await client.get<Website[]>('/websites/');
    return response.data;
};

export const createWebsite = async (website: WebsiteCreate): Promise<Website> => {
    const response = await client.post<Website>('/websites/', website);
    return response.data;
};
