from config import correct_and_find_plates

def main():
    validList = startCapture()
    print("Valid before CFP func:", validList)
    plates = correct_and_find_plates(validList)
    print("Final Corrected Plates:", plates)
    print("ValidLisCount:", len(validList))
    directMatch = 0
    for plat in plates:
        if plat == "131D36617":
            directMatch += 1
    print("Direct Matches:", str(directMatch) + "/" + str(len(plates)))
    quit()

if __name__ == "__main__":
    main()