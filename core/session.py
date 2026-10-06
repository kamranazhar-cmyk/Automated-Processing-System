from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from core.logger import get_logger


logger = get_logger("Session")


@dataclass(frozen=True)
class SessionUser:
    """
    Immutable identity information for the currently
    authenticated APS user.
    """

    user_id: int
    username: str
    full_name: str
    role: str
    login_time: datetime


class UserSession:
    """
    Runtime session manager for the APS application.

    The session does not authenticate users itself.

    Authentication is performed by AuthenticationService.
    This class stores the identity returned after successful
    authentication and provides controlled access to it.
    """

    def __init__(self) -> None:
        self._user: SessionUser | None = None

    @property
    def is_authenticated(self) -> bool:
        """
        Return True when a user is currently authenticated.
        """

        return self._user is not None

    @property
    def user(self) -> SessionUser | None:
        """
        Return the current authenticated user.

        Returns None when no user is logged in.
        """

        return self._user

    @property
    def user_id(self) -> int | None:
        """
        Return the current user's database ID.
        """

        return (
            self._user.user_id
            if self._user is not None
            else None
        )

    @property
    def username(self) -> str | None:
        """
        Return the current username.
        """

        return (
            self._user.username
            if self._user is not None
            else None
        )

    @property
    def full_name(self) -> str | None:
        """
        Return the current user's full name.
        """

        return (
            self._user.full_name
            if self._user is not None
            else None
        )

    @property
    def role(self) -> str | None:
        """
        Return the current user's role.
        """

        return (
            self._user.role
            if self._user is not None
            else None
        )

    @property
    def login_time(self) -> datetime | None:
        """
        Return the current session login time.
        """

        return (
            self._user.login_time
            if self._user is not None
            else None
        )

    def start(
        self,
        user_id: int,
        username: str,
        full_name: str,
        role: str,
    ) -> SessionUser:
        """
        Start a new authenticated session.

        A session cannot be silently overwritten. If another
        user is already authenticated, the existing session
        must first be cleared.
        """

        if self.is_authenticated:
            raise RuntimeError(
                "An authenticated session already exists."
            )

        if user_id <= 0:
            raise ValueError(
                "User ID must be a positive integer."
            )

        username = username.strip()
        full_name = full_name.strip()
        role = role.strip()

        if not username:
            raise ValueError(
                "Username cannot be empty."
            )

        if not full_name:
            raise ValueError(
                "Full name cannot be empty."
            )

        if not role:
            raise ValueError(
                "Role cannot be empty."
            )

        authenticated_user = SessionUser(
            user_id=user_id,
            username=username,
            full_name=full_name,
            role=role,
            login_time=datetime.now(timezone.utc),
        )

        self._user = authenticated_user

        logger.info(
            "User session started: '%s' (user_id=%s, role=%s).",
            username,
            user_id,
            role,
        )

        return authenticated_user

    def clear(self) -> None:
        """
        End the current authenticated session.
        """

        if self._user is None:
            return

        username = self._user.username

        self._user = None

        logger.info(
            "User session ended: '%s'.",
            username,
        )

    def require_authentication(self) -> SessionUser:
        """
        Return the authenticated user or raise an error
        when no authenticated session exists.
        """

        if self._user is None:
            raise PermissionError(
                "Authentication is required."
            )

        return self._user


session = UserSession()