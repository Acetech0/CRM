import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getContact, updateContact, deleteContact } from '../api/contacts';
import { getActivities, createActivity, updateActivity, deleteActivity } from '../api/activities';
import type { Contact, ContactCreate } from '../types/contact';
import { ActivityType, type Activity } from '../types/activity';
import { ArrowLeft, User, Phone, Mail, Calendar } from 'lucide-react';

const ContactDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [contact, setContact] = useState<Contact | null>(null);
    const [activities, setActivities] = useState<Activity[]>([]);
    const [loading, setLoading] = useState(true);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editForm, setEditForm] = useState<ContactCreate>({ first_name: '', last_name: '', email: '', phone: '' });

    // Activity State
    const [newNote, setNewNote] = useState('');
    const [editingActivityId, setEditingActivityId] = useState<string | null>(null);
    const [editContent, setEditContent] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            if (!id) return;
            try {
                setLoading(true);
                // getContact returns ContactSummary { contact, deals, ... }
                const summary = await getContact(id);
                setContact(summary.contact);
                // We can use summary.recent_activities but keeping separate call for now if logic differs
                setActivities(summary.recent_activities);

                // Pre-fill edit form
                setEditForm({
                    first_name: summary.contact.first_name,
                    last_name: summary.contact.last_name,
                    email: summary.contact.email,
                    phone: summary.contact.phone
                });
            } catch (error) {
                console.error('Failed to fetch contact details', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [id]);

    const handleDelete = async () => {
        if (!id || !window.confirm("Are you sure you want to delete this contact?")) return;
        try {
            await deleteContact(id);
            navigate('/contacts');
        } catch (error) {
            console.error("Failed to delete contact", error);
            alert("Failed to delete contact");
        }
    };

    const handleUpdate = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!id) return;
        try {
            const updated = await updateContact(id, editForm);
            setContact(updated);
            setShowEditModal(false);
        } catch (error) {
            console.error("Failed to update contact", error);
            alert("Failed to update contact");
        }
    };

    // Activity Handlers
    const handleAddNote = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!id || !newNote.trim()) return;
        try {
            const activity = await createActivity({
                contact_id: id,
                type: ActivityType.NOTE,
                content: newNote
            });
            setActivities([activity, ...activities]);
            setNewNote('');
        } catch (error) {
            console.error("Failed to add note", error);
        }
    };

    const handleDeleteActivity = async (activityId: string) => {
        if (!window.confirm("Delete this activity?")) return;
        try {
            await deleteActivity(activityId);
            setActivities(activities.filter(a => a.id !== activityId));
        } catch (error) {
            console.error("Failed to delete activity", error);
        }
    };

    const startEditingActivity = (activity: Activity) => {
        setEditingActivityId(activity.id);
        setEditContent(activity.content);
    };

    const handleUpdateActivity = async (activityId: string) => {
        try {
            const updated = await updateActivity(activityId, { content: editContent });
            setActivities(activities.map(a => a.id === activityId ? updated : a));
            setEditingActivityId(null);
        } catch (error) {
            console.error("Failed to update activity", error);
        }
    };

    if (loading) return <div className="p-8">Loading details...</div>;
    if (!contact) return <div className="p-8">Contact not found.</div>;

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div className="flex justify-between items-center mb-4">
                    <Link to="/contacts" className="flex items-center text-sm text-blue-600 hover:text-blue-800">
                        <ArrowLeft className="w-4 h-4 mr-1" /> Back to Contacts
                    </Link>
                    <div className="flex space-x-2">
                        <button onClick={() => setShowEditModal(true)} className="px-3 py-1 bg-white border border-gray-300 rounded text-sm font-medium hover:bg-gray-50 text-gray-700"> Edit </button>
                        <button onClick={handleDelete} className="px-3 py-1 bg-red-50 border border-red-200 rounded text-sm font-medium hover:bg-red-100 text-red-600"> Delete </button>
                    </div>
                </div>

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
                            <div className="px-4 py-5 sm:px-6 border-b border-gray-200 flex justify-between items-center">
                                <h3 className="text-lg leading-6 font-medium text-gray-900">Activity Timeline</h3>
                            </div>

                            {/* Add Note Form */}
                            <div className="px-4 py-4 bg-gray-50 border-b border-gray-200">
                                <form onSubmit={handleAddNote}>
                                    <div className="flex gap-2">
                                        <input
                                            type="text"
                                            placeholder="Log a note..."
                                            className="flex-1 shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                                            value={newNote}
                                            onChange={(e) => setNewNote(e.target.value)}
                                        />
                                        <button type="submit" className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                            Add Note
                                        </button>
                                    </div>
                                </form>
                            </div>

                            <div className="px-4 py-5 sm:p-6 max-h-[600px] overflow-y-auto">
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
                                                    <div className="min-w-0 flex-1 pt-1.5 ">
                                                        <div className="flex justify-between space-x-4">
                                                            <div>
                                                                <p className="text-sm text-gray-500">
                                                                    <span className="font-medium text-gray-900">{activity.type.toUpperCase()}</span>
                                                                </p>
                                                            </div>
                                                            <div className="flex items-center space-x-2 text-sm text-gray-500">
                                                                <span>{new Date(activity.created_at).toLocaleString()}</span>
                                                                {editingActivityId !== activity.id && (
                                                                    <>
                                                                        <button onClick={() => startEditingActivity(activity)} className="text-blue-600 hover:text-blue-800">Edit</button>
                                                                        <button onClick={() => handleDeleteActivity(activity.id)} className="text-red-600 hover:text-red-800">Delete</button>
                                                                    </>
                                                                )}
                                                            </div>
                                                        </div>

                                                        {editingActivityId === activity.id ? (
                                                            <div className="mt-2">
                                                                <textarea
                                                                    className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                                                                    rows={3}
                                                                    value={editContent}
                                                                    onChange={(e) => setEditContent(e.target.value)}
                                                                />
                                                                <div className="mt-2 flex space-x-2">
                                                                    <button onClick={() => handleUpdateActivity(activity.id)} className="text-xs bg-blue-600 text-white px-2 py-1 rounded">Save</button>
                                                                    <button onClick={() => setEditingActivityId(null)} className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded">Cancel</button>
                                                                </div>
                                                            </div>
                                                        ) : (
                                                            <p className="text-sm text-gray-900 mt-1 whitespace-pre-wrap">{activity.content}</p>
                                                        )}
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
            {/* Edit Modal */}
            {showEditModal && (
                <div className="fixed inset-0 z-10 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        <div className="fixed inset-0 transition-opacity" aria-hidden="true" onClick={() => setShowEditModal(false)}>
                            <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
                        </div>
                        <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                <h3 className="text-lg leading-6 font-medium text-gray-900">Edit Contact</h3>
                                <form onSubmit={handleUpdate} className="mt-4 space-y-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700">First Name</label>
                                            <input required type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                                value={editForm.first_name} onChange={e => setEditForm({ ...editForm, first_name: e.target.value })} />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700">Last Name</label>
                                            <input required type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                                value={editForm.last_name} onChange={e => setEditForm({ ...editForm, last_name: e.target.value })} />
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Email</label>
                                        <input required type="email" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                            value={editForm.email} onChange={e => setEditForm({ ...editForm, email: e.target.value })} />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Phone</label>
                                        <input required type="tel" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                            value={editForm.phone} onChange={e => setEditForm({ ...editForm, phone: e.target.value })} />
                                    </div>
                                    <div className="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                        <button type="submit" className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:col-start-2 sm:text-sm">
                                            Save Changes
                                        </button>
                                        <button type="button" onClick={() => setShowEditModal(false)} className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:col-start-1 sm:text-sm">
                                            Cancel
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ContactDetail;
