import requests, time, datetime, ast, sys
from bs4 import BeautifulSoup as bs
from concurrent.futures import ProcessPoolExecutor, as_completed
from ast import literal_eval


def parse(stock):
    stonk = {}
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
    url = "https://finviz.com/quote.ashx?t=" + str(stock)
    page = requests.get(url, headers = headers)
    soup = bs(page.content,"html.parser")
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
                    stonk[name] = col
                    count1 = 0

    #return stock name & stock table     
    return (stock,str(stonk))

def conmain():
    try:
        # Master dictionary
        master = {}
        
        # Get list of stocks from Excel sheet
        f = open('stocknames.txt','r')
        stocks = f.read()
        f.close()
        stocks = ast.literal_eval(stocks)
        URLs = sorted(stocks)

        # Asynch Multi-Processing
        with ProcessPoolExecutor(max_workers=10) as executor:
            start = time.time()
            futures = {executor.submit(parse, url): url for url in URLs}
            for result in as_completed(futures):
                link = futures.get(result)
                try:
                    data = result.result()
                except Exception as e:
                    print("Error:",e)
                else:
                    print(".", end="")
                    master[(data[0])] = ast.literal_eval(data[1])
            end = time.time()

            # Write master table to txt
            d = datetime.datetime.now()
            d = d.strftime('%Y%m%d')
            if "win" in sys.platform:
                filename = "DATAFILE\\FINVIZ " + d + '.txt'
            else:
                filename = "DATAFILE/FINVIZ " + d + '.txt'
            f = open(str(filename),'w')
            f.write(str(master))
            f.close()
            print("Time Taken: {:.6f}s".format(end-start))
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
