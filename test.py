
def resolveSpecialCharacters(s):
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    return s.rstrip(punctuation)

string = "Special $#! characters \':/\]0  spaces 888323"

print(resolveSpecialCharacters(string))
