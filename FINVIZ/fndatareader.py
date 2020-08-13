import xlsxwriter, datetime, ast, sys
import finviz
#import finconcurrent


# Access datafile, if no args use current date
def file(*args):
    if len(args) == 0 or args == ((),):
        d = datetime.datetime.now()
        d = d.strftime('%Y%m%d')

        if "win" in sys.platform:
            filename = "DATAFILE\\FINVIZ " + d + '.txt'
        else:
            filename = "DATAFILE/FINVIZ " + d + '.txt'

        while True:
            try:
                f = open(str(filename),'r')
                old_STONK = f.read()
                old_STONK = ast.literal_eval(old_STONK)
                f.close()
                break
            except Exception as e:
                print('File for current day not found, making now...')
                #if __name__ is 'fndatareader':finconcurrent.fnmain()
                finviz.fnmain()
    else:
        d = str(args[0])
        if "win" in sys.platform:
            filename = "DATAFILE\\FINVIZ " + d + '.txt'
        else:
            filename = "DATAFILE/FINVIZ " + d + '.txt'
        f = open(str(filename),'r')
        old_STONK = f.read()
        old_STONK = ast.literal_eval(old_STONK)
        f.close()


    # Sort alphabetically by key 
    STONK = {k: old_STONK[k] for k in sorted(old_STONK)}

    return STONK

if __name__ == '__main__':
    x=file()
