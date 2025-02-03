import praw
import csv
import re
import os
import webbrowser

# Reddit API Credentials (Replace with your actual credentials)
REDDIT_CLIENT_ID = "PxnLYXKRvVpFSsNC_MbVig"
REDDIT_CLIENT_SECRET = "OOb1skWiIZ5sots36w3HOruYeD9b9A"
REDDIT_USER_AGENT = "script:sentiment-analysis:v1.0 (by u/MolassesWrong4174)"
REDIRECT_URI = "http://localhost:3000"  # Update with your redirect URI
SCOPES = ['identity', 'read']

# OAuth2 Reddit Authentication Flow
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    redirect_uri=REDIRECT_URI  # Ensure that redirect URI is specified here
)

def authenticate():
    """Authenticate and authorize the script via OAuth."""
    auth_url = reddit.auth.url(scopes=SCOPES, state="unique_state", duration="permanent")
    print(f"Please go to this URL to authenticate: {auth_url}")
    webbrowser.open(auth_url)

    # Get the authorization code from the user
    code = input("Enter the authorization code from the URL: ")

    # Get access token
    access_token = reddit.auth.authorize(code)
    print("Access Token:", access_token)
    return reddit

# Run the function for authentication if required
if __name__ == "__main__":
    reddit = authenticate()

# Function to extract the post ID from the URL
def extract_post_id(url):
    """Extracts the post ID from a Reddit URL."""
    match = re.search(r"comments/([a-z0-9]+)/", url)
    return match.group(1) if match else None

# Function to scrape comments from Reddit
def scrape_comments(url):
    """
    Scrapes comments from a Reddit post or subreddit URL.
    Returns a CSV file with the scraped data.
    """
    post_id = extract_post_id(url)
    
    if post_id:  # If URL is for a single post
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)  # Load all top-level comments

        comments = []
        for comment in submission.comments.list():
            comments.append([
                submission.title,
                comment.author.name if comment.author else "[deleted]",
                comment.body,
                comment.score,
                comment.created_utc
            ])

        filename = "reddit_comments.csv"
    
    else:  # If URL is for a subreddit
        subreddit_name = url.rstrip('/').split('/')[-1]
        subreddit = reddit.subreddit(subreddit_name)
        comments = []

        for submission in subreddit.hot(limit=10):  # Scrape top 10 posts
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                comments.append([
                    submission.title,
                    comment.author.name if comment.author else "[deleted]",
                    comment.body,
                    comment.score,
                    comment.created_utc
                ])

        filename = f"{subreddit_name}_comments.csv"

    # Save to CSV
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Post Title", "Author", "Comment", "Score", "Created UTC"])
        writer.writerows(comments)

    return filename  # Return filename for frontend handling

# Run the function with the manually set URL
if __name__ == "__main__":
    REDDIT_URL = "https://www.reddit.com/r/Nike/"  # Replace with actual Reddit URL
    output_file = scrape_comments(REDDIT_URL)
    print(f"Scraped data saved to {output_file}")
