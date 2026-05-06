import sys, json, urllib.request, http.cookiejar, os

# Récupérer le cookie depuis les variables d'environnement
cookie = os.environ.get('DIDASK_COOKIE', '')

def fetch(url):
    req = urllib.request.Request(url, headers={'Cookie': cookie})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

NEW_TAG_ID = '69fb067c453567000168a6bc'

raw = json.load(sys.stdin)
courses = raw['data']['data']
out = []

for c in courses:
    project_id = c.get('projectId')
    is_new = False
    if project_id:
        try:
            project = fetch(f'https://craif.didask.com/api/studio/projects/{project_id}')
            tags = project.get('data', {}).get('tags', [])
            is_new = any(t['_id'] == NEW_TAG_ID for t in tags)
        except:
            pass

    out.append({
        'slug': c['slug'],
        'name': c['displayedName']['fr'],
        'duration': c['duration'],
        'image': c['banner']['asset']['sources'][0]['url'],
        'url': 'https://craif.didask.com/fr/courses/' + c['slug'],
        'is_new': is_new
    })

# Trier : nouveaux parcours en premier
out.sort(key=lambda x: (0 if x['is_new'] else 1))

print(json.dumps(out, ensure_ascii=False, indent=2))
