import datetime, ast, sys
import fndatareader, finviz


# Complete data, best used when FINVIZ is run with low bandwidth
def rerun():
    d = datetime.datetime.now()
    d = d.strftime('%Y%m%d')

    STONK = fndatareader.file(int(d))

    f = open('stocknames.txt','r')
    stocks = f.read()
    stocks = ast.literal_eval(stocks)

    count = 1
    # Keep running until master hash contains as many stocks as file list
    while count != 0:
        count = 0 
        for stock in stocks:
            if stock not in STONK:
                print(stock,"REDO")
                try:
                    data = finviz.getdata(stock)
                    data = data.table()
                    STONK[stock] = data
                    count += 1
                except Exception as e:
                    print('RERUN ERROR: ' + '[' +str(stock) + ']' + ":" + str(e))

    # Write new file
    if "win" in sys.platform:
        filename = "DATAFILE\\FINVIZ " + d + '.txt'
    else:
        filename = "DATAFILE/FINVIZ " + d + '.txt'
    f = open(str(filename),'w')
    f.write(str(STONK))
    f.close()



