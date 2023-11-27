#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 27-Jun-2023                         ####
#### Modified On 28-Jun-2023                         ####
####                                                 ####
#### Objective: This is the main calling             ####
#### python script that will invoke the              ####
#### main class, which will contextualize the source ####
#### files & then store the vectors into the index   ####
#### besides capturing the source data inside an     ####
#### organized pickle file for better use.           ####
####                                                 ####
#########################################################

import clsFeedVectorDB as cfvd

from clsConfigClient import clsConfigClient as cf
import clsL as log

from datetime import datetime, timedelta

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

########################################################
################    Global Area   ######################
########################################################

cd = cfvd.clsFeedVectorDB()

########################################################
################  End Of Global Area   #################
########################################################

def main():
    try:
        var = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*' * 240)
        print('Start Time: ' + str(var))
        print('*' * 240)

        print('*' * 240)
        print('Creating vector-document store:: ')
        print('*' * 240)

        r1 = cd.genData()

        if r1 == 0:
            print()
            print('Successfully created RAG-Index!')
        else:
            print()
            print('Failed to create RAG-Index!')

        print('*' * 240)
        var1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('End Time: ' + str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == '__main__':
    main()
