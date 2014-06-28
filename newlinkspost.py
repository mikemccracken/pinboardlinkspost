import getpass
from operator import itemgetter
import os
import pprint
import readline
import sys
import datetime

try:
    import pinboard
except ImportError:
    print('''error, no pinboard. try
    pip install -e git://github.com/mgan59/python-pinboard.git@v1.1#egg=python-pinboard
    ''')
    sys.exit()

username = raw_input("Pinboard username [mmc]: ")
if username == '':
    username = 'mmc'
password = getpass.getpass("Pinboard password: ")

pconn = pinboard.open(username, password)

num_posts = raw_input("how many posts? (10) ")

if num_posts != '':
    num_posts = int(num_posts)
else:
    num_posts = 10

links = sorted(pconn.posts(count=num_posts),
               key=itemgetter('time'))

seen = {}
if os.path.exists("seen.txt"):
    with open("seen.txt") as seenf:
        for line in seenf.readlines():
            used, url = line[0], line[2:-1]  # strip space and line ending
            seen[url] = used

def print_help():
    print("""help:
y: use as-is
n/N: default - don't use
o: open in browser to review
e[ted]: edit [t-tags, e-extended desc, d-desc]
h: print help
d: done - skip remaining links and write post
q: quit - stop and don't update seen.txt, no post is written.
""")

editwhichkey = dict(t='tags',
                    e='extended',
                    d='description')

newpoststr = ''
tags = set()
for link in links:
    url = link['href']
    if url in seen:
        continue
    cmd = None
    while cmd not in ['y', 'n', 'N', '', 'd', 'q']:
        print("url : {url}\ndesc: {desc}\ntags: {tags}\next : {ext}".format(
            url=link['href'],
            desc=link['description'].encode('utf-8'),
            ext=link['extended'].encode('utf-8'),
            tags=', '.join(link['tags']).encode('utf-8')))

        cmd = raw_input("Use? y/N/o/e[ted]/h/d/q: ")
        if cmd == 'h':
            print_help()
        if cmd == 'o':
            os.system('sensible-browser ' + link['href'])
        if cmd.startswith('e'):
            which = editwhichkey[cmd[-1]]
            placeholder = link[which]
            if which == 'tags':
                placeholder = ', '.join(link[which])

            def h():
                readline.insert_text(placeholder)
            readline.set_startup_hook(h)

            input = raw_input("{}: ".format(which))
            if which == 'tags':
                input = input.split(', ')
            link[which] = input
            readline.set_startup_hook(None)
            pprint.pprint(link)
            try:
                pconn.add(link['href'],
                          link['description'],
                          extended=link['extended'],
                          tags=link['tags'],
                          date=link['time_parsed'],
                          toread=link.get('toread', 'no'),
                          replace="yes")
                print("updated.")
            except pinboard.AddError:
                print("error updating link!")
                
    if cmd == 'y':
        newpoststr += "* [%s](%s)\n\t%s\n\n" % (link['description'],
                                              url,
                                              link['extended'])
        map(tags.add, link['tags'])
        seen[url] = 'y'
    elif cmd in ['N', 'n', '']:
        seen[url] = 'n'
    elif cmd == 'd':
        print("skipping remaining links.")
        break
    elif cmd == 'q':
        resp = raw_input("Are you sure you want to quit and not save local changes? type 'yes' if you're sure. ")
        if resp == 'yes':
            print("quitting without writing any info - any updated links on pinboard are still there")
            sys.exit(0)
    print("\n")

tags_str = ', '.join([t.strip() for t in tags])

with open("seen.txt", 'w+') as seenf:
    for url, used in seen.items():
        seenf.write("%s %s\n" % (used, url))

dirstr = datetime.datetime.now().strftime('%Y/%m')
daystr = datetime.datetime.now().strftime('%b-%d')
monthdaystr = datetime.datetime.now().strftime('%B %d, %Y')
slugdatestr = datetime.datetime.now().strftime('%B-%d-%Y')

dirname = "posts/{}".format(dirstr)

if not os.path.exists(dirname):
    os.makedirs(dirname)

filename = "{}/links-{}.md".format(dirname, daystr)

timestr_hm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

header = """<!--
.. title: Links for {monthdaystr}
.. date: {datestr}
.. slug: links-for-{slugdatestr}
.. tags: {tags_str}
-->
""".format(monthdaystr=monthdaystr, datestr=timestr_hm,
           slugdatestr=slugdatestr,
           tags_str=tags_str)

s = header + newpoststr

with open(filename, 'w') as f:
    f.write(s.encode('utf-8'))

print "opening emacs on ", filename

os.system('emacs -nw %s' % filename)
