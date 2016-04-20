import xml.etree.ElementTree as ET

posts = ET.parse("Posts.xml")
posts_root = posts.getroot()

comments = ET.parse("Comments.xml")
comments_root = comments.getroot()

users = ET.parse("Users.xml")
users_root = users.getroot()

name_to_user_id = dict()
user_id_to_name = dict()
for child in users_root:
    name_to_user_id[child.attrib['DisplayName']] = int(child.attrib['Id'])
    user_id_to_name[int(child.attrib['Id'])] = child.attrib['DisplayName']


def get_post_owner_id(attributes):
    if attributes.get('OwnerUserId') is not None:
        return int(attributes['OwnerUserId'])
    else:
        try:
            return int(name_to_user_id[attributes['OwnerDisplayName']])
        except KeyError:
            return None


def get_post_owner_name(attributes):
    if attributes.get('OwnerDisplayName') is not None:
        return attributes['OwnerDisplayName']
    else:
        try:
            return user_id_to_name[int(attributes['OwnerUserId'])]
        except KeyError:
            return "This_is_not_supposed_to_appear_anywhere_in_users_xml"


def get_comment_owner_id(attributes):
    if attributes.get('UserId') is not None:
        return int(attributes['UserId'])
    else:
        try:
            return int(name_to_user_id[attributes['UserDisplayName']])
        except KeyError:
            return None


def get_comment_owner_name(attributes):
    if attributes.get('UserDisplayName') is not None:
        return attributes['UserDisplayName']
    else:
        try:
            return user_id_to_name[int(attributes['UserId'])]
        except KeyError:
            return "This_is_not_supposed_to_appear_anywhere_in_users_xml"


class Event:
    def __init__(self, attributes, is_post):
        self.is_post = int(is_post)
        self.id = int(attributes['Id'])
        if is_post:
            if attributes.get('ParentId') is not None:
                self.parent_id = int(attributes['ParentId'])
            else:
                self.parent_id = self.id
            self.owner_id = get_post_owner_id(attributes)
            self.owner_name = get_post_owner_name(attributes)
            self.text = attributes['Body']
            try:
                self.title = attributes['Title']
            except KeyError:
                self.title = ""
            self.post_type = int(attributes['PostTypeId'])
        else:
            self.parent_id = int(attributes['PostId'])
            self.owner_id = get_comment_owner_id(attributes)
            self.owner_name = get_comment_owner_name(attributes)
            self.text = attributes['Text']


max_index = Event(posts_root[-1].attrib, True).id
question_list = [set() for i in range(max_index + 1)]
question_indexes = [i for i in range(max_index + 1)]
question_dict = dict()

for child in posts_root:
    post = Event(child.attrib, True)
    question_list[post.parent_id].add((post.owner_id, post.owner_name))
    question_dict[post.id] = post

for child in comments_root:
    comment = Event(child.attrib, False)
    question_list[question_dict[comment.parent_id].parent_id].add((comment.owner_id, comment.owner_name))

question_indexes.sort(key=lambda index: len(question_list[index]), reverse=True)

template = open("template.html", "r")
result = open("result.html", "w")
beginning_length = 16
html_beginning = ""
html_ending = ""
html_middle = ""

for i in range(beginning_length):
    html_beginning += template.readline()

while template:
    s = template.readline()
    if s == "":
        break
    html_ending += s


def get_html_string(answer, size, number):
    b = '<div><p class = "list_left"><b>{0}. </b><a href="http://www.apple.stackexchange.com/questions/{1}">{2}</a></p>'
    e = '<p class="list_right">{3}</p></div><div style="clear: both;"></div>\n'
    return (b + e).format(number, answer.id, answer.title, size)


for i in range(1, 251):
    html_middle += get_html_string(question_dict[question_indexes[i]], len(question_list[question_indexes[i]]), i)

result.write(html_beginning + html_middle + html_ending)
