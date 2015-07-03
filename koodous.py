import settings
import requests

def apk_info(sha256):
    res = requests.get(url='https://koodous.com/api/apks/%s' % sha256,
                       headers={"Authorization": "Token %s" % \
                                                        settings.KOODOUS_TOKEN})
    return res.json()


if __name__ == '__main__':
    apk_info('02b09baff81df89b50ae8d7465587497839c99b8410c3a2106606b4ad02f772b')
