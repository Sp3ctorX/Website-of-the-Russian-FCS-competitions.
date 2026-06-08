import urllib.request

# Test different pages
pages = [
    '/home',
    '/login',
    '/admin/dashboard',
    '/manager/dashboard',
    '/participant/profile',
    '/expert/dashboard'
]

for page in pages:
    try:
        req = urllib.request.Request('http://localhost:8888' + page)
        with urllib.request.urlopen(req) as response:
            print('%s: %s' % (page, response.status))
    except Exception as e:
        print('%s: ERROR - %s' % (page, str(e)[:50]))
