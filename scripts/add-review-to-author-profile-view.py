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

# Ask which author to generate html for?
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
    author = raw_input('Enter the author ID again: ')

html = consts.AUTHOR_HEADER

author_obj = author_entries[author]
s = '<img class="rounded-circle" src="img/' + author + '.png" alt="' + author_obj['name'] + '">'
s += '</div><div class="col-lg-auto member-info">'
s += '<h2 class="name">' + author_obj['name'] + '</h2>'
s += '<h4 class="location">' + author_obj['location'] + '</h4></div></div>'
s += '<p>' + author_obj['bio'] + '</p><hr>'
html += s

posts_by_author = filter(lambda entry: entry['profile'] == author, review_entries)
for post in posts_by_author:
    html = '<div class="post-preview"><a href="../../' + post['article'] + '.html">'
    html += '<h2 class="post-title">' + post['title'] + '</h2>'
    html += '<h3 class="post-subtitle">' + post['subtitle'] + '</h3></a>' if 'subtitle' in post.keys() else '</a>'
    html += '<p class="post-meta">by <a href="../../author-profile/' + post['profile'] + '">'
    html += post['author'] + '</a> on ' + post['date'] + '</p>'
    html += '<a href="../../' + post['article'] + '.html">'
    html += '<img class="preview-image" src="../img/' + post['image'] + '"></a></div><hr>\n\n'

html += consts.PAGINATION_HEADER


############################################################################
# STEP 1: Convert the metadata in `author-data.json` to author html
############################################################################



