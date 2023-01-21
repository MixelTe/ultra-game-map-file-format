from typing import Callable, Any

IFieldName = str
IParser = Callable[[str], Any]
DefaultParser = lambda v: v


def parseFile(name: str, parsers: dict[IFieldName, IParser] = {}):
    with open(name, "r", encoding="utf8") as f:
        content = f.read().strip().strip(";")

    Map = {}

    for el in content.split(";"):
        if not (":" in el or "=" in el):
            print(f"[{__name__} parseFile] Bad value:\n", el)
            continue
        isList = ":" in el
        key, value = map(str.strip, el.split(":" if isList else "="))
        parser = parsers[key] if key in parsers else DefaultParser

        if isList:
            Map[key] = list(map(parser, map(str.strip, value.split("\n"))))
        else:
            Map[key] = parser(value)

    return Map


def loadMap(name: str):
    parser_point = lambda v: tuple(map(int, v.split(" ")))
    parser_idWithNums = lambda v: (v.split(" ")[0], *list(map(int, v.split(" ")[1:])))
    return parseFile(name, {
        "map": lambda v: list(v),
        "guys": parser_idWithNums,
        "items": parser_idWithNums,
        "spawn": parser_point,
        "exits": parser_point,
    })


from pprint import pprint

def printMap(Map):
    for key in Map:
        if (key == "map"):
            print(f"{key}:", '\n'.join(map(''.join, Map[key])), sep="\n")
        else:
            print(key, end=": ")
            pprint(Map[key])


printMap(loadMap("coolMap.ultra_game_map"))
