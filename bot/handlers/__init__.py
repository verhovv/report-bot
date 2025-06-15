from aiogram import Router, Bot
from aiogram.types import Message
from asgiref.sync import sync_to_async
from datetime import datetime
from django.utils import timezone

from panel.models import Group, Template, User
from aiogram.filters.command import CommandStart

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    await User.objects.aget_or_create(id=message.from_user.id, username=message.from_user.username)


@router.message()
async def on_message(message: Message, bot: Bot):
    group_ids = [group.id async for group in Group.objects.all()]

    if message.chat.id not in group_ids or \
            not message.text.startswith(f'@{(await bot.get_me()).username}'):
        return

    now = timezone.now()
    if now.hour < 12 or now.hour == 12 and now.minute <= 5:
        day = True
        template = await Template.objects.aget(name='Дневной отчет')
    else:
        day = False
        template = await Template.objects.aget(name='Вечерний отчет')

    fields = {field.name.lower(): field.type async for field in template.fields.all()}
    for line in message.text.splitlines():
        try:
            field_name, value = line.split(':')
            field_name = field_name.lower()
        except:
            continue

        value = value.replace(',', '.').strip()

        if field_name not in fields:
            continue

        field_type = fields[field_name]

        try:
            match field_type:
                case 'int':
                    int(value)
                case 'float':
                    float(value)
                case 'date':
                    datetime.strptime(value, '%d.%m.%Y')
        except:
            continue

        del fields[field_name]

    group = await Group.objects.aget(id=message.chat.id)
    group.tried = True
    await group.asave()

    if not fields:

        if day:
            group.day_report = True
        else:
            group.evening_report = True

        await group.asave()
        await message.reply(text='Отчет успешно принят')
        return

    text = f'Ошибки в следующих полях:\n{'\n'.join(fields)}\n\nПравильная форма отчета:\n'

    async for field in template.fields.all():
        match field.type:
            case 'int':
                text += f'{field.name}: 100 (Целое число)\n'
            case 'float':
                text += f'{field.name}: 100.52 (Дробное число)\n'
            case 'date':
                text += f'{field.name}: 05.11.2025 (Дата)\n'
            case 'str':
                text += f'{field.name}: текст\n'

    await message.reply(text=text)
