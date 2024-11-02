import os
import re
from datetime import datetime

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class ContactManager:
    def __init__(self):
        self.contacts = []
    
    def add_contact(self, name, phone, email, address):
        if not self._is_valid_phone(phone):
            raise ValueError("Invalid phone number format")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        if self._phone_exists(phone):
            raise ValueError("Phone number already exists")
            
        contact = Contact(name, phone, email, address)
        self.contacts.append(contact)
        self._sort_contacts()
        return contact
    
    def update_contact(self, index, name, phone, email, address):
        if not self._is_valid_phone(phone):
            raise ValueError("Invalid phone number format")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        if phone != self.contacts[index].phone and self._phone_exists(phone):
            raise ValueError("Phone number already exists")
            
        contact = self.contacts[index]
        contact.name = name
        contact.phone = phone
        contact.email = email
        contact.address = address
        contact.updated_at = datetime.now()
        self._sort_contacts()
        
    def delete_contact(self, index):
        return self.contacts.pop(index)
    
    def search_contacts(self, query):
        query = query.lower()
        return [
            (i, contact) for i, contact in enumerate(self.contacts)
            if query in contact.name.lower() or query in contact.phone
        ]
    
    def _sort_contacts(self):
        self.contacts.sort(key=lambda x: x.name.lower())
    
    def _is_valid_phone(self, phone):
        return bool(re.match(r'^\+?1?\d{9,15}$', phone))
    
    def _is_valid_email(self, email):
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    def _phone_exists(self, phone):
        return any(contact.phone == phone for contact in self.contacts)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n=== Contact Management System ===")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contacts")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

def display_contact(contact):
    print(f"\nName: {contact.name}")
    print(f"Phone: {contact.phone}")
    print(f"Email: {contact.email}")
    print(f"Address: {contact.address}")
    print(f"Created: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Last Updated: {contact.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

def get_contact_details(existing_contact=None):
    print("\nEnter contact details:")
    name = input("Name: ").strip()
    if not name:
        raise ValueError("Name cannot be empty")
        
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    address = input("Address: ").strip()
    
    return name, phone, email, address

def main():
    manager = ContactManager()
    
    while True:
        clear_screen()
        display_menu()
        
        choice = input("\nEnter your choice (1-6): ")
        
        try:
            if choice == '1':
                details = get_contact_details()
                contact = manager.add_contact(*details)
                print("\n✅ Contact added successfully!")
                display_contact(contact)
                
            elif choice == '2':
                if not manager.contacts:
                    print("\nNo contacts found!")
                else:
                    print("\n=== Contact List ===")
                    for i, contact in enumerate(manager.contacts, 1):
                        print(f"\n{i}. {contact.name}")
                        print(f"   📞 {contact.phone}")
                
            elif choice == '3':
                query = input("\nEnter name or phone number to search: ").strip()
                results = manager.search_contacts(query)
                
                if not results:
                    print("\nNo matching contacts found!")
                else:
                    print(f"\nFound {len(results)} matching contacts:")
                    for i, contact in results:
                        print(f"\n{i + 1}. {contact.name}")
                        print(f"   📞 {contact.phone}")
                    
                    view_details = input("\nEnter contact number to view details (or press Enter to skip): ")
                    if view_details.isdigit() and 1 <= int(view_details) <= len(results):
                        display_contact(results[int(view_details) - 1][1])
                
            elif choice == '4':
                if not manager.contacts:
                    print("\nNo contacts to update!")
                    continue
                    
                print("\n=== Select Contact to Update ===")
                for i, contact in enumerate(manager.contacts, 1):
                    print(f"{i}. {contact.name} ({contact.phone})")
                
                index = int(input("\nEnter contact number: ")) - 1
                if 0 <= index < len(manager.contacts):
                    print("\nCurrent details:")
                    display_contact(manager.contacts[index])
                    details = get_contact_details(manager.contacts[index])
                    manager.update_contact(index, *details)
                    print("\n✅ Contact updated successfully!")
                else:
                    print("\n❌ Invalid contact number!")
                
            elif choice == '5':
                if not manager.contacts:
                    print("\nNo contacts to delete!")
                    continue
                    
                print("\n=== Select Contact to Delete ===")
                for i, contact in enumerate(manager.contacts, 1):
                    print(f"{i}. {contact.name} ({contact.phone})")
                
                index = int(input("\nEnter contact number: ")) - 1
                if 0 <= index < len(manager.contacts):
                    contact = manager.delete_contact(index)
                    print(f"\n✅ Contact '{contact.name}' deleted successfully!")
                else:
                    print("\n❌ Invalid contact number!")
                
            elif choice == '6':
                print("\nThank you for using Contact Management System!")
                break
                
            else:
                print("\n❌ Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")
            
        except ValueError as e:
            print(f"\n❌ Error: {str(e)}")
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {str(e)}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()