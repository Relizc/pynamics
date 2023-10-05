import pygamepro

pygamepro.Logger.print("&e&lThis is an test demo of logger in pygamepro.&r\nAll formatting codes starts with an && plus color code.\nThe color codes are based of minecraft's color codes: https://minecraft.fandom.com/wiki/Formatting_codes")

print()

pygamepro.Logger.print("&dPrinting with channels")
pygamepro.Logger.print("Hello I am client", pygamepro.CLIENT)
pygamepro.Logger.print("Whassup Client?", pygamepro.SERVER)
pygamepro.Logger.print("Just informing you", pygamepro.INFO)
pygamepro.Logger.print("I'm heating up very quickly", pygamepro.WARNING)
pygamepro.Logger.print("Seems like an error", pygamepro.ERROR)
pygamepro.Logger.print("I need to debug the problem", pygamepro.DEBUG)

print()

pygamepro.Logger.print("&dPrinting with prefixes")
pygamepro.Logger.print("Custom prefix", prefix = "Custom>>")
pygamepro.Logger.print("&aRegular prefix but green log", prefix = "NotMe")
pygamepro.Logger.print("&aPurple prefix but green log", prefix = "&dNotMe")
pygamepro.Logger.print("Everything is blue!", prefix = "&9NotMe")

print()

pygamepro.Logger.print("&dAll color codes")
for item in pygamepro.Logger.__dict__:
    if not item.startswith("_"):
        d = pygamepro.Logger.__dict__[item]
        if isinstance(d, tuple):
            pygamepro.Logger.print(d[0] + " &r- " + d[1] + item)