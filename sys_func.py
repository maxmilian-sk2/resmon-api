import psutil
import asyncio

async def get_cpu_thread_count() :
    
    cpuCount = int()

    try :
        cpuCount = await asyncio.to_thread(psutil.cpu_count, logical=True)
    except :
        cpuCount = -1
        # logging

    return cpuCount

async def get_cpu_load(perCore):

    fullLoad = float()
    perCoreLoad = list()

    if perCore :
        try :
            perCoreLoad = await asyncio.to_thread(psutil.cpu_percent, interval=1, percpu = True)
        except :
            pass
            # logging

        return perCoreLoad

    else :
        try :
            fullLoad = await asyncio.to_thread(psutil.cpu_percent, interval=1)
        except :
            fullLoad = -1.0
            # logging
        
        return fullLoad

