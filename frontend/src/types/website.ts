export interface Website {
    id: string;
    domain: string;
    name?: string;
    tracking_id: string;
    is_active: boolean;
    created_at: string;
    tenant_id: string;
}

export interface WebsiteCreate {
    domain: string;
    name?: string;
}
