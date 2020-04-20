import getopt
import hashlib
import sys
import urllib.request
import xml.etree.ElementTree as ElementTree


def sha1(user, password):
    return hashlib.sha1(('%s|%s' % (user, password)).encode('utf8')).hexdigest()


def read_user_sha1(argv):
    ur = ''
    pd = ''
    opts, args = getopt.getopt(argv, "hu:p:", ["user=", "password="])
    for opt, arg in opts:
        if opt == '-h':
            print('freedns.py -u <user> -p <password>')
            sys.exit()
        elif opt in ("-u", "--user"):
            ur = arg
        elif opt in ("-p", "--password"):
            pd = arg
    return sha1(ur, pd)


def update_record_if_necessary(records, live_ip):
    updated = []
    for item in records.findall('item'):
        host = item.find('host').text
        address = item.find('address').text
        url = item.find('url').text

        if address in updated:
            continue

        if live_ip == address:
            print('No change needed for ' + host + '!')
        else:
            http = urllib.request.urlopen(url)
            print(http.read_user_sha1().decode())
            updated.append(address)


def live_address():
    http = urllib.request.urlopen('http://ip.dnsexit.com/')

    if http.status != 200:
        sys.exit()

    return http.read().decode().strip()


def dns_records(sha1_value):
    http = urllib.request.urlopen('https://freedns.afraid.org/api/?action=getdyndns&style=xml&v=2&sha=' + sha1_value)

    if http.status != 200:
        sys.exit()

    return ElementTree.fromstring(http.read())


def main(argv):
    try:
        user_sha1 = read_user_sha1(argv)
    except getopt.GetoptError:
        print('freedns.py -u <user> -p <password>')
        sys.exit(2)

    update_record_if_necessary(dns_records(user_sha1), live_address())


if __name__ == "__main__":
    main(sys.argv[1:])
