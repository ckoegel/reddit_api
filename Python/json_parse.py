import json
import os
import sys

path = "/home/ckoegel/Documents/Stock_Analyzer/JSON_Files"
files = os.listdir(path)
for file in files:
	if os.path.isfile(os.path.join(path,file)):
		f = open(os.path.join(path,file),'r')
		print(f)
		txtfile_name = "/home/ckoegel/Documents/Stock_Analyzer/JSON_Files/Parsed/" + file.partition(".")[0] + ".txt"
		print(txtfile_name)
		jfile = json.load(f)
		data = jfile["data"]
		posts = data["children"]
		for k in posts:
			post_data = k["data"]
			if post_data["subreddit"] == "wallstreetbets":
				title = post_data["title"]
				upvotes = post_data["ups"]
				up_ratio = post_data["upvote_ratio"]
				post_type = post_data["link_flair_text"]
				original_stdout = sys.stdout # Save a reference to the original standard output
				print_post = "Title: %s\nUpvotes: %s\nUpvote Ratio: %s\nPost Type: %s\n" % (title, upvotes, up_ratio, post_type)
				with open(txtfile_name, 'a') as p:
					sys.stdout = p # Change the standard output to the file we created.
					print(print_post.encode('utf-8'))
					sys.stdout = original_stdout # Reset the standard output to its original value
	f.close()

