def ordinalize(cardinal):
    cardinal = str(cardinal)
    if cardinal.endswith("1") and not cardinal.endswith("11"):
        cardinal += "st"
    elif cardinal.endswith("2") and not cardinal.endswith("12"):
        cardinal += "nd"
    elif cardinal.endswith("3") and not cardinal.endswith("13"):
        cardinal += "rd"
    else:
        cardinal += "th"
    return cardinal
