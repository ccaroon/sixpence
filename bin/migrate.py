#!/usr/bin/env python
import argparse
import json
import os
import re
import yaml

from tinydb import TinyDB

from icon_search import IconSearch

class DbMigrator:
    CACHE_FILE = "./migration_cache.yml"
    def __init__(self, old_db_path):
        self.__old_db_path = old_db_path
        file_base, _ = os.path.splitext(self.__old_db_path)
        self.__new_db_path = f"{file_base}-v2.json"

        self.__icon_search = IconSearch()

        self.__cache = { "icons": {}, "tags": {}}
        self.__read_cache()
        self.__icon_cache = self.__cache["icons"]
        self.__tag_cache = self.__cache["tags"]


    def __read_cache(self):
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r") as fptr:
                self.__cache = yaml.safe_load(fptr)


    def __write_cache(self):
        with open(self.CACHE_FILE, "w") as ftpr:
            yaml.safe_dump(self.__cache, ftpr)


    def __read_old_db(self):
        records = []
        with open(self.__old_db_path, "r") as fptr:
            while line := fptr.readline():
                entry = json.loads(line)
                records.append(entry)

        return records


    # NOTE: "Borrowed" from src/models/tag.py
    def __normalize_tag(self, name):
        norm_name = name.strip()
        norm_name = name.lower()
        norm_name = re.sub(r'^\W+|\W+$',      '',  norm_name)
        norm_name = re.sub(r'[^a-zA-Z0-9_\-.]', ' ', norm_name)
        norm_name = re.sub(r'\s+',            '-', norm_name)

        return norm_name


    def __note2tags(self, entry):
        notes = entry["notes"]

        tags = self.__tag_cache.get(notes, [])
        if not tags:
            deleted = "Deleted" if entry.get("deleted_at") else "Active"
            print("#######################################################")
            print(f"# Note -> Tag: {entry['category']} | {entry['amount']} | {deleted}")
            print("#######################################################")
            print(f"\t=> {entry['notes']}")
            tag_str = ""
            while not tag_str:
                tag_str = input(f"Note2Tags> ")
                if tag_str == "Q":
                    self.__cleanup_exit("Quitting!")

                if tag_str:
                    tags = tag_str.split(",")
                    tags = [self.__normalize_tag(tg) for tg in tags]

            self.__tag_cache[notes] = tags

        return tags


    def __find_icon(self, keyword):
        choice = None

        cached_icon = self.__icon_cache.get(keyword)
        if cached_icon:
            choice = cached_icon
        else:
            choice = None
            search_term = keyword
            while not choice:
                matches = self.__icon_search.by_category(search_term)
                print("#######################################################")
                print(f"# Choose Icon: {keyword}                           ")
                print("#######################################################")
                for idx, icon in enumerate(matches):
                    print(f"{idx}) {icon}")

                response = input(f"Icon # | New Keyword> ")

                if response.isdigit():
                    idx = int(response)
                    while idx >= len(matches):
                        response = input(f"Invalid Choice> ")
                        idx = int(response)

                    choice = matches[idx]
                else:
                    if response == "Q":
                        self.__cleanup_exit("Quitting!")
                    else:
                        choice = None
                        search_term = response

            self.__icon_cache[keyword] = choice

        return choice


    def __cleanup_exit(self, msg, code=0):
        self.__write_cache()
        print(msg)
        exit(code)


    def migrate(self):
        if os.path.exists(self.__new_db_path):
            confirm = input(f"{self.__new_db_path} exists. Overwrite? (yes|no)> ")
            if confirm == "yes":
                os.remove(self.__new_db_path)
            else:
                self.__cleanup_exit("Migration Cancelled!")

        old_records = self.__read_old_db()

        db = TinyDB(self.__new_db_path)
        num_recs = len(old_records)
        new_records = []
        for idx, entry in enumerate(old_records):
            print(f"Converting: {entry["_id"]} | {idx+1:04}/{num_recs:04}")
            self.__munge_expenses_fields(entry)
            self.__munge_budget_fields(entry)
            self.__munge_shared_fields(entry)

            new_records.append(entry)

        print("\nData Conversion Complete!")

        # Sort the records on creation date
        new_records.sort(key=lambda entry: entry["created_at"])

        # Much faster for lots of records
        db.insert_multiple(new_records)

        self.__cleanup_exit(f"Migrated {num_recs} entries: {self.__new_db_path}")


    def __munge_shared_fields(self, entry):
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
            new_icon = self.__find_icon(entry["category"])
            entry["icon"] = new_icon

        if entry.get("notes"):
            tags = self.__note2tags(entry)
            del entry["notes"]
            entry["tags"] = tags


    def __munge_budget_fields(self, entry):
        if "history" in entry:
            for item in entry["history"]:
                item["date"] //= 1000

        if "firstDue" in entry:
            entry["first_due"] = entry["firstDue"]
            del entry["firstDue"]


    def __munge_expenses_fields(self, entry):
        category_repair = {
            "Home:Improvement": "Home:Improvements",
            "Home:Repair": "Home:Maintenance",
            "Bank:Fee": "Bank:Fees",
            "Travel": "Personal:Travel:Misc",
            "Travel:Dining": "Personal:Travel:Dining",
            "Travel:Lodging": "Personal:Travel:Lodging",
            "Travel:Misc": "Personal:Travel:Misc",
        }
        # Fix Categories
        if entry["category"] in category_repair:
            entry["category"] = category_repair.get(entry["category"])


def main(args):
    migrator = DbMigrator(args.old_db_file)
    migrator.migrate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Migrate Old DB Format (NedDB) to New DB (TinyDb) format"
    )

    parser.add_argument("old_db_file", type=str)

    args = parser.parse_args()
    main(args)
