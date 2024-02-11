import datetime
import pathlib
import pickle
from collections import UserDict


class InvalidFormat(Exception):
    def __call__(self):
        print('Invalid format, use DD-MM-YYYY')


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    pass
    
class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.validate(new_value):
            self.__value = new_value
        else:
            raise ValueError
        
    def validate(self, new_value):
        date_today = datetime.datetime.now().date()
        print(date_today)
        try:
            birthday_date = datetime.datetime.strptime(new_value, '%d-%m-%Y')
        except ValueError:
            print('not valid BD date format, should be DD-MM-YYYY')
            return False
        if date_today < birthday_date.date():
            print('BD date not ok')
            return False
        else:
            print('BD date is ok')
            return True
            


class Phone(Field):
    def __init__(self, value): # phone number validation
        self.__value = None
        self.value = value
        
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.validate(new_value):
            self.__value = new_value
        else:
            raise ValueError

    def validate(self, new_value):
        if len(new_value) != 10:
            print('Incorrect lenght of number')
            return False
        elif new_value.isdigit() == False:
            print('Number should be digits only')
            return False
        else:
            return True


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def __repr__(self):
        tail = f', birthday: {self.birthday}' if self.birthday else ''
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}" + tail

    def add_phone(self, phone):
        self.phone = Phone(phone)
        if self.phone:
            self.phones.append(self.phone)
        # for i in self.phones:
        #     print(i)

    def edit_phone(self, old_phone, new_phone):
        for index, number in enumerate(self.phones):
            if number.value == old_phone:
                self.phones[index] = Phone(new_phone)
                print(f'old number {old_phone} changed to new one {new_phone}')
                return 
        print("phone to edit not exist")
        raise ValueError
        

    def find_phone(self, phone):
        try:
            for number in self.phones:
                if number.value == phone:
                    print(f'I found necessary number {number.value}')
                    return number
        except ValueError:
            print('phone not found') 

    def remove_phone(self, phone):
        for number in self.phones:
            if number.value == phone:
                self.phones.remove(number)
                print(f'{number} removed')

    def days_to_birthday(self):
        if self.birthday is None:
            print('record has NO bd date')
            return None
        else:
            date_today = datetime.datetime.now().date()
            bd_date = datetime.datetime.strptime(self.birthday.value, '%d-%m-%Y').date()
            bd_date = bd_date.replace(year=date_today.year)
            if date_today > bd_date:
                bd_date = bd_date.replace(year=date_today.year+1)
            days_count = bd_date - date_today
            print(days_count.days)
            return days_count.days


class Iterable:
    MAX_VALUE = 10
    def __init__(self, adressbook, N):
        self.current_value = 0
        self.addressbook = adressbook
        self.N = N

    def __next__(self):
        start = self.current_value * self.N
        end = start + self.N
        records = list(self.addressbook.data.values())[start:end]
        if not records:
            raise StopIteration
        else:
            self.current_value += 1
            return records
        
    def __iter__(self):
        return self

class AddressBook(UserDict):
    N = 2
    storage_path = 'AdressBook.bin'

    def load(self):
        if pathlib.Path(self.storage_path).exists():
            with open(self.storage_path, 'rb') as file:
                self.data = pickle.load(file)
                print(self.data)
                return self.data
            
    def save(self):
        with open(self.storage_path, 'wb') as file:
            pickle.dump(self.data, file)

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name_to_find):
        for record in self.data.values():
            if record.name.value == name_to_find:
                print(f'{record} found')
                return record
        return None
    
    def global_search(self, query):
        result = set()
        for name, record in self.data.items():
            if query.lower() in name.lower():
                result.add(record)
            elif record.phones:
                for phone in record.phones:
                    if query in phone.value:
                        result.add(record)
        print(result)
        return result


    def delete(self, name):
        try: 
            record_to_delete = self.find(name)
            if record_to_delete:
                self.data.pop(record_to_delete.name.value)
                print(self.data)
        except ValueError:
            print('such phone to delete not found')

    def __iter__(self):
        return Iterable(self, self.N)

    def iterator(self):
        page = 1
        for r in self:
            print(r)
            print(f'page {page}')
            page += 1





if __name__ == "__main__":
    bd_date = '02-02-2020'
    bd = Birthday(bd_date)
    print(bd)
    bob = 'Bob'
    record = Record(bob, bd_date)
    record.days_to_birthday()
    record.add_phone('0502456560')
    # print(record)
    record1 = Record("Nick")
    record2 = Record('Ken')
    ab = AddressBook()
    ab.load()
    print(ab)
    # ab.add_record(record)
    # ab.add_record(record1)
    # ab.add_record(record2)
    # ab.iterator()
    result = ab.iterator()
    print(result)
    ab.global_search('k')
