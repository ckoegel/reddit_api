import praw
import sys
import schedule
import time
from datetime import datetime
from client_info import *

now = datetime.now()
txtfile_name = "C:/Users/ckoeg/Documents/Stock_Analyzer/"
dt_string = now.strftime("%b-%d-%Y %H")
txtfile_name = txtfile_name + dt_string + ".txt"
hour_count = 0

def pull_API():
    now = datetime.now()
    dt_string = now.strftime("%b-%d-%Y %H")
    global hour_count
    global txtfile_name
    hour_count = hour_count + 1
    if hour_count >= 24:
        hour_count = 0
        txtfile_name = "C:/Users/ckoeg/Documents/Stock_Analyzer/"
        txtfile_name = txtfile_name + dt_string + ".txt"
    
    
    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, password=my_pass, user_agent="testscript by u/EMerjNC",	username="EMerjNC")
    for submission in reddit.subreddit("pennystocks").new(limit=100):
        original_stdout = sys.stdout # Save a reference to the original standard output
        print_post = "%s`%s`%s`%s`%s`" % (submission.title, submission.score, submission.upvote_ratio, submission.num_comments, submission.created_utc)
        #print_post = "Title: %s\nUpvotes: %s\nUpvote Ratio: %s\nPost Type: %s\n" % (title, upvotes, up_ratio, post_type)
        with open(txtfile_name, 'a') as p:
            sys.stdout = p # Change the standard output to the file we created.
            print(print_post.encode('utf-8'))
            sys.stdout = original_stdout # Reset the standard output to its original value
            p.close()

def timeP():
    print(dt_string)
    #print("Hi")

schedule.every().hour.at(":30").do(timeP)
schedule.every().hour.at(":30").do(pull_API)


while True:
    schedule.run_pending()
    time.sleep(1)