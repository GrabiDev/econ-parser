import xml.etree.ElementTree as ET
import urllib.request
import json, datetime, os

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

morning_briefing_url = os.environ['BRIEFING_URL']
morning_briefing_output = os.environ['OUTPUT_XML']

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
output_tree.write(os.path.join(os.getcwd(), morning_briefing_output), encoding='UTF-8', xml_declaration=True)