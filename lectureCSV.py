import csv, struct

with open('data.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for (_,dt,_,_,_,seq,hex) in reader:
        if hex=="Message": continue
        if hex:
            mes_bin=bytes.fromhex(hex)
            (_,_,total_in,_,_,total_out,_,_,period)=struct.unpack('<BBIBBIBBI', mes_bin)
            print(f"{dt}, {seq} : {total_in=:3} {total_out=:3} {period=:7} {hex}")
