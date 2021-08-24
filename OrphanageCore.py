# Импорт модулей вк
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# Импорт библиотек
import threading
import random

from tokes import main_token  # Токен группы

# Импорт сущност
from Noah import Noah_Ai

# Phrases
from Phrases import recieve_pattern


# Авторизация
vk_session = vk_api.VkApi(token=main_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Переменные
Current_unit = 'Ной'
Admin_id = int(258124709)  # Айдишник Создателя.


# Фукнциональный класс

class communicate:
    def reciever(self):  # TODO Будет использоваться для отправки сообщений в приложении
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    msg = event.text.lower()
                    id = event.user_id
                    return {'msg': msg, 'user': id}

    def text_send(self, id, text):  # Текстовое сообщение
        vk_session.method('messages.send', {
            'user_id': id, 'message': text, 'random_id': 0
        })

    def img_send(self, id, img):  # Фото отравка
        vk_session.method('messages.send',
                          {
                              'user_id': id,
                              'attachment': img,
                              'random_id': 0
                          })


comm = communicate()
"""
Крч надо реализовать смену ядра, так что все содержимое ядра скорее всего перенсется в файл ноя
А значит надо делать консольный выбор перса, хотя в идеале сделать чтобы был определенный стандарт,
т.е всегда начиналось с ноя, а потом уже свитч, впринципе можно сделать изначальный вызов файла Ноя
а потом уже других ботов, надо будет тогда с импортами разобраться, и ваще как бы страх перестрах как бы.
Скорее всего некоторые переменные из Phrases, перенесу в кор файл Ноя. А сейчас утал
Впринципе механизм распознавания сообщений и отправки хорош, мне не надо делать триллард If elif,
Так что ваще заебок.
"""


class OrphanageCore(Noah_Ai):
    def __init__(self):
        super().__init__()

        print(
            'Приют запущен. \n Активное Ядро - {Unit} '.format(Unit=Current_unit))

        comm.text_send(Admin_id, 'Снова ты. Ладно, присаживайся в гостевой.')
        threading.Thread(target=self.say()).start()

    def say(self):

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    msg = event.text.lower()
                    id = event.user_id
                    """
                    if id == Admin_id:
                        try:
                            eval(msg)
                        except:
                            print('Введенная команда корявая')
                    else:
                        pass
                    """
                    # Необязательный блок для получения имени
                    user_get = vk_session.method('users.get', {'user_ids': id})
                    user_getb = user_get[0]
                    first_name = user_getb['first_name']
                    last_name = user_getb['last_name']
                    full_name = first_name + " " + last_name
                    print('Получено сообщение "{msg}" от {name} ( id = {user})'.format(
                        user=id, name=full_name, msg=msg))

                    for pattern in recieve_pattern:

                        if msg in pattern.keys():
                            block = pattern[msg]
                            respond = random.choice(block)
                            comm.text_send(id, respond)

                            print('{Unit} отправил - "{answer}", в ответ на "{msg}"'.format(
                                Unit=Current_unit, answer=respond, msg=msg))


OrpCore = OrphanageCore()


if __name__ == '__main__':
    OrpCore
