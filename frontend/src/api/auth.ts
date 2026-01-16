import client from './client';
import type { LoginCredentials, RegisterCredentials, TokenResponse } from '../types/auth';

export const login = async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const response = await client.post<TokenResponse>('/auth/login', credentials);
    return response.data;
};

export const register = async (credentials: RegisterCredentials): Promise<void> => {
    await client.post('/auth/register', credentials);
};
