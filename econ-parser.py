import xml.etree.ElementTree as ET
import urllib.request
import json, datetime

def get_pub_datetime(item):
  pub_datetime_str = item.find('pubDate').text
  pub_datetime = datetime.datetime.strptime(pub_datetime_str, '%a, %d %b %Y %H:%M:%S %Z')
  return pub_datetime

def is_published_today(item):
  today = datetime.date.today()
  pub_date = get_pub_datetime(item).date()
  if pub_date == today:
    return True
  return False


CONF_FILE = 'config.json' #os.path.join(os.environ['APP_HOME'], 'config.json')

with open(CONF_FILE) as cfg:
  CONFIG_JSON = json.load(cfg)

morning_briefing_url = CONFIG_JSON['url']['morning_briefing']

page = urllib.request.urlopen(morning_briefing_url)

tree = ET.fromstring(page.read())
channel = tree.findall('channel')[0]

# retrieve all item elements
items = channel.findall('item')

# filetr the newest items (might be more than one!)
for item in items:
  if not is_published_today(item):
    channel.remove(item)

output_tree = ET.ElementTree(element=tree)
output_tree.write('briefing.xml', encoding='UTF-8', xml_declaration=True)