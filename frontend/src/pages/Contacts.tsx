import React, { useEffect, useState } from 'react';
import { getContacts, createContact } from '../api/contacts';
import type { Contact, ContactCreate } from '../types/contact';
import { Plus, Phone, Mail } from 'lucide-react';
import { Link } from 'react-router-dom';

const Contacts: React.FC = () => {
    const [contacts, setContacts] = useState<Contact[]>([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [newContact, setNewContact] = useState<ContactCreate>({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
    });

    const fetchContacts = async () => {
        try {
            setLoading(true);
            const data = await getContacts();
            setContacts(data);
        } catch (error) {
            console.error('Failed to fetch contacts', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchContacts();
    }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await createContact(newContact);
            setShowModal(false);
            setNewContact({ first_name: '', last_name: '', email: '', phone: '' });
            fetchContacts();
        } catch (error) {
            console.error('Failed to create contact', error);
            alert('Failed to create contact');
        }
    };

    if (loading) return <div className="p-8">Loading contacts...</div>;

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div className="flex justify-between mb-6">
                    <h1 className="text-2xl font-bold text-gray-900">Contacts</h1>
                    <button
                        onClick={() => setShowModal(true)}
                        className="flex items-center px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700"
                    >
                        <Plus className="w-5 h-5 mr-2" />
                        New Contact
                    </button>
                </div>

                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                    <ul className="divide-y divide-gray-200">
                        {contacts.map((contact) => (
                            <li key={contact.id}>
                                <Link to={`/contacts/${contact.id}`} className="block hover:bg-gray-50">
                                    <div className="flex items-center px-4 py-4 sm:px-6">
                                        <div className="flex-1 min-w-0 flex items-center">
                                            <div className="flex-shrink-0">
                                                <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                                                    <span className="text-gray-500 font-medium">{contact.first_name[0]}{contact.last_name[0]}</span>
                                                </div>
                                            </div>
                                            <div className="min-w-0 flex-1 px-4 md:grid md:grid-cols-2 md:gap-4">
                                                <div>
                                                    <p className="text-sm font-medium text-blue-600 truncate">{contact.first_name} {contact.last_name}</p>
                                                    <p className="mt-2 flex items-center text-sm text-gray-500">
                                                        <Mail className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                                                        <span className="truncate">{contact.email}</span>
                                                    </p>
                                                </div>
                                                <div className="hidden md:block">
                                                    <p className="mt-2 flex items-center text-sm text-gray-500">
                                                        <Phone className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                                                        {contact.phone}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            {/* Modal */}
            {showModal && (
                <div className="fixed inset-0 z-10 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        <div className="fixed inset-0 transition-opacity" aria-hidden="true">
                            <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
                        </div>
                        <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                <h3 className="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                                    Add New Contact
                                </h3>
                                <form onSubmit={handleCreate} className="mt-4 space-y-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700">First Name</label>
                                            <input required type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                                value={newContact.first_name} onChange={e => setNewContact({ ...newContact, first_name: e.target.value })} />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700">Last Name</label>
                                            <input required type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                                value={newContact.last_name} onChange={e => setNewContact({ ...newContact, last_name: e.target.value })} />
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Email</label>
                                        <input required type="email" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                            value={newContact.email} onChange={e => setNewContact({ ...newContact, email: e.target.value })} />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Phone</label>
                                        <input required type="tel" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                            value={newContact.phone} onChange={e => setNewContact({ ...newContact, phone: e.target.value })} />
                                    </div>
                                    <div className="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                        <button type="submit" className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:col-start-2 sm:text-sm">
                                            Save
                                        </button>
                                        <button type="button" onClick={() => setShowModal(false)} className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:col-start-1 sm:text-sm">
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

export default Contacts;
