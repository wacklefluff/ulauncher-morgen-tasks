"""
Morgen API Client

Handles all communication with the Morgen API v3.
Uses urllib.request (stdlib) to avoid external dependencies.
"""

import json
import logging
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)


# --- Exceptions ---

class MorgenAPIError(Exception):
    """Base exception for Morgen API errors."""

    def __init__(self, message, status_code=None, response_body=None):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)


class MorgenAuthError(MorgenAPIError):
    """Authentication failed (401) - invalid API key."""
    pass


class MorgenRateLimitError(MorgenAPIError):
    """Rate limit exceeded (429)."""
    pass


class MorgenValidationError(MorgenAPIError):
    """Invalid request parameters (400)."""
    pass


class MorgenNetworkError(MorgenAPIError):
    """Network connectivity issues (timeout, DNS, connection refused)."""
    pass


# --- Client ---

class MorgenAPIClient:
    """Client for the Morgen API v3."""

    BASE_URL = "https://api.morgen.so/v3"

    def __init__(self, api_key):
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty")
        self.api_key = api_key.strip()
        self.timeout = 10  # seconds

    def _make_request(self, endpoint, method="GET", data=None):
        """
        Make an HTTP request to the Morgen API.

        Returns the parsed JSON response dict.
        Raises MorgenAPIError subclasses on failure.
        """
        url = f"{self.BASE_URL}{endpoint}"

        headers = {
            "Authorization": f"ApiKey {self.api_key}",
            "Accept": "application/json",
        }

        body = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))

        except urllib.error.HTTPError as e:
            error_body = None
            try:
                error_body = e.read().decode("utf-8")
            except Exception:
                pass

            if e.code == 401:
                raise MorgenAuthError(
                    "Invalid API key. Check your Morgen API key in preferences.",
                    status_code=401,
                    response_body=error_body,
                )
            elif e.code == 429:
                raise MorgenRateLimitError(
                    "Rate limit exceeded. Try again later.",
                    status_code=429,
                    response_body=error_body,
                )
            elif e.code == 400:
                raise MorgenValidationError(
                    f"Bad request: {error_body or 'invalid parameters'}",
                    status_code=400,
                    response_body=error_body,
                )
            else:
                raise MorgenAPIError(
                    f"API error ({e.code}): {error_body or e.reason}",
                    status_code=e.code,
                    response_body=error_body,
                )

        except urllib.error.URLError as e:
            raise MorgenNetworkError(
                f"Cannot reach Morgen API: {e.reason}",
            )

        except json.JSONDecodeError as e:
            raise MorgenAPIError(f"Invalid JSON response from API: {e}")

    def list_tasks(self, limit=100, updated_after=None):
        """
        List tasks from Morgen.

        WARNING: Costs 10 API points per call. Use caching!

        Args:
            limit: Max tasks to return (max 100).
            updated_after: ISO datetime string to fetch only newer tasks.

        Returns:
            Dict: {"data": {"tasks": [...], "labelDefs": [...], "spaces": [...]}}
        """
        params = f"?limit={min(limit, 100)}"
        if updated_after:
            params += f"&updatedAfter={updated_after}"

        logger.info("Fetching tasks from Morgen API (limit=%d)", limit)
        response = self._make_request(f"/tasks/list{params}")

        task_count = len(response.get("data", {}).get("tasks", []))
        logger.info("Retrieved %d tasks from API", task_count)

        return response

    def create_task(self, title, description=None, due=None, time_zone=None, priority=0):
        """
        Create a new task in Morgen.

        Args:
            title: Task title (required, min 1 char).
            description: Optional description.
            due: Due date as YYYY-MM-DDTHH:mm:ss (exactly 19 chars, no tz suffix).
            time_zone: IANA timezone string (e.g. "Europe/Berlin").
            priority: 0 (undefined) through 9 (lowest). 1 = highest.

        Returns:
            Dict: {"data": {"id": "..."}}
        """
        if not title or not title.strip():
            raise ValueError("Task title is required")

        if not 0 <= priority <= 9:
            raise ValueError("Priority must be between 0 and 9")

        if due:
            if len(due) != 19:
                raise ValueError(
                    f"Due date must be exactly 19 characters (YYYY-MM-DDTHH:mm:ss), got {len(due)}: {due}"
                )
            if due[4] != "-" or due[7] != "-" or due[10] != "T" or due[13] != ":" or due[16] != ":":
                raise ValueError(f"Invalid due date format, expected YYYY-MM-DDTHH:mm:ss: {due}")

        body = {"title": title.strip(), "priority": priority}

        if description:
            body["description"] = description
        if due:
            body["due"] = due
            if time_zone:
                body["timeZone"] = time_zone

        logger.info("Creating task: %s", title)
        response = self._make_request("/tasks/create", method="POST", data=body)

        task_id = response.get("data", {}).get("id")
        logger.info("Task created: %s", task_id)

        return response
