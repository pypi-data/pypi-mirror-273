from typing import Any

from example.conf import sdk


@sdk.socket.on('message')
def handle_message(data: Any) -> None:
    print('received message: ')
    print(data)
