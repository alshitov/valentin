import os
import sys
import vk_api
import random
import configparser


def config():
    cfg = configparser.ConfigParser()
    cfg.read('usr.ini')
    section = cfg['LOGGING']

    return {
        'login': section['login'],
        'token': section['token'],
        'owner_id': section['owner_id'],
        'from_group': section['from_group']
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


def attach(upload):
    randint = random.randint(a=1, b=10)
    dir_ = os.path.dirname(os.path.realpath(__file__))
    photo = '{0}/img/{1}.jpg'.format(dir_, randint)
    photo_list = upload.photo_wall(photo)
    return ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)


def main():
    cfg = config()
    session = vk_auth(cfg)
    upload = vk_api.VkUpload(session)
    attachment = attach(upload)
    session.wall.post(
        message='Всё в порядке! Валентин сегодня не умер!',
        owner_id=cfg['owner_id'],
        from_group=cfg['from_group'],
        attachment=attachment
    )


if __name__ == '__main__':
    main()