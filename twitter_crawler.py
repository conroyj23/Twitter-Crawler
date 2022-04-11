# test.py

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import const # ***NOTE: A 'const' file is requried to run, using twitter developer acc keys. This has not been provided for confidentiality.
import tweepy
from tweepy import Stream

# A listener handles tweets that are received from the stream.
# This is a basic listener that prints recieved tweets to standard output
class TweetListener(Stream):

    def onData(self, data):  # return data
        print(data)
        return True

    def onError(self, status):  # return status on error
        print(status)


def main():
    # Set up auth using my developer account keys, enable the api with this auth
    auth = tweepy.OAuthHandler(const.CONSUMER_KEY, const.CONSUMER_SECRET)
    auth.set_access_token(const.ACCESS_TOKEN, const.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    # client = tweepy.Client(bearer_token=const.BEARER_TOKEN)

    # Try/Catch verify the twitter api and set up twitter stream with the keys
    try:
        api.verify_credentials()
        print('Verification Successful.')
    except:
        print('Authentication Error.')
    twitterStream = Stream(const.CONSUMER_KEY, const.CONSUMER_SECRET, const.ACCESS_TOKEN, const.ACCESS_TOKEN_SECRET)

    # Task 1
    users = api.lookup_users(screen_name = {"github", "twitter"})
    task_one(users)

    # Prints each user's bidirectional friendships & follower data
    # Task 2
    print("\t\t\t\t********* Begin Task 2: *********")
    users = api.lookup_users(screen_name={"github", "twitter", "ud_conroyj4", "ud_tweepycrawler"})
    for user in users:  # for each user in the list of users
        friendships = []
        friendshipCount = 0
        followers = []
        name = user.screen_name
        for follower in user.followers():  # grabs latest 20 followers of the current user
            followers.append(follower.screen_name) # add follower's name to followers list
            # grabs friendship data of user and follower
            friendship = api.get_friendship(source_screen_name=user.screen_name,
                                             target_screen_name=follower.screen_name)
            if friendship[0].following == True:  # if user is following their follower:
                friendships.append(follower.screen_name)  # add follower to friendship list
                friendshipCount += 1  # increase friendship count

        print(f"{user.screen_name}'s Account Statistics: ")
        print(f"Number of bidirectional friendships: {friendshipCount}")
        print(f"Screen names of bidirectional friendships: {friendships}")

        print(f"The number of followers: {user.followers_count}")
        print(f"Names of followers: {followers}")  # API.get_followers()
        print("\n--------------------------------------------------------------------------------------------------")
    print("\t\t\t\t********* End Task 2 *********\n")

    # Task 3a
    print("\t\t\t\t********* Begin Task 3a: *********")
    # Grabs 50 most recent tweets containing the terms 'Ohio' AND 'weather'
    tweets = api.search_tweets(q="Ohio AND weather", count=50)
    counter = 1
    for tweet in tweets:
        print(f"\tTweet {counter}: \n{tweet.text}\n\n")
        counter += 1
    print("\t\t\t\t********* End Task 3a *********\n")

    # Task 3b
    print("\t\t\t\t********* Begin Task 3b: *********")
    # Grabs 50 most recent tweets within the 25 mile radius of these dayton region coordinates
    tweets = api.search_tweets(q="", geocode="39.758949,-84.191605,25mi", count=50)
    counter = 1
    for tweet in tweets:
        print(f"\tTweet {counter}: \n{tweet.text}\n\n")
        counter += 1
    print("\t\t\t\t********* End Task 3b *********\n")

    # Task 4
    # Grabs the 3 popular tweets from TheHackerNews in the past week
    # emails them to user
    print("\t\t\t\t********* Begin Task 4: *********")
    print("Task 4 is my own idea,\nThe code grabs 3 popular tweets from TheHackerNews in the past week, "
          "then emails them to the user (receiver_email)")

    # grabs 3 most popular tweets from the past couple weeks from TheHackerNews that aren't retweets
    tweets = api.search_tweets(q="from:TheHackersNews -is:retweet", result_type="popular", count=3)
    emailBody = ""
    counter = 1

    # loops through every tweet, and appends the tweet # and the tweet's text to 'body'
    for tweet in tweets:
        print(f"\tTweet {counter}: \n{tweet.text}\n\n")
        emailBody += f"Tweet {counter}:\n{tweet.text}\n\n"
        counter += 1

    # Setting sender & receiver emails
    sender_email = "jackstwitternews@gmail.com"
    receiver_email = "jackstwitternews@gmail.com"
    password = "" # password removed from GitHub publication for confidentiality

    # Setting the email subject and addresses
    message = MIMEMultipart("alternative")
    message["Subject"] = "The Hacker News - 3 Popular Tweets"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Setting the Text of the email
    text = f"""\
    {emailBody}"""
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    # Sends email using SMTP
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    print("3 Hacker News Tweets Sent")
    print("\t\t\t\t********* End Task 4 *********\n")

    return  # end main


def task_one(users):
    print("\t\t\t\t********* Begin Task 1: *********")
    for user in users:
        print("\nUser name: ", user.name)
        print("Screen Name: ", user.screen_name)
        print("User ID: ", user.id)
        print("Location: ", user.location)
        print("User description: ", user.description)
        print("The number of followers: ", user.followers_count)
        print("The number of friends: ", user.friends_count)
        print("The number of tweets (i.e., statuses): ", user.statuses_count)
        print("User URL: ", user.url)
        print("\n--------------------------------------------------------------------------------------------------")
    print("\t\t\t\t********* End Task 1 *********\n")


# call main()
if __name__ == '__main__':
    main()

