export interface LoginCredentials {
    tenant_slug: string;
    email: string;
    password: string;
}

export interface RegisterCredentials {
    company_name: string;
    company_slug: string;
    admin_name: string;
    admin_email: string;
    admin_password: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}
