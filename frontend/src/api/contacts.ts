import client from './client';
import type { Contact, ContactCreate, ContactSummary } from '../types/contact';

export const getContacts = async (): Promise<Contact[]> => {
    const response = await client.get<Contact[]>('/contacts');
    return response.data;
};

export const createContact = async (contact: ContactCreate): Promise<Contact> => {
    const response = await client.post<Contact>('/contacts', contact);
    return response.data;
};

export const getContact = async (id: string): Promise<ContactSummary> => {
    const response = await client.get<ContactSummary>(`/contacts/${id}/summary`);
    return response.data;
};

export const updateContact = async (id: string, contact: Partial<ContactCreate>): Promise<Contact> => {
    const response = await client.put<Contact>(`/contacts/${id}`, contact);
    return response.data;
};

export const deleteContact = async (id: string): Promise<void> => {
    await client.delete(`/contacts/${id}`);
};
