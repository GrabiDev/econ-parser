import xml.etree.ElementTree as ET
import urllib.request
import json, datetime, os, sys
from time import sleep

BRIEFING_URL = os.environ['BRIEFING_URL']
OUTPUT_XML = os.environ['OUTPUT_XML']
WAIT_TIME_MINUTES = 5
MAX_ATTEMPTS = -1 # no limit by default
MAX_RECONNECT_ATTEMPTS = 5
RECONNECT_TIME_MINUTES = 1

if 'WAIT_TIME_MINUTES' in os.environ:
  WAIT_TIME_MINUTES = int(os.environ['WAIT_TIME_MINUTES'])

if 'MAX_ATTEMPTS' in os.environ:
  MAX_ATTEMPTS = int(os.environ['MAX_ATTEMPTS'])

if 'MAX_RECONNECT_ATTEMPTS' in os.environ:
  MAX_RECONNECT_ATTEMPTS = int(os.environ['MAX_RECONNECT_ATTEMPTS'])

if 'RECONNECT_TIME_MINUTES' in os.environ:
  RECONNECT_TIME_MINUTES = int(os.environ['RECONNECT_TIME_MINUTES'])

failed_attempts = 0
reconnect_attempts = 0

# parses item's timestamp to datetime object
def get_pub_datetime(item):
  pub_datetime_str = item.find('pubDate').text
  pub_datetime = datetime.datetime.strptime(pub_datetime_str, '%a, %d %b %Y %H:%M:%S %Z')
  return pub_datetime

# checks if item was published today
def is_published_today(item):
  today = datetime.date.today()
  pub_date = get_pub_datetime(item).date()
  if pub_date == today:
    return True
  return False

# downloads the whole feed from The Economist
def get_root(briefing_url):
  page = urllib.request.urlopen(briefing_url)
  # if page loaded correctly
  if page.status == 200:
    return ET.fromstring(page.read())
  # otherwise reconnect, if within reconnection limit
  else:
    if reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
      sleep(RECONNECT_TIME_MINUTES*60)
      reconnect_attempts += 1

      return get_root(briefing_url)
    # when limit reached, shut down
    else:
      sys.exit('Cannot connect to the feed. Check BRIEFING_URL and internet connection.')

# Parses the downloaded feed and checks correctness
def get_output_tree(root):
  channel = root.findall('channel')[0]

  # retrieve all item elements
  items = channel.findall('item')

  # filter the newest items (might be more than one!)
  for item in items:
    if not is_published_today(item):
      channel.remove(item)

  # check if any items left in the feed
  items = channel.findall('item')
  today = datetime.date.today()

  # if no items left and today is not Sunday
  if (len(items) == 0) and (today.isoweekday() != 7):
    # also check whether attempt limit reached
    if (MAX_ATTEMPTS == -1) or (failed_attempts < MAX_ATTEMPTS):
      # record new failed attempts
      failed_attempts += 1
      # then wait, download new feed and recursively try again
      sleep(WAIT_INTERVAL_MINUTES*60)
      new_root = get_root(BRIEFING_URL)

      return get_output_tree(new_root)
  
  # otherwise, return output tree
  return ET.ElementTree(element=root)

# main execution
if __name__ == '__main__':
  root = get_root(BRIEFING_URL)
  output_tree = get_output_tree(root)

  output_tree.write(os.path.join(os.getcwd(), OUTPUT_XML), encoding='UTF-8', xml_declaration=True)