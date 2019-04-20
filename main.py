import os
import sys
import vk_api
import random
import json


def read_content():
    with open('content.json', mode='r') as f:
        return json.load(f)


def vk_auth(content):
    session = vk_api.VkApi(
        login=content['logging']['login'],
        token=content['logging']['token']
    )

    try:
        session.auth(reauth=True, token_only=True)
    except vk_api.AuthError as ex:
        print(ex)
        sys.exit()

    return session.get_api()


def rand_text(content):
    greets = content['greet']
    names = content['name']
    rand_greet = greets[random.randint(a=0, b=len(greets))]
    rand_name = names[random.randint(a=0, b=len(names))]

    return rand_greet, rand_name


def attach(upload):
    randint = random.randint(a=1, b=10)
    dir_ = os.path.dirname(os.path.realpath(__file__))
    photo = '{0}/img/{1}.jpg'.format(dir_, randint)
    photo_list = upload.photo_wall(
        photos=photo
    )

    return ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)


def main():
    content = read_content()
    session = vk_auth(content)
    upload = vk_api.VkUpload(session)
    attachment = attach(upload)
    rand_text_ = rand_text(content)

    session.wall.post(
        message='{0}! {1} сегодня не умер!'.format(
            rand_text_[0], rand_text_[1]
        ),
        owner_id=content['logging']['owner_id'],
        from_group=content['logging']['from_group'],
        attachment=attachment
    )


if __name__ == '__main__':
    main()
