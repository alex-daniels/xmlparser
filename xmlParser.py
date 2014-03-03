import datetime
import locale
import sys
import xml.dom.minidom

itemFile = open('items.dat', 'w')
categoryFile = open('category.dat', 'w')
bidsFile = open('bids.dat', 'w')
bidderFile = open('bidders.dat', 'w')
sellerFile = open('sellers.dat', 'w')
descriptionFile = open('descriptions.dat', 'w')

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

def process_file(filename):
    """
    Process one items-???.xml file.
    """
    dom = xml.dom.minidom.parse(filename)

    #begin the parsing madness
    #still somewhat efficient!
    itemList = dom.getElementsByTagName('Item')

    procItemTable(itemList)
    procCatTable(itemList)
    procBidTable(itemList)
    procBidderTable(itemList)
    procSellerTable(itemList)
    procDescTable(itemList)
    """
    locales = item.getElementsByTagName("Location")
        for locale in locales:
            location = locale.childNodes[0].nodeValue
            itemList.append("{}<>".format(location))
        
        countries = item.getElementsByTagName("Country")
        for country in countries:
            countryLoc = country.childNodes[0].nodeValue
            itemList.append("{}<>".format(countryLoc))
    """



def procItemTable(itemList):
#find all items to fit the item table schema
    for item in itemList:
        itemList = []
        itemId = item.getAttribute('ItemID')
        itemList.append("{}<>".format(itemId))

        nList = item.getElementsByTagName('Name')
        if(nList):
            for names in nList:
                name = names.childNodes[0].nodeValue
                itemList.append("{}<>".format(name))
        else:
            name = "NULL"
            itemList.append("{}<>".format(name))

        currPrice = item.getElementsByTagName("Currently")
        if(currPrice):
            for prices in currPrice:
                price = prices.childNodes[0].nodeValue
                price = transform_dollar(price)
                itemList.append("{}<>".format(price))
        else:
            price = "NULL"
            itemList.append("{}<>".format(price))

        buyPrices = item.getElementsByTagName("Buy_Price")
        if (buyPrices):
            for buy in buyPrices:
               buyPrice = buy.childNodes[0].nodeValue
               itemList.append("{}<>".format(buyPrice))
        else:
            buyPrice = "NULL"
            itemList.append("{}<>".format(buyPrice))

        timeStart = item.getElementsByTagName("Started")
        if(timeStart):
            for starts in timeStart:
                start = starts.childNodes[0].nodeValue
                start = transform_dttm(start)
                itemList.append("{}<>".format(start))
        else:
            start = "NULL"
            itemList.append("{}<>".format(start))

        timeEnd = item.getElementsByTagName("Ends")
        if(timeEnd):
            for ends in timeEnd:
                end = ends.childNodes[0].nodeValue
                end = transform_dttm(end)
                itemList.append("{}".format(end))
        else:
            end = "NULL"
            itemList.append("{}".format(end))

        """
        locales = item.getElementsByTagName("Location")
        for locale in locales:
            location = locale.childNodes[0].nodeValue
            itemList.append("{}<>".format(location))
        
        countries = item.getElementsByTagName("Country")
        for country in countries:
            countryLoc = country.childNodes[0].nodeValue
            itemList.append("{}<>".format(countryLoc))
        """
        write_to_file(itemList, itemFile)
        del itemList
#END
def procCatTable(itemList):
#find all items to fit the category table
    for item in itemList:
        itemId = item.getAttribute('ItemID')
        catList = item.getElementsByTagName('Category')

        for categoryItem in catList:
            categoryList = []
            categoryList.append("{}<>". format(itemId))
            category = categoryItem.childNodes[0].nodeValue
            categoryList.append("{}".format(category))
            write_to_file(categoryList, categoryFile)
            del categoryList
#END
def procBidTable(itemList):
#find all items to fit bid table
    for item in itemList:
        bidList = []
        itemId = item.getAttribute('ItemID')
        bidList.append("{}<>".format(itemId))

        firstBid = item.getElementsByTagName("First_Bid")
        for bids in firstBid:
            bid = bids.childNodes[0].nodeValue
            bid = transform_dollar(bid)
            bidList.append("{}<>".format(bid))
        
        numBids = item.getElementsByTagName("Number_of_Bids")
        for bids in numBids:
            bid = bids.childNodes[0].nodeValue
            bidList.append("{}".format(bid))

        write_to_file(bidList, bidsFile)
        del bidList
#END
def procBidderTable(itemList):
#find all items to fit bidder table    
    for item in itemList:
        bidderList = []
        itemId = item.getAttribute('ItemID')
        bidderList.append("{}<>".format(itemId))

        bids = item.getElementsByTagName("Bid")
        if(bids):
            for bid in bids:
                bidders = bid.getElementsByTagName("Bidder")
                for bidder in bidders:
                    bidderId = bidder.getAttribute("UserID")
                    bidderRating = bidder.getAttribute("Rating")
                    bidderList.append("{}<>".format(bidderId))
                    bidderList.append("{}<>".format(bidderRating))

                    locales = bidder.getElementsByTagName("Location")
                    if(locales):
                        for locale in locales:
                            location = locale.childNodes[0].nodeValue
                            bidderList.append("{}<>".format(location))
                    else:
                        location = "Null"
                        bidderList.append("{}<>".format(location)) 

                    countries = bidder.getElementsByTagName("Country")
                    if(countries):
                        for country in countries:
                            nCountry = country.childNodes[0].nodeValue
                            bidderList.append("{}<>".format(nCountry))
                    else:
                        nCountry = "Null"
                        bidderList.append("{}<>".format(nCountry))

                bidTimes = bid.getElementsByTagName("Time")
                if(bidTimes):
                    for bidTime in bidTimes:
                        bTime = bidTime.childNodes[0].nodeValue
                        bTime = transform_dttm(bTime)
                        bidderList.append("{}<>".format(bTime))
                else:
                    bTime = "Null"
                    bidderList.append("{}<>".format(bTime))

                amounts = bid.getElementsByTagName("Amount")
                if(amounts):
                    for amount in amounts:
                        bidPrice = amount.childNodes[0].nodeValue
                        bidPrice = transform_dollar(bidPrice)
                        bidderList.append("{}".format(bidPrice))
                else:
                    bidPrice = "NULL"
                    bidderList.append("{}".format(bidPrice))
        else:
            bidderList.append("NULL")

        write_to_file(bidderList, bidderFile)
        del bidderList
#END
def procSellerTable(itemList):
#find all items to fit seller table 
    for item in itemList:
        sellerList = []
        itemId = item.getAttribute('ItemID')
        sellerList.append("{}<>".format(itemId))

        sellers = item.getElementsByTagName("Seller")
        for seller in sellers:
            userid = seller.getAttribute("UserID")
            rating = seller.getAttribute("Rating")
            sellerList.append("{}<>".format(userid))
            sellerList.append("{}".format(rating))

        write_to_file(sellerList, sellerFile)
        del seller
#END
def procDescTable(itemList):
#find all items to fit description table
    for item in itemList:
        descList = []
        itemId = item.getAttribute('ItemID')
        descList.append("{}<>".format(itemId))

        descriptions = item.getElementsByTagName("Description")
        for desc in descriptions:
            if(desc.hasChildNodes()):
                description = desc.childNodes[0].nodeValue
                descList.append("{}".format(description))
            else:
                description = "NULL"
                descList.append("{}".format(description))

        write_to_file(descList, descriptionFile)
        del descList
#END
def write_to_file(itemList, fileDat):
#write to specified file
    for i in range(len(itemList)):
        fileDat.write(itemList[i])
    fileDat.write("\n")

def main():
    if len(sys.argv) <= 1:
        print("Usage: python3", sys.argv[0], "[file] [file] ...")

    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

    for filename in sys.argv[1:]:
        process_file(filename)

    itemFile.close()
    categoryFile.close()
    bidsFile.close()
    bidderFile.close()
    sellerFile.close()
    descriptionFile.close()

if __name__ == "__main__":
    main()