def config():
    settings = {
        
    # Time when to post discord data: 24H format (Example: 1630 <= 4:30PM)
    "settime": "21",
    
    # Holidays of when not to post to discord
    "Holidays":
    ["05/25/20","07/03/20","09/07/20","11/26/20","12/25/20","01/01/21"],
    
    # Indicate if post goes to Test (True) or Live (False)
    "Test_Server": False,

    # Sleep time after data collection 
    "sleeptime": 3600,
    }

    # ---------------------------------------------------------------------
    return settings

