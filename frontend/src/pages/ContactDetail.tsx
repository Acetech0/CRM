import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getContact } from '../api/contacts';
import { getActivities } from '../api/activities';
import type { Contact } from '../types/contact';
import type { Activity } from '../types/activity';
import { ArrowLeft, User, Phone, Mail, Calendar } from 'lucide-react';

const ContactDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [contact, setContact] = useState<Contact | null>(null);
    const [activities, setActivities] = useState<Activity[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            if (!id) return;
            try {
                setLoading(true);
                const [contactData, activitiesData] = await Promise.all([
                    getContact(id),
                    getActivities(id), // Assuming API supports filtering by contact_id or returns activities for the contact
                ]);
                setContact(contactData);
                setActivities(activitiesData);
            } catch (error) {
                console.error('Failed to fetch contact details', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [id]);

    if (loading) return <div className="p-8">Loading details...</div>;
    if (!contact) return <div className="p-8">Contact not found.</div>;

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <Link to="/contacts" className="flex items-center mb-4 text-sm text-blue-600 hover:text-blue-800">
                    <ArrowLeft className="w-4 h-4 mr-1" /> Back to Contacts
                </Link>

                <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
                    {/* Contact Info Card */}
                    <div className="lg:col-span-1">
                        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                            <div className="px-4 py-5 sm:px-6 flex items-center">
                                <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-4">
                                    <User className="w-6 h-6" />
                                </div>
                                <div>
                                    <h3 className="text-lg leading-6 font-medium text-gray-900">{contact.first_name} {contact.last_name}</h3>
                                    <p className="mt-1 max-w-2xl text-sm text-gray-500">Created on {new Date(contact.created_at).toLocaleDateString()}</p>
                                </div>
                            </div>
                            <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
                                <dl className="sm:divide-y sm:divide-gray-200">
                                    <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt className="text-sm font-medium text-gray-500 flex items-center"><Mail className="w-4 h-4 mr-2" /> Email</dt>
                                        <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{contact.email}</dd>
                                    </div>
                                    <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt className="text-sm font-medium text-gray-500 flex items-center"><Phone className="w-4 h-4 mr-2" /> Phone</dt>
                                        <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{contact.phone}</dd>
                                    </div>
                                </dl>
                            </div>
                        </div>
                    </div>

                    {/* Activities / Timeline */}
                    <div className="lg:col-span-2">
                        <div className="bg-white shadow sm:rounded-lg">
                            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                                <h3 className="text-lg leading-6 font-medium text-gray-900">Activity Timeline</h3>
                            </div>
                            <div className="px-4 py-5 sm:p-6">
                                {activities.length > 0 ? (
                                    <ul className="flow-root">
                                        {activities.map((activity, idx) => (
                                            <li key={activity.id} className="relative pb-8">
                                                {idx !== activities.length - 1 && (
                                                    <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true"></span>
                                                )}
                                                <div className="relative flex space-x-3">
                                                    <div>
                                                        <span className="h-8 w-8 rounded-full bg-green-500 flex items-center justify-center ring-8 ring-white">
                                                            <Calendar className="h-4 w-4 text-white" />
                                                        </span>
                                                    </div>
                                                    <div className="min-w-0 flex-1 pt-1.5 justify-between space-x-4">
                                                        <div>
                                                            <p className="text-sm text-gray-500">
                                                                <span className="font-medium text-gray-900">{activity.type}</span>: {activity.description}
                                                            </p>
                                                        </div>
                                                        <div className="text-right text-sm whitespace-nowrap text-gray-500">
                                                            {new Date(activity.created_at).toLocaleString()}
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p className="text-gray-500 text-sm">No recent activity.</p>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ContactDetail;
