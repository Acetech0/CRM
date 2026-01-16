import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { login as apiLogin, register as apiRegister } from '../api/auth';
import { useAuth } from '../context/AuthContext';

type AuthTab = 'signin' | 'signup';

const AuthPage: React.FC = () => {
    const [activeTab, setActiveTab] = useState<AuthTab>('signin');

    // Form States
    const [companyName, setCompanyName] = useState('');
    const [tenantSlug, setTenantSlug] = useState('');
    const [adminName, setAdminName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // UI States
    const [error, setError] = useState('');
    const [successMsg, setSuccessMsg] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const clearForm = () => {
        setCompanyName('');
        setTenantSlug('');
        setAdminName('');
        setEmail('');
        setPassword('');
        setError('');
        setSuccessMsg('');
    };

    const handleTabChange = (tab: AuthTab) => {
        setActiveTab(tab);
        clearForm();
    };

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const data = await apiLogin({ tenant_slug: tenantSlug, email, password });
            login(data.access_token);
            navigate('/dashboard');
        } catch (err: unknown) {
            let message = 'Login failed. Please check your credentials.';
            if (axios.isAxiosError(err) && err.response?.data?.detail) {
                message = err.response.data.detail;
            }
            setError(message);
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccessMsg('');

        try {
            await apiRegister({
                company_name: companyName,
                company_slug: tenantSlug,
                admin_name: adminName,
                admin_email: email,
                admin_password: password
            });
            setSuccessMsg('Registration successful! Please sign in.');
            setTimeout(() => {
                handleTabChange('signin');
                // Retain slug for easier login
                setTenantSlug(tenantSlug);
            }, 1500);
        } catch (err: unknown) {
            console.error('Registration Error:', err);
            let message = 'Registration failed. Please try again.';

            if (!(err as any).response) {
                // Network Error / CORS / Server Down
                message = "Network error. Please check your connection or server status.";
            } else if (axios.isAxiosError(err) && err.response?.data) {
                const detail = err.response.data.detail;

                // Priority 1: Direct string message (400/409)
                if (typeof detail === 'string') {
                    message = detail;
                }
                // Priority 2: Array of validation errors (422)
                else if (Array.isArray(detail) && detail.length > 0) {
                    // Extract validation messages properly (Pydantic 'val_error' schema)
                    // We join them if multiple, or just take the first one
                    const errors = detail.map((e: any) => e.msg).filter(Boolean);
                    if (errors.length > 0) {
                        message = errors.join(', ');
                    }
                }
            }

            setError(message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-50">
            <div className="w-full max-w-md bg-white rounded-lg shadow-md overflow-hidden">
                {/* Tabs */}
                <div className="flex border-b">
                    <button
                        className={`flex-1 py-4 text-center font-medium ${activeTab === 'signin' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
                        onClick={() => handleTabChange('signin')}
                    >
                        Sign In
                    </button>
                    <button
                        className={`flex-1 py-4 text-center font-medium ${activeTab === 'signup' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
                        onClick={() => handleTabChange('signup')}
                    >
                        Sign Up
                    </button>
                </div>

                <div className="p-8">
                    {error && (
                        <div className="mb-4 p-3 bg-red-50 text-red-700 rounded border border-red-200 text-sm">
                            {error}
                        </div>
                    )}
                    {successMsg && (
                        <div className="mb-4 p-3 bg-green-50 text-green-700 rounded border border-green-200 text-sm">
                            {successMsg}
                        </div>
                    )}

                    {activeTab === 'signin' ? (
                        <form onSubmit={handleLogin} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Tenant Slug</label>
                                <input
                                    type="text"
                                    required
                                    className="w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    value={tenantSlug}
                                    onChange={(e) => setTenantSlug(e.target.value)}
                                    placeholder="acme-corp"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                <input
                                    type="email"
                                    required
                                    className="w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="admin@example.com"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                                <input
                                    type="password"
                                    required
                                    className="w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                {loading ? 'Signing In...' : 'Sign In'}
                            </button>
                        </form>
                    ) : (
                        <form onSubmit={handleRegister} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
                                <input
                                    type="text"
                                    required
                                    className="w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    value={companyName}
                                    onChange={(e) => setCompanyName(e.target.value)}
                                    placeholder="Acme Corp"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Tenant Slug</label>
                                <input
                                    type="text"
                                    required
                                    className="w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    value={tenantSlug}
                                    onChange={(e) => setTenantSlug(e.target.value)}
                                    placeholder="acme-corp"
                                />
                                <p className="mt-1 text-xs text-gray-500">This will be your unique identifier.</p>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Admin Name</label>
                                <input
                                    type="text"
                                    required
                                    className="w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    value={adminName}
                                    onChange={(e) => setAdminName(e.target.value)}
                                    placeholder="Alice Admin"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Admin Email</label>
                                <input
                                    type="email"
                                    required
                                    className="w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="admin@example.com"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                                <input
                                    type="password"
                                    required
                                    className="w-full px-3 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                {loading ? 'Creating Tenant...' : 'Register Tenant'}
                            </button>
                        </form>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AuthPage;
