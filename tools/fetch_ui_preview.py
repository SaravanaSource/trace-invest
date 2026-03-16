import http.client, sys

def fetch(url):
    host, path = url.replace('http://','').split('/',1)
    path = '/' + path
    port = 80
    if ':' in host:
        host, p = host.split(':')
        port = int(p)
    try:
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request('GET', path)
        r = conn.getresponse()
        content = r.read(5000).decode('utf-8','replace')
        print('\n---', url, 'STATUS', r.status, '---')
        print(content[:2000])
    except Exception as e:
        print('\n---', url, 'ERROR ---')
        print(e)

if __name__ == '__main__':
    fetch('http://localhost:8080/strategy-lab')
    fetch('http://localhost:8000/research-ui')
