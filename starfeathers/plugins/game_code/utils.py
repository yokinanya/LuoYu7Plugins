import json
import os


def game_code(game: str):
    code_file = os.path.abspath(os.path.join(os.path.dirname(__file__), f"codes.json"))
    with open(code_file, "r", encoding="utf-8") as gamecode:
        codes = json.load(gamecode)
        codes = codes[game]
        gamecode.close()
    code = ""
    for key in codes:
        code = code + f"{codes[key]}：{key}\n"
    return code


def game_code_writer(game: str, code: str, description: str, operation: str):
    code_file = os.path.abspath(os.path.join(os.path.dirname(__file__), f"codes.json"))
    status = 0

    def write_json(codes: dict):
        with open(code_file, "w", encoding="utf-8") as gamecode:
            json.dump(codes, gamecode)
            gamecode.close()

    with open(code_file, "r", encoding="utf-8") as gamecode:
        codes = json.load(gamecode)
        gamecode.close()

    if operation == "add":
        codes[game][code] = description
        write_json(codes)
        status = 200
    elif operation == "del":
        try:
            del codes[game][code]
            write_json(codes)
        except KeyError:
            status = 404
        except:
            status = 502
    elif operation == "edit":
        try:
            codes[game][code] = description
            write_json(codes)
        except KeyError:
            status = 404
        except:
            status = 502
    return status
