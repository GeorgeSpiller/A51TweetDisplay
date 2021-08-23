import tweepy
import webbrowser
import demoji
from colors import bcolors


def authenticate():

    # read keys and tokens
    KT_raw = open("keys_and_tokens.txt", "r").read().split("\n")
    KeyTokenDict = {}
    for line in KT_raw:
        KeyTokenDict[line.split("=")[0].strip()] = line.split("=")[1].strip().replace("\"", "")
    callback_uri = 'oob' # https://cfe.sh/twitter/callback
    consumer_key = KeyTokenDict["consumer_key"]
    consumer_secret = KeyTokenDict["consumer_secret"]

    # re-uthenticate user
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
    redirect_url = auth.get_authorization_url()
    print(f"{bcolors.OKCYAN}Twitter Authentication{bcolors.ENDC}")
    print("Please press enter, and Python will open the following url:")
    print(f"{bcolors.OKCYAN}\t{redirect_url}{bcolors.ENDC}")
    print("So you can link an account to use with the API. If the link \ndoesn't open, just copy and paste the url into your browser.")
    _ = input("\nPress Enter to continue. ")

    webbrowser.open(redirect_url)
    user_pin_input = input("Please enter the pin: ")
    
    auth.get_access_token(user_pin_input)
    print(f"{bcolors.OKGREEN}Twitter User Auth Accepted!{bcolors.ENDC}")

    return tweepy.API(auth)


def tweetTextToFile(ListOfStrings, fileName):
    
    f = open(f"{fileName}.txt", "w")
    for tweetString in ListOfStrings:
        cleanTweetString = tweetString.strip().replace("\n", " ")
        cleanTweetStringNoEmoji = demoji.replace_with_desc(cleanTweetString)
        f.write(f"{cleanTweetStringNoEmoji}\n")
    f.close()


def getTweets(api, amount):
    tweetStrings = []
    A51Tweets = api.user_timeline(screen_name = 'Arena_51_Gaming', count = amount)
    print(f"{len(A51Tweets)} Tweets recieved.")
    for status in A51Tweets:
        tweetStrings.append(status.text)
    return tweetStrings
    tweetTextToFile(tweetStrings, fileName)


if __name__ == "__main__":
    print(f"{bcolors.FAIL}Please run main.py for full functionality.{bcolors.ENDC}{bcolors.WARNING} This script alone will: \n\tAuthenticate a user\n\tGet @Arena_51_Gaming 's most recent 5 tweets\n\tSave thoes tweet's test to a text file{bcolors.ENDC}")

    api = authenticate()
    tweets = getTweets(api)
    tweetTextToFile(tweets, "recent-tweets")
    exit()