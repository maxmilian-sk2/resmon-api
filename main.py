from fastapi import FastAPI, Query
from docker_func import instantiate_docker_client, get_docker_containers, get_docker_networks
from sys_func import get_cpu_thread_count, get_cpu_load

app = FastAPI()

instantiate_docker_client()

@app.get("/api/docker/containers/")
async def containers(targetStatus: str = Query(..., description = "Status to fetch, e.g. exited", min_length=1)) :
    
    containerList = await get_docker_containers(targetStatus)

    return {
        "container_amount" : len(containerList)
    }

@app.get("/api/docker/networks/")
async def networks() :
    
    netList = await get_docker_networks()

    return {
        "network_amount" : len(netList)
    }

@app.get("/api/sys/cpucores/")
async def cpu_cores() :
    
    count = await get_cpu_thread_count()

    return {
        "core_count" : count
    }

@app.get("/api/sys/cpuload/")
async def cpu_load(perCore: bool = Query(False, description="Show individual core loads")) :
    
    if perCore :
        perCoreLoad = await get_cpu_load(True)

        return {
            "core_loads" : perCoreLoad
        }

    else :
        fullLoad = await get_cpu_load(False)

        return {
            "cpu_load" : fullLoad
        }