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

export interface ContactSummary {
    contact: Contact;
    recent_activities: any[]; // refine type later if needed
    deals: any[];
    activity_count: number;
    total_pipeline_value: number;
}
