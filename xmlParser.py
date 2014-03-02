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

    for item in itemList:
        listList = []
        itemList = []
        cateList = []
        bidList = []
        bidderList = []
        sellerList = []
        descriptionList = []

        itemId = item.getAttribute('ItemID')

        itemList.append("{}<>".format(itemId))
        cateList.append("{}<>".format(itemId))
        bidList.append("{}<>".format(itemId))
        bidderList.append("{}<>".format(itemId))
        sellerList.append("{}<>".format(itemId))
        descriptionList.append("{}<>".format(itemId))
        
        nList = item.getElementsByTagName('Name')
        for names in nList:
            name = names.childNodes[0].nodeValue
            itemList.append("{}<>".format(name))
        
        catList = item.getElementsByTagName('Category')
        for categoryItem in catList:
            category = categoryItem.childNodes[0].nodeValue
            listList.append("{}<>".format(category))
        
        currPrice = item.getElementsByTagName("Currently")
        for prices in currPrice:
            price = prices.childNodes[0].nodeValue
            price = transform_dollar(price)
            itemList.append("{}<>".format(price))
        
        buyPrices = item.getElementsByTagName("Buy_Price")
        if (buyPrices):
            for buy in buyPrices:
               buyPrice = buy.childNodes[0].nodeValue
               itemList.append("{}<>".format(buyPrice))
        else:
            buyPrice = "Null"
            itemList.append("{}<>".format(buyPrice))

        bids = item.getElementsByTagName("Bid")
        if(bids):
            for bid in bids:
                bidders = bid.getElementsByTagName("Bidder")
                for bidder in bidders:
                    bidderId = bidder.getAttribute("UserID")
                    bidderRating = bidder.getAttribute("Rating")
                    listList.append("{}<>".format(bidderId))
                    listList.append("{}<>".format(bidderRating))

                    locales = bidder.getElementsByTagName("Location")
                    if(locales):
                        for locale in locales:
                            location = locale.childNodes[0].nodeValue
                            listList.append("{}<>".format(location))
                    else:
                        location = "Null"
                        listList.append("{}<>".format(location)) 

                    countries = bidder.getElementsByTagName("Country")
                    if(countries):
                        for country in countries:
                            nCountry = country.childNodes[0].nodeValue
                            listList.append("{}<>".format(nCountry))
                    else:
                        nCountry = "Null"
                        listList.append("{}<>".format(nCountry))

                bidTimes = bid.getElementsByTagName("Time")
                if(bidTimes):
                    for bidTime in bidTimes:
                        bTime = bidTime.childNodes[0].nodeValue
                        bTime = transform_dttm(bTime)
                        listList.append("{}<>".format(bTime))
                else:
                    bTime = "Null"
                    listList.append("{}<>".format(bTime))

                amounts = bid.getElementsByTagName("Amount")
                if(amounts):
                    for amount in amounts:
                        bidPrice = amount.childNodes[0].nodeValue
                        bidPrice = transform_dollar(bidPrice)
                        listList.append("{}<>".format(bidPrice))
                else:
                    bidPrice = "Null"
                    listList.append("{}<>".format(bidPrice))
        else:
            listList.append("Null<>")

        firstBid = item.getElementsByTagName("First_Bid")
        for bids in firstBid:
            bid = bids.childNodes[0].nodeValue
            bid = transform_dollar(bid)
            listList.append("{}<>".format(bid))
        
        numBids = item.getElementsByTagName("Number_of_Bids")
        for bids in numBids:
            bid = bids.childNodes[0].nodeValue
            listList.append("{}<>".format(bid))
        
        locales = item.getElementsByTagName("Location")
        for locale in locales:
            location = locale.childNodes[0].nodeValue
            itemList.append("{}<>".format(location))
        
        countries = item.getElementsByTagName("Country")
        for country in countries:
            countryLoc = country.childNodes[0].nodeValue
            itemList.append("{}<>".format(countryLoc))

        timeStart = item.getElementsByTagName("Started")
        for starts in timeStart:
            start = starts.childNodes[0].nodeValue
            start = transform_dttm(start)
            itemList.append("{}<>".format(start))

        timeEnd = item.getElementsByTagName("Ends")
        for ends in timeEnd:
            end = ends.childNodes[0].nodeValue
            end = transform_dttm(end)
            itemList.append("{}".format(end))

        sellers = item.getElementsByTagName("Seller")
        for seller in sellers:
            userid = seller.getAttribute("UserID")
            rating = seller.getAttribute("Rating")
            listList.append("{}<>".format(userid))
            listList.append("{}<>".format(rating))

        descriptions = item.getElementsByTagName("Description")
        for desc in descriptions:
            if(desc.hasChildNodes()):
                description = desc.childNodes[0].nodeValue
                descriptionList.append("{}".format(description))
            else:
                description = "Null"
                descriptionList.append("{}".format(description))

        write_to_file(itemList, itemFile)
        write_to_file(cateList, categoryFile)
        write_to_file(bidList, bidsFile)
        write_to_file(bidderList, bidderFile)
        write_to_file(sellerList, sellerFile)
        write_to_file(descriptionList, descriptionFile)
        del itemList
        del catList
        del bidList
        del bidderList
        del sellerList
        del descriptionList
        del listList

def write_to_file(itemList, fileDat):
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