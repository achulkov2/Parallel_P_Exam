# Parallel_P_Exam

In order to run the program you need to run solve.py (Python 3). It requires three dumps from apple.stackexchange.com: Posts.xml, Comments.xml and Users.xml,
which are not included in the repository because of their excessive size (As it was told that doing so is allowed). It also requires an html template (template.html)
and a stylesheet (style.css), both files included in the repository. The output of the program will be written to the file result.html. It will contain a list of 100 posts
with the most unique repliers and commenters.

Technical details/comments:
My program looks through the list of posts and seeks out the author of the post, getting his user id if it is given and his username otherwise. However there are users, who
cannot be found in the user logs (my presumption is that they deleted their accounts), as well as different users with the same username. That raises difficulties in the case
when two users, for whom only the username is given in the post log, share the same name, as they are practically impossible to distinguish. In this case I assume that it is
the same user, as the scenario of one person with only the username known leaving multiple comments is in my opinion more likely than username collisions. 
