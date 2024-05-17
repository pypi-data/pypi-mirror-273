from _typeshed import Incomplete
from datetime import datetime
from sentry_sdk.integrations import Integration
from tlc.core.utils.track_project_metadata import compute_project_usage_metadata as compute_project_usage_metadata, get_project_usage_metadata as get_project_usage_metadata
from typing import Any

class JupyterExcepthookIntegration(Integration):
    """Hook into Jupyter's excepthook to capture unhandled exceptions so that they get reported to Sentry."""
    identifier: str
    @staticmethod
    def setup_once() -> None: ...

class Telemetry:
    """Telemetry class for 3LC.

    This class is responsible for initializing the telemetry system for 3LC.
    """
    telemetry_instance: Telemetry | None
    def __init__(self) -> None:
        """Initialize the telemetry system."""
    @staticmethod
    def instance() -> Telemetry:
        """Get the telemetry instance."""
    @staticmethod
    def try_derive_user_id(event: dict | None) -> None: ...
    @staticmethod
    def consider_scrub_url(url: str) -> str:
        """Remove sensitive information from the URL."""
    @staticmethod
    def scrub_urls(event: dict | None) -> dict | None: ...
    @staticmethod
    def filter_urls(event: dict | None) -> dict | None: ...
    @staticmethod
    def before_send_transaction(event: dict | None, hint: dict) -> dict | None:
        """Remove sensitive information from the URL."""
    @staticmethod
    def before_send(event: dict[str, Any], hint: dict[str, Any]) -> dict[str, Any] | None:
        """Filter out exceptions that should not be sent to Sentry.

        These are:

        1. HTTPException, PermissionDeniedException as these are handled errors in Starlite.

        2. Exceptions that do not include tlc in the stacktrace. E.g. if the users has imported tlc in a notebook and
           triggers unrelated errors.

        3. Some critical log messages we know happen during testing.
        """
    @staticmethod
    def get_sentry_environment() -> str:
        '''Get the Sentry environment.

        This method uses various heuristics to determine the environment in which the code is running.

        1. If the TLC_SENTRY_ENVIRONMENT environment variable is set, it will take precedence over the other logic.
        2. If the tlc module is installed from a wheel, the environment will be set to "production".
        3. If neither of these are set, we will assume that we are running from a development environment.

        :returns: The Sentry environment. By convention this will be one of "production", "testing", "staging", or
            "development".
        '''
    @staticmethod
    def get_sentry_dashboard_config() -> dict: ...

class RunningMessage:
    start_time: Incomplete
    trigger_time: Incomplete
    def __init__(self, start_time: datetime) -> None: ...
    async def consider_message(self) -> None: ...
