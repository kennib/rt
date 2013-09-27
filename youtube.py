#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from lxml import objectify

COMMENT_URL = "http://gdata.youtube.com/feeds/api/videos/{video_id}/comments?max-results={max_results}"
VIDEO_ID = "lBzET3tBkmU"
RESULTS_PER_REQUEST = 50
MAX_RESULTS = 66

# A class which stores the author and text of comments
class Comment():
  def __init__(self, text, author):
    self.text = text.encode('utf-8')
    self.author = author.encode('utf-8')

  def __repr__(self):
    return "<comment `"+self.author+"` said `"+self.text+"`>"


comments = []
# Fetch comments in batches
# Youtube limits requests to 50 per request
for index in xrange(0, MAX_RESULTS, RESULTS_PER_REQUEST):
  # Construct the url
  url = COMMENT_URL.format(**{
    "video_id":  VIDEO_ID,
    "max_results": RESULTS_PER_REQUEST,
  })

  # No start index if the index is 0
  # Youtube dislikes having a start index of 0
  if index:
    url += "&start-index={}".format(index)

  # Fetch the data
  result = urllib2.urlopen(url)
  # Parse the data
  obj = objectify.fromstring(result.read())

  # Place into comment objects
  for child in obj.getchildren():
    if child.tag.endswith('entry'):
      content = child.content.text
      author = child.author.name.text

      comment = Comment(content, author)
      comments.append(comment)

  print url

print comments
