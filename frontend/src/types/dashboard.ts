export interface DashboardOverview {
    total_contacts: number;
    active_deals: number;
    pipeline_value: number;
}

export interface PipelineStage {
    stage: string;
    count: number;
    value: number;
}
