from flet import Icons as FletIcons

import inflector

class IconSearch:

    CATEGORY_MAP = {
        "auto": ["car"],
        "cash": ["money", "currency"],
        "income": ["payment", "paymentss"], # ss => Trick inflector :(
        "salary": ["payment", "paymentss"]  # ss => Trick inflector :(
    }


    def __init__(self, **kwargs):
        self.__icons = [icn.value for icn in list(FletIcons)]
        self.__icon_map = kwargs.get("icon_map", {})
        self.__inflect = inflector.Inflector()


    @property
    def icon_map(self):
        return self.__icon_map


    def by_keyword(self, keyword, **kwargs):
        keyword = self.__inflect.singularize(keyword)
        filter_variations = kwargs.get("filter_variations", True)

        matches = []
        for icn_name in self.__icons:
            # Don't add variations
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
        keywords = category.lower().split(":")
        # Assume more specific keywords at end of category string
        # Ex: Bills:Water | Personal:Books etc.
        keywords.reverse()

        found_icons = []

        cat_kws = []
        for kw in keywords:
            cat_kws.extend(self.CATEGORY_MAP.get(kw, [kw]))

        for kw in cat_kws:
            icons = self.by_keyword(kw)
            # Filter dups, but keep ordered
            for icon in icons:
                if icon not in found_icons:
                    found_icons.append(icon)

        return found_icons


    def interactive(self, keyword, **kwargs):
        hint = kwargs.get("hint", "N/A")
        choice = None

        cached_icon = self.__icon_map.get(keyword)
        if cached_icon:
            choice = cached_icon
        else:
            choice = None
            search_term = keyword
            while not choice:
                matches = self.search(search_term)
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

            self.__icon_map[keyword] = choice


        return choice
