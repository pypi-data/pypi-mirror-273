class WatchlistItem:
    """
    Represents an item in a watchlist.

    Attributes:
        symbol (str): The symbol of the item.
        id (str): The ID of the item.
    """

    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol")
        self.id = kwargs.get("id")


class Watchlist:
    """
    Represents a watchlist.

    Attributes:
        id (str): The ID of the watchlist.
        name (str): The name of the watchlist.
        public_id (str): The public ID of the watchlist.
        items (list): A list of WatchlistItem objects representing the items in the watchlist.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.public_id = kwargs.get("public_id")
        self.items = [
            WatchlistItem(**item) for item in kwargs.get("items", {}).get("item", [])
        ]
