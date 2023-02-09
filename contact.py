class ContactList(list):
    def search(self, name):
        '''Return all contacts that contain the search value in their name.'''
        matching_contacts = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)

        return matching_contacts


class Contact:
    all_contacts = ContactList()

    def __init__(self, name, email):
        self._name = name
        self._email = email
        __class__.all_contacts.append(self)

    def __str__(self):
        return f"{self._name}, email is {self._email}"

    def __repr__(self):
        return f"{__class__.__name__}('{self._name}', '{self._email}')"

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email


class Friend(Contact):
    def __init__(self, name, email, phone):
        super().__init__(name, email)
        self._phone = phone

    def __str__(self):
        return f"{super().__str__()}, phone is {self.phone}"

    @property
    def phone(self):
        return self._phone


class Supplier(Contact):
    def order(self, order):
        print(f"If self were a real system we would send {order} order to {self._name}")


class MailSender:
    def send_mail(self, message):
        print(f"-------\nSending mail to {self.email}\nMessage:\n\n{message}\n-------")
        # Add e-mail logic here


class EmailableContact(Contact, MailSender):
    pass


if __name__ == "__main__":
    c1 = Contact("John A", "johna@example.net")
    c2 = Contact("John B", "johnb@example.net")
    c3 = EmailableContact("Jenna C", "jennac@example.net")
    f1 = Friend("Joe Bloggs", "joe@bloggs.net", "+35319998888")
    filtered_contacts = [c.name for c in Contact.all_contacts.search('John')]

    c3.send_mail("How's it going?")

    print(c1)
    print(c2)
    print(c3)
    print(f1)
    print(filtered_contacts)
