#!/usr/bin/env python
import argparse
import json
import os
import re
import arrow

from tinydb import TinyDB

from app.config import Config
from utils.icon_search import IconSearch
from models.budget import Budget
from models.tag import Tag

class DbMigrator:
    CATEGORY_FIXES = {
        "Bank:Fee": "Bank:Fees",
        "Charity": "Personal:Charity",
        "Home:Improvement": "Home:Improvements",
        "Home:Repair": "Home:Maintenance",
        "Mortgage": "Home:Mortgage",
        "Personal:Entertainment:Acorntv": "Subscriptions:Acorntv",
        "Personal:Entertainment:Britbox": "Subscriptions:Britbox",
        "Personal:Entertainment:Disney+": "Subscriptions:Disney+",
        "Personal:Entertainment:Hulu": "Subscriptions:Hulu",
        "Personal:Entertainment:Netflix": "Subscriptions:Netflix",
        "Personal:Entertainment:Paramount+": "Subscriptions:Paramount+",
        "Personal:Entertainment:Spotify": "Subscriptions:Spotify",
        "Personal:Subscriptions:Amazon Prime": "Subscriptions:Amazon Prime",
        "Personal:Subscriptions:Audible": "Subscriptions:Audible",
        "Personal:Subscriptions:Icloud": "Subscriptions:Icloud",
        "Personal:Subscriptions:Kindle Unlimited": "Subscriptions:Kindle Unlimited",
        "Personal:Subscriptions:Nintendo": "Subscriptions:Nintendo Online",
        "Personal:Subscriptions:Prime Video No Ads": "Subscriptions:Prime Video Ad Free",
        "Personal:Subscriptions:PSN": "Subscriptions:Playstation Network",
        "Personal:Travel:Lodging": "Travel:Lodging",
        "Salary:Paycheck": "Income:Salary",
        "Travel": "Travel:Misc",
    }

    TAG_FIXES = {
        "1-800-pet-meds": "petmeds.com",
        "1-800-petmeds": "petmeds.com",
        "1800petmeds": "petmeds.com",
        "2015-honda-fix-ex": "2015-honda-fit",
        "2016-hyundai-velster": "2016-hyundai-veloster",
        "2017-coachmen-catalina-sbx": "2017-coachmen-catalina",
        "2017-honda-civic": "2017-honda-civic-sport",
        "3dprinting": "3d-printing",
        "3ds": "nintendo-3ds",
        "5502": "5520-middleton-road",
        "5520": "5520 middleton road",
        "acro-bee": "acrobee",
        "akashi-sushi": "akashi",
        "alien": "aliens",
        "amazon": "amazon.com",
        "apple": "apple.com",
        "appstate": "appalachian-state-university",
        "art-book": "art-books",
        "asu": "appalachian-state-university",
        "atm-surcharge": "atm-fee",
        "audible": "audible.com",
        "backyard-birds-cards": "backyard-birds-and-gifts",
        "backyard-birds-gifts": "backyard-birds-and-gifts",
        "bangdood": "banggood",
        "battery": "batteries",
        "board-game": "board-games",
        "book": "books",
        "brantleys-restaurant": "village-restaurant",
        "brantleys-village-restaurant": "village-restaurant",
        "cape-lookup-ferry": "cape-lookout-ferry",
        "celo": "celo-inn",
        "cengage-learning-inc": "cengage-group",
        "cengage": "cengage-group",
        "chewy": "chewy.com",
        "chirstmas": "christmas",
        "cip-bonus": "caip-bonus",
        "civc": "2017-honda-civic-sport",
        "civic": "2017-honda-civic-sport",
        "coachmen": "2017 coachmen catalina",
        "cole": "cole-caroon",
        "conv.-fee": "fees",
        "cookout": "cook-out",
        "cougar": "cougar-caroon",
        "craft-supplies": "arts-crafts",
        "crafts": "arts-crafts",
        "crafty": "arts-crafts",
        "craig-yo-kai-watch": "yo-kai-watch",
        "dad": "tom-caroon",
        "delta-airlines": "delta-air-lines",
        "dermatologist": "dermatology",
        "duke-regional": "duke-regional-hospital",
        "duke-urgent-care": "urgent-care",
        "durham-city-county": "durham-county",
        "fee": "fees",
        "firetv": "fire-tv",
        "first-citizens": "first-citizens-bank",
        "flint-lock": "flintlock-campground",
        "flintlock": "flintlock-campground",
        "fujisan": "fujisan-japanese-steakhouse",
        "game": "games",
        "games-magazine": "games-world-of-puzzles",
        "geer-st.-garden": "geer-st-garden",
        "gog": "gog.com",
        "grandaddys-antiques": "granddaddys-antiques",
        "grandaddys": "granddaddys-antiques",
        "grow-light": "grow-lights",
        "haley": "haley-caroon",
        "inc": "2017-honda-civic-sport",
        "income-tax": "income-taxes",
        "international-pos-fee": "intl-pos-fee",
        "intl-purchase": "intl-pos-fee",
        "ios-app": "ios",
        "iphone-14": "iphone",
        "jimmys-famous-hotdogs": "jimmys-famous-hot-dogs",
        "jimmys": "jimmys-famous-hot-dogs",
        "kfc": "kentucky-fried-chicken",
        "kindle-fire-tablet": "kindle-fire",
        "lawn-mov-trim": "lawn-care",
        "lawnmower": "lawn-mower",
        "lei": "lei-home-enhancements",
        "linda": "linda-caroon",
        "macys": "macos",
        "mario": "mario-bros",
        "mason": "mason-caroon",
        "mayflower-restaurant": "mayflower-seafood",
        "michaelangos-pizza": "michaelangelos-pizza",
        "microsoft": "microsoft.com",
        "mika": "mika-torres",
        "moes-southwest-grile": "moes-southwest-grill",
        "moes": "moes-southwest-grill",
        "mom": "linda-caroon",
        "mosquito": "mosquitos",
        "mr.-cheesesteak": "mr-cheesesteak",
        "mr.-tire": "mr-tire",
        "mtg": "magic-the-gathering",
        "my-eye-dr": "myeyedr",
        "nate": "nathan",
        "natha": "nathan",
        "nathan-caroon": "nathan",
        "ncdmv": "dmv",
        "newbeedrone": "new-bee-drone",
        "ninth-street-baker": "ninth-street-bakery",
        "noodle-company": "noodles-company",
        "nwitch": "nswitch",
        "oriental-deli-subs": "oriental-deli",
        "paypaly-giving-fund": "paypal",
        "paypay": "paypal",
        "petmeds": "petmeds.com",
        "piggly-wiggle": "piggly-wiggly",
        "playstation-5": "ps5",
        "pnc": "pnc-bank",
        "pontaic-g6": "2009-pontiac-g6",
        "pontiac-g6": "2009-pontiac-g6",
        "pos-fee": "intl-pos-fee",
        "prednisone-5mg": "prednisone",
        "ps-vita": "playstation-vita",
        "quad": "quadcopters",
        "quadcopter": "quadcopters",
        "raven": "raven-caroon",
        "regional-anesthesia-pllc": "regional-anesthesia",
        "samsun": "samsung",
        "sansu": "sansui",
        "shelton-plumbing-co": "shelton-plumbing",
        "snack": "snacks",
        "southern-farm-bureau-life-insurance": "farm-bureau",
        "southern-fb-life-insurance": "farm-bureau",
        "special-fund": "special-offering",
        "stand-litore": "stant-litore",
        "stocking-stuffer": "stocking-stuffers",
        "stocking": "stocking-stuffers",
        "switch": "nswitch",
        "tax": "taxes",
        "termite-contract": "termite-plan",
        "thai-china": "thai-china-buffet",
        "tjmaxx": "tj-maxx",
        "tobacco-wood-brewing-company": "tobacco-wood-brewing",
        "tom": "tom-caroon",
        "turbotax": "turbotax.com",
        "ultrasound": "ultra-sound",
        "veloster": "2016-hyundai-veloster",
        "vitamin-d": "vitamins",
        "walmart": "wal-mart",
        "wasp-automotive": "wasp-auto",
        "wikimedia-foundation-inc": "wikimedia-foundation",
        "wikipedia": "wikimedia-foundation",
        "wikipedia": "wikimedia-foundation",
        "windows": "ms-windows",
        "windows10": "ms-windows",
        "wounded-warriors-project": "wounded-warrior-project",
        "yaris": "2007-toyota-yaris",
        "zip-car-wash": "zips-car-wash",
    }

    def __init__(self, old_db_path, **kwargs):
        self.__old_db_path = old_db_path
        self.__working_dir = kwargs.get("working_dir", "/tmp")

        file_name = os.path.basename(self.__old_db_path)
        self.__new_db_path = f"{self.__working_dir}/{file_name.capitalize()}.json"

        cwd = os.path.dirname(__file__)

        self.__config = Config.initialize(
            f"{cwd}/migration.yml", transient=["session"])
        self.__config.set("session:env", "prod")
        self.__config.set("session:docs_dir", self.__working_dir)
        self.__icon_search = IconSearch()

        if not self.__config.get("icons"):
            self.__config.set("icons", {})
        self.__icon_cache = self.__config.get("icons")

        if not self.__config.get("tags"):
            self.__config.set("tags", {})
        self.__tag_cache = self.__config.get("tags")


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

        # Start/End with non-word char => strip
        norm_name = re.sub(r"^\W+|\W+$", "", norm_name)
        # Strip Misc Char that don't want as space
        norm_name = re.sub(r"[']", "", norm_name)
        # Non-var chars => space
        norm_name = re.sub(r"[^a-zA-Z0-9_\-.]", " ", norm_name)
        # Spaces => '-'
        norm_name = re.sub(r"\s+", "-", norm_name)

        fixed_tag =self.TAG_FIXES.get(norm_name)
        if fixed_tag:
            norm_name = fixed_tag

        return norm_name


    def __note2tags(self, entry):
        cache_key = f"{entry['created_at']}|{entry['category']}|{entry['notes']}"
        tags = self.__tag_cache.get(cache_key, None)

        if tags is None:
            date = arrow.get(entry["created_at"])
            deleted = "Deleted" if entry.get("deleted_at") else "Active"
            print("#######################################################")
            print(f"# Note -> Tag: {entry['category']} | {entry['amount']} | {date.format('YYYY-MM-DD')} | {deleted}")
            print("#######################################################")
            print(f"\t=> {entry['notes']}")
            tag_str = ""
            while not tag_str:
                tag_str = input(f"Note2Tags> ")
                if tag_str == "Q":
                    raise RuntimeError("note2tag -- user exit")

                if tag_str:
                    if tag_str == "--":
                        tags = []
                    else:
                        tags = tag_str.split(",")

                        tags = [self.__normalize_tag(tg) for tg in tags]

            self.__tag_cache[cache_key] = tags

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
                        raise RuntimeError("find_icon -- user exit")
                    else:
                        choice = None
                        search_term = response

            self.__icon_cache[keyword] = choice

        return choice


    def __write_tags(self, tags:list[str]):
        # Update Tags DB
        for tg_name in tags:
            if not Tag.exists(tg_name):
                new_tg = Tag(name=tg_name)
                new_tg.save()


    def __cleanup_exit(self, msg, code=0):
        self.__config.save()
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
            try:
                print(f"Converting: {entry["_id"]} | {idx+1:04}/{num_recs:04}")
                self.__munge_expenses_fields(entry)
                self.__munge_budget_fields(entry)
                self.__munge_shared_fields(entry)

                new_records.append(entry)
            except Exception as err:
                # don't really care to much what error is here
                # just break so to write converted records, cache
                # and exit cleanly
                print(err)
                break

        print("\nData Conversion Complete!")

        # Sort the records on creation date
        new_records.sort(key=lambda entry: entry["created_at"])

        # Much faster for lots of records
        db.insert_multiple(new_records)

        self.__cleanup_exit(f"Migrated {len(new_records)} entries: {self.__new_db_path}")


    def __munge_shared_fields(self, entry):
        # delete _id
        del entry["_id"]

        # Standardize & Fix Categories
        entry["category"] = Budget.normalize_category(entry["category"])

        # Fix Categories
        if entry["category"] in self.CATEGORY_FIXES:
            entry["category"] = self.CATEGORY_FIXES.get(entry["category"])

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

            self.__write_tags(tags)


    def __munge_budget_fields(self, entry):
        if "history" in entry:
            for item in entry["history"]:
                item["date"] //= 1000

        if "firstDue" in entry:
            entry["first_due"] = entry["firstDue"]
            del entry["firstDue"]


    def __munge_expenses_fields(self, entry):
        # normalize tags
        if "tags" in entry:
            new_tags = []
            for tag in entry["tags"]:
                new_tags.append(self.__normalize_tag(tag))

            entry["tags"] = new_tags
            self.__write_tags(new_tags)


def main(args):
    migrator = DbMigrator(args.old_db_file, working_dir=args.working_dir)
    migrator.migrate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Migrate Old DB Format (NedDB) to New DB (TinyDb) format"
    )

    parser.add_argument("old_db_file", type=str)
    parser.add_argument("working_dir", type=str)

    args = parser.parse_args()
    main(args)
