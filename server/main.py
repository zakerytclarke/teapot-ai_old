from teapot import Teapot

teapot = Teapot()

# print(teapot.reply("John is from Arizona."))

teapot.train("George Washington was the first President of the United States")
# teapot.train("George Washington was born on February 22 1732")
# teapot.train("Washington's mother was Mary Washington and his father was August Washington")
# teapot.train("Washington was a delegate to the First Continental Congress, which was created by the Thirteen Colonies to respond to various laws passed by the British government")

#teapot.train("John Adams was the second President of the United States")
teapot.train("The second president of the United States was John Adams")

# teapot.viewKnowledge()

reply=teapot.reply("Who was George Washington")

print(reply)

reply=teapot.reply("Who was the second president of the United States")

print(reply)