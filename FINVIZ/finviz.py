import requests, time, datetime, ast, sys
from bs4 import BeautifulSoup as bs
from multiprocessing.pool import ThreadPool as Pool
from ast import literal_eval


# Webscrape and convert data into hash table, return as stockdata
class getdata():
    def __init__(self, stock):
        self.stock = stock
        self.stockdata = {}
        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
        url = "https://finviz.com/quote.ashx?t=" + str(stock)
        page = requests.get(url, headers = headers)
        soup = bs(page.content,"html.parser")#bs(page.content,"html")
        table = soup.find('table', class_ = "snapshot-table2")
        rows = table.findAll("tr")

        count1 = 0 
        # Row of table
        for row in rows:
            row = row.findChildren(text=True)
            # Columns of each row
            for col in row:
                if col != '\n':
                    count1 += 1
                    if count1 == 1:
                        name = col
                    if count1 == 2:
                        self.stockdata[name] = col
                        count1 = 0
    def table(self):
        return self.stockdata


# Main body, use multiprocess to create master hash talble
def fnmain():
    # Check runtime
    start_time = time.time()
           
    STONK = {}

    # Create master hash table
    def add2list(stock):
        data = getdata(stock)
        data = data.table()
        STONK[stock] = data

        return STONK
    
    # Worker for pools
    def worker(stock):
        try:
            add2list(stock)
        except Exception as e:
            print('ERROR: ' + '[' +str(stock) + ']' + ":" + str(e))
            
    # Get list of stocks from Excel sheet
    f = open('stocknames.txt','r')
    stocks = f.read()
    stocks = ast.literal_eval(stocks)
    stocks = sorted(stocks)

    poolz = 20
    print("Processor count",poolz)
    pool = Pool(poolz)
    pool.map(worker,stocks)
    pool.terminate()
    pool.join()         

    d = datetime.datetime.now()
    d = d.strftime('%Y%m%d')
    if "win" in sys.platform:
        filename = "DATAFILE\\FINVIZ " + d + '.txt'
    else:
        filename = "DATAFILE/FINVIZ " + d + '.txt'
    f = open(str(filename),'w')
    f.write(str(STONK))
    f.close()

    # End runtime
    print("Runtime: --- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    fnmain()
