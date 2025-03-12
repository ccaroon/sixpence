from flet import Icons as FletIcons

import inflector

class IconSearch:
    IGNORE_WORDS = [
        "as", "do", "in", "of", "my", "then", "to", "a", "an", "and", "but",
        "for", "or", "the",
    ]

    # KNOWN-ICON-KW -> PERSONAL-KW
    KEYWORD_MAP = {
        "account_balance": ["bank", "loan"],
        "airplane_ticket": ["transportation"],
        "apartment": ["housing"],
        "audio": ["audible", "audiobook"],
        "bedroom_parent": ["furnishings"],
        "blender": ["appliance"],
        "car": ["auto", "automobile"],
        "card_membership": ["registration"],
        "cast_for_education": ["college", "university"],
        "church": ["tithes"],
        "clean_hands": ["haba"],
        "cloud": ["aws", "icloud"],
        "computer": ["software"],
        "connected_tv": ["acorntv", "britbox", "cbs", "disney+", "hulu", "paramount+", "netflix"],
        "currency_exchange": ["rollover"],
        "desk": ["office"],
        "direction_bike": ["recreation"],
        "double_arrow": ["transfer"],
        "electric_bolt": ["electricity"],
        "emoji_nature": ["garden", "gardening"],
        "fact_check": ["inspect", "inspection"],
        "fastfood": ["eating", "foodcourt"],
        "gamepad": ["nintendo", "playstation", "psn", "xbox"],
        "gas": ["fuel"],
        "giftcard": ["gift"],
        "home_repair_service": ["maintenance", "improvement"],
        "hotel": ["lodging"],
        "house": ["home", "mortgage"],
        "landscape": ["landscaping"],
        "medical_services": ["health"],
        "medication": ["medicine"],
        "memory": ["electronics"],
        "menu_book": ["book", "kindle"],
        "menu": ["misc"],
        "money_off": ["taxes"],
        "money": ["allowance", "cash", "charity"],
        "monitor_heart": ["life"],
        "music": ["spotify"],
        "nightlife": ["entertainment"],
        "payments": ["income", "salary"],
        "remove_red_eye": ["optometrist"],
        "shield": ["insurance"],
        "shipping": ["amazon", "fedex", "ups", "usps"],
        "shopify": ["clothes"],
        "signal_wifi": ["internet"],
        "water_drop": ["water", "water/sewer"],
    }


    def __init__(self, **kwargs):
        self.__icons = [icn.value for icn in list(FletIcons)]
        self.__inflect = inflector.Inflector()


    def smart_search(self, query, **kwargs):
        min_len = kwargs.get("min_len", 2)

        found_icons = set()
        words = query.split()

        # Expand and/or Filter Word List
        keywords = []
        for word in words:
            if len(word) >= min_len and word not in self.IGNORE_WORDS:
                singular = self.__inflect.singularize(word)
                plural = self.__inflect.pluralize(word)
                mapped_kw = []
                for icon_kw, personal_kws in self.KEYWORD_MAP.items():
                    if (
                        word in personal_kws or
                        singular in personal_kws or
                        plural in personal_kws
                    ):
                        mapped_kw.append(icon_kw)

                if mapped_kw:
                    keywords.extend(mapped_kw)
                else:
                    singular = self.__inflect.singularize(word)
                    plural = self.__inflect.pluralize(word)
                    keywords.extend(set([word, singular, plural]))

        # Find Icons base on each keyword
        for kw in keywords:
            icons = self.by_keyword(kw)
            found_icons.update(icons)

        return list(found_icons)


    def by_keyword(self, keyword, **kwargs):
        filter_variations = kwargs.get("filter_variations", True)

        matches = []
        for icn_name in self.__icons:
            # Don't include variations
            if filter_variations and icn_name.endswith(("_sharp", "_rounded")):
                continue

            if keyword == icn_name:
                matches.append(icn_name)

            if icn_name.startswith(f"{keyword}_"):
                matches.append(icn_name)

            if icn_name.endswith(f"_{keyword}"):
                matches.append(icn_name)

            if f"_{keyword}_" in icn_name:
                matches.append(icn_name)

        return matches


    def by_category(self, category):
        found_icons = []
        keywords = category.lower().split(":")
        # Assume more specific keywords at end of category string
        # Ex: Bills:Water | Personal:Books etc.
        keywords.reverse()

        for kw in keywords:
            icons = self.smart_search(kw)
            # Filter dupes, but keep ordered
            icons.sort()
            for icon in icons:
                if icon not in found_icons:
                    found_icons.append(icon)

        return found_icons
