#This is to find whether the scraped URLs are unique or not 
with open('Indore_restaurant_details.txt','rb+') as f:
    seen = set()
    i = 1 
    for line in f:
        line_lower = line.lower()
        if line_lower in seen:
            print(line)
        else:
            seen.add(line_lower)
            print("No duplication on line:{}".format(i))
            i += 1 
