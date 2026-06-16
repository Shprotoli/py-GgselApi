from typing import Union

from requests import Response

from schemas.ggsel_object import GgselGlobalObject
from schemas.error_response_object import ErrorResponseObject

ApiResult = Union[GgselGlobalObject, ErrorResponseObject, Response]


def handler_response_api(type_wrapper: GgselGlobalObject | None, data: Response | dict | list
                         ) -> ApiResult:
    """
    Universal API response handler.

    This function processes data returned from the API (Response, dict, or list)
    and attempts to wrap it into a domain object (`ggsel_object`) using the provided
    `type_wrapper`.

    If wrapping is not possible, the function returns the raw `Response` object.

    If a TypeError occurs during object construction, an `ErrorResponseObject`
    is returned instead.

    Behavior:
        - list     → type_wrapper(data)
        - dict     → type_wrapper(**data)
        - Response → returned unchanged
        - TypeError → ErrorResponseObject(**data)

    :param type_wrapper:
        A domain model class used to deserialize API response data.
        If None, no wrapping should be performed.

    :param data:
        Raw API response data. Possible types:
        - Response: raw HTTP response object
        - dict: parsed JSON object
        - list: parsed JSON array

    :return:
        - Instance of `type_wrapper` if deserialization succeeds
        - `ErrorResponseObject` if an error occurs during deserialization
        - `Response` if the input is already a raw HTTP response
    """
    try:
        """
        Pattern-based dispatch of API response data.

        This block determines how raw API response data should be interpreted
        and converted into a domain model.

        Matching rules:
            - list     → passed as a positional constructor argument
            - dict     → unpacked as keyword arguments (**data)
            - Response → returned as-is (raw HTTP response, no wrapping)

        This logic assumes that `type_wrapper` is a callable model class
        that can deserialize structured API data into a domain object.
        """
        match data:
            case list():
                return type_wrapper(data)
            case dict():
                return type_wrapper(**data)
            case Response():
                return data
    except TypeError:
        return ErrorResponseObject(**data)
