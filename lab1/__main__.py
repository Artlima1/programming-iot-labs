from catalog import Catalog

catalog = Catalog()
catalog.loadFromJson("catalog.json")
catalog.printAll()
catalog.saveToJson("output_catalog.json")