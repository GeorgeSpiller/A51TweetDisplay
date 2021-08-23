import assemble_tweets as astwt
import TwitterScraper as twtScrp
import ImageManager as imgMagr
from colors import bcolors
import colorama
colorama.init()

def verifyInput(userInput, min, default, max):
    if userInput == "":
        return default
    try:
        int(userInput)
    except ValueError:
        print(f"{bcolors.FAIL}Input must be a number{bcolors.ENDC}")
        exit()
    if min == None:
        min = 0
    if max == None:
        max = float('inf')
    if userInput > max:
        return max
    if userInput < min:
        return min
    return default


print(f"\n{bcolors.BOLD}BRB Screen Recent Tweets GIF Generator{bcolors.ENDC}\n")

# Authenticate user to use twitter API
api = twtScrp.authenticate()

print(f"{bcolors.OKBLUE}Settings.{bcolors.ENDC}")
print(f"{bcolors.OKCYAN}How many tweets to display? More than 8 leads to <400 GIF\n frames, which can take a loong time to compile.{bcolors.ENDC}")
input_amount = input(f" (min: 3, default: 5, recomended max: 8): ")
amount = verifyInput(input_amount, 3, 5, None)
print(f"{bcolors.OKCYAN}How many pixels per frame do you wish the Tweets to move?{bcolors.ENDC}")
input_PPF = input(" (default 20, recomended max: 100): ")
PPF = verifyInput(input_PPF, None, 20, None)
print(f"{bcolors.OKCYAN}What duration (in milliseconds) sould each frame play?{bcolors.ENDC}")
input_duration = input(" (min: 50, default:100, max:2000): ")
duration = verifyInput(input_duration, 50, 100, 2000)

# Get <amount> number of most recent tweets from A51 twitter, save strings to <filename>
# api: The authenticated user client 
# fileName = "recent-tweets", amount=5
tweetStrings = twtScrp.getTweets(api, amount)
twtScrp.tweetTextToFile(tweetStrings, "recent-tweets")

# Convert tweet strings to tweet images
imgMagr.clearOutputDir() # DELETES all files in ./TweetsOut/
tweets = astwt.generateTweetImages()

# Get list of image frames
# speed: How many pixels each image moves per frame 
# saveImages=False
imgList = astwt.SliderAnimation(PPF, tweets)

# Compile image frames to GIF
astwt.ExportGif(imgList, duration)


