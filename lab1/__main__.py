from catalog import Catalog

catalog = Catalog()
catalog.loadFromJson("catalog.json")
catalog.printAll()