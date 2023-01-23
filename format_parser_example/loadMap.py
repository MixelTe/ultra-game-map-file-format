from typing import Callable, Any

ICustomType = str
ICustomTypeParser = Callable[[str], Any]


def parseFile(name: str, customTypes: dict[ICustomType, ICustomTypeParser] = {}):
    with open(name, "r", encoding="utf8") as f:
        content = f.read().strip().strip(";")

    Map = {}

    for el in content.split(";"):
        if not (":" in el or "=" in el):
            print(f"[{__name__} parseFile] Bad value:\n", el)
            continue
        isList = ":" in el
        key, value = map(str.strip, el.split(":" if isList else "="))

        if ("(" in key and ")" in key):
            types = key[key.find("(") + 1:key.find(")")].split()
        else:
            types = ["str"]

        def parser(v: str):
            if len(types) == 1:
                type = types[0]
                if "[]" not in type:
                    return parseType(v, type, customTypes)
                type = type[:type.index("[]")]
                return list(map(lambda vl: parseType(vl, type, customTypes), v.split()))
            r = []
            listType = None
            listV = []
            values = v.split()
            for i in range(len(values)):
                value = values[i]
                if len(types) <= i or listType:
                    if listType:
                        listV.append(parseType(value, listType, customTypes))
                    else:
                        r.append(value)
                    continue
                type = types[i]
                if "[]" in type:
                    type = type[:type.index("[]")]
                    listType = type
                    listV.append(parseType(value, type, customTypes))
                else:
                    r.append(parseType(value, type, customTypes))
            if listType:
                r.append(listV)
            return tuple(r)

        if "(" in key:
            key = key[:key.find("(")].strip()

        if isList:
            Map[key] = list(map(parser, map(str.strip, value.split("\n"))))
        else:
            Map[key] = parser(value)

    return Map

def parseType(v, type, customTypes):
    try:
        if (type in customTypes): return customTypes[type](v)
        if (type == "str"): return str(v)
        if (type == "int"): return int(v)
        if (type == "float"): return float(v)
        if (type == "bool"): return bool(v)
        if (type == "map"): return list(v)
        return None
    except Exception:
        return None


def loadMap(name: str):
    return parseFile(name, {})


from pprint import pprint

def printMap(Map):
    for key in Map:
        if (key == "map"):
            print(f"{key}:", '\n'.join(map(''.join, Map[key])), sep="\n")
        else:
            print(key, end=": ")
            pprint(Map[key])


printMap(loadMap("coolMap_types.ultra_game_map"))
