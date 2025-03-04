from abc import abstractmethod


class Notification:
    @abstractmethod
    async def notify(self, user_id: str, message: str) -> None:
        pass
