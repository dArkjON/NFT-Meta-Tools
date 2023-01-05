import requests
from web3 import Web3
import json
import time



def printer():
   print ('=================================================')
   print ('             NFT Meta Parser Web3                ')
   print ('               create by dArkjON                 ')
   print ('=================================================')
   print ('               ++++++++++++++++++++              ')
   

def connectETH():
   global eth
   eth = "https://rpc.flashbots.net/"
   global web3 
   web3 = Web3(Web3.HTTPProvider(eth))
   global server
   server = 'ETH'   
   link = web3.isConnected()
   if (link == True):
     print ('Connected to ETH Blockchain')
     print ('Block Nummer : ' + str(web3.eth.block_number))
   else:
     print ('Offline')

def connectBNB():
   global eth
   eth = "https://bsc-dataseed.binance.org/"
   global web3 
   web3 = Web3(Web3.HTTPProvider(eth))
   global server
   server = 'BNB'
   link = web3.isConnected()
   if (link == True):
     print ('Connected to BNB Blockchain')
     print ('Block Nummer : ' + str(web3.eth.block_number))
   else:
     print ('Offline')
     
def connectMATIC():
   global eth
   eth = "https://polygon-rpc.com/"
   global web3 
   web3 = Web3(Web3.HTTPProvider(eth))
   global server
   server = 'MATIC'   
   link = web3.isConnected()
   if (link == True):
     print ('Connected to Matic(Polygon) Blockchain')
     print ('Block Nummer : ' + str(web3.eth.block_number))
   else:
     print ('Offline')


menu_options = {
    1: 'ETH Server',
    2: 'BNB Server',
    3: 'Matic Server',
    4: 'Exit',
}

menu2_options = {
    1: 'Parse Meta',
    2: 'Back to Main Menu',
    3: 'Exit',
}

def contract():
    contractAddress = input("Enter Contract Address : ")
    
    #openwork : add check 'try'
    
    print("Contract Address is: " + contractAddress)
    contractAddress = web3.toChecksumAddress(contractAddress)
    getABI(contractAddress)

    
    
  
def getABI(contract):
    if (server == 'ETH'):
        link = "https://api.etherscan.io/api?module=contract&action=getabi&address="+contract+"&apikey=YourApiKeyToken"
    elif (server == 'BNB'):
        link = "https://api.bscscan.com/api?module=contract&action=getabi&address="+contract+"&apikey=YourApiKeyToken"
    elif (server == 'MATIC'):
        link = "https://api.polygonscan.com/api?module=contract&action=getabi&address="+contract+"&apikey=YourApiKeyToken"
    
    response = requests.get(link)
    parsed = json.loads(response.text)
    cabi = parsed['result']
    abicontract = web3.eth.contract(address=contract, abi=cabi)
    name = abicontract.functions.name().call()
    try:
        nummer = abicontract.functions.totalSupply().call()
    except:
        nummer = abicontract.functions.getTokenCount().call()
    URI = abicontract.functions.tokenURI(1).call()
    print ('Contract Name: '+ name + ' - Token Counter: '+str(nummer)+' - URI: ' + URI)
    for key in menu2_options.keys():
        print (key, '--', menu2_options[key] )
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
    if option == 1:
        parsenum = int(input('Please enter last ID to Parse (default:'+str(nummer)+'): ') or nummer)
        URIparse(name, URI, parsenum, contract)
    elif option == 2:
        print ()

    elif option == 3:
        print('Thanks message before exiting')
        exit()
    else:
        print('Invalid option. Please enter a number between 1 and 4.')

def URIparse(name, url, nummer, contract):
    prefix = url[:4]
    if (prefix == 'ipfs'):
      print ('IPFS Parser for ' + name + ' ' + str(nummer))
      splitter = (url.split('/')) 
      nid = (int(splitter[3]))
      
      #openwork : add file check like web parse
      
      for x in range(nummer): 
          url = 'https://cloudflare-ipfs.com/ipfs/'+str(splitter[2])+'/'+str(nid)
          f = requests.get(url)
          parsed = json.loads(f.text)
          print (parsed)
          f = open(name + '_' + str(contract) + ".csv", "a")
          f.write(str(parsed))
          f.write('\n')
          f.close()
          nid += 1
      
    else:
      print ('Web Parser for ' + name + ' ' + str(nummer))
      Segments = url.rpartition('/')
      fex = ""
      try:
          nid = (int(Segments[2]))
      except:
          splitter = (Segments[2].split('.')) 
          nid = (int(splitter[0]))
          fex = splitter[1]
       
      
      for x in range(nummer): 
          if (fex == ""):
              url = str(Segments[0])+'/'+str(nid)
          else:
              url = str(Segments[0])+'/'+str(nid)+'.'+fex
          
          f = requests.get(url)
          parsed = json.loads(f.text)
          print (parsed)
          f = open(name + '_' + str(contract) + ".csv", "a")
          f.write(str(parsed))
          f.write('\n')
          f.close()
          nid += 1

def print_menu():
    printer()
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
     connectETH()
     contract()
     time.sleep(2)

def option2():
     connectBNB()
     contract()
     time.sleep(2)
def option3():
     connectMATIC()
     contract()
     time.sleep(2)
     
if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            print('Thanks message before exiting')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')
