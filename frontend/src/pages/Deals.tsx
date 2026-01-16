import React, { useEffect, useState } from 'react';
import { getDeals, updateDealStage } from '../api/deals';
import { DealStage, type Deal } from '../types/deal';
import { Loader } from 'lucide-react';

const STAGES = Object.values(DealStage);

const Deals: React.FC = () => {
    const [deals, setDeals] = useState<Deal[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchDeals = async () => {
        try {
            setLoading(true);
            const data = await getDeals();
            setDeals(data);
        } catch (error) {
            console.error('Failed to fetch deals', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDeals();
    }, []);

    const moveStage = async (deal: Deal, nextStage: DealStage) => {
        try {
            await updateDealStage(deal.id, nextStage);
            setDeals(deals.map(d => d.id === deal.id ? { ...d, stage: nextStage } : d));
        } catch (error) {
            console.error('Failed to update stage', error);
            alert('Failed to update deal stage');
        }
    };

    if (loading) return <div className="p-8 flex items-center"><Loader className="animate-spin mr-2" /> Loading Pipeline...</div>;

    return (
        <div className="min-h-screen bg-gray-50 overflow-x-auto">
            <div className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8 min-w-[1000px]">
                <h1 className="text-2xl font-bold text-gray-900 mb-6 px-4 sm:px-0">Deals Pipeline</h1>

                <div className="grid grid-cols-5 gap-4">
                    {STAGES.map(stage => (
                        <div key={stage} className="bg-gray-100 p-3 rounded-lg min-h-[500px]">
                            <h3 className="font-semibold text-gray-700 mb-3 text-sm uppercase tracking-wider">{stage}</h3>
                            <div className="space-y-3">
                                {deals.filter(d => d.stage === stage).map(deal => (
                                    <div key={deal.id} className="bg-white p-4 rounded shadow hover:shadow-md transition-shadow">
                                        <h4 className="font-medium text-gray-900">{deal.title}</h4>
                                        <p className="text-sm text-gray-500 mt-1">${deal.value.toLocaleString()}</p>

                                        {/* Simple Move Actions */}
                                        <div className="mt-4 flex justify-between">
                                            {/* Logic for Previous Stage could go here but focusing on forward momentum */}
                                            <div></div>
                                            {stage !== DealStage.CLOSED && (
                                                <button
                                                    onClick={() => {
                                                        const currentIndex = STAGES.indexOf(stage);
                                                        if (currentIndex < STAGES.length - 1) {
                                                            moveStage(deal, STAGES[currentIndex + 1]);
                                                        }
                                                    }}
                                                    className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded hover:bg-blue-200"
                                                >
                                                    Next &rarr;
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Deals;
