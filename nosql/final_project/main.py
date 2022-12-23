from magic_store.kv_idea.store import Store
import pprint

def test():
    store = Store()

    result = store.put("key1", "test text")
    print(result)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)

    result = store.put("key1", "test text inny", namespace="osiolek")
    print(result)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)

    result = store.put("key1", "nierowazna czynnosc")
    print(result)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)
    print("===========================")
    x = store.get("key1")
    print(x)
    result = store.put("key1", "xxxxxxxxxxxxxxxxxxx", guard=x["guard"])
    print(result)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)

    x = store.get("key1", namespace="osiolek")
    result = store.delete("key1", namespace="osiolek", guard=x["guard"])
    print(result)
    pp.pprint(store._store)

    result = store.put("key1", "reaktywacja", namespace="osiolek")
    print(result)
    result = store.save()
    print(result)

def testLoad():
    store = Store()
    result = store.load()
    print(result)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)


if __name__ == '__main__':
    #test()
    testLoad()


