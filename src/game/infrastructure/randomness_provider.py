from abc import ABC


class IRandomnessProvider(ABC):
    async def get_random_bytes(self, n: int) -> bytes:
        """Get n random bytes"""
        pass


class LocalRandomnessProvider(IRandomnessProvider):
    async def get_random_bytes(self, n: int) -> bytes:
        pass


class RandomDotOrgProvider(IRandomnessProvider):
    async def get_random_bytes(self, n: int) -> bytes:
        pass
