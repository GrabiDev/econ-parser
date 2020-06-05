import xml.etree.ElementTree as ET
import urllib.request
import json, datetime, os
from time import sleep

BRIEFING_URL = os.environ['BRIEFING_URL']
OUTPUT_XML = os.environ['OUTPUT_XML']
WAIT_TIME_MINUTES = os.environ['WAIT_TIME_MINUTES']
MAX_ATTEMPTS = -1 # no limit by default

if os.environ['MAX_ATTEMPTS']:
  MAX_ATTEMPTS = os.environ['MAX_ATTEMPTS']

failed_attempts = 0

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

def get_root(briefing_url):
  page = urllib.request.urlopen(briefing_url)
  return ET.fromstring(page.read())

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