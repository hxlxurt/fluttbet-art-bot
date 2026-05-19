from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from keyboards import get_socials_keyboard, get_pricelist, get_contacts, get_collab, main, back, tradecollab

import keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message:Message):

    photo = FSInputFile('fluttbetstart.jpg')

    await message.answer_photo(
        photo=photo,
        caption=
        '⋆˚࿔ Для продолжения, пожалуйста, выберите команду из списка меню (˵ •̀ ᴗ - ˵) ✧',
    reply_markup=kb.main)


class FormArt(StatesGroup):
    name = State()
    contact = State()
    tip = State()
    description = State()
    reference = State()
    dop = State()

class Trade(StatesGroup):
    nickname = State()
    link = State()
    tip4ik = State()
    idea = State()

class dm(StatesGroup):
    text = State()


@router.callback_query(F.data == 'trade_type_trade')
async def trade_type_trade(callback: CallbackQuery, state: FSMContext):

    await state.update_data(tip4ik="Трейд")
    await state.set_state(Trade.idea)

    await callback.message.edit_text("⋆˚࿔ Вы выбрали: Трейд")

    await callback.message.answer("⋆˚࿔ Опишите вашу идею")

    await callback.answer()

@router.callback_query(F.data == 'trade_type_collab')
async def trade_type_collab(callback: CallbackQuery, state: FSMContext):

    await state.update_data(tip4ik="Коллаб")
    await state.set_state(Trade.idea)

    await callback.message.edit_text("⋆˚࿔ Вы выбрали: Коллаб")

    await callback.message.answer("⋆˚࿔ Опишите вашу идею")

    await callback.answer()



@router.message(F.text == '･: * Соц-сети * :･')
async def socials_handler(message: Message):
    await message.answer(
    '⋆˚࿔  Соц-сети и работы автора\n'
    'Чтобы перейти по ссылке, нажмите на одну из кнопок ниже:',
    reply_markup=get_socials_keyboard()
)

@router.message(F.text == '･: * Заказать арт * :･')
async def start_art_form(message: Message, state: FSMContext):
    await state.set_state(FormArt.name)
    await message.answer(
'⋆˚࿔ Давайте вместе оформим заказ на арт ৻(  •̀ ᗜ •́  ৻) \n'
'Пожалуйста, введите Ваше имя или ник',
    reply_markup=kb.back
)


@router.message(F.text == '･: * Написать сообщение * :･')
async def start_dm_form(message: Message, state: FSMContext):
    await state.set_state(dm.text)
    await message.answer(
'⋆˚࿔ Хотите, чтобы я передал важное сообщение автору (｡· o ·｡) ?\n'
'Нет проблем — пишите здесь всё, что пожелаете, а я мигом отправлю это в ЛС Fluttbet! Не забудьте указать свой тег telegram (@username), если Вы хотите, чтобы с Вами связались ♡', reply_markup=kb.back)


@router.message(F.text == '･: * Трейд/Коллаб * :･')
async def start_trade_form(message: Message, state: FSMContext):
    await state.set_state(Trade.nickname)
    await message.answer('⋆˚࿔ Укажите свой тег telegram (@username) и имя/ник', reply_markup=kb.back)

@router.message(Command('artform'))
async def art_one(message: Message, state:FSMContext):
    await state.set_state(FormArt.name)
    await message.answer('Введите ваше имя или ник', reply_markup=kb.back)

@router.message(FormArt.name)
async def art_two(message: Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormArt.contact)
    await message.answer("⋆˚࿔ Укажите свой тег telegram (@username)")


@router.message(FormArt.contact)
async def art_three(message: Message, state:FSMContext):
    await state.update_data(contacts=message.text)
    await state.set_state(FormArt.tip)
    await message.answer(
        "⋆˚࿔ Какой тип заказа Вас интересует (портрет / полный рост / адопт / другое)?"
    )


@router.message(FormArt.tip)
async def art_four(message: Message, state:FSMContext):
    await state.update_data(tip=message.text)

    # СНАЧАЛА РЕФЕРЕНСЫ
    await state.set_state(FormArt.reference)

    await message.answer(
        "⋆˚࿔ Пожалуйста, приложите референсы персонажа(ей) "
        "в формате фото, файла или ссылки"
    )


@router.message(FormArt.reference)
async def art_five(message: Message, state: FSMContext):

    if message.text:
        await state.update_data(reference={'type': 'text', 'data': message.text})

    elif message.photo:
        await state.update_data(reference={'type': 'photo', 'data': message.photo[-1].file_id})

    elif message.document:
        await state.update_data(reference={'type': 'document', 'data': message.document.file_id})

    else:
        await message.answer("Пожалуйста, отправьте ссылку, фото или файл 🖼️")
        return

    # ПОТОМ ОПИСАНИЕ
    await state.set_state(FormArt.description)

    await message.answer(
        "⋆˚࿔ Пожалуйста, опишите идею вашего заказа "
        "или оставьте ''-'', если Вы хотите дать полную свободу автору"
    )


@router.message(FormArt.description)
async def art_six(message: Message, state:FSMContext):
    await state.update_data(description=message.text)

    await state.set_state(FormArt.dop)

    await message.answer(
        "⋆˚࿔ Если у Вас есть вопросы, дополнительная информация о заказе/персонажах "
        "или любая другая важная информация — можете оставить её здесь.\n\n"
    )


@router.message(FormArt.dop)
async def art_final(message: Message, state: FSMContext):
    await state.update_data(dop=message.text)

    data = await state.get_data()

    msg = (
        f"Новая заявка на арт:\n"
        f"Имя/ник: {data['name']}\n"
        f"Контакт: {data['contacts']}\n"
        f"Тип заказа: {data['tip']}\n"
        f"Описание: {data['description']}\n"
        f"Доп: {data['dop']}"
    )

    YOUR_ID = 1038611552

    ref = data.get('reference')

    if ref['type'] == 'text':
        await message.bot.send_message(
            chat_id=YOUR_ID,
            text=f"{msg}\nРеференс: {ref['data']}"
        )

    elif ref['type'] == 'photo':
        await message.bot.send_photo(
            chat_id=YOUR_ID,
            photo=ref['data'],
            caption=msg
        )

    elif ref['type'] == 'document':
        await message.bot.send_document(
            chat_id=YOUR_ID,
            document=ref['data'],
            caption=msg
        )

    await state.clear()

    await message.answer(
        '⋆˚࿔ Я отправил Вашу заявку автору (˶>⩊<˶)\n'
        'Fluttbet обязательно свяжется с Вами в ближайшее время!',
    reply_markup=kb.main
)

@router.message(Command('trade'))
async def trade_one(message: Message, state:FSMContext):
    await state.set_state(Trade.nickname)
    await message.answer('⋆˚࿔ Давайте вместе оформим оформим форму для трейда или коллабы ৻(  •̀ ᗜ •́  ৻)\n'
                        '⋆˚࿔ Укажите свой тег telegram (@username) и имя/ник', reply_markup=kb.back)

@router.message(Trade.nickname)
async def trade_second(message: Message, state:FSMContext):
    await state.update_data(nickname = message.text)
    await state.set_state(Trade.link)
    await message.answer("⋆˚࿔ Пожалуйста, отправьте ссылку на Ваши работы")

@router.message(Trade.link)
async def trade_three(message: Message, state:FSMContext):
    await state.update_data(link=message.text)

    await state.set_state(Trade.tip4ik)

    await message.answer(
        "⋆˚࿔ Обязательно укажите тип работы:",
        reply_markup=tradecollab
    )

@router.callback_query(Trade.tip4ik)
async def trade_type_choose(callback: CallbackQuery, state: FSMContext):

    if callback.data == "trade_type_trade":
        selected_type = "Трейд"

    elif callback.data == "trade_type_collab":
        selected_type = "Коллаб"

    else:
        return

    await state.update_data(tip4ik=selected_type)

    await callback.message.edit_text(
        f"⋆˚࿔ Вы выбрали: {selected_type}"
    )

    # следующий state
    await state.set_state(Trade.idea)

    await callback.message.answer(
        "⋆˚࿔ Опишите вашу идею"
    )

    await callback.answer()

@router.message(Trade.idea)
async def trade_final(message: Message, state: FSMContext):
    await state.update_data(idea=message.text)


    data = await state.get_data()

    msg = (
        f"Новый трейд/коллаб:\n"
        f"Ник: {data['nickname']}\n"
        f"Ссылка на работы: {data['link']}\n"
        f"Тип: {data['tip4ik']}\n"
        f"Идея: {data['idea']}"
    )

    YOUR_ID = 1038611552

    await message.bot.send_message(chat_id=YOUR_ID, text=msg)

    await state.clear()

    await message.answer(
   '⋆˚࿔ Я отправил Вашу заявку автору (˶>⩊<˶)\n'
    'Fluttbet обязательно свяжется с Вами в ближайшее время!',
    reply_markup=kb.main
)

@router.message(Command('dm'))
async def dm_one(message:Message, state:FSMContext):
    await state.set_state(dm.text)
    await message.answer('⋆˚࿔ Хотите, чтобы я передал важное сообщение автору (｡· o ·｡) ?\n'
'Нет проблем — пишите здесь всё, что пожелаете, а я мигом отправлю это в ЛС Fluttbet! Не забудьте указать свой тег telegram (@username), если Вы хотите, чтобы с Вами связались ♡', reply_markup=kb.back)

@router.message(Command('socials'))
async def cmd_contacts(message:Message): 
    await message.answer('･: * Соц-сети * :･', reply_markup=get_socials_keyboard())

@router.message(dm.text)
async def dm_two(message: Message, state: FSMContext):
    YOUR_ID = 1038611552

    await message.copy_to(chat_id=YOUR_ID)

    await state.clear()

    await message.answer(
        '⋆˚࿔ Спасибо! Я отправил Ваше сообщение автору (੭„• ֊ •„)੭ ⸝♡',
        reply_markup=kb.main
)

@router.message(Command('cancel'))
async def cmd_cancel(message:Message, state: FSMContext):
    await state.clear()
    await message.answer("⋆˚࿔ Вы вернулись в главное меню ( ദ്ദി˶ᵔ ᗜ ᵔ˶)\n" \
    "Для продолжения, пожалуйста, выберите команду из списка",
    reply_markup=kb.main
)


@router.callback_query(F.data == 'back')
async def cmd_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.answer(
    "⋆˚࿔ Вы вернулись в главное меню ( ദ്ദി˶ᵔ ᗜ ᵔ˶)\n" \
    "Для продолжения, пожалуйста, выберите команду из списка",
    reply_markup=kb.main)