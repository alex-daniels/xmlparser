"""
Alex Daniels
CS451

"""

import datetime
import locale
import sys
import xml.dom.minidom

def transform_dollar(dollar_str):
    """
    Returns the amount (in XXXXX.xx format) denoted by a money-string
    like $3,453.23. 
    """
    return '{:.2f}'.format(locale.atof(dollar_str.strip("$")))

def transform_dttm(dttm_str):
    """
    Returns date/time string in format like "2001-03-25 10:25:57" from
    a format like "Mar-25-01 10:25:57".
    """
    dt = datetime.datetime.strptime(dttm_str, "%b-%d-%y %H:%M:%S")  
    return dt.isoformat(' ')

def process_file(filename, itemFile, userFile, bidsFile, catFile):
    """
    Process one items-???.xml file.
    """
    dom = xml.dom.minidom.parse(filename)

    #begin the parsing madness
    itemList = dom.getElementsByTagName('Item')

    itemTable(itemList, itemFile)
    userTable(itemList, userFile)
    bidTable(itemList, bidsFile)
    categoryTable(itemList, catFile)

def itemTable(itemList, itemFile):
    for item in itemList:
        itemList = []
        itemId = item.getAttribute('ItemID')
        itemId.replace('"', '')
        itemList.append("{}<>".format(itemId))

        names = item.getElementsByTagName('Name')
        if(names):
            name = names[0].childNodes[0].data
            newname = name.replace('"', '')
            itemList.append("{}<>".format(newname))
        else:
            name = "NULL"
            itemList.append("{}<>".format(name))

        currPrice = item.getElementsByTagName("Currently")
        if(currPrice):
            price = currPrice[0].childNodes[0].data
            price = transform_dollar(price)
            newprice = price.replace('"', '')
            itemList.append("{}<>".format(newprice))
        else:
            price = "NULL"
            itemList.append("{}<>".format(price))

        buyPrices = item.getElementsByTagName("Buy_Price")
        if (buyPrices):
               buyPrice = buyPrices[0].childNodes[0].data
               buyPrice = transform_dollar(buyPrice)
               newbuyPrice = buyPrice.replace('"', '')
               itemList.append("{}<>".format(newbuyPrice))
        else:
            buyPrice = "NULL"
            itemList.append("{}<>".format(buyPrice))

        firstBid = item.getElementsByTagName("First_Bid")
        if(firstBid):
            bid = firstBid[0].childNodes[0].data
            bid = transform_dollar(bid)
            itemList.append("{}<>".format(bid))

        numBids = item.getElementsByTagName("Number_of_Bids")
        if(numBids):
            bid = numBids[0].childNodes[0].data
            itemList.append("{}<>".format(bid))
       
        timeStart = item.getElementsByTagName("Started")
        if(timeStart):
            start = timeStart[0].childNodes[0].data
            start = transform_dttm(start)
            newstart = start.replace('"', '')
            itemList.append("{}<>".format(newstart))
        else:
            start = "NULL"
            itemList.append("{}<>".format(start))

        timeEnd = item.getElementsByTagName("Ends")
        if(timeEnd):
            end = timeEnd[0].childNodes[0].data
            end = transform_dttm(end)
            newend = end.replace('"', '')
            itemList.append("{}<>".format(newend))
        else:
            end = "NULL"
            itemList.append("{}<>".format(end))

        sellers = item.getElementsByTagName("Seller")
        if(sellers):
            userid = sellers[0].getAttribute("UserID")
            itemList.append("{}<>".format(userid))
        descriptions = item.getElementsByTagName("Description")
        for desc in descriptions:
            if(desc.hasChildNodes()):
                description = desc.childNodes[0].data
                itemList.append("{}".format(description))
            else:
                description = "NULL"
                itemList.append("{}".format(description))

        write_to_file(itemList, itemFile)
        del itemList

def userTable(itemList, userFile):
    for item in itemList:
        userList = []

        sellers = item.getElementsByTagName("Seller")
        if(sellers):
            userid = sellers[0].getAttribute("UserID")
            rating = sellers[0].getAttribute("Rating")
            userList.append("{}<>".format(userid))
            userList.append("{}<>".format(rating))

        locales = item.getElementsByTagName("Location")
        location = locales[len(locales)-1].childNodes[0].data
        newlocation = location.replace('"', '')
        userList.append("{}<>".format(newlocation))
        
        countries = item.getElementsByTagName("Country")
        countryLoc = countries[len(countries)-1].childNodes[0].data
        newcountryLoc = countryLoc.replace('"', '')
        userList.append("{}".format(newcountryLoc))

        write_to_file(userList, userFile)
        del userList

        bids = item.getElementsByTagName("Bid")
        if(bids):
            for bid in bids:
                userList = []
                bidders = bid.getElementsByTagName("Bidder")
                for bidder in bidders:
                    bidderId = bidder.getAttribute("UserID")
                    bidderRating = bidder.getAttribute("Rating")
                    userList.append("{}<>".format(bidderId))
                    userList.append("{}<>".format(bidderRating))

                    locales = bidder.getElementsByTagName("Location")
                    if(locales):
                        locale = locales[0].getElementsByTagName("Location")
                        location = locales[len(locales)-1].childNodes[0].data
                        userList.append("{}<>".format(location))
                    else:
                        location = "Null"
                        userList.append("{}<>".format(location)) 

                    countries = bidder.getElementsByTagName("Country")
                    if(countries):
                        country = countries[0].getElementsByTagName("Country")
                        countryLoc = countries[len(countries)-1].childNodes[0].data
                        userList.append("{}".format(countryLoc))
                    else:
                        nCountry = "Null"
                        userList.append("{}".format(nCountry))

            write_to_file(userList, userFile)
            del userList

def bidTable(itemList, bidFile):
    for item in itemList:
        itemId = item.getAttribute('ItemID')
        bids = item.getElementsByTagName("Bid")
        if(bids):
            for bid in bids:
                bidList = []
                bidList.append("{}<>".format(itemId))
                bidders = bid.getElementsByTagName("Bidder")
                for bidder in bidders:
                    bidderId = bidder.getAttribute("UserID")
                    bidList.append("{}<>".format(bidderId))

                times = bid.getElementsByTagName("Time")
                if(times):
                    time = times[0].childNodes[0].data
                    time = transform_dttm(time)
                    bidList.append("{}<>".format(time))
                amounts = bid.getElementsByTagName("Amount")
                if(amounts):
                    amount = amounts[0].childNodes[0].data
                    amount = transform_dollar(amount)
                    bidList.append("{}".format(amount))

                write_to_file(bidList, bidFile)
                del bidList

def categoryTable(itemList, catFile):
#find all items to fit the category table
    for item in itemList:
        itemId = item.getAttribute('ItemID')
        catList = item.getElementsByTagName('Category')

        for categoryItem in catList:
            categoryList = []
            categoryList.append("{}<>". format(itemId))
            category = categoryItem.childNodes[0].data
            categoryList.append("{}".format(category))
            write_to_file(categoryList, catFile)
            del categoryList
#END
def write_to_file(itemList, fileDat):
#write to specified file
    for i in range(len(itemList)):
        fileDat.write(itemList[i])
    fileDat.write("\n")

def main():
    if len(sys.argv) <= 1:
        print("Usage: python3", sys.argv[0], "[file] [file] ...")

    """
    OSX 10.9 doesn't like en_US.UTF-8 for some reason
    But likes en_US.utf8
    Doing either or for compatibility
    """
    try:
        import locale
        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    except Exception:
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except Exception as e:
            messages.error(request, 'An error occurred: {0}'.format(e))

    itemFile = open('items.dat', 'w')
    userFile = open('users.dat', 'w')
    bidFile = open('bids.dat', 'w')
    catFile = open('categories.dat', 'w')
    
    length = len(sys.argv[1:])
    counter = 1
    print("Processing: ")
    for filename in sys.argv[1:]:
        percent = float(counter) / length
        status = '#' * (int(round(percent * 20)))
        spaces = ' ' * (20 - len(status))
        process_file(filename, itemFile, userFile, bidFile, catFile)
        sys.stdout.write("\r[{0}] {1}%".format(status + spaces, int(round(percent * 100))))
        #sys.stdout.write("\rProcessing Files: %0.1f%%" % ((counter / length) * 100))
        counter += 1

    print("\n")
    
    itemFile.close()
    userFile.close()
    bidFile.close()
    catFile.close()

if __name__ == "__main__":
    main()
