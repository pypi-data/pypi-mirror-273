

import simpledali
import datetime
import os
import argparse
import bz2
import asyncio
import pathlib
import re


# tomllib is std in python > 3.11 so do conditional import
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

async def doget(gap_start, chan, max=10):
    programname="simpleDali_get"
    username="dragrace"
    processid=0
    architecture="python"
    dali = simpledali.SocketDataLink("eeyore.seis.sc.edu", 6382, verbose=True)
    dali.verbose = True
    serverId = await dali.id(programname, username, processid, architecture)
    print(f"Resp: {serverId}")

    info = await dali.parsedInfoStatus()
    print()
    print(simpledali.util.prettyPrintInfo(info))
    print()
    info = await dali.parsedInfoStreams()
    print()
    print(simpledali.util.prettyPrintInfo(info))
    await dali.close()

async def otherdoget(gap_start, chan, max=10):
    programname="simpleDali_get"
    username="dragrace"
    processid=0
    architecture="python"
    dali = simpledali.SocketDataLink("eeyore.seis.sc.edu", 6382, verbose=True)
    dali.verbose = True
    serverId = await dali.id(programname, username, processid, architecture)
    print(f"Resp: {serverId}")
    print(await dali.parsedInfoStreams())

    dali_list = []
    timeStr = '2023-11-10T00:05:23Z'
    gap_start_time = simpledali.util.optional_date(timeStr)
    #await dali.match(chan)
    print("earliest:")
    await dali.positionLatest()
    #p = await dali.readEarliest()
    #print(f"{p} {simpledali.hptimeToDatetime(p.dataStartTime)}")
    #print()
    #await dali.positionAfter(gap_start_time)
    count = 0
    async for daliPacket in dali.stream():
        p = daliPacket
        print(f"{p} {simpledali.hptimeToDatetime(p.dataStartTime)}")
        count += 1
        if count > max:
            break
    #for i in range(max):
    #    p = await dali.read(gap_start+i)
    #    print(f"{p} {simpledali.hptimeToDatetime(p.dataStartTime)}")

    await dali.close()

async def run():
    await doget(25044, "CO_CASEE_00_HHZ/MSEED")

def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()
