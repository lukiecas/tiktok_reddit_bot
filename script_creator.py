import praw
import os
reddit = praw.Reddit(client_id='OCCThCqol3C9RYbKgOFdeg',
                     client_secret='5j47nUj0NZq5Br1ikVaTS6GnFupcRA',
                     user_agent='<console:redditpostcollector:1.0>')
sub_name = input("enter subreddit name: ")
i = 0
for submission in reddit.subreddit(sub_name).top(time_filter="all", limit=1000):
    text = submission.title + submission.selftext 
    title = submission.title.replace(" " , "_")
    text = text.replace("AITA", "Am I in the wrong")
    with open(f'./{sub_name}/{i}.txt', 'w') as f:
        f.write(text)
    i = i+1


