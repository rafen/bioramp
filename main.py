from time import sleep
from bioramp import BioRamp

mins = 5

def main():
    while True:
        try:
            BioRamp().read()
            sleep(60 * mins)
        except Exception as e:
            print(e)

main()
