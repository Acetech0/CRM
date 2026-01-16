export const ActivityType = {
    CALL: 'call',
    EMAIL: 'email',
    NOTE: 'note',
    MEETING: 'meeting',
    FORM: 'form'
} as const;

export type ActivityType = typeof ActivityType[keyof typeof ActivityType];

export interface Activity {
    id: string;
    type: ActivityType;
    content: string;
    created_at: string;
    contact_id: string;
}

export interface ActivityCreate {
    contact_id: string;
    type: ActivityType;
    content: string;
}

export interface ActivityUpdate {
    type?: ActivityType;
    content?: string;
}
