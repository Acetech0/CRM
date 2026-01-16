export const DealStage = {
    LEAD: 'LEAD',
    QUALIFIED: 'QUALIFIED',
    PROPOSAL: 'PROPOSAL',
    NEGOTIATION: 'NEGOTIATION',
    CLOSED: 'CLOSED'
} as const;

export type DealStage = typeof DealStage[keyof typeof DealStage];

export interface Deal {
    id: number;
    title: string;
    value: number;
    stage: DealStage;
    contact_id: number;
    created_at: string;
}
