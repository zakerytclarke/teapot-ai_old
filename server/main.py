from teapot import Teapot

teapot = Teapot()

teapot.setMode("qa")

teapot.train("George Washington was the first President of the United States")
teapot.train("George Washington was born on February 22 1732")
teapot.train("Washington's mother was Mary Washington and his father was August Washington")
teapot.train("Washington was a delegate to the First Continental Congress, which was created by the Thirteen Colonies to respond to various laws passed by the British government")

teapot.train("John Adams was the second President of the United States")
teapot.train("The second president of the United States was John Adams")



reply=teapot.reply("Who was the second president of the United States of America")

print(reply)

# teapot.loadScript("I am near <location>")
# teapot.loadScript("at <location>")
# teapot.loadScript("nearby <location>")

# teapot.loadScript("My name is <person>")


# print(teapot.reply("I am near the library"))
