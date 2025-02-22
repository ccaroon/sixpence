from flet import Icons as FletIcons


class IconSearch:
    def __init__(self, **kwargs):
        self.__icons = [icn.value for icn in list(FletIcons)]
        self.__icon_map = kwargs.get("icon_map", {})


    @property
    def icon_map(self):
        return self.__icon_map


    def search(self, keyword):
        # once found, cache?
        # ends with: _car
        # starts with : car_
        # contains: _car_

        matches = []
        for icn_name in self.__icons:
            if keyword == icn_name:
                matches.append(icn_name)

            if icn_name.startswith(f"{keyword}_"):
                matches.append(icn_name)

            if icn_name.endswith(f"_{keyword}"):
                matches.append(icn_name)

            if f"_{keyword}_" in icn_name:
                matches.append(icn_name)

        return matches


    def interactive_search(self, keyword, **kwargs):
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
