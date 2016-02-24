# encoding:utf-8
from optparse import OptionParser
import ConfigParser
from Crypto.Cipher import AES

KEY = 'ahksikijuhygtfds'
aes = AES.new(KEY)

def fill128(data):
    length = len(data)
    if (length < 256):
        data = data + ':' * (256 - length)
        return data
    else:
        print "Error:encode data to long"

def encode(data):
    data = fill128(data)
    return aes.encrypt(data)

def decode(data):
    decrypt_data = aes.decrypt(data)
    length = decrypt_data.find(':')
    return decrypt_data[:length]

config = ConfigParser.RawConfigParser()

#load default configure
config.read('config.cfg')
host = config.get('Base', 'host')
port = config.get('Base', 'port')

user_name = config.get('Aliyun', 'user_name')
passwd = config.get('Aliyun', 'passwd')
access_key = config.get('Aliyun', 'access_key')
access_secret = config.get('Aliyun', 'access_secret')
regin = config.get('Aliyun', 'regin')
oss_endpoint = config.get('Aliyun', 'oss_endpoint')

passwd = decode(passwd)
access_key = decode(access_key)
access_secret = decode(access_secret)

parser = OptionParser()
parser.add_option("-H", "--host", dest="host", help="cloud gate listening host", default=host)
parser.add_option("-p", "--port", dest="port", help="cloud gate listening port", default=port)
parser.add_option("-n", "--name", dest="user_name", help="set your login user name", default=user_name)
parser.add_option("-P", "--passwd", dest="passwd", help="set your login passwd", default=passwd)
parser.add_option("-k", "--key", dest="access_key", help="set your access key", default=access_key)
parser.add_option("-s", "--secret", dest="access_secret", help="set your access secret", default=access_secret)
parser.add_option("-r", "--regin", dest="regin", help="set your regin, like 'cn-hongkong'", default=regin)
parser.add_option("-o", "--oss-endpoint", dest="oss_endpoint", help="set your oss end point", default=oss_endpoint)

(options, args) = parser.parse_args()

HOST=options.host
PORT=options.port

IDENTITY={
    "aliyun":{
        "user_name":options.user_name,
        "passwd":options.passwd,
        "access_key":options.access_key,
        "access_secret":options.access_secret,
        "regin":options.regin,
        "oss_endpoint":options.oss_endpoint
    },
}

print HOST, PORT, IDENTITY

#dump new configure
config.set('Base', 'host', HOST)
config.set('Base', 'port', PORT)

options.passwd = encode(options.passwd)
options.access_key = encode(options.access_key)
options.access_secret = encode(options.access_secret)

config.set('Aliyun', 'user_name', options.user_name)
config.set('Aliyun', 'passwd', options.passwd)
config.set('Aliyun', 'access_key', options.access_key)
config.set('Aliyun', 'access_secret', options.access_secret)
config.set('Aliyun', 'regin', options.regin)
config.set('Aliyun', 'oss_endpoint', options.oss_endpoint)

with open('config.cfg', 'wb') as configfile:
    config.write(configfile)

