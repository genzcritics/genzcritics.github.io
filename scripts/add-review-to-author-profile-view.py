# This script takes care of the time-consuming task of adding a review to the `author-profile` 
# view for each member of Gen Z Critics. All author metadata (name, location, bio) is stored 
# in `author-data.json`. This file parses through the json file and creates all html files with 
# correct pagination numbers and links to the correct articles.

import json
import consts

with open('../author-data.json') as author_data:
    author_entries = json.load(author_data)

with open('../reviews-data.json') as reviews_data:
    review_entries = json.load(reviews_data)


############################################################################
# STEP 1: Ask which author to generate the html for
############################################################################
print '##################################################'
print '#################### hello :) ####################'
print '##################################################'
print '\nHere is a list of all author IDs so you can verify the author ID:'
authors_in_alphabetical_order = sorted(author_entries.keys())
for author_id in authors_in_alphabetical_order:
    if 'anthony-d' in author_id:
        print author_id + ' **for this author, please enter `anthony-d` instead of `'+ author_id + '`'
    else:
        print author_id
print '##################################################'

author = raw_input('Now enter the author ID: ')
while author not in authors_in_alphabetical_order:
    author = raw_input('That author does not exist; please enter the author ID again: ') # TODO: How do you quit out of the program?????


############################################################################
# STEP 2: Flesh out the header for this specific author's profile
############################################################################
header = consts.AUTHOR_HEADER

author_obj = author_entries[author]
s = '<img class="rounded-circle" src="../img/' + author + '.jpg" alt="' + author_obj['name'] + '">'
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
for post in reversed(posts_by_author): # the json is in chronological order; we want to display reverse chronological order
    post_html = '<div class="post-preview"><a href="../../' + post['article'] + '.html">'
    post_html += '<h2 class="post-title">' + post['title'] + '</h2>'
    post_html += '<h3 class="post-subtitle">' + post['subtitle'] + '</h3></a>' if 'subtitle' in post.keys() else '</a>'
    post_html += '<p class="post-meta">by <a href="../../author-profile/' + post['profile'] + '">'
    post_html += post['author'] + '</a> on ' + post['date'] + '</p>'
    post_html += '<a href="../../' + post['article'] + '.html">'
    post_html += '<img class="preview-image" src="../img/' + post['image'] + '"></a></div><hr>\n\n'
    posts.append(post_html)


############################################################################
# STEP 4: Flesh out the complete html code for each page view, depending on 
# how many pages the author requires
############################################################################
html = ''
CLOSE_POSTS_DIV = '</div></div></div><hr>'
reminder_message = ''

num_pages = len(posts) / 4 # TODO: Maybe include an error-catcher here if the value is 0.
num_posts_leftover = len(posts) % 4

# TODO: What if num_pages is 0? Could there be such a scenario?
#   - Probably not. I would probably not have entered in that author's ID at the 
#     beginning if that were the case. But this is an important note for always 
#     posting the review first (i.e., putting in the necessary information in 
#     reviews-data.json, before running this python script.)
if num_pages == 1 and num_posts_leftover == 0: # the author only needs one page
    html = header + reduce((lambda x, y: x + y), posts) + CLOSE_POSTS_DIV + consts.AUTHOR_FOOTER
else: # the author needs multiple pages. Pagination to be done manually.
    reminder_message = '***Remember to manually include pagination for each page!***'
    reminder_message += '\n***Also remember to copy `index.html` from `page/1` to the "root" repo of that author and adjust the pagination for that specific page accordingly.***'
    html_pages = []
    
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

if num_pages == 1 and num_posts_leftover == 0:
    filename = absolute_path + '/index.html'
    with open(filename, 'w') as f:
        try:
            f.write(html)
        except:
            print 'Errored on: ' + filename
else:
    absolute_path += '/page/'
    for page in html_pages:
        filename = absolute_path + str(html_pages.index(page) + 1) + '/index.html'
        with open(filename, 'w') as f:
            try:
                f.write(page)
            except:
                print 'Errored on: ' + filename

print reminder_message
