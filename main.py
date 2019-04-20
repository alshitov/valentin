import os
import sys
import vk_api
import requests
import configparser


def config():
    cfg = configparser.ConfigParser()
    cfg.read('usr.ini')
    section = cfg['LOGGING']

    return {
        'login': section['login'],
        'id_': section['id_']
    }


def vk_auth(cfg):
    session = vk_api.VkApi(
        login=cfg['login'],
        token=cfg['token']
    )

    try:
        session.auth(reauth=True, token_only=True)
    except vk_api.AuthError as ex:
        print(ex)
        sys.exit()

    return session.get_api()


def main():
    cfg = config()
    session = vk_auth(cfg)
    session.wall.post(
        message='Всё в порядке! Валентин сегодня не умер!',
        owner_id=-cfg['group_id'],
        from_group=cfg['from_group']
    )


if __name__ == '__main__':
    main()