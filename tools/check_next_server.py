import http.client
import time
import sys

port = 8080
path = '/strategy-lab'

def check():
    t0 = time.time()
    timeout = 20
    while time.time() - t0 < timeout:
        try:
            conn = http.client.HTTPConnection('localhost', port, timeout=3)
            conn.request('GET', path)
            r = conn.getresponse()
            print('STATUS', r.status)
            return 0
        except Exception as e:
            time.sleep(1)
    print('FAILED')
    return 1

if __name__ == '__main__':
    sys.exit(check())
