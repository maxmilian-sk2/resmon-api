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

async def get_ram_utilization() :

    ramUtilization = {
        "percent" : -1.0,
        "used_gb" : -1.0,
        "total_gb" : -1.0
    }

    try :
        memory = await asyncio.to_thread(psutil.virtual_memory)
        ramUtilization = {
            "percent" : memory.percent,
            "used_gb" : round(memory.used / (1024 ** 3), 2),
            "total_gb" : round(memory.total / (1024 ** 3), 2)
        }
    except :
        pass
        # logging

    return ramUtilization

async def get_disk_name(path) :

    diskName = "unknown"

    try :
        partitions = await asyncio.to_thread(psutil.disk_partitions)
        match = max(
            (part for part in partitions if path.startswith(part.mountpoint)),
            key = lambda part : len(part.mountpoint),
            default = None
        )
        if match :
            diskName = match.device
    except :
        pass
        # logging

    return diskName

async def get_disk_usage(path = "/") :

    diskUsage = {
        "name" : "unknown",
        "percent" : -1.0,
        "used_gb" : -1.0,
        "total_gb" : -1.0
    }

    try :
        disk = await asyncio.to_thread(psutil.disk_usage, path)
        diskUsage = {
            "name" : await get_disk_name(path),
            "percent" : disk.percent,
            "used_gb" : round(disk.used / (1024 ** 3), 2),
            "total_gb" : round(disk.total / (1024 ** 3), 2)
        }
    except :
        pass
        # logging

    return diskUsage

