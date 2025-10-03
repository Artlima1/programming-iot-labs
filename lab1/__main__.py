from catalog import Catalog

catalog = Catalog()
catalog.loadFromJson("catalog.json")
catalog.insertFromJon("new_device.json")
catalog.saveToJson("output_catalog.json")