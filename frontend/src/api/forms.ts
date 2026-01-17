import client from './client';
import type { Form, FormCreate, FormStats } from '../types/form';

export const getForms = async (websiteId: string): Promise<Form[]> => {
    const response = await client.get<Form[]>(`/websites/${websiteId}/forms`);
    return response.data;
};

export const createForm = async (websiteId: string, form: FormCreate): Promise<Form> => {
    const response = await client.post<Form>(`/websites/${websiteId}/forms`, form);
    return response.data;
};

export const getForm = async (formId: string): Promise<Form> => {
    const response = await client.get<Form>(`/forms/${formId}`);
    return response.data;
};

export const getFormStats = async (formId: string): Promise<FormStats> => {
    const response = await client.get<FormStats>(`/forms/${formId}/stats`);
    return response.data;
};
