export const DealStage = {
    LEAD: 'LEAD',
    QUALIFIED: 'QUALIFIED',
    PROPOSAL: 'PROPOSAL',
    NEGOTIATION: 'NEGOTIATION',
    CLOSED: 'CLOSED'
} as const;

export type DealStage = typeof DealStage[keyof typeof DealStage];

export interface Deal {
    id: string;
    title: string;
    value: number;
    stage: DealStage;
    contact_id: string;
    created_at: string;
}

export interface DealCreate {
    title: string;
    value: number;
    stage?: DealStage;
    contact_id: string;
}

export interface DealUpdate {
    title?: string;
    value?: number;
    stage?: DealStage;
}
