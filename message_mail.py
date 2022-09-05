import rpa as r
from conf import conf


def main():
    r.init()
    r.url('https://www.google.com/intl/ru/gmail/about/')  # открыть gmail
    r.click('//*[@data-action="sign in"]')
    if r.read('//*[@class="ahT6S "]') == 'Вход':  # проверка авторизован ли пользователь
        authorization()  # авторизоваться если нет
    else:  # иначе открыть почту
        r.url('https://mail.google.com/mail/u/0/#inbox')
    read_page()
    r.close()


def authorization():  # авторизация
    r.type('//*[@id="identifierId"]', conf['login'])
    r.click('Далее')
    r.type('//*[@name="password"]', conf['password'])
    r.click('Далее')


def read_page():  # прочтение страницы
    r.dump('', 'message.txt')
    for i in range(conf['qty'] + 1):  # количество страниц, которые нужно записать
        for j in range(1, 6):  # количества писем на одной странице
            r.click(f'//*[@class="zA yO"][{j}]')  # открыть письмо
            read_message()  # записать его содержимое
            r.click('//*[@class="asa"]')  # вернуться на страницу писем
        r.click('//*[@id=":mi"]')  # переключить страницу
        r.wait(3)


def read_message():
    header = ' '.join(r.read('//*[@class="hP"]').split())  # заголовок
    who = ' '.join(r.read('//*[@class="cf gJ"]').split())  # отравитель
    text = ' '.join(r.read('//*[@class="ii gt"]').split())  # содержание письма
    message = '\n'.join([f'Тема письма: {header}', f'От кого: {who}', f'Текст письма: {text}', f'{"."*100}\n'])
    r.write(message, 'message.txt')  # записать письмо в текстовый документ


if __name__ == '__main__':
    main()
