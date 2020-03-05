# Qtum-Block-Ripper-Coinstake
A script to print the coinstake input and output values

**Use -txindex on startup to enable blockchain transaction queries.**
May have to reload whole blockchain first.
Otherwise may get: ```ERROR, no response from qtumd```

Set the starting block, number of blocks, and the flag ```isLinux``` to 
select Linux or Windows machines.

A program to read the coinstake transaction for a block to determine the input
and output for the staking address. Prints the first input and the first two outputs.

QBR uses qtum-cli to send RPC queries to the qtumd server application
to send getblockhash and getblock queries to the blockchain to grab the
block number and selected parameters for each block.

Run from the same directory holding qtum-cli and qtumd.

Output for block 500,000, 10 blocks:

```Qtum Block Ripper - CoinStake 2020-02-28
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
```

2020-02-27 Repurposed from Qtum Block Ripper
