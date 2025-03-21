from urllib.request import urlopen
import re
from html import unescape

file = open("generate tracker list.txt", "r")
text = file.read()
file.close()
if text == "":
    print("\"generate tracker list.txt\" is empty")
    print("Please open it & input links to the archipelago rooms you want to track, followed by the slots you want to track")
    print("Then run this program again & it will automatically fetch the tracker links & fill in Tracker List.txt")
    print()
    print("For example:")
    print("https://archipelago.gg/room/ABC")
    print("4")
    print("5")
    print("6")
    print("https://archipelago.gg/room/123")
    print("4-6")
    print()
    userInput = input("Press enter to close")
    exit()
fullMatches = re.finditer("(https?:[^\n ]*).*((\n(\d+-\d+|\d+))+)",text)
file = open("Tracker List.txt", "w")
for x in fullMatches:
    numberMatches = re.finditer("((\d+)-(\d+))|(\d+)",x[2])
    numberlist = []
    for y in numberMatches:
        if y[1]:
            for z in range(int(y[2]),int(y[3])+1):
                numberlist.append(z)
        else:
            numberlist.append(int(y[4]))
    page = urlopen(x[1])
    html_bytes = page.read()
    html = unescape(html_bytes.decode("utf-8"))
    for y in numberlist:
        trackerMatch = re.search("<tr>\n.*>{}<.*\n.*>(.*)</a.*\n.*>(.*)<.*(\n.*?)*tracker([^\"]*)".format(y), html)
        try:
            hostSite = re.search("(.*/)room/", x[1])[1]
            file.write("{} ({}): {}generic_tracker{}\n".format(trackerMatch[2], trackerMatch[1], hostSite, trackerMatch[4]))
        except:
            print("Couldn't find slot {} in multiworld at {}\nPlease check that the slot number is correct.".format(y, x[1]))
            print("If this problem occurs for multiple slots, it's likely a temporary connection problem.")
            print()
    file.write("\n")
file.close()
userInput = input("Tracker List.txt updated. Press enter to close")
