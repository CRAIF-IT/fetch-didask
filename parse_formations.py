import sys, json, urllib.request, http.cookiejar

COOKIES_FILE = 'cookies.txt'
NEW_TAG_ID = '69fb067c453567000168a6bc'

cookie_jar = http.cookiejar.MozillaCookieJar(COOKIES_FILE)
cookie_jar.load(ignore_discard=True, ignore_expires=True)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

def fetch(url):
    with opener.open(url) as r:
        return json.loads(r.read())

raw = json.load(sys.stdin)
courses = raw['data']['data']
out = []

for c in courses:
    project_id = c.get('projectId')
    is_new = False
    if project_id:
        try:
            project = fetch(f'https://craif.didask.com/api/studio/projects/{project_id}/summary')
            tags = project.get('data', {}).get('tags', [])
            is_new = any(t['_id'] == NEW_TAG_ID for t in tags)
        except Exception as e:
            sys.stderr.write(f'Erreur projet {project_id}: {e}\n')

    out.append({
        'slug': c['slug'],
        'name': c['displayedName']['fr'],
        'duration': c['duration'],
        'image': c['banner']['asset']['sources'][0]['url'],
        'url': 'https://craif.didask.com/fr/courses/' + c['slug'],
        'is_new': is_new
    })

out.sort(key=lambda x: (0 if x['is_new'] else 1))
print(json.dumps(out, ensure_ascii=False, indent=2))
