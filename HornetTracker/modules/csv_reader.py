import csv


def csv_reader(data: str):
    try:
        csv_text = data.split("\n")
        reader = csv.DictReader(csv_text, delimiter=",")
        return list(reader)
    except TypeError:
        return False
    except Exception:
        return False
