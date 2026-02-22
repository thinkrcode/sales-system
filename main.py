from enum import Enum
from faker import Faker
import json

class SaleField(Enum):  # name,value
    SELLER_ID = "seller_id"
    COUNTRY = "country"
    FIRST_NAME = "firstName"
    LAST_NAME = "lastName"
    PRODUCT = "product"

# Only Product Sale
class Sale:
    def __init__(self,seller_id,country,firstName,lastName,product):
        self.seller_id = seller_id
        self.country = country
        self.firstName = firstName
        self.lastName = lastName
        self.product = product

    def to_dict(self) -> dict:
        return {
            "seller_id":self.seller_id,
            "country":self.country,
            "firstName":self.firstName,
            "lastName":self.lastName,
            "product":self.product
        }
    def __str__(self) -> str:
        return f"{self.firstName} {self.lastName}, {self.country}, Product: {self.product}"

# Business Logic Operations Section
class SaleService:
    def __init__(self,repo,faker):  # free from class dependency
        self.repository = repo
        self.fake = faker

    def create_fake_sales(self,count=5) -> None:
        """
        Creates a fake sales record
        """
        sales = self.repository.load()
   
        for _ in range(count):
            sale = Sale(    # Sale constructor this here!
                self.fake.random_digit(),
                self.fake.country(),
                self.fake.first_name(),
                self.fake.last_name(),
                self.fake.license_plate()
            )
            sales.append(sale.to_dict())

        self.repository.save(sales)

    def create_sale(self,seller_id,country,firstName,lastName,product) -> None:
        """
        Creates a new sales record
        """
        sales = self.repository.load()
        sale = Sale(    # Sale constructor this here!
            seller_id,
            country,
            firstName,
            lastName,
            product
        )
        sales.append(sale.to_dict())

        self.repository.save(sales)

    def list_sales(self) -> None:
        sales = [Sale(**s) for s in self.repository.load()]
        for index, sale in enumerate(sales):
            print(f"{index}: {sale}")

    def update_sale_field(self, index: int, field: SaleField, new_value) -> None:
        """
        Updates a specific field of the Sale object in a specific row.
        - index: which row
        - field: SaleField enum
        - new_value: new value
        """
        sales = self.repository.load()
        
        if index < 0 or index >= len(sales):
            raise IndexError("Index out of range")
        
        sale = Sale(**sales[index])
        setattr(sale, field.value, new_value)
        sales[index] = sale.to_dict()
        self.repository.save(sales)

    def delete_sale(self, index: int) -> None:
        """
        Deletes the Sale object in a specific row.
        """
        sales = self.repository.load()
        
        if index < 0 or index >= len(sales):
            raise IndexError("Index out of range")
        
        removed_sale = sales.pop(index)
        self.repository.save(sales)

        print(f"Deleted information: {removed_sale}")
        
    def delete_sale_field(self, index: int, field: SaleField) -> None:
        """
        Clears the area of the Sale object in a specific row (sets it to None).
        """
        sales = self.repository.load()
        
        if index < 0 or index >= len(sales):
            raise IndexError("Index out of range")
        
        sale = Sale(**sales[index])
        setattr(sale, field.value, None)
        
        sales[index] = sale.to_dict()
        self.repository.save(sales)


    def search_record(self, value, field: SaleField) -> list[Sale]:  # business logic for returns sale object
        """
        Searches by feature for record
        """
        sales = self.repository.load()
        sales = [Sale(**s) for s in sales]  # dict → Sale object
        return [s for s in sales if getattr(s, field.value) == value]

# Only File Handling
class JsonRepository: 
    
    def __init__(self,filename):
        self.filename = filename
    
    def load(self) -> list:
        """
        Reads JSON files and returns them as a list
        """
        try:
            with open(self.filename) as file:
                return json.load(file)
        except (FileNotFoundError,json.JSONDecodeError):
            return []
        
    def save(self,data) -> None:
        """
        Writes data to JSON files
        """
        with open(self.filename,"w",encoding="utf-8") as file:
            json.dump(data,file,ensure_ascii=False,indent=2)

#  Main Section
repo = JsonRepository("test.json")
service = SaleService(repo, Faker())

while True:
    print("""
    1 - List Sales
    2 - Create Sale
    3 - Update Sale Field
    4 - Delete Sale
    5 - Search Record
    6 - Exit
    """)
    
    choice = input("Enter your choice: ")
    
    match choice:
        case "1":
            service.list_sales()
        case "2":
            count = int(input("How many sales do you want to add? \n > "))
            for _ in range(count):
                seller_id = int(input("Seller ID: "))
                country = input("Country: ")
                firstName = input("First Name: ")
                lastName = input("Last Name: ")
                product = input("Product: ")
                service.create_sale(seller_id, country, firstName, lastName, product)
                print("Sale added!")
        case "3":
            index = int(input("Enter the index to update: "))
            print("Which field do you want to update?")
            for field in SaleField:
                print(f"{field.name} - {field.value}")
            field_input = input("Field name: ").strip().upper()
            if field_input in SaleField.__members__:
                field = SaleField[field_input]
                new_value = input("Enter the new value: ")
                service.update_sale_field(index, field, new_value)
                print("Sale updated!")
            else:
                print("Invalid field.")
        case "4":
            index = int(input("Enter the index to delete: "))
            service.delete_sale(index)
        case "5":
            print("Which field do you want to search by?")
            for field in SaleField:
                print(f"{field.name} - {field.value}")
            field_input = input("Field name: ").strip().upper()
            if field_input in SaleField.__members__:
                field = SaleField[field_input]
                value = input("Enter the value to search for: ")
                results = service.search_record(value, field)
                print("Search Results:")
                for sale in results:
                    print(sale)
            else:
                print("Invalid field.")
        case "6":
            print("Exiting...")
            break
        case _:
            print("Invalid choice, please try again.")