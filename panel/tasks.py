from celery import shared_task
import requests

from panel.models import Publication, Group
from config import config


@shared_task
def remind(when):
    for group in Group.objects.all():
        need = False
        if when == 'day' and not group.day_report:
            need = True
            text = 'Напоминание! Нужно сделать дневной отчет'
        if when == 'evening' and not group.evening_report:
            need = True
            text = 'Напоминание! Нужно сделать вечерний отчет'

        if need:
            requests.post(
                url=f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage',
                data={
                    'chat_id': group.id,
                    'text': f'@{group.main_username}\n{text}'
                }
            )


@shared_task
def check_reports(when):
    is_good = True

    for group in Group.objects.all():
        need = False
        if when == 'day' and not group.day_report \
                or when == 'evening' and not group.evening_report:
            if is_good:
                requests.post(
                    url=f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage',
                    data={
                        'chat_id': config.TARGET_GROUP_ID,
                        'text': f'@{config.JOB_USERNAME}\n\nВ ходе {"дневного" if when == "day" else "вечернего"} контроля отчетов в чатах найма обнаружены нарушения:'
                    }
                )

                is_good = False

            requests.post(
                url=f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage',
                data={
                    'chat_id': config.TARGET_GROUP_ID,
                    'text': f'Группа: {group.name}\nОтветственный: @{group.main_username}'
                }
            )

        if when == 'day':
            group.day_report = False
        if when == 'evening':
            group.evening_report = False

        group.save()

    if is_good:
        requests.post(
            url=f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage',
            data={
                'chat_id': config.TARGET_GROUP_ID,
                'text': f'@{config.JOB_USERNAME}\n\nВ ходе {"дневного" if when == "day" else "вечернего"} контроля отчетов в чатах найма нарушения не обнаружены'
            }
        )


@shared_task
def send_publication(publication_id):
    publication = Publication.objects.get(id=publication_id)

    def send_mail(group_id):
        if not publication.file:
            requests.post(
                url=f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage',
                data={
                    'chat_id': group_id,
                    'text': publication.text
                }
            )
            return

        if not publication.file_id:
            with open(publication.file.path, 'rb') as f:
                response = requests.post(
                    url=f'https://api.telegram.org/bot{config.BOT_TOKEN}/send{publication.type.capitalize()}',
                    data={
                        'chat_id': group_id,
                        'caption': publication.text
                    },
                    files={publication.type: f}
                )

            if publication.type == 'photo':
                file_id = response.json()['result']['photo'][-1]['file_id']
            else:
                file_id = response.json()['result']['video']['file_id']

            publication.file_id = file_id
            publication.save()
            return

        requests.post(
            url=f'https://api.telegram.org/bot{config.BOT_TOKEN}/send{publication.type.capitalize()}',
            json={
                'chat_id': group_id,
                'caption': publication.text,
                publication.type: publication.file_id
            }
        )

    for group in Group.objects.all():
        send_mail(group.id)
