import React, { useEffect, useState } from 'react';
import { getOverview, getPipeline } from '../api/dashboard';
import type { DashboardOverview, PipelineStage } from '../types/dashboard';
import { LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Dashboard: React.FC = () => {
    const [overview, setOverview] = useState<DashboardOverview | null>(null);
    const [pipeline, setPipeline] = useState<PipelineStage[]>([]);
    const [loading, setLoading] = useState(true);
    const { logout } = useAuth();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [overviewData, pipelineData] = await Promise.all([
                    getOverview(),
                    getPipeline()
                ]);
                setOverview(overviewData);
                setPipeline(pipelineData);
            } catch (error) {
                console.error('Failed to fetch dashboard data', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div className="flex items-center justify-center h-screen">Loading...</div>;
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-white shadow">
                <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex items-center">
                            <h1 className="text-xl font-bold text-gray-900">CRM Dashboard</h1>
                        </div>
                        <div className="flex items-center">
                            <button
                                onClick={logout}
                                className="flex items-center text-gray-500 hover:text-gray-700"
                            >
                                <LogOut className="w-5 h-5 mr-1" />
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            <main className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                {/* Stats Grid */}
                <div className="grid grid-cols-1 gap-5 mb-8 sm:grid-cols-3">
                    <div className="p-5 overflow-hidden bg-white rounded-lg shadow">
                        <dt className="text-sm font-medium text-gray-500 truncate">Total Contacts</dt>
                        <dd className="mt-1 text-3xl font-semibold text-gray-900">{overview?.total_contacts || 0}</dd>
                    </div>
                    <div className="p-5 overflow-hidden bg-white rounded-lg shadow">
                        <dt className="text-sm font-medium text-gray-500 truncate">Active Deals</dt>
                        <dd className="mt-1 text-3xl font-semibold text-gray-900">{overview?.active_deals || 0}</dd>
                    </div>
                    <div className="p-5 overflow-hidden bg-white rounded-lg shadow">
                        <dt className="text-sm font-medium text-gray-500 truncate">Pipeline Value</dt>
                        <dd className="mt-1 text-3xl font-semibold text-gray-900">
                            ${(overview?.pipeline_value || 0).toLocaleString()}
                        </dd>
                    </div>
                </div>

                {/* Pipeline Summary */}
                <div className="bg-white rounded-lg shadow">
                    <div className="px-4 py-5 border-b border-gray-200 sm:px-6">
                        <h3 className="text-lg font-medium leading-6 text-gray-900">Pipeline by Stage</h3>
                    </div>
                    <div className="px-4 py-5 sm:p-6">
                        {pipeline.length > 0 ? (
                            <ul className="space-y-4">
                                {pipeline.map((stage) => (
                                    <li key={stage.stage} className="flex flex-col">
                                        <div className="flex justify-between mb-1 text-sm font-medium">
                                            <span>{stage.stage}</span>
                                            <span>{stage.count} deals (${stage.value.toLocaleString()})</span>
                                        </div>
                                        {/* Simple Bar using width percentage based on max value (approximated for now) */}
                                        <div className="w-full h-2 bg-gray-200 rounded-full">
                                            <div
                                                className="h-2 bg-blue-600 rounded-full"
                                                style={{ width: `${Math.min((stage.count / Math.max(...pipeline.map(p => p.count))) * 100, 100)}%` }}
                                            ></div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="text-gray-500">No deals in pipeline.</p>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
