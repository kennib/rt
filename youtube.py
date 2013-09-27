#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from lxml import objectify

COMMENT_URL = "http://gdata.youtube.com/feeds/api/videos/{video_id}/comments?max-results={max_results}"
VIDEO_ID = "hbenhC7M8VI"
RESULTS_PER_REQUEST = 50
MAX_RESULTS = 1000

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
  obj = objectify.fromstring(result.read().replace('\xef\xbb\xbf', ''))

  # Place into comment objects
  request_comments = []
  for child in obj.getchildren():
    if child.tag.endswith('entry'):
      content = child.content.text
      author = child.author.name.text

      comment = Comment(content, author)
      request_comments.append(comment)
  
  # Add the comments from this request to the pool of comments
  comments += request_comments

  # Stop requests if all comments have been parsed
  if len(request_comments) is 0:
    break


# Do some NLP to find interesting results
from collections import Counter
import nltk
stopwords = nltk.corpus.stopwords.words('english')

word_bag = Counter()
for comment in comments:
  if "should" in comment.text:
    sentences = nltk.sent_tokenize(comment.text)
    sent_words = [nltk.pos_tag(nltk.word_tokenize(comment.text)) for sentence in sentences if "should" in sentence]
    sent_keywords = [
      [word for word, pos in sentence
        if word.lower() not in stopwords
          and ("NN" in pos or pos is "VB")]
      for sentence in sent_words]
    keywords = sum(sent_keywords, [])
    word_bag.update(keywords)

print word_bag
