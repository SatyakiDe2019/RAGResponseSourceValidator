#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 24-Nov-2023                         ####
#### Modified On 26-Nov-2023                         ####
####                                                 ####
#### Objective: This is the main calling             ####
#### python script that will invoke the              ####
#### RAG class to get the validated response out of  ####
#### the OpenAI-enabled bots.                        ####
####                                                 ####
#########################################################

import clsRAGOpenAI as crao

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

cr = crao.clsRAGOpenAI()

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
        print('Loading vector-document store:: ')
        print('*' * 240)

        strVal = str(input("Your question here: "))
        res, sourceRefernces = cr.getData(strVal)
        r1 = len(res)
        r2 = len(sourceRefernces)

        if ((r1 > 0) and (r2 > 0)):
            print()
            print('Successfully Searched with reference from RAG-OpenAI!')
        else:
            print()
            print('Failed to Search with reference from RAG-OpenAI!')

        print('*' * 240)
        var1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('End Time: ' + str(var1))
        print('*' * 240)

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == '__main__':
    main()
