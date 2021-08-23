from ImageManager import createTweetImage
from PIL import Image
import os
import time
from colors import bcolors

TWEET_SCREENSHOT_DIR = os.path.abspath(os.getcwd() + "\\TweetsOut")
GIF_RAW_DIR = os.path.abspath(os.getcwd() + "\\bin")
TWEET_SIZE = (800, 800)
CANVAS_SIZE = (1920, 1080)
Y_START_VALUE = 80

def generateTweetImages():
    # generate indevidual tweet images
    tweet_data_raw = open("recent-tweets.txt", "r").read().split("\n")
    tweet_data = [i for i in tweet_data_raw if i]
    for tweetIndex in range(len(tweet_data)):
        print(f"Creating Tweet: {tweetIndex+1}/{len(tweet_data)}", end='\r')
        createTweetImage(tweet_data[tweetIndex], f"tweet-{tweetIndex}")

    tweets = []
    for file in os.listdir(TWEET_SCREENSHOT_DIR):
        filename = os.fsdecode(file)
        if filename.endswith(".png"): 
            tweets.append(os.path.join(TWEET_SCREENSHOT_DIR, filename))
    
    return tweets


def getHighestTweet(tweets):
    heights = []
    for tweet in tweets:
        im_currTweet = Image.open(tweet, "r")
        im_currTweet.thumbnail(TWEET_SIZE)
        heights.append(im_currTweet.size[1])
    return max(heights)


def SliderAnimation(speed, tweets, saveImages=False):
    '''
    speed: how many pixels the tweets move in each frame
    '''
    TQ = []
    imageSequnce = []
    TopTweetFlag = False
    BotTweetFlag = False
    nameItter = 0
    FirstTweetPos = -400
    tweetPaddingY = (CANVAS_SIZE[1] -(getHighestTweet(tweets)*2))//3
    tweetPaddingX = 60
    bottomRowY = CANVAS_SIZE[1] - (tweetPaddingY+getHighestTweet(tweets)) # CANVAS_SIZE[1] - TWEET_SIZE[1]//2 - tweetPadding
    topRowY = tweetPaddingY # 80
    background = Image.open('resources/A51-BK.png', 'r')
    

    for i in range(len(tweets)):
        tweetStartPos = FirstTweetPos + (TWEET_SIZE[0] + tweetPaddingX)*i
        TQ.append([tweets[i], tweetStartPos, tweetStartPos])

    anchor = TQ[0][1] - speed
   
    while TQ[0][1] not in range(anchor-speed, anchor+speed):
        nameItter +=1
        print(f"{bcolors.WARNING} Compiling GIF Frame:{bcolors.ENDC} {nameItter}", end='\r')
        # update TQ
        for tweetTuple in TQ:
            tweetTuple[1] += speed
            tweetTuple[2] -= speed

        # create canvas
        img = Image.new('RGB', (1920,1080), color='white')
        img.paste(background, (0,0))

        for tweet in TQ:
            TopTweetFlag = True
            BotTweetFlag = True
            # check if image end does not reach the canvas
            if (tweet[1] + TWEET_SIZE[0] + tweetPaddingX < 0):
                TopTweetFlag = False
            if (tweet[2] + TWEET_SIZE[1] + tweetPaddingX < 0):
                # if lower tweet doesnt, then move the image pos to be the highest
                highestPos = max([x[2] for x in TQ])
                tweet[2] = highestPos + TWEET_SIZE[0] + tweetPaddingX
                BotTweetFlag = False
            # check if image start does not reach the canvas
            if (tweet[1] > 1920):
                # if it doesnt, then move the image pos to be the lowest
                lowestPos = min([x[1] for x in TQ])
                tweet[1] = lowestPos - (TWEET_SIZE[0] + tweetPaddingX)
                TopTweetFlag = False
            if (tweet[2] > 1920):
                BotTweetFlag = False

            if (TopTweetFlag or BotTweetFlag):
                im_currTweet = Image.open(tweet[0], "r")
                im_currTweet.thumbnail(TWEET_SIZE)
            else:
                continue

            if TopTweetFlag:
                img.paste(im_currTweet, (tweet[1], topRowY))
            if BotTweetFlag:
                img.paste(im_currTweet, (tweet[2], bottomRowY))
        
        imageSequnce.append(img)
        if saveImages:
            try:
                path=f'{GIF_RAW_DIR}\\frame-{nameItter}.png'
                img.save(path)
            except OSError:
                result = True
                path=f'{GIF_RAW_DIR}\\frame-{nameItter}.png'
                dots = 3
                while result:
                    try: 
                        img.save(path)
                        result = False
                    except OSError:
                        time.sleep(0.5)
                        result = True
                        dots +=1
                        dotString = "."*dots
                        print(f"OS Error {dotString}", end='\r')

    print()
    print(f"{bcolors.OKGREEN}Done! {bcolors.ENDC}{nameItter}")
    return imageSequnce
    

def ExportGif(imgList,duration, name="OUT"):
    print(" Exporting GIF...", end='\r')
    if imgList == None:
        images = []
        for file in os.listdir(GIF_RAW_DIR):
            filename = os.fsdecode(file)
            if filename.endswith(".png"): 
                imagePath = os.path.join(GIF_RAW_DIR, filename)
                images.append(Image.open(imagePath, "r"))
    else:
        images = imgList
    images[0].save(f'{name}.gif',
               save_all=True, append_images=images[1:], optimize=True, loop=0, duration=duration)
    print(f"{bcolors.OKGREEN}GIF Exported as {name}.gif{bcolors.ENDC}")
    


if __name__ == "__main__":
    print(f"{bcolors.FAIL}Please run main.py for full functionality.{bcolors.ENDC}{bcolors.WARNING} This script alone will:\n\tConvert all tweets in recent-tweets.txt to images\n\tCompile GIF frames of all tweets in a sliding animation\n\tExport thoes GIF frames.{bcolors.ENDC}")

    tweets = generateTweetImages()
    frames = SliderAnimation(40, tweets)
    ExportGif(frames, "SampleGif")
    exit()


