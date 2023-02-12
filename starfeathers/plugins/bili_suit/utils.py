from requests import get as rqGet
from os.path import exists as osPathExists
from os import makedirs as osMakedirs
import os
import zipfile

SAVEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), r"suit"))


def isNum(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_suit(suit_id, base_dir=SAVEDIR):
    '''
    获取单个装扮素材

    输入:
        - suit_id: 装扮ID
        - base_dir: 存储路径
    输出: 素材文件夹
    '''
    final_status = 100
    try:
        rq_get = rqGet(
            'https://api.bilibili.com/x/garb/mall/item/suit/v2?&part=suit&item_id='
            + str(suit_id))
    except:
        return dict(), 1

    res = rq_get.json()

    if res['data']['item']['item_id'] == 0:
        return dict(), 0

    suit_name = res['data']['item']['name']

    base_dir += '/'
    base_dir += res['data']['item']['name']

    if not os.path.exists(base_dir):
        # Save suit !!
        if not osPathExists(base_dir):
            osMakedirs(base_dir)
        with open(base_dir + '/suit_info.json', 'w', encoding='utf-8') as suit_json_file:
            suit_json_file.write(rq_get.text)

        # part 1. Emoji
        emoji_list = [
            (item['name'][1:-1], item['properties']['image'])
            for item in res['data']['suit_items']['emoji_package'][0]['items']
        ]
        if not osPathExists(base_dir + '/emoji/'):
            osMakedirs(base_dir + '/emoji/')

        for i, item in enumerate(emoji_list):
            img_name = item[0]
            try:
                with open(base_dir + '/emoji/' + img_name + '.png', 'wb') as emoji_file:
                    emoji_file.write(rqGet(item[1]).content)
            except OSError:
                img_name = img_name.split('_')[0] + '_{}'.format(i)
                try:
                    with open(base_dir + '/emoji/' + img_name + '.png', 'wb') as emoji_file:
                        emoji_file.write(rqGet(item[1]).content)
                except:
                    pass
                final_status = 101
            except:
                return dict(), 1

        # part 2. Background
        bg_dict = res['data']['suit_items']['space_bg'][0]['properties']
        bg_list = list()

        for key, value in bg_dict.items():
            if key[0] == 'i':
                bg_list.append((key, value))

        if not osPathExists(base_dir + '/background/'):
            osMakedirs(base_dir + '/background/')

        for item in bg_list:
            try:
                with open(base_dir + '/background/' + item[0] + '.jpg', 'wb') as bg_file:
                    bg_file.write(rqGet(item[1]).content)
            except:
                return dict(), 1

        # part 3. Others
        if not osPathExists(base_dir + '/properties/'):
            osMakedirs(base_dir + '/properties/')
        pro_list = [
            ('properties.zip', res['data']['suit_items']['skin'][0]['properties']['package_url']),
            ('fan_share_image.jpg', res['data']['item']['properties']['fan_share_image']),
            ('image_cover.jpg', res['data']['item']['properties']['image_cover']),
            ('avatar.jpg', res['data']['fan_user']['avatar']),
            ('thumbup.jpg', res['data']['suit_items']['thumbup'][0]['properties']['image_preview'])
        ]
        for item in pro_list:
            try:
                with open(base_dir + '/properties/' + item[0], 'wb') as pro_file:
                    pro_file.write(rqGet(item[1]).content)
            except:
                return dict(), 1
    else:
        pass
    return suit_name, final_status


def zip_suit(suit_name, dir=SAVEDIR):
    '''
    打包素材文件
    输入：
        - suit_name：装扮名（用于构建完整存储路径）
        - dir：存储路径
    输出：
        - SAVEFILE：输出文件路径
    '''
    SUITDIR = os.path.abspath(os.path.join(dir, suit_name))
    SAVEFILE = os.path.abspath(os.path.join(dir, f'{suit_name}.zip'))
    if not os.path.exists(SAVEFILE):
        zipList = []
        zf = zipfile.ZipFile(SAVEFILE, mode='w', compression=zipfile.ZIP_LZMA)
        for dir, subdirs, files in os.walk(SUITDIR):  # 遍历目录，加入列表
            for fileItem in files:
                zipList.append(os.path.join(dir, fileItem))
            for dirItem in subdirs:
                zipList.append(os.path.join(dir, dirItem))
        for i in zipList:
            zf.write(i, i.replace(SUITDIR, ''))
        zf.close()
    else:
        pass
    return SAVEFILE
