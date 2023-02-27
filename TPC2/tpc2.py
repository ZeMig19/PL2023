import sys

def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def main():
    sum = 0
    process_input = True
    for line in sys.stdin:
        line = line.strip()
        for word in line.split():
            if word.lower() == "off":
                process_input = False
            elif line.lower() == "on":
                process_input = True
            elif process_input == True and is_number(word):
                sum += int(word)
            else:
                numb_str = ""
                for l in word:
                    if process_input == True and is_number(l):
                        numb_str = numb_str + l
                    else:
                        if is_number(numb_str):
                            sum += int(numb_str)
                            numb_str = ""
                    if process_input == True and "=" == l:
                        print(sum)
                        sum = 0
                if is_number(numb_str):
                    sum += int(numb_str)
                    numb_str = ""

if __name__ == "__main__":
    main()