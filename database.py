import pandas as pd

class Database:
    def __init__(self, file_path):
        self.data_base = pd.read_excel(file_path)

    def filter_by_category(self, category):
        return self.data_base[self.data_base['category'] == category]

    def get_address_and_names_by_category(self, category):
        table_by_category = self.filter_by_category(category)
        addresses = table_by_category['eng_address'].tolist()
        names = table_by_category['name'].tolist()
        return addresses, names