import React, { useEffect, useState } from 'react';
import { getDeals, createDeal, updateDeal, updateDealStage, deleteDeal } from '../api/deals';
import { getContacts } from '../api/contacts';
import { DealStage, type Deal, type DealCreate } from '../types/deal';
import { Loader } from 'lucide-react';

const STAGES = Object.values(DealStage);

const Deals: React.FC = () => {
    const [deals, setDeals] = useState<Deal[]>([]);
    const [loading, setLoading] = useState(true);
    const [contacts, setContacts] = useState<any[]>([]);
    const [showModal, setShowModal] = useState(false);
    const [editingDealId, setEditingDealId] = useState<string | null>(null);
    const [formData, setFormData] = useState<DealCreate>({
        title: '',
        value: 0,
        stage: DealStage.LEAD,
        contact_id: ''
    });

    const fetchData = async () => {
        try {
            setLoading(true);
            const [dealsData, contactsData] = await Promise.all([
                getDeals(),
                getContacts()
            ]);
            setDeals(dealsData);
            setContacts(contactsData);
        } catch (error) {
            console.error('Failed to fetch data', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleCreateClick = () => {
        setEditingDealId(null);
        setFormData({ title: '', value: 0, stage: DealStage.LEAD, contact_id: contacts.length > 0 ? contacts[0].id : '' });
        setShowModal(true);
    };

    const handleEditClick = (deal: Deal) => {
        setEditingDealId(deal.id);
        setFormData({
            title: deal.title,
            value: deal.value,
            stage: deal.stage,
            contact_id: deal.contact_id
        });
        setShowModal(true);
    };

    const handleDeleteClick = async (dealId: string) => {
        if (!window.confirm("Are you sure you want to delete this deal?")) return;
        try {
            await deleteDeal(dealId);
            setDeals(deals.filter(d => d.id !== dealId));
        } catch (error) {
            console.error("Failed to delete deal", error);
            alert("Failed to delete deal");
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (editingDealId) {
                const updated = await updateDeal(editingDealId, formData);
                setDeals(deals.map(d => d.id === editingDealId ? updated : d));
            } else {
                const created = await createDeal(formData);
                setDeals([...deals, created]);
            }
            setShowModal(false);
        } catch (error) {
            console.error("Failed to save deal", error);
            alert("Failed to save deal");
        }
    };

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
                <div className="flex justify-between items-center mb-6 px-4 sm:px-0">
                    <h1 className="text-2xl font-bold text-gray-900">Deals Pipeline</h1>
                    <button onClick={handleCreateClick} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                        New Deal
                    </button>
                </div>

                <div className="grid grid-cols-5 gap-4">
                    {STAGES.map(stage => (
                        <div key={stage} className="bg-gray-100 p-3 rounded-lg min-h-[500px]">
                            <h3 className="font-semibold text-gray-700 mb-3 text-sm uppercase tracking-wider">{stage}</h3>
                            <div className="space-y-3">
                                {deals.filter(d => d.stage === stage).map(deal => (
                                    <div key={deal.id} className="bg-white p-4 rounded shadow hover:shadow-md transition-shadow group relative">
                                        <div className="absolute top-2 right-2 hidden group-hover:flex space-x-1">
                                            <button onClick={() => handleEditClick(deal)} className="text-gray-400 hover:text-blue-600 p-1">
                                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                                            </button>
                                            <button onClick={() => handleDeleteClick(deal.id)} className="text-gray-400 hover:text-red-600 p-1">
                                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                            </button>
                                        </div>
                                        <h4 className="font-medium text-gray-900 pr-12">{deal.title}</h4>
                                        <p className="text-sm text-gray-500 mt-1">${deal.value.toLocaleString()}</p>

                                        {/* Simple Move Actions */}
                                        <div className="mt-4 flex justify-between">
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

            {/* Modal */}
            {showModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
                    <div className="bg-white rounded-lg p-6 max-w-md w-full">
                        <h2 className="text-xl font-bold mb-4">{editingDealId ? 'Edit Deal' : 'New Deal'}</h2>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium">Title</label>
                                <input
                                    type="text"
                                    required
                                    className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                                    value={formData.title}
                                    onChange={e => setFormData({ ...formData, title: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium">Value ($)</label>
                                <input
                                    type="number"
                                    required
                                    className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                                    value={formData.value}
                                    onChange={e => setFormData({ ...formData, value: parseFloat(e.target.value) })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium">Stage</label>
                                <select
                                    className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                                    value={formData.stage}
                                    onChange={e => setFormData({ ...formData, stage: e.target.value as DealStage })}
                                >
                                    {STAGES.map(s => <option key={s} value={s}>{s}</option>)}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium">Contact</label>
                                <select
                                    className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                                    value={formData.contact_id}
                                    onChange={e => setFormData({ ...formData, contact_id: e.target.value })}
                                    required
                                >
                                    <option value="">Select a contact...</option>
                                    {contacts.map((c: any) => (
                                        <option key={c.id} value={c.id}>{c.first_name} {c.last_name}</option>
                                    ))}
                                </select>
                            </div>
                            <div className="flex justify-end space-x-2 mt-6">
                                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 border rounded text-gray-700 bg-white hover:bg-gray-50">Cancel</button>
                                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Save</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Deals;
