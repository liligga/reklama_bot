from bot import app


async def main():
    async with app:
        async for dialog in app.get_dialogs():
            if dialog.chat.type == 'group' or dialog.chat.type == 'supergroup':
                print(dialog.chat.title or dialog.chat.first_name, dialog.chat.id)


app.run(main())
