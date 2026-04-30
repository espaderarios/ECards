import csv
import io


def generate_csv(entries):
    """entries: list of {'front':..., 'back':...}"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Front", "Back"])
    for e in entries or []:
        writer.writerow([e.get('front', ''), e.get('back', '')])
    return output.getvalue()
