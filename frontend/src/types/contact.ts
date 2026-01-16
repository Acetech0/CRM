export interface Contact {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    created_at: string;
}

export interface ContactCreate {
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
}
