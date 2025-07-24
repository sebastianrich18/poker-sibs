import bcrypt


class HashingService:
    """
    Service for hashing operations using bcrypt.
    """

    @staticmethod
    def hash(password: str) -> str:
        """
        Hashes the given password using bcrypt with salt.
        """
        # Generate salt and hash password
        salt = bcrypt.gensalt(
            rounds=12
        )  # 12 rounds = good balance of security/performance
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify(stored_hash: str, provided_password: str) -> bool:
        """
        Verifies a provided password against a stored bcrypt hash.
        """
        return bcrypt.checkpw(
            provided_password.encode("utf-8"), stored_hash.encode("utf-8")
        )
