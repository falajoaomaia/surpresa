from BeautifulSoup import *
from lcdcontrol import *
import simplejson as json
import urllib
import unicodedata
import textwrap
import sys
import time

def decode(text):
    soup = BeautifulSoup(text, convertEntities=BeautifulSoup.HTML_ENTITIES)
    text = ''.join(soup.findAll(text=True))
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

try:
    printer = file('/dev/usblp0', 'w')
except:
    printer = file('/dev/null', 'w')

#on mac/linux, use a posix path to the port. on windows, use a number (zero-indexed) e.g. COM4 -> 3
lcd = LCDControl(sys.argv[1]) if len(sys.argv) > 1 else LCDControl()
lcd.set_text("Iniciando", "... aguarde".rjust(16, ' '))
lcd.blink()

path = "http://search.twitter.com/search.json?q=%23ficanatalia"
feed = json.load(urllib.urlopen(path))

try:
    last_id = long(file("last_printed_id").readline())
except IOError:
    last_id = 0

entries = [e for e in feed['results'] if long(e['id']) > last_id]

if len(entries) > 0:

    lcd.set_text("{} novos tweets".format(len(entries)), "Imprimindo".rjust(16, " "))

    for e in entries:
        text = "@{0}: {1}".format(e['from_user'], decode(e['text']))
        text = "\n".join(textwrap.wrap(text, 40))+"\n\n\n"
        printer.write(text)
        print(text)
        if long(e['id']) > last_id: last_id = long(e['id'])

    printer.close()
    file("last_printed_id",'w+').write("%s" % last_id)

    time.sleep(15)

lcd.set_text("Tchau!", " ")
time.sleep(1)
lcd.set_led(False)
lcd.close()
