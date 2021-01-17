import discord, datetime, asyncio, sys
import fnalerts, fnexcel, fnrerun, fnconcurrent

from config import config

def timestamp():
    timestamp = "[" + str(datetime.datetime.now()) + "]"
    return timestamp
# -------------------------------------------------------------------------------

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(timestamp(),'Logged in as:')
        print(timestamp(),self.user.name, "id#:", self.user.id)
        print(" # -------------------------------")

    async def on_message(self, message):
        # Bot won't respond to its own messages
        if message.author == self.user:
            return
        print(timestamp(),"[",message.author,message.channel,"]",message.content)

    async def my_background_task(self):
        await self.wait_until_ready()
        try:
            print(" # -------------------------------")
            # Holidays, no discord posts on these days
            holidays = (config())["Holidays"]
            print("Exlcuded Days:",holidays)
            # Set time of 5:00PM (1700)
            settime = (config())["settime"]
            print("Post Time:",settime)
            # Sleep after data collection
            sleeptime = (config())["sleeptime"]
            print("Sleep Time:",sleeptime)
            # If Post to Test Server
            Test_Server = (config())["Test_Server"]
            print(" # -------------------------------")
            if Test_Server:
                fin_alert = 704579221149974558
                the_lab = 704579238375850055
                print("Running Test Server")
            else:        
                fin_alert = 701128332778930197 
                the_lab = 701143224798150706
                print("Running Live Server")
            print(" # -------------------------------")
            
            # finance-alert channel ID goes here
            channel = self.get_channel(fin_alert)
            lab = self.get_channel(the_lab)
           
            # Loop starts
            while not self.is_closed():

                # Current Time
                tim3variable = ((datetime.datetime.now()).strftime("%H%M"))
                # Current Day of the Week
                weekday = str((datetime.datetime.now()).strftime("%a"))
                # Current Date
                date = str((datetime.datetime.now()).strftime("%m/%d/%y"))

                if settime in tim3variable:
                    
                    print(timestamp(),"Collecting today's data...")
                    if __name__ == "__main__":
                        fnconcurrent.conmain()
                    reback = fnrerun.rerun()
                    alert = fnalerts.alerts()
                    
                    # Collect data, no discord posts on weekends
                    if  weekday == "Sat" or weekday == "Sun":     
                        print(timestamp(),'Weekend data collected. ' + tim3variable + ' ' + date)
                        await asyncio.sleep(sleeptime)
                        
                    # Collect data, no discord posts on holidays
                    elif date in holidays:
                        print(timestamp(),'Holiday data collected. ' + tim3variable + ' ' + date)
                        await asyncio.sleep(sleeptime)
                        
                    # Collect data, send alerts 
                    else:
                        print(timestamp(),'Sending alert... ' + tim3variable + ' ' + date)
                        
                        # Alert: RSI under 30
                        try:
                            r_num = 30
                            rsi = alert.RSI(r_num)
                            if rsi == []:
                                rsi_head = ("**UNDER %s RSI (14)**\nStocks with RSI below %s...```None detected!```") \
                                           % (str(r_num),str(r_num))
                                await channel.send(rsi_head)
                            else:
                                rsi_head =  "**UNDER %s RSI (14)**\nStocks with RSI below %s..." % (str(r_num),str(r_num))
                                rsi_s = ''
                                for r in rsi:
                                    rsi_s = rsi_s + r + '\n'

                                msg = rsi_head + "```" + rsi_s + " ```\n"
                                print(timestamp(),"RSI msg:",len(msg))                         
                                await channel.send(msg)
                        except Exception as e:
                            print("RSI30 Message Error:",e)
                            
                        
                        # Alert: SMAnp ---
                        try:
                            np_num = 20
                            np = alert.SMAnp(np_num)
                            if np == []:
                                np_head = " \n**POSITIVE SMA%s**\nStocks with SMA%s that are now positive...```None Detected!```" \
                                          % (str(np_num),str(np_num))
                                await channel.send(np_head)
                            else:
                                np_head = " \n**POSITIVE SMA%s**\nStocks with SMA%s that are now positive..." % (str(np_num),str(np_num))
                                np_s = ''
                                for n in np:
                                    np_s =  np_s + n + '\n\n'

                                msg = np_head + "```" + np_s + "```\n"
                                print(timestamp(),"SMAnp msg:",len(msg))
                                await channel.send(msg)    
                        except Exception as e:
                            print("SMAnp Message Error:",e)
                            
                        # Alert: SMAvs ---
                        try:
                            msg_count = 0
                            vs = alert.SMAvs()
                            if vs == []:
                                vs_head = "**SMA50 vs 200**\nStocks with a SMA50 higher than their SMA200...```None Detected!```"
                                await channel.send(vs_head)
                            else:
                                vs_head = "**SMA50 vs 200**\nStocks with a SMA50 higher than their SMA200..."
                                vs_s = ''
                                for v in vs:
                                    vs_s =  vs_s + v + '\n\n'

                                msg = "\nSMA50 > SMA200\n_______________\n\n" + vs_s
                                print(timestamp(),"SMAvs msg:",len(msg))
                                # Discord has 2000 character limit, split into sendable messages
                                # Get first 19XX characters and find index of last split, add 2 to account for the split
                                n = int((msg[:1900]).rfind('\n\n')) + 2
                                msg = [msg[i:i+n] for i in range(0,len(msg), n)]

                                for m in msg:
                                    if msg_count == 0:
                                        m = vs_head + "```" + m + "```\n"
                                    else:
                                        m = "```" + m + "```\n"

                                    await channel.send(m)
                                    msg_count += 1
                        except Exception as e:
                            print("SMAvs Message Error",e)

                        # Create excel
                        fnexcel()
                        # Send excel to the-lab
                        try:
                            header = 'Excel Sheet: ' + ((datetime.datetime.now()).strftime("%m-%d-%Y"))
                            filename = "FINVIZ " + ((datetime.datetime.now()).strftime("%Y%m%d")) + '.xlsx'
                            if "win" in sys.platform:
                                filepath = "DATAEXCEL\\FINVIZ " + ((datetime.datetime.now()).strftime("%Y%m%d")) + '.xlsx'
                            else:
                                filepath = "DATAFILE/FINVIZ " + filename
                            await lab.send(header, file=discord.File(filepath,filename))
                        except Exception as e:
                            print("Excel Message Error",e)
                            
                        # task completed, go to sleep
                        await asyncio.sleep(sleeptime)
                                            
                else:
                    # Check time every x seconds
                    if (tim3variable)[-1:] == '0':
                        print(timestamp(),'waiting... ' + tim3variable + ' ' + date)
                    await asyncio.sleep(20)
                    
        except Exception as e:
            print(timestamp(),"Discord Bot Error" ,e)

try:
    client = MyClient()
    client.run('')
except Exception as e:
    print(e)

