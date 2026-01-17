import React, { useEffect, useState } from 'react';
import { getWebsites, createWebsite } from '../api/websites';
import type { Website } from '../types/website';
import { Plus, Copy, Check } from 'lucide-react';

const Websites: React.FC = () => {
    const [websites, setWebsites] = useState<Website[]>([]);
    const [loading, setLoading] = useState(true);
    const [isCreating, setIsCreating] = useState(false);
    const [newDomain, setNewDomain] = useState('');
    const [newName, setNewName] = useState('');
    const [copiedId, setCopiedId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [submitLoading, setSubmitLoading] = useState(false);

    useEffect(() => {
        fetchWebsites();
    }, []);

    const fetchWebsites = async () => {
        try {
            const data = await getWebsites();
            setWebsites(data);
        } catch (error) {
            console.error('Failed to fetch websites', error);
        } finally {
            setLoading(false);
        }
    };

    const validateDomain = (domain: string): string | null => {
        if (!domain) return "Domain is required.";

        // Reserved words check
        const reserved = ['system', 'admin', 'internal', '__internal__', 'localhost'];
        if (reserved.includes(domain)) return "This domain name is reserved.";

        // Regex for valid hostname (simplified but strict enough)
        // Starts with alphanumeric, dots allowed, ends with alphanumeric, min 2 chars for TLD
        const domainRegex = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$/;
        if (!domainRegex.test(domain)) return "Invalid domain format. Example: example.com";

        return null; // Valid
    };

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setSubmitLoading(true);

        // 1. Sanitization
        let sanitizedDomain = newDomain.trim().toLowerCase();
        sanitizedDomain = sanitizedDomain.replace(/^https?:\/\//, '');
        sanitizedDomain = sanitizedDomain.replace(/\/$/, ''); // Remove trailing slash

        // 2. Client-Side Validation
        const validationError = validateDomain(sanitizedDomain);
        if (validationError) {
            setError(validationError);
            setSubmitLoading(false);
            return;
        }

        try {
            await createWebsite({ domain: sanitizedDomain, name: newName });
            setNewDomain('');
            setNewName('');
            setIsCreating(false);
            fetchWebsites();
        } catch (err: any) {
            console.error('Failed to create website', err);
            // 3. Error Mapping
            if (err.response) {
                if (err.response.status === 409) {
                    setError("This domain is already registered in your workspace.");
                } else if (err.response.status === 400) {
                    setError("Invalid domain format rejected by server.");
                } else {
                    setError("Something went wrong. Please try again.");
                }
            } else {
                setError("Network error. Please check your connection.");
            }
        } finally {
            setSubmitLoading(false);
        }
    };

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
        setCopiedId(text);
        setTimeout(() => setCopiedId(null), 2000);
    };

    if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>;

    return (
        <div className="min-h-screen bg-gray-50">

            <main className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold text-gray-900">Websites</h2>
                    <button
                        onClick={() => {
                            setIsCreating(!isCreating);
                            setError(null);
                        }}
                        className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                    >
                        <Plus className="w-5 h-5 mr-2" /> Add Website
                    </button>
                </div>

                {isCreating && (
                    <div className="mb-8 bg-white p-6 rounded-lg shadow">
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Domain</label>
                                <div className="mt-1">
                                    <input
                                        type="text"
                                        required
                                        placeholder="example.com"
                                        value={newDomain}
                                        onChange={(e) => {
                                            setNewDomain(e.target.value);
                                            if (error) setError(null); // Clear error on edit
                                        }}
                                        className={`block w-full rounded-md shadow-sm sm:text-sm p-2 border ${error ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'}`}
                                    />
                                </div>
                                {error && (
                                    <p className="mt-2 text-sm text-red-600" id="email-error">
                                        {error}
                                    </p>
                                )}
                                <p className="mt-1 text-xs text-gray-500">
                                    Enter root domain (e.g., example.com) without https://
                                </p>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Name (Optional)</label>
                                <input
                                    type="text"
                                    value={newName}
                                    onChange={(e) => setNewName(e.target.value)}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                                />
                            </div>
                            <div className="flex justify-end space-x-3">
                                <button
                                    type="button"
                                    onClick={() => {
                                        setIsCreating(false);
                                        setError(null);
                                    }}
                                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    disabled={submitLoading}
                                    className={`px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-medium ${submitLoading ? 'opacity-75 cursor-not-allowed' : ''}`}
                                >
                                    {submitLoading ? 'Creating...' : 'Create Website'}
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                    <ul className="divide-y divide-gray-200">
                        {websites.map((website) => (
                            <li key={website.id} className="px-6 py-4">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <h3 className="text-lg font-medium text-gray-900">{website.domain}</h3>
                                        <p className="text-sm text-gray-500">{website.name || 'No name'}</p>
                                    </div>
                                    <div className="flex items-center space-x-4">
                                        <div className="flex items-center bg-gray-100 rounded px-3 py-1">
                                            <span className="text-xs font-mono text-gray-600 mr-2">{website.tracking_id}</span>
                                            <button
                                                onClick={() => copyToClipboard(website.tracking_id)}
                                                className="text-gray-400 hover:text-gray-600"
                                                title="Copy Tracking ID"
                                            >
                                                {copiedId === website.tracking_id ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
                                            </button>
                                        </div>
                                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${website.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                            {website.is_active ? 'Active' : 'Inactive'}
                                        </span>
                                    </div>
                                </div>
                            </li>
                        ))}
                        {websites.length === 0 && (
                            <li className="px-6 py-12 text-center text-gray-500">
                                No websites registered yet.
                            </li>
                        )}
                    </ul>
                </div>
            </main>
        </div>
    );
};

export default Websites;
