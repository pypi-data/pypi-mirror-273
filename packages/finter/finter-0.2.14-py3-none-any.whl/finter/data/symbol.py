from finter.api import SymbolApi
from finter.settings import get_api_client


class Symbol:
    """
    A class to handle the conversion of financial symbols between different identifiers based on API responses.

    This class provides a method to convert financial symbol identifiers from one format to another using the SymbolApi.

    Methods:
        convert(_from: str, to: str, source: Union[str, list], date: Optional[str] = None, universe: Optional[int] = None) -> Optional[dict]:
            Converts financial symbols from one identifier format to another and handles potential errors during API calls.

    Attributes:
        _from (str): The source identifier type (e.g., 'id').
        to (str): The target identifier type (e.g., 'entity_name').
        source (Union[str, list]): The actual identifier(s) to be converted. Can be a single identifier or a list of identifiers.
        date (Optional[str]): The date for which the conversion is applicable (default is None, implying the current date).
        universe (Optional[int]): An optional parameter to specify the universe of the identifiers (default is None).
    """

    @classmethod
    def convert(cls, _from, to, source, date=None, universe=None):
        """
        Converts identifiers from one type to another using the SymbolApi service.

        Args:
            _from (str): The type of the source identifier.
            to (str): The type of the target identifier.
            source (Union[str, list]): The identifier or list of identifiers to convert.
            date (Optional[str]): The date for which the identifier conversion is relevant (not used in current implementation).
            universe (Optional[int]): The universe context for the conversion (not used in current implementation).

        Returns:
            Optional[dict]: A dictionary mapping the source identifiers to the converted identifiers, or None if the API call fails.

        Raises:
            Exception: Captures any exceptions raised during the API call, logs the error, and returns None.
        """
        if isinstance(
            source, list
        ):  # Check if the source is a list and convert it to a comma-separated string if true.
            source = ",".join(map(str, source))
        try:
            api_response = SymbolApi(get_api_client()).id_convert_retrieve(
                _from=_from, to=to, source=source
            )
            return api_response.code_mapped  # Return the mapping from the API response.
        except Exception as e:
            print(
                f"Symbol API call failed: {e}"
            )  # Log any exceptions encountered during the API call.
            return None
