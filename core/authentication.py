from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from core.logger import get_logger
from core.security import verify_password
from database.connection import database


logger = get_logger("Authentication")


@dataclass(frozen=True)
class AuthenticationResult:
    """
    Result returned by the APS authentication service.
    """

    success: bool
    username: str
    user_id: int | None = None
    full_name: str | None = None
    role: str | None = None
    message: str = ""


class AuthenticationService:
    """
    Central authentication service for APS.

    Responsibilities:
    - Locate the requested user.
    - Verify the supplied password.
    - Confirm that the account is active.
    - Update the successful login timestamp.
    - Return authenticated user information.

    Session management is intentionally handled separately
    in APS-003C.
    """

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> AuthenticationResult:
        """
        Authenticate a user against the APS users table.
        """

        username = username.strip()

        if not username:
            return AuthenticationResult(
                success=False,
                username=username,
                message="Username is required.",
            )

        if not password:
            return AuthenticationResult(
                success=False,
                username=username,
                message="Password is required.",
            )

        try:
            with database.session() as connection:
                cursor = connection.execute(
                    """
                    SELECT
                        id,
                        username,
                        password_hash,
                        full_name,
                        role,
                        is_active
                    FROM users
                    WHERE username = ?
                    LIMIT 1
                    """,
                    (username,),
                )

                user = cursor.fetchone()

                if user is None:
                    logger.warning(
                        "Authentication failed: unknown username '%s'.",
                        username,
                    )

                    return AuthenticationResult(
                        success=False,
                        username=username,
                        message="Invalid username or password.",
                    )

                if not bool(user["is_active"]):
                    logger.warning(
                        "Authentication rejected: inactive account '%s'.",
                        username,
                    )

                    return AuthenticationResult(
                        success=False,
                        username=username,
                        user_id=user["id"],
                        full_name=user["full_name"],
                        role=user["role"],
                        message="User account is inactive.",
                    )

                if not verify_password(
                    password,
                    user["password_hash"],
                ):
                    logger.warning(
                        "Authentication failed: invalid password for '%s'.",
                        username,
                    )

                    return AuthenticationResult(
                        success=False,
                        username=username,
                        user_id=user["id"],
                        full_name=user["full_name"],
                        role=user["role"],
                        message="Invalid username or password.",
                    )

                login_time = datetime.now(timezone.utc).isoformat()

                connection.execute(
                    """
                    UPDATE users
                    SET last_login_at = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        login_time,
                        login_time,
                        user["id"],
                    ),
                )

                logger.info(
                    "User authenticated successfully: '%s'.",
                    username,
                )

                return AuthenticationResult(
                    success=True,
                    username=user["username"],
                    user_id=user["id"],
                    full_name=user["full_name"],
                    role=user["role"],
                    message="Authentication successful.",
                )

        except Exception:
            logger.exception(
                "Authentication service error for username '%s'.",
                username,
            )

            return AuthenticationResult(
                success=False,
                username=username,
                message="Authentication service error.",
            )


authentication_service = AuthenticationService()