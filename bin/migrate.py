#!/usr/bin/env python
import argparse
import json
import os
import yaml

from tinydb import TinyDB

from icon_search import IconSearch

def __read_sxp_db(filename):
    records = []
    with open(args.input_file, "r") as fptr:
        while line := fptr.readline():
            entry = json.loads(line)
            records.append(entry)

    return records


def __munge_shared_fields(entry, icon_search, icon_cache):
    # delete _id
    del entry["_id"]

    # reformat/rename date fields
    for field in ("date", "createdAt", "updatedAt", "archivedAt"):
        if field in entry:
            value = entry.get(field)
            new_value = value["$$date"] // 1000 if value else None
            del entry[field]

            if field == "archivedAt":
                new_field = "deleted_at"
            else:
                new_field = field.replace("At", "_at")

            entry[new_field] = new_value

    if "icon" in entry:
        new_icon = icon_search.interactive(entry["category"], cache=icon_cache)
        entry["icon"] = new_icon


def __munge_budget_fields(entry):
    if "history" in entry:
        for item in entry["history"]:
            item["date"] //= 1000

    if "firstDue" in entry:
        entry["first_due"] = entry["firstDue"]
        del entry["firstDue"]


def __munge_expenses_fields(entry):
    pass


def main(args):
    input_file = args.input_file
    file_base, _ = os.path.splitext(input_file)
    output_file = f"{file_base}-v2.json"

    icon_cache = {}
    icon_map_file = "./icon_map.yml"
    if os.path.exists(icon_map_file):
        with open(icon_map_file, "r") as fptr:
            icon_cache = yaml.safe_load(fptr)

    icon_search = IconSearch()

    if os.path.exists(output_file):
        confirm = input(f"{output_file} exists. Overwrite? (yes|no)> ")
        if confirm == "yes":
            os.remove(output_file)
        else:
            print("Migration Cancelled!")
            exit(1)

    records = __read_sxp_db(input_file)

    db = TinyDB(output_file)
    num_recs = len(records)
    for idx, entry in enumerate(records):
        print(f"Converting: {entry["_id"]} | {idx:04}/{num_recs:04}", end="\r")
        __munge_shared_fields(entry, icon_search, icon_cache)
        __munge_budget_fields(entry)

    print("\nData Conversion Complete!")

    # Sort the records on creation date
    records.sort(key=lambda entry: entry["created_at"])

    # Much faster for lots of records
    db.insert_multiple(records)

    with open(icon_map_file, "w") as ftpr:
        yaml.safe_dump(icon_cache, ftpr)

    print(f"Successfully migrated {num_recs} entries: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate data from Old (NedDB) format to New (TinyDb) format")

    parser.add_argument("input_file", type=str)

    args = parser.parse_args()
    main(args)
