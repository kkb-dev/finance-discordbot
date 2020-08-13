import xlsxwriter, datetime, sys
import fndatareader 


# Create excel file using data from textfile
def esheet(*args):

    try:
        d = args[0]
        d = int(d)
    except:
        d = datetime.datetime.now()
        d = d.strftime('%Y%m%d')
        
    try:
        STONK = fndatareader.file(int(d))
    except:
        STONK = fndatareader.file()

    if "win" in sys.platform:
        filename = "DATAEXCEL\\FINVIZ " + str(d) + '.xlsx'
    else:
        filename = "DATAEXCEL/FINVIZ " + str(d) + '.xlsx'

    workbook = xlsxwriter.Workbook(filename) 
    worksheet = workbook.add_worksheet()


    headlist = 'Earnings	Name	Index	Price	Prev Close	Change	Target Price	Market Cap	Dividend	Dividend %	Perf Week	Perf Month	Perf Quarter	Perf Half Y	Perf Year	Perf YTD	RSI (14)	52W Range	SMA20	SMA50	SMA200	52W Low	52W High	Insider Own	P/E	Forward P/E	P/S	P/B	Cash/sh	P/C	P/FCF	Shs Outstand	Shs Float	Book/sh	PEG	EPS (ttm)	EPS Q/Q	EPS next Q	EPS this Y	EPS next Y	EPS past 5Y	EPS next 5Y	Insider Trans	Quick Ratio	Current Ratio	Debt/Eq	LT Debt/Eq	ROA	Inst Own	Employees	Sales	Sales Q/Q	Sales past 5Y	Oper. Margin	Gross Margin	Profit Margin	Income	ROE	ROI	ATR	Volatility	Avg Volume	Rel Volume	Volume	Short Float	Short Ratio'
    headlist = headlist.split('\t')
    NEWST = {}
    print(STONK)
    for stock,data in STONK.items():
        
        ST = {}
        for h in headlist:
            try:
                ST[h] = data[h]
            except KeyError:
                ST[h] = stock
            except Exception as e:
                print('fnexcel:',e)
        NEWST[stock] = ST

    
    # Get header names of columns, write name & start column
    row = 0
    col = 0
    for name, data in NEWST.items():
        for d in data:
            worksheet.write(row, col, d)
            col += 1
        break

    # Get data from the row, write to columns
    row = 1
    col = 0
    for name,data in NEWST.items():
        if col == 0:
            col = 1
            worksheet.write(row, col, name)
            col = 9999
        for d in data:
            if col == 9999:
                col = 0
                worksheet.write(row, col, data[d])
                col = 1
            else:
                worksheet.write(row, col, data[d])
                col += 1

        row += 1
        col = 0
            
    workbook.close() 

if __name__ == '__main__':
    while True:
        inp = input("\n---\n---\nex.20200423\nEnter date or press nothing to create today...:")
        esheet(inp)
        print(("!!!!!!!!!!!!!!!!!!!! File made !!!!!!!!!!!!!!!!!!!!").upper())
