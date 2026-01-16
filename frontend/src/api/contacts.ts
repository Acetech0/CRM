import client from './client';
import type { Contact, ContactCreate } from '../types/contact';

export const getContacts = async (): Promise<Contact[]> => {
    const response = await client.get<Contact[]>('/contacts');
    return response.data;
};

export const createContact = async (contact: ContactCreate): Promise<Contact> => {
    const response = await client.post<Contact>('/contacts', contact);
    return response.data;
};

export const getContact = async (id: string): Promise<Contact> => {
    const response = await client.get<Contact>(`/contacts/${id}/summary`);
    return response.data;
};
