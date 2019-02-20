# This script takes care of the time-consuming task of adding a review to the `author-profile` 
# view for each member of Gen Z Critics. All author metadata (name, location, bio) is stored 
# in `author-data.json`. This file parses through the json file and creates all html files with 
# correct pagination numbers and links to the correct articles.

import json
import consts

with open('../author-data.json') as d:
    author_entries = json.load(d)

with open ('../reviews-data.json') as d:
    review_entries = json.load(d)


############################################################################
# STEP 1: Ask which author to generate the html for
############################################################################
print '##################################################'
print '#################### hello :) ####################'
print '##################################################'
print '\nHere is a list of all author IDs, ordered alphabetically, so you can verify the author ID:\n'
authors_in_alphabetical_order = sorted(author_entries.keys())
for author_id in authors_in_alphabetical_order:
    if 'anthony-d' in author_id:
        print author_id + ' **for this author, please enter `anthony-d` instead of `'+ author_id + '`'
    else:
        print author_id
print '##################################################'

author = raw_input('Now please enter the author ID: ')
while author not in authors_in_alphabetical_order:
    author = raw_input('That author does not exist; please enter the author ID again: ')


############################################################################
# STEP 2: Flesh out the header for this specific author's profile
############################################################################
header = consts.AUTHOR_HEADER

author_obj = author_entries[author]
s = '<img class="rounded-circle" src="img/' + author + '.png" alt="' + author_obj['name'] + '">'
s += '</div><div class="col-lg-auto member-info">'
s += '<h2 class="name">' + author_obj['name'] + '</h2>'
s += '<h4 class="location">' + author_obj['location'] + '</h4></div></div>'
s += '<p>' + author_obj['bio'] + '</p><hr>'
header += s


############################################################################
# STEP 3: Determine which posts this author has written by parsing through 
# reiview-data.json, and create htmls for each post.
############################################################################
posts_by_author = filter(lambda entry: entry['profile'] == author, review_entries)
posts = []
for post in posts_by_author.reverse(): # the json is in chronological order; we want to display reverse chronological order
    post_html = '<div class="post-preview"><a href="../../' + post['article'] + '.html">'
    post_html += '<h2 class="post-title">' + post['title'] + '</h2>'
    post_html += '<h3 class="post-subtitle">' + post['subtitle'] + '</h3></a>' if 'subtitle' in post.keys() else '</a>'
    post_html += '<p class="post-meta">by <a href="../../author-profile/' + post['profile'] + '">'
    post_html += post['author'] + '</a> on ' + post['date'] + '</p>'
    post_html += '<a href="../../' + post['article'] + '.html">'
    post_html += '<img class="preview-image" src="../img/' + post['image'] + '"></a></div><hr>\n\n'
    posts.append(post_html)


############################################################################
# STEP 4: Write the complete html code for each page view, except for the 
# penultimate and last pages
############################################################################
num_pages = len(posts) / 4
num_posts_leftover = len(posts) % 4

html = header
html_pages = []

if num_pages == 0: # Just the single page suffices
    html += reduce((lambda x, y: x + y), posts)
    html += consts.AUTHOR_FOOTER_NO_PAGINATION
    filename = '/Users/sharonkim/genzcritics.github.io/reviews/author-profile/' + author + 'index.html'
    with open(filename, 'w') as f:
        try:
            f.write(html)
        except:
            print 'Errored on: ' + filename
else: # The author requires more than one page to display all reviews
    for i in range(0, num_pages):
        html += posts[i*4] + posts[i*4 + 1] + posts[i*4 + 2] + posts[i*4 + 3]
        html += consts.PAGINATION_HEADER
        pagination = [''] * 7
        if i == 0: # If it's the first page, i.e. contains the most recent posts
            pagination[0] = '<a href="" class="active">1</a>'
            for j in range(1, 5):
                pagination[j] = '<a href="../' + str(j+1) + '">' + str(j+1) + '</a>'
            pagination[5] = '<a href="../6">Next &rarr;</a>'
            pagination[6] = ''
        elif i == 1: # Second page
            pagination[0] = '<a href="../1">&larr; Prev</a>'
            pagination[1] = '<a href="../1">1</a>'
            pagination[2] = '<a href="" class="active">2</a>'
            for j in range(3, 6):
                pagination[j] = '<a href="../' + str(j) + '">' + str(j) + '</a>'
            pagination[6] = '<a href="../2">Next &rarr;</a>'
        else: # For all other pages; last and penultimate pages handled below
            pagination[0] = '<a href="../' + str((i+1)-1) + '">&larr; Prev</a>'
            pagination[1] = '<a href="../' + str((i+1)-2) + '">' + str((i+1)-2) + '</a>'
            pagination[2] = '<a href="../' + str((i+1)-1) + '">' + str((i+1)-1) + '</a>'
            pagination[3] = '<a href="" class="active">' + str((i+1)-0) + '</a>'
            pagination[4] = '<a href="../' + str((i+1)+1) + '">' + str((i+1)+1) + '</a>'
            pagination[5] = '<a href="../' + str((i+1)+2) + '">' + str((i+1)+2) + '</a>'
            pagination[6] = '<a href="../' + str((i+1)+1) + '">Next &rarr;</a>'
        html += '\n'.join(pagination)
        
        html += consts.PAGINATION_FOOTER
        html += consts.FOOTER
        html_pages.append(html)


# ############################################################################
# # STEP 4: Save the html pages as index.html files into the correct repositories
# ############################################################################
absolute_path = '/Users/sharonkim/genzcritics.github.io/reviews/author-profile/' + author
for page in html_pages:
    filename = absolute_path + str(html_pages.index(page) + 1) + '/index.html'
    with open(filename, 'w') as f:
        try:
            f.write(page)
        except:
            print 'Errored on: ' + filename