# ############################################################################
# # STEP 2: Write the complete html code for each page view, except for the 
# # penultimate and last pages
# ############################################################################
# num_pages = len(posts) / 4
# num_posts_leftover = len(posts) % 4
# 
# html_pages = []
# for i in range(0, num_pages):
#     html = consts.HEADER
#     html += posts[i*4] + posts[i*4 + 1] + posts[i*4 + 2] + posts[i*4 + 3]
#     html += consts.PAGINATION_HEADER
#     
#     pagination = [''] * 7
#     if i == 0: # If it's the first page, i.e. contains the most recent posts
#         pagination[0] = '<a href="" class="active">1</a>'
#         for j in range(1, 5):
#             pagination[j] = '<a href="../' + str(j+1) + '">' + str(j+1) + '</a>'
#         pagination[5] = '<a href="../6">Next &rarr;</a>'
#         pagination[6] = ''
#     elif i == 1: # Second page
#         pagination[0] = '<a href="../1">&larr; Prev</a>'
#         pagination[1] = '<a href="../1">1</a>'
#         pagination[2] = '<a href="" class="active">2</a>'
#         for j in range(3, 6):
#             pagination[j] = '<a href="../' + str(j) + '">' + str(j) + '</a>'
#         pagination[6] = '<a href="../2">Next &rarr;</a>'
#     else: # For all other pages; last and penultimate pages handled below
#         pagination[0] = '<a href="../' + str((i+1)-1) + '">&larr; Prev</a>'
#         pagination[1] = '<a href="../' + str((i+1)-2) + '">' + str((i+1)-2) + '</a>'
#         pagination[2] = '<a href="../' + str((i+1)-1) + '">' + str((i+1)-1) + '</a>'
#         pagination[3] = '<a href="" class="active">' + str((i+1)-0) + '</a>'
#         pagination[4] = '<a href="../' + str((i+1)+1) + '">' + str((i+1)+1) + '</a>'
#         pagination[5] = '<a href="../' + str((i+1)+2) + '">' + str((i+1)+2) + '</a>'
#         pagination[6] = '<a href="../' + str((i+1)+1) + '">Next &rarr;</a>'
#     html += '\n'.join(pagination)
#     
#     html += consts.PAGINATION_FOOTER
#     html += consts.FOOTER
#     html_pages.append(html)
# 
# 
# ############################################################################
# # STEP 3: Write the complete html code for the penultimate and last pages
# ############################################################################
# if num_posts_leftover == 0:
#     # First, flesh out the html and pagination for the last page
#     html = consts.HEADER
#     for post in posts[-4:]:
#         html += post
#     html += consts.PAGINATION_HEADER
#     
#     pagination = [''] * 7
#     pagination[0] = '<a href="../' + str(num_pages - 1) + '">&larr; Prev</a>'
#     for i in range(num_pages - 4, num_pages):
#         pagination[i - (num_pages - 4)] = '<a href="../' + str(i) + '">' + str(i) + '</a>'
#     pagination[5] = '<a href="" class="active">' + str(num_pages) + '</a>'
#     pagination[6] = ''
#     html += '\n'.join(pagination)
#     
#     html += consts.PAGINATION_FOOTER
#     html += consts.FOOTER
#     html_pages[len(html_pages) - 1] = html
#     
#     # Now flesh out the html and pagination for the penultimate page
#     html = consts.HEADER
#     for post in posts[-8:-4]:
#         html += post
#     html += consts.PAGINATION_HEADER
#     
#     pagination = [''] * 7
#     pagination[0] = '<a href="../' + str(num_pages-2) + '">&larr; Prev</a>'
#     pagination[1] = '<a href="../' + str(num_pages-4) + '">' + str(num_pages-4) + '</a>'
#     pagination[2] = '<a href="../' + str(num_pages-3) + '">' + str(num_pages-3) + '</a>'
#     pagination[3] = '<a href="../' + str(num_pages-2) + '">' + str(num_pages-2) + '</a>'
#     pagination[4] = '<a href="" class="active">' + str(num_pages-1) + '</a>'
#     pagination[5] = '<a href="../' + str(num_pages) + '">' + str(num_pages) + '</a>'
#     pagination[6] = '<a href="../' + str(num_pages) + '">Next &rarr;</a>'
#     html += '\n'.join(pagination)
#     
#     html += consts.PAGINATION_FOOTER
#     html += consts.FOOTER
#     
#     html_pages[len(html_pages) - 2] = html
# else:
#     # First, flesh out the html and pagination for the last page
#     html = consts.HEADER
#     for post in posts[-num_posts_leftover:]:
#         html += post
#     html += consts.PAGINATION_HEADER
#     
#     pagination = [''] * 7
#     pagination[0] = '<a href="../' + str(num_pages) + '">&larr; Prev</a>'
#     for i in range(num_pages - 3, num_pages + 1):
#         pagination[i - (num_pages - 4)] = '<a href="../' + str(i) + '">' + str(i) + '</a>'
#     pagination[5] = '<a href="" class="active">' + str(num_pages + 1) + '</a>'
#     pagination[6] = ''
#     html += '\n'.join(pagination)
#     
#     html += consts.PAGINATION_FOOTER
#     html += consts.FOOTER
#     html_pages.append(html)
#     
#     # Now flesh out the html and pagination for the penultimate page
#     html = consts.HEADER
#     for post in posts[-(4 + num_posts_leftover):-num_posts_leftover]:
#         html += post
#     html += consts.PAGINATION_HEADER
#     
#     pagination = [''] * 7
#     pagination[0] = '<a href="../' + str(num_pages-1) + '">&larr; Prev</a>'
#     pagination[1] = '<a href="../' + str(num_pages-3) + '">' + str(num_pages-3) + '</a>'
#     pagination[2] = '<a href="../' + str(num_pages-2) + '">' + str(num_pages-2) + '</a>'
#     pagination[3] = '<a href="../' + str(num_pages-1) + '">' + str(num_pages-1) + '</a>'
#     pagination[4] = '<a href="" class="active">' + str(num_pages) + '</a>'
#     pagination[5] = '<a href="../' + str(num_pages+1) + '">' + str(num_pages+1) + '</a>'
#     pagination[6] = '<a href="../' + str(num_pages+1) + '">Next &rarr;</a>'
#     html += '\n'.join(pagination)
#     
#     html += consts.PAGINATION_FOOTER
#     html += consts.FOOTER
#     
#     # -2 because at this point the size of html_pages has increased -.-
#     html_pages[len(html_pages) - 2] = html
# 
# 
# ############################################################################
# # STEP 4: Save the html pages as index.html files into the correct repositories
# ############################################################################
# absolute_path = '/Users/sharonkim/genzcritics.github.io/reviews/page/'
# for page in html_pages:
#     filename = absolute_path + str(html_pages.index(page) + 1) + '/index.html'
#     with open(filename, 'w') as f:
#         try:
#             f.write(page)
#         except:
#             print 'Errored on: ' + filename
