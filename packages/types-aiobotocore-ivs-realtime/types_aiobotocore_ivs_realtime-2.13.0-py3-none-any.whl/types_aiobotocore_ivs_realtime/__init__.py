"""
Main interface for ivs-realtime service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ivs_realtime import (
        Client,
        IvsrealtimeClient,
    )

    session = get_session()
    async with session.create_client("ivs-realtime") as client:
        client: IvsrealtimeClient
        ...

    ```
"""

from .client import IvsrealtimeClient

Client = IvsrealtimeClient

__all__ = ("Client", "IvsrealtimeClient")
