import client from './client';
import type { Activity } from '../types/activity';

export const getActivities = async (contact_id: string): Promise<Activity[]> => {
    const response = await client.get<Activity[]>(`/activities/${contact_id}`);
    return response.data;
};
