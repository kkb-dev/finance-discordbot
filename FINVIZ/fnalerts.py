import datetime
import fndatareader


# convert list into dictionary from RSI,SMA into dictionaries
def Conv(lst):
    dic = {}
    for l in lst:
        x = l.split(': ')
        dic[(x[0])] = x[1]
    return dic

# main body
class alerts():
    def __init__(self,*args):
        if args == ():
            args = ()
        else:
            args = int(str(args[0]))
        #import datasheet of selected date, empty defaults to current date
        self.STONK = fndatareader.file(args)

    # Get the name of all data columns
    def headers(self):
        for name, data in self.STONK.items():
            __counter = 1
            print(str(__counter)+'.',"Name")
            for d in data:
                print(str(__counter)+'.',d)
                __counter += 1
            break
        
    # Print list of stocks below chosen RSI (defaults to 30)
    def RSI(self,*args):
        RSIs = []
        try:
            args = float(str(args[0]))
        except:
            args = 30
        
        for name, data in self.STONK.items():
            if float((data["RSI (14)"])) < float(args):
                RSIs.append(name + ": " + str((data["RSI (14)"])))
                
        return RSIs
            
    # Get moving average, choose duration (supports 20,50,200)
    def SMA(self,*args):
        SMAs = []
        try:
            args = int(args[0])
        except:
            raise Exception("Value must be integers: 20, 50, or 200")
            
        for name, data in self.STONK.items():
            SMAs.append(name + ": " + str((data[("SMA"+str(args))])))
            
        return SMAs

    # Check if SMA goes from negative to positive, compare yesterday vs today
    def SMAnp(self, *args):
        SMAnps = []
        try:
            movav = args[0]
        except:
            movav = 20
            
        time = datetime.datetime.now()
        if time.strftime('%a') == 'Mon': #Get previous friday
            time = time - datetime.timedelta(days=3)
        else:
            time = time - datetime.timedelta(days=1)
        time = time.strftime('%Y%m%d')

        # Current SMA ----
        curr = self.SMA(movav)
        curr = Conv(curr)
        #Yesterday's SMA ----
        yest = alerts(time)
        yest = yest.SMA(movav)
        yest = Conv(yest)

        for key in curr:
            # Use try/catch in case current data contains stock with no previous data
            try:
                if float((yest[key])[:-1]) < 0:
                    if float((curr[key])[:-1]) > float((yest[key])[:-1]):
                        if float((curr[key])[:-1]) > 0:
                            SMAnps.append(key+":\n"+"PREVIOUS: "+yest[key]+"\nCURRENT: "+curr[key])
            except:
                pass
            
        return SMAnps

    # Check when SMA50 crosses over SMA200
    def SMAvs(self):
        
        SMA50vs200s = []
        mak50 = self.SMA(50)
        mak200 = self.SMA(200)

        mak50 = Conv(mak50)
        mak200 = Conv(mak200)

        for key in mak50:
            try:
                if float((mak50[key])[:-1]) > 0:
                    if float((mak50[key])[:-1]) >= float((mak200[key])[:-1]):
                        SMA50vs200s.append(key+":\n"+mak50[key]+ " > " +(mak200[key]))
            except Exception as e:
                pass
            
        return SMA50vs200s


