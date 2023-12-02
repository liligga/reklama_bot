from bot import app
from pyrogram.enums import ChatType
import logging


async def main():
    async with app:
        async for dialog in app.get_dialogs():
            if dialog.chat.type == ChatType.GROUP or dialog.chat.type == ChatType.SUPERGROUP:
                print(dialog.chat.title or dialog.chat.first_name, dialog.chat.id)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(main())
