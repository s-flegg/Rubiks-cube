class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()


def convert(c, encrypt):
    """
    :type c: chr
    :param c: character to convert
    :type encrypt: bool
    :param encrypt: True for encryption, False for decryption
    :return: converted chr
    """
    val = ord(c)
    if encrypt:
        val += 10
    else:
        val -= 10

    # ensure characters remain as printable characters, loops between 32 and 127
    if val < 32:
        val = 127 - (31 - val)
    if val > 127:
        val = 31 + (val - 127)

    return chr(val)


def file(location, encrypt):
    """
    Encrypts/ decrypts an entire file
    Only non-printable character in file should be newline
    :type location: str
    :param location: path to file
    :type encrypt: bool
    :param encrypt: True or False, encrypt or decrypt respectively
    :return: None
    """

    # reads entire file as string
    with open(location, "w") as f:
        # variable creation to allow access at these indentation levels
        converted = ""

        # reads each character one by one
        to_convert = f.read()

        # iterate through string, character by character
        for c in to_convert:
            val = ord(c)
            # skip newline characters
            if val != 10:
                converted += convert(c, encrypt)

        f.write(converted)


def string(s, encrypt):
    """
    Encrypts/decrypts given string
    :type s: str
    :param s: string to convert, no non-printable characters
    :type encrypt: bool
    :param encrypt: True to encrypt, False to decrypt
    :return: converted string
    """

    # initialise variable
    converted = ""

    # iterate through string by each character
    for c in s:
        converted += convert(c, encrypt)

    return converted
