from flet import Icons as FletIcons

import inflector

class IconSearch:
    IGNORE_WORDS = [
        "for", "the", "and"
    ]

    # TODO: reverse this mapping
    #  ICON -> keywords
    CATEGORY_MAP = {
        "acorntv": ["connected_tv"],
        "auto": ["car"],
        "bank": ["account_balance"],
        "britbox": ["connected_tv"],
        "cash": ["money", "currency"],
        "clothes": ["shopify"],
        "disney+": ["connected_tv"],
        "electricity": ["electric_bolt"],
        "fuel": ["gas"],
        "hulu": ["connected_tv"],
        "icloud": ["cloud"],
        "income": ["payment"],
        "inspect": ["fact_check"],
        "inspection": ["fact_check"],
        "lodging": ["hotel"],
        "netflix": ["connected_tv"],
        "nintendo": ["gamepad"],
        "paramount+": ["connected_tv"],
        "playstation": ["gamepad"],
        "psn": ["gamepad"],
        "salary": ["payment"],
        "spotify": ["music"],
        "tithes": ["church"],
        "xbox": ["gamepad"],
    }


    def __init__(self, **kwargs):
        self.__icons = [icn.value for icn in list(FletIcons)]
        self.__inflect = inflector.Inflector()


    def smart_search(self, query, **kwargs):
        min_len = kwargs.get("min_len", 3)

        found_icons = set()
        words = query.split()

        # Expand and/or Filter Word List
        all_words = []
        for word in words:
            if len(word) >= min_len and word not in self.IGNORE_WORDS:
                all_words.extend(self.CATEGORY_MAP.get(word, [word]))

        # Add plural form of all words
        keywords = []
        for word in all_words:
            keywords.append(word)
            plural = self.__inflect.pluralize(word)
            if plural != word:
                keywords.append(plural)

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
            for icon in icons:
                if icon not in found_icons:
                    found_icons.append(icon)

        return found_icons


    def interactive(self, keyword, **kwargs):
        hint = kwargs.get("hint", "N/A")
        icon_cache = kwargs.get("cache", {})
        choice = None

        cached_icon = icon_cache.get(keyword)
        if cached_icon:
            choice = cached_icon
        else:
            choice = None
            search_term = keyword
            while not choice:
                matches = self.smart_search(search_term)
                print(f"\n==> {hint} | {keyword.upper()} <==")
                for idx, icon in enumerate(matches):
                    print(f"{idx}) {icon}")

                response = input(f"Icon # | New Keyword> ")

                if response.isdigit():
                    idx = int(response)
                    choice = matches[idx]
                else:
                    choice = None
                    search_term = response

            icon_cache[keyword] = choice

        return choice
