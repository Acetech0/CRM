import React, { useEffect, useState } from 'react';
import { getWebsites } from '../api/websites';
import { getForms, createForm } from '../api/forms';
import type { Website } from '../types/website';
import type { Form } from '../types/form';
import { Plus, Code } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Forms: React.FC = () => {
    const [websites, setWebsites] = useState<Website[]>([]);
    const [selectedWebsiteId, setSelectedWebsiteId] = useState<string>('');
    const [forms, setForms] = useState<Form[]>([]);
    const [loading, setLoading] = useState(true);
    const [isCreating, setIsCreating] = useState(false);
    const [newFormName, setNewFormName] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchWebsites();
    }, []);

    useEffect(() => {
        if (selectedWebsiteId) {
            fetchForms(selectedWebsiteId);
        } else {
            setForms([]);
        }
    }, [selectedWebsiteId]);

    const fetchWebsites = async () => {
        try {
            const data = await getWebsites();
            setWebsites(data);
            if (data.length > 0) {
                setSelectedWebsiteId(data[0].id);
            }
        } catch (error) {
            console.error('Failed to fetch websites', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchForms = async (websiteId: string) => {
        try {
            const data = await getForms(websiteId);
            setForms(data);
        } catch (error) {
            console.error('Failed to fetch forms', error);
        }
    };

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedWebsiteId) return;

        try {
            await createForm(selectedWebsiteId, {
                name: newFormName,
                fields: [
                    { key: 'name', label: 'Full Name', field_type: 'text', required: true, order: 0, placeholder: 'Your Name' },
                    { key: 'email', label: 'Email Address', field_type: 'email', required: true, order: 1, placeholder: 'you@example.com' },
                    { key: 'message', label: 'Message', field_type: 'textarea', required: true, order: 2, placeholder: 'How can we help?' }
                ]
            });
            setNewFormName('');
            setIsCreating(false);
            fetchForms(selectedWebsiteId);
        } catch (error) {
            console.error('Failed to create form', error);
            alert('Failed to create form.');
        }
    };

    if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>;

    return (
        <div className="min-h-screen bg-gray-50">

            <main className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold text-gray-900">Forms</h2>
                    <div className="flex items-center space-x-4">
                        <select
                            value={selectedWebsiteId}
                            onChange={(e) => setSelectedWebsiteId(e.target.value)}
                            className="block w-64 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                        >
                            <option value="" disabled>Select a Website</option>
                            {websites.map(w => (
                                <option key={w.id} value={w.id}>{w.domain}</option>
                            ))}
                        </select>
                        <button
                            onClick={() => setIsCreating(!isCreating)}
                            disabled={!selectedWebsiteId}
                            className={`flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 ${!selectedWebsiteId ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                            <Plus className="w-5 h-5 mr-2" /> Create Form
                        </button>
                    </div>
                </div>

                {isCreating && (
                    <div className="mb-8 bg-white p-6 rounded-lg shadow">
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Form Name</label>
                                <input
                                    type="text"
                                    required
                                    placeholder="Contact Us"
                                    value={newFormName}
                                    onChange={(e) => setNewFormName(e.target.value)}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                                />
                            </div>
                            <div className="flex justify-end space-x-3">
                                <button
                                    type="button"
                                    onClick={() => setIsCreating(false)}
                                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-medium"
                                >
                                    Create Form
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                    <ul className="divide-y divide-gray-200">
                        {forms.map((form) => (
                            <li key={form.id} className="px-6 py-4 hover:bg-gray-50 cursor-pointer" onClick={() => navigate(`/forms/${form.id}`)}>
                                <div className="flex items-center justify-between">
                                    <div>
                                        <h3 className="text-lg font-medium text-gray-900">{form.name}</h3>
                                        <p className="text-sm text-gray-500">{form.fields.length} fields</p>
                                    </div>
                                    <div className="flex items-center text-gray-500">
                                        <Code className="w-5 h-5 mr-2" />
                                        <span className="text-sm">View & Embed</span>
                                    </div>
                                </div>
                            </li>
                        ))}
                        {forms.length === 0 && (
                            <li className="px-6 py-12 text-center text-gray-500">
                                {selectedWebsiteId ? 'No forms found for this website.' : 'Select a website to view forms.'}
                            </li>
                        )}
                    </ul>
                </div>
            </main>
        </div>
    );
};

export default Forms;
