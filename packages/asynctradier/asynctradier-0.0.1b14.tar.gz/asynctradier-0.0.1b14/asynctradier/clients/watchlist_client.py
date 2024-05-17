from typing import List

from asynctradier.common.watchlist import Watchlist
from asynctradier.utils.webutils import WebUtil


class WatchlistClient:
    """
    A client for interacting with the watchlist API.

    Args:
        session (WebUtil): The session object used for making HTTP requests.
        account_id (str): The ID of the account.
        token (str): The authentication token.
        sandbox (bool, optional): Whether to use the sandbox environment. Defaults to False.
    """

    def __init__(
        self, session: WebUtil, account_id: str, token: str, sandbox: bool = False
    ) -> None:
        self.session = session
        self.account_id = account_id
        self.token = token
        self.sandbox = sandbox

    async def get_watchlists(self) -> List[Watchlist]:
        """
        Get all watchlists for the account.

        Returns:
            List[Watchlist]: A list of Watchlist objects.
        """
        url = "/v1/watchlists"
        response = await self.session.get(url)
        watchlists = response.get("watchlists", {}).get("watchlist", [])
        return [Watchlist(**watchlist) for watchlist in watchlists]

    async def get_watchlist(self, watchlist_id: str) -> Watchlist:
        """
        Get a specific watchlist by ID.

        Args:
            watchlist_id (str): The ID of the watchlist.

        Returns:
            Watchlist: The Watchlist object.
        """
        url = f"/v1/watchlists/{watchlist_id}"
        response = await self.session.get(url)
        return Watchlist(**response.get("watchlist"))

    async def create_watchlist(self, name: str, symbols: List[str]) -> Watchlist:
        """
        Create a new watchlist.

        Args:
            name (str): The name of the watchlist.
            symbols (List[str]): A list of symbols to add to the watchlist.

        Returns:
            Watchlist: The Watchlist object.
        """
        url = "/v1/watchlists"
        data = {"name": name, "symbols": ",".join(symbols).upper()}
        response = await self.session.post(url, data=data)
        return Watchlist(**response.get("watchlist"))

    async def update_watchlist(
        self, watchlist_id: str, name: str, symbols: List[str]
    ) -> Watchlist:
        """
        Update an existing watchlist.

        Args:
            watchlist_id (str): The ID of the watchlist.
            name (str): The new name of the watchlist.
            symbols (List[str]): A list of symbols to add to the watchlist.

        Returns:
            Watchlist: The Watchlist object.
        """
        url = f"/v1/watchlists/{watchlist_id}"
        data = {"name": name, "symbols": ",".join(symbols).upper()}
        response = await self.session.put(url, data=data)
        return Watchlist(**response.get("watchlist"))

    async def delete_watchlist(self, watchlist_id: str) -> None:
        """
        Delete a watchlist by ID.

        Args:
            watchlist_id (str): The ID of the watchlist.
        """
        url = f"/v1/watchlists/{watchlist_id}"
        await self.session.delete(url)

    async def add_symbols_to_watchlist(
        self, watchlist_id: str, symbols: List[str]
    ) -> Watchlist:
        """
        Add symbols to an existing watchlist.

        Args:
            watchlist_id (str): The ID of the watchlist.
            symbols (List[str]): A list of symbols to add to the watchlist.

        Returns:
            Watchlist: The Watchlist object.
        """
        url = f"/v1/watchlists/{watchlist_id}/symbols"
        data = {"symbols": ",".join(symbols).upper()}
        response = await self.session.post(url, data=data)
        return Watchlist(**response.get("watchlist"))

    async def remove_symbol_from_watchlist(
        self, watchlist_id: str, symbol: str
    ) -> Watchlist:
        """
        Remove a symbol from an existing watchlist.

        Args:
            watchlist_id (str): The ID of the watchlist.
            symbol (str): The symbol to remove from the watchlist.

        Returns:
            Watchlist: The Watchlist object.
        """
        url = f"/v1/watchlists/{watchlist_id}/symbols/{symbol.upper()}"
        response = await self.session.delete(url)
        return Watchlist(**response.get("watchlist"))
