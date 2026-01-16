import client from './client';
import type { Activity, ActivityCreate, ActivityUpdate } from '../types/activity';

export const getActivities = async (contact_id: string): Promise<Activity[]> => {
    const response = await client.get<Activity[]>(`/activities/${contact_id}`);
    return response.data;
};

export const createActivity = async (activity: ActivityCreate): Promise<Activity> => {
    const response = await client.post<Activity>('/activities', activity);
    return response.data;
};

export const updateActivity = async (id: string, activity: ActivityUpdate): Promise<Activity> => {
    const response = await client.put<Activity>(`/activities/${id}`, activity);
    return response.data;
};

export const deleteActivity = async (id: string): Promise<void> => {
    await client.delete(`/activities/${id}`);
};
