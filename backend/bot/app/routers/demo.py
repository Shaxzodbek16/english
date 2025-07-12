from aiogram import Router, F

demo_router = Router()


@demo_router.message(F.text == "demo")
async def handle_demo(message):
    await message.answer(
        "This is a demo response. You can customize this message as needed."
    )
