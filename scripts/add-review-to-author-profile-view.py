# This script takes care of the time-consuming task of adding a review to the `author-profile` 
# view for each member of Gen Z Critics. All author metadata (name, location, bio) is stored 
# in `author-data.json`. This file parses through the json file and creates all html files with 
# correct pagination numbers and links to the correct articles.

import json
import consts
import os

with open('./author-data.json') as author_data:
    author_entries = json.load(author_data)

with open('./reviews-data.json') as reviews_data:
    review_entries = json.load(reviews_data)


############################################################################
# STEP 1: Ask which author to generate the html for
############################################################################
print '##################################################'
print '#################### hello :) ####################'
print '##################################################'
print '\nAuthors with more than 4 reviews:'
valid_authors = []
for author in author_entries.keys():
    if len(filter(lambda entry: entry['profile'] == author, review_entries)) > 4:
        print author
        valid_authors.append(author)

author = raw_input('\nEnter the author ID: ')
while author not in valid_authors:
    author = raw_input('That author has not written enough reviews; please enter a valid author instead: ')


############################################################################
# STEP 2: First, make the root ${author}/index.html html and append to the 
# beginning of html_pages
############################################################################
header = consts.AUTHOR_ROOT_HEADER
author_obj = author_entries[author]
s = '<img class="rounded-circle" src="../img/' + author + '.jpg" alt="' + author_obj['name'] + '">'
s += '</div><div class="col-lg-auto member-info">'
s += '<h2 class="name">' + author_obj['name'] + '</h2>'
s += '<h4 class="location">' + author_obj['location'] + '</h4></div></div>'
s += '<p>' + author_obj['bio'] + '</p><hr>\n\n'
header += s

posts_by_author = filter(lambda entry: entry['profile'] == author, review_entries)
posts = []

for post in list(reversed(posts_by_author))[:4]:
    post_html = '<div class="post-preview"><a href="../../' + post['article'] + '.html">'
    post_html += '<h2 class="post-title">' + post['title'] + '</h2>'
    post_html += '<h3 class="post-subtitle">' + post['subtitle'] + '</h3></a>' if 'subtitle' in post.keys() else '</a>'
    post_html += '<p class="post-meta">by <a href="">'
    post_html += post['author'] + '</a> on ' + post['date'] + '</p>'
    post_html += '<a href="../../' + post['article'] + '.html">'
    post_html += '<img class="preview-image" src="../img/' + post['image'] + '"></a></div><hr>\n\n'
    posts.append(post_html)

html_pages = []

html_page = header
html_page += reduce(lambda a, b: a + b, posts)
html_page += consts.PAGINATION_HEADER + '*****INSERT PAGINATION HERE*****\n' + consts.PAGINATION_FOOTER
html_page += consts.AUTHOR_FOOTER
html_pages.append(html_page)


############################################################################
# STEP 3: Now make the htmls for the first page (non-root) AND the other 
# pages as well, and similarly append to html_pages
############################################################################
header = consts.AUTHOR_HEADER
posts = []

author_obj = author_entries[author]
s = '<img class="rounded-circle" src="../img/' + author + '.jpg" alt="' + author_obj['name'] + '">'
s += '</div><div class="col-lg-auto member-info">'
s += '<h2 class="name">' + author_obj['name'] + '</h2>'
s += '<h4 class="location">' + author_obj['location'] + '</h4></div></div>'
s += '<p>' + author_obj['bio'] + '</p><hr>'
header += s

for post in reversed(posts_by_author): # the json is in chronological order; we want to display reverse chronological order
    post_html = '<div class="post-preview"><a href="../../../../' + post['article'] + '.html">'
    post_html += '<h2 class="post-title">' + post['title'] + '</h2>'
    post_html += '<h3 class="post-subtitle">' + post['subtitle'] + '</h3></a>' if 'subtitle' in post.keys() else '</a>'
    post_html += '<p class="post-meta">by <a href="">'
    post_html += post['author'] + '</a> on ' + post['date'] + '</p>'
    post_html += '<a href="../../../../' + post['article'] + '.html">'
    post_html += '<img class="preview-image" src="../img/' + post['image'] + '"></a></div><hr>\n\n'
    posts.append(post_html)

html = ''

num_pages = len(posts) / 4
num_posts_leftover = len(posts) % 4

for i in range(0, num_pages):
    html_page = header
    html_page += posts[i*4] + posts[i*4 + 1] + posts[i*4 + 2] + posts[i*4 + 3]
    html_page += consts.PAGINATION_HEADER + '*****INSERT PAGINATION HERE*****\n' + consts.PAGINATION_FOOTER
    html_page += consts.AUTHOR_FOOTER
    html_pages.append(html_page)

if num_posts_leftover > 0:
    html_page = header
    for i in range(0, num_posts_leftover):
        html_page += posts[num_pages*4 + i]
    html_page += consts.PAGINATION_HEADER + '*****INSERT PAGINATION HERE*****\n' + consts.PAGINATION_FOOTER
    html_page += consts.AUTHOR_FOOTER
    html_pages.append(html_page)


#############################################################################
# STEP 5: Save the html pages as index.html files into the correct repositories
#############################################################################
absolute_path = '/Users/sharonkim/genzcritics.github.io/reviews/author-profile/' + author

# Make sure a copy of the first page is in the "root" repo of that specific author
with open(absolute_path + '/index.html', 'w') as f:
    try: f.write(html_pages[0])
    except: print 'Errored on root index.html'

absolute_path += '/page/'
for page in html_pages[1:]:
    curr_page = html_pages.index(page)
    filename = absolute_path + str(curr_page) + '/index.html'
    with open(filename, 'w') as f:
        try:
            f.write(page)
        except IOError:
            os.mkdir(absolute_path + str(curr_page))

print '***Remember to manually include pagination for each page!***'
