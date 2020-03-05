version = "2020-02-28"

'''
Qtum Block Ripper - CoinStake.py

Copyright (c) 2020 Jackson Belove
Beta software, use at your own risk
MIT License, free, open software for the Qtum Community

Use -txindex on startup to enable blockchain transaction queries.
May have to reload whole blockchain first.
Otherwise may get: ERROR, no response from qtumd

A program to read the coinstake transaction for a block to determine the input
and output for the staking address. Prints the first input and the first two outputs.

QBR uses qtum-cli to send RPC queries to the qtumd server application
to send getblockhash and getblock queries to the blockchain to grab the
block number and selected parameters for each block.

Run from the same directory holding qtum-cli and qtumd.

Output for block 500,000, 10 blocks:

Qtum Block Ripper - CoinStake 2020-02-28
block,input,out1,out2
500000,156.04612633,156.44638433,0.00000000
500001,789.85043641,400.54000000,400.54678968
500002,246.07000000,123.63000000,123.64731556
500003,483.88000000,242.14000000,242.14000000
500004,134.68000000,135.08034041,0.00000000
500005,6701.70742972,3351.05000000,3351.05983760
500006,174.69726513,182.33767307,0.00000000
500007,8128.55427614,4064.47000000,4064.48829658
500008,169.06476274,173.07685077,0.00000000
500009,170.55171380,174.57316629,0.00000000

2020-02-27 Repurposed from Qtum Block Ripper

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

import subprocess
import os, sys              # for file operations

block = 500000              # starting block number, working forwards
numBlocks = 10              # number of blocks to collect
isLinux = False             # set True for Linux platforms, False for Windows

if isLinux == True:      
    linuxPrefix = "./"     # use .\ on Linux platforms
else:
    linuxPrefix = ""        # use a null string on Windows platforms

def parse_number(field, offset, lenData, periodAllowed):
    '''
    parse the global variable "data" which is the response from qtum-cli calls.
    Search for the text "field", then get the digit characters starting 
    "offset" characters from the start of the field, and search through at
    least "lenData" characters, and respond to a period "." if "periodAllowed"
    is True.
    
    For example, to find the balance from the qtum-cli command getinfo:
                       periodAllowed = True
                       v
    ..."balance": 14698.3456000, \r\n...
                  ^    
                  offset = 10 characters from start of balance
    '''
    global data
    
    temp = ' '
    
    dataIndex = data.find(field, 0, lenData)
    
    # print("dataIndex =", dataIndex)

    i = dataIndex + offset      # point at the first digit
    
    if dataIndex > 0:  # found field
        while i <= lenData - 1:
            
            if data[i] >= '0' and data[i] <= '9':
                temp += data[i]
            elif data[i] == "." and periodAllowed == True:  # if period allowed
                temp += data[i]
            elif data[i] == ",":
                break
            elif (i == dataIndex + offset) and (data[i] == "-"):  # allow negative sign
                temp += data[i]                                   # first character only
            else:  
                print("QM error, bad character in ", field)
                break
                    
            i += 1  
            if i >= lenData:
                break
            
        return(temp)
            
    else:
        return(-1)      # an error

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                            
print("Qtum Block Ripper - CoinStake", version)
print("block,input,out1,out2")  # screen copy to CSV text file for Excel import

endBlock = block + numBlocks

while block < endBlock:

    # get blockhash for a this block = = = = = = = = = = = = = =
    
    strBlock = str(block)

    # Linux "./qtum-cli getblockhash " + strBlock
    # Windows "qtum-cli getblockhash " + strBlock"
    
    params = linuxPrefix + "qtum-cli getblockhash " + strBlock

    # print("get blockhash, ", params)

    try:
        blockHashRaw = str(subprocess.check_output(params, shell = True))
            
    except:
        print("ERROR, no response from qtumd A")  

    # data examples for block 300,000
    # print(blockHashRaw) # b'26ce2f5974ba3cd4ce4958b05cda489ea46aa2ae116f58ebf6139d8b07f189d1\r\n'

    blockHash = blockHashRaw[2:66]
    # print(blockHash)    # 26ce2f5974ba3cd4ce4958b05cda489ea46aa2ae116f58ebf6139d8b07f189d1

    # get block details = = = = = = = = = = = = = = = = = = = =

    params = linuxPrefix + "qtum-cli getblock " + blockHash

    # print("get block details, ", params)

    try:
        output = str(subprocess.check_output(params, shell = True))
    except:
        print("ERROR, no response from qtumd B")

    data = str(output)
    lenData = len(data)
    
    # print(data)
    
    '''
    Examples for block 300,000 - Windows - blank spaces replaced by asterisk *
    Windows renders newline as "\r\n", Linux as "\n" which leads to different
    offsets below

    b'{\r\n**"hash":*"26ce2f5974ba3cd4ce4958b05cda489ea46aa2ae116f58ebf6139d8b07f189d1",\r\n**
    "confirmations":*260660,\r\n**"strippedsize":*891,\r\n**"size":*927,\r\n**"weight":*3600,\r\n**
    "height":*300000,\r\n**"version":*536870912,\r\n**"versionHex":*"20000000",\r\n**"merkleroot":*
    "d051978448099e9582ce188557cf8bae50fb37845abd5365afc6b91696034ead",\r\n**"hashStateRoot":*
    "698afb8f5df597d8c4068dda109dcc17f4eb8cfde86db76653cda080b1f17b74",\r\n**"hashUTXORoot":*
    "9e729950c184acd011471252a0c1a4bc279cd4c1e86d543bead4af6df787b2dd",\r\n**"tx":*[\r\n****
    "e5e88124ed986528cd3449e2d8bf1b89ddc94418dfd1ccf99b19973d7fd30631",\r\n****
    "53f8c4f2df7bdbfea82f65aab4c6957c90412bf85f416be5866e56bd8e846272"\r\n**],\r\n**
    "time":*1547434016,\r\n**"mediantime":*1547433600,\r\n**"nonce":*0,\r\n**"bits":*
    "1a04b508",\r\n**"difficulty":*3564141.394673374,\r\n**"chainwork":*
    "0000000000000000000000000000000000000000000000d3fb205668d6015fdc",\r\n**
    "nTx":*2,\r\n**"previousblockhash":*"5c1b213e9d35febf4f0c98eaabad78dc605d075333000633f09daafbdd1c86c4",\r\n**
    "nextblockhash":*"70b57562c96663c17f688a6bc447d4a75042c2df87496ca76768d0bfaf647605",\r\n**"flags":*
    "proof-of-stake",\r\n**"proofhash":*"0000000000000000000000000000000000000000000000000000000000000000",\r\n**
    "modifier":*"88b3d7600748e67b5e2b1c6c1ff7d5b3994bbc88b78bb173d38220192af63391",\r\n**"signature":*
    "3044022013f75c05bf6a8a853b6f8f77b5cb534eb82ab9d23c21ff4797da20969a979e4b02204a9b36ca11
    caf0ff4068d98bfca80996f2a4e0fe3b5838829506dfac3e0d1149"\r\n}\r\n'
    
    '''
     
    # print("lenData =", lenData)       # lenData = 1491

    i = data.find("[")
    
    tx = ''

    if isLinux == True:
        i += 81                         # 81 on Linux
    else:
        i += 85                         # 85 on Windows, due to \r\n need 4 more chars
        
    end = i + 64                        # tx id 64 characters in length

    # print("i", i, "end", end)         # i 619 end 683

    while i < end:
        # print(data[i])
        tx += data[i]
        i += 1

    # print("tx =", tx)
    
    # get coinstake transaction = = = = = = = = = = = = = = = = = =

    params = linuxPrefix + "qtum-cli getrawtransaction " + tx + " true"

    # print("get coinstake, ", params)

    try:
        output = str(subprocess.check_output(params, shell = True))
    except:
        print("ERROR, no response from qtumd C")

    data = str(output)
    lenData = len(data)
    
    # Get the #1 and #2 outputs. These will be a single 
    # stake or a split stake (the 2nd and 3rd outputs)

    i = 0
    j = 0
    
    while i < 2:  # was 4
        j = data.find("value", j)
        # print(j)
        j+= 5
        i += 1

    j += 3         # start of first value charactrer, 4th vout    

    reward1 = ''

    i = 0
    
    while data[j + i] != ",":
        reward1 += data[j + i]
        i += 1

    # print("reward1 = ", reward1)
        
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    
    # find the second potential stake value
    
    i = 0
    j = 0
    
    while i < 3: 
        j = data.find("value", j)
        # print(j)
        j+= 5
        i += 1

    j += 3         # start of first value charactrer, 3rd vout    

    reward2 = ''

    i = 0
    
    while data[j + i] != ",":
        reward2 += data[j + i]
        i += 1
  
    if reward2[0] == "0":      # likely a 0.4 for single UTXO stake, so zero out
        reward2 = "0.00000000"

    # print("reward2 = ", reward2)    
    
    # get the input transaction for the coinstake = = = = = = = = = 
    
    i = data.find("vin")
    
    tx = ''

    if isLinux == True:
        i += 31                 # Linux, start of the txid
    else:
        i += 35                 # Windows
        
    end = i + 64                # tx id 64 characters in length

    # print("i", i, "end", end)

    while i < end:
        # print(data[i])
        tx += data[i]
        i += 1

    # print("txid = ", tx)
         
    vOut = parse_number("vout", 7, lenData, False) # vout position of stake UTXO
    
    # print("vOut =", vOut)
    
    # get the UTXO stake input = = = = = = = = = = = = = = = =

    params = linuxPrefix + "qtum-cli getrawtransaction " + tx + " true"

    # print("get UTXO input, ", params)

    try:
        output = str(subprocess.check_output(params, shell = True))
    except:
        print("ERROR, no response from qtumd D")

    data = str(output)
    lenDataVin = len(data)

    # print(data)
    
    # get the value of the stake UTXO input
        
    i = 0
    j = 0
    
    while i < int(vOut) + 1:                # zero based
        j = data.find("value", j)
        # print(j)
        j+= 5
        i += 1

    j += 3         # start of first value charactrer, 4th vout    

    inputUTXO = ''

    i = 0
    
    while data[j + i] != ",":
        inputUTXO += data[j + i]
        i += 1    

    # print("inputUTXO = ", inputUTXO)

    temp = str(block) + "," + str(inputUTXO) + "," + str(reward1) + "," + str(reward2)
    
    print(temp)    

    block += 1

    # print(block)
    
sys.exit(0)

