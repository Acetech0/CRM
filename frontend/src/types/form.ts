export type FieldType = 'text' | 'email' | 'number' | 'textarea' | 'select' | 'checkbox';

export interface FormField {
    id: string;
    key: string;
    label: string;
    field_type: FieldType;
    required: boolean;
    order: number;
    options?: string[];
    placeholder?: string;
}

export interface FormFieldCreate {
    key: string;
    label: string;
    field_type: FieldType;
    required?: boolean;
    order?: number;
    options?: string[];
    placeholder?: string;
}

export interface Form {
    id: string;
    name: string;
    website_id: string;
    settings: Record<string, any>;
    created_at: string;
    fields: FormField[];
}

export interface FormCreate {
    name: string;
    settings?: Record<string, any>;
    fields: FormFieldCreate[];
}

export interface FormStats {
    submission_count: number;
    last_submission: string | null;
}
