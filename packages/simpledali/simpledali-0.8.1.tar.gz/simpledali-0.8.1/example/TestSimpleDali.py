import simpledali
from  simplemseed import MSeed3Header, MSeed3Record, MiniseedHeader, MiniseedRecord, encodeSteim2, seedcodec
import asyncio
import logging
from datetime import datetime, timedelta
from array import array
import os, socket
import jwt
from threading import Thread

logging.basicConfig(level=logging.DEBUG)

host = socket.gethostname()#"glass.caltech.edu"
port = 26100
uri = f"ws://{host}:{port}/datalink"
username =  os.getlogin()  


async def init_dali(
    host,
    port,
    verbose=False,
    programname="simpleDali",
    username="username",
    processid=0,
    architecture="python",
):
    dali = simpledali.SocketDataLink(host, port, verbose=verbose)
    # dali = simpledali.WebSocketDataLink(uri, verbose=True)
    serverId = await dali.id(programname, username, processid, architecture)
    print(f"Resp: {serverId}")
    return dali


async def send_test_mseed3(dali):
    network = "XX"
    station = "TEST"
    location = "00"
    channel = "HNZ"
    numsamples = 100
    sampleRate = 100
    recordtimerange = timedelta(seconds=(numsamples-1)/sampleRate)
    starttime = simpledali.utcnowWithTz() - recordtimerange
    shortData = array("h")  # shorts
    for i in range(numsamples):
        shortData.append(i)

    header = MSeed3Header()
    header.starttime = starttime
    header.sampleRatePeriod = sampleRate
    identifier = "FDSN:XX2024_REALFAKE_01234567_H_HRQ_Z"
    ms3record = MSeed3Record(header, identifier, shortData)

    print(f"before writeMSeed3 {ms3record.identifier} {starttime.isoformat()}")
    sendResult = await dali.writeMSeed3(ms3record)
    print(f"writemseed resp {sendResult}")


async def send_test_mseed2(dali, encoding="STEIM2", blocks=63):
    network = "XX"
    station = "TEST"
    location = "00"
    channel = "HNZ"
    numsamples = 100
    sampleRate = 100
    recordtimerange = timedelta(seconds=(numsamples-1)/sampleRate)
    starttime = simpledali.utcnowWithTz() - recordtimerange
    shortData = array("h")  # shorts
    for i in range(numsamples):
        shortData.append(i)

    header = MSeed3Header()
    header.starttime = starttime
    header.sampleRatePeriod = sampleRate

    msh = MiniseedHeader(network, station, location, channel, starttime, numsamples, sampleRate)

    if encoding == "STEIM2":
        print("STEIM2 before")
        # msh.encoding = seedcodec.STEIM2
        msh = MiniseedHeader(network, station, location, channel, starttime, numsamples, sampleRate, encoding=seedcodec.STEIM2)
        encoded = encodeSteim2(shortData)
        msr = MiniseedRecord(msh, encoded)
        print("STEIM2 after")
    else:
        msr = MiniseedRecord(msh, shortData)

    print(f"before writeMSeed {starttime.isoformat()}")
    sendResult = await dali.writeMSeed(msr)
    print(f"writemseed resp {sendResult}")


async def main():
    numSend = 100
    verbose = True
    programname = "simpleDali"
    mseedType = "MSEED"
    processid = 0
    architecture = "python"
    async with simpledali.SocketDataLink(host, port, verbose=verbose) as dali:
    # async with simpledali.WebSocketDataLink(uri, verbose=verbose) as dali:
        serverId = await dali.id(programname, username, processid, architecture)
        print(f"Resp: {serverId}")
        for i in range(numSend):
            if mseedType == "MSEED3":
                await send_test_mseed3(dali)
            elif mseedType == "MSEED":
                await send_test_mseed2(dali)
            else:
                raise ValueError("Provided unknown mseed format: %s"%mseedType)
            await asyncio.sleep(1)


debug = False
asyncio.run(main(), debug=debug)
