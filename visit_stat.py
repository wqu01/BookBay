#visit_stats.py
#Author: Ebenezer Reyes
#any person may use this file, howerever there is
#very little reuse value.
#stats for Book and user visits.

from datetime import * #for timing between visits.
# each user will have a homepage
# in each homepage they will have
# recommendations. 6 of them to be
# exact. 3 will be from previos
# users that they have visited.
# the rest will be from books
# they have viewed.


def timediff(time): 
    t = datetime.now() - time
    return(t.seconds)
### stats based on the user_visit_history
def Top3User(user,first_time = False):
    size = len(user.user_visit_set.all()) # list of previos users visited.
    ul = []
    for i in range(size):
        ul.append(user.user_visit_set.all()[i])
## now, I create a dict with each different user ID and the number of visits
## timediff enter a time and get the difference between that time and now in seconds.
## time objects have to be create by the function datetime.now() in order
## for this function to work.
    now = datetime.now()
    visit_freq = dict()

    for i in ul:
        try:
            visit_freq[i.User.id] += 1.0 / timediff(i.DateTime)
        except Exception:
            visit_freq[i.id] = 1.0 /timediff(i.DateTime)

    for i in [(k, visit_freq[k]) for k in sorted(visit_freq, key=visit_freq.get, reverse = True)][0:3]:
        yield(i)

## visit_freq has a key for each user and a value equal to each

def Top3Books(user):
    pass