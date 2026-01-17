import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getForm, getFormStats } from '../api/forms';
import type { Form, FormStats } from '../types/form';
import { ArrowLeft, Copy, Check } from 'lucide-react';

const FormDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [form, setForm] = useState<Form | null>(null);
    const [stats, setStats] = useState<FormStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [copiedCode, setCopiedCode] = useState(false);

    useEffect(() => {
        if (id) {
            fetchData(id);
        }
    }, [id]);

    const fetchData = async (formId: string) => {
        try {
            const [formData, statsData] = await Promise.all([
                getForm(formId),
                getFormStats(formId)
            ]);
            setForm(formData);
            setStats(statsData);
        } catch (error) {
            console.error('Failed to fetch form details', error);
        } finally {
            setLoading(false);
        }
    };

    const copyEmbedCode = () => {
        if (!form) return;
        const code = `<div id="crm-form-${form.id}"></div>
<script src="${import.meta.env.VITE_API_URL?.replace('/api/v1', '') || 'http://localhost:8000'}/public/v1/forms/${form.id}/embed.js"></script>`;
        navigator.clipboard.writeText(code);
        setCopiedCode(true);
        setTimeout(() => setCopiedCode(false), 2000);
    };

    if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
    if (!form) return <div className="flex items-center justify-center h-screen">Form not found</div>;

    return (
        <div className="min-h-screen bg-gray-50">

            <main className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div className="mb-6">
                    <Link to="/forms" className="flex items-center text-gray-500 hover:text-gray-900 mb-4">
                        <ArrowLeft className="w-4 h-4 mr-1" /> Back to Forms
                    </Link>
                    <div className="flex justify-between items-start">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900">{form.name}</h2>
                            <p className="text-gray-500 text-sm mt-1">ID: {form.id}</p>
                        </div>
                        <div className="text-right">
                            {/* Stats Placeholder */}
                            <div className="bg-white px-4 py-2 rounded shadow-sm border text-sm">
                                <span className="text-gray-500">Submissions:</span> <b>{stats?.submission_count || 0}</b>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                    {/* Fields List */}
                    <div className="bg-white shadow sm:rounded-lg">
                        <div className="px-4 py-5 border-b border-gray-200 sm:px-6 flex justify-between items-center">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">Form Fields</h3>
                            {/* <button className="text-sm text-blue-600 hover:text-blue-500">Add Field</button> */} {/* MVP: Read only first */}
                        </div>
                        <div className="bg-gray-50 px-4 py-5 sm:p-6 pb-20">
                            {/* Preview of Form */}
                            <form className="space-y-4 pointer-events-none opacity-75">
                                {form.fields.sort((a, b) => a.order - b.order).map((field) => (
                                    <div key={field.id}>
                                        <label className="block text-sm font-medium text-gray-700">
                                            {field.label} {field.required && <span className="text-red-500">*</span>}
                                        </label>
                                        {field.field_type === 'textarea' ? (
                                            <textarea className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border" rows={3}></textarea>
                                        ) : (
                                            <input type={field.field_type} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border" placeholder={field.placeholder || ''} />
                                        )}
                                    </div>
                                ))}
                                {form.fields.length === 0 && <p className="text-gray-400 italic text-center">No fields configured.</p>}
                                <button className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600">
                                    Submit
                                </button>
                            </form>
                        </div>
                    </div>

                    {/* Integration Info */}
                    <div className="space-y-6">
                        <div className="bg-white shadow sm:rounded-lg">
                            <div className="px-4 py-5 border-b border-gray-200 sm:px-6">
                                <h3 className="text-lg leading-6 font-medium text-gray-900">Integration</h3>
                            </div>
                            <div className="px-4 py-5 sm:p-6">
                                <p className="text-sm text-gray-500 mb-4">
                                    Copy and paste this code into your website's HTML where you want the form to appear.
                                </p>
                                <div className="relative">
                                    <pre className="bg-gray-800 text-gray-100 p-4 rounded-md text-sm overflow-x-auto">
                                        {`<div id="crm-form-${form.id}"></div>
<script src="${import.meta.env.VITE_API_URL?.replace('/api/v1', '') || 'http://localhost:8000'}/public/v1/forms/${form.id}/embed.js"></script>`}
                                    </pre>
                                    <button
                                        onClick={copyEmbedCode}
                                        className="absolute top-2 right-2 p-2 rounded-md bg-gray-700 text-white hover:bg-gray-600"
                                        title="Copy Code"
                                    >
                                        {copiedCode ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default FormDetail;
