from src.notification import Notification


class ConsoleNotification(Notification):
    def __init__(self):
        """
        Can be used to initialize any client or connection
        """
        pass

    async def notify(self, user_id: str, message: str) -> None:
        print(f"User {user_id}: {message}")
