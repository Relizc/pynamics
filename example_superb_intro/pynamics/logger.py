

class Logger:

    # Colors uses the official minecraft color codes: https://minecraft.fandom.com/wiki/Formatting_codes

    BLACK         = ("0", '\u001b[30m')
    DARK_BLUE     = ("1", "\u001b[34m")
    DARK_GREEN    = ("2", "\u001b[32m")
    DARK_CYAN     = ("3", "\u001b[36m")
    DARK_RED      = ("4", "\u001b[31m")
    DARK_PURPLE   = ("5", "\u001b[35m")
    DARK_YELLOW   = ("6", "\u001b[33m")
    GRAY          = ('7', "\u001b[37;1m")
    DARK_GRAY     = ('8', "\u001b[37m")
    BLUE          = ('9', "\u001b[34;1m")
    GREEN         = ('a', "\u001b[32;1m")
    CYAN          = ('b', "\u001b[36;1m")
    RED           = ('c', "\u001b[31;1m")
    PURPLE        = ('d', "\u001b[35;1m")
    YELLOW        = ('e', "\u001b[33;1m")
    WHITE         = ('f', "\u001b[37;1m")
    RESET         = ('r', "\u001b[0m")
    BOLD          = ('l', "\u001b[1m")
    UNDERLINE     = ('n', "\u001b[4m")
    REVERSE       = ("o", "\u001b[7m")
    

    def init():
        import os
        os.system('')

    def colorize(text):
        for i in Logger.__dict__.values():
            if isinstance(i, tuple):
                char = i[0]
                text = text.replace("&" + char, i[1])
        return text + Logger.RESET[1]

    def print(text, channel: object = None, **kwargs: object) -> object:
        if channel != None:
            if channel == 0:
                text = f"&a(Client) {text}"
            elif channel == 1:
                text = f"&b(Server) {text}"
            elif channel == 2:
                text = f"&r(Info) {text}"
            elif channel == 3:
                text = f"&e(Warning) {text}"
            elif channel == 4:
                text = f"&c(Error) {text}"
            elif channel == 5:
                text = f"&9(Debug) {text}"
        if kwargs.get("prefix", None) != None:
            text = f"{kwargs.get('prefix')} {text}"
        print(Logger.colorize(text))