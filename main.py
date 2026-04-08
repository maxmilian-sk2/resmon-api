from fastapi import FastAPI, Query, Header, HTTPException, status, Depends
from pathlib import Path
from docker_func import instantiate_docker_client, get_docker_containers, get_docker_networks
from sys_func import get_cpu_thread_count, get_cpu_load

# Load API token

apiToken = ''
try :
    with Path('.env.example').open('r') as envFile :
        apiToken = envFile.read().lstrip('API_TOKEN=')
except :
    print("Missing API_TOKEN configuration")
    #logging
    quit()

# Instantiate FastAPI and Docker client

app = FastAPI()

instantiate_docker_client()

# API token verification function

def verify_auth(bearer: str = Header(None, alias="Authorization")) -> str:

    if not bearer:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Bearer header missing (API Token)")

    if bearer != apiToken:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid API Token")
    
    return bearer

######

# Endpoints

@app.get("/api/docker/containers/")
async def containers(targetStatus: str = Query(..., description = "Status to fetch, e.g. exited", min_length=1), bearer: str = Depends(verify_auth)) :

    options = ('created', 'running', 'paused', 'restarting', 'exited', 'dead')

    if targetStatus not in options :
        return {
            "container_amount" : -1
        }

    containerList = await get_docker_containers(targetStatus)

    return {
        "container_amount" : len(containerList)
    }

@app.get("/api/docker/networks/")
async def networks(bearer: str = Depends(verify_auth)) :
    
    netList = await get_docker_networks()

    return {
        "network_amount" : len(netList)
    }

@app.get("/api/sys/cpucores/")
async def cpu_cores(bearer: str = Depends(verify_auth)) :
    
    count = await get_cpu_thread_count()

    return {
        "core_count" : count
    }

@app.get("/api/sys/cpuload/")
async def cpu_load(perCore: bool = Query(False, description="Show individual core loads"), bearer: str = Depends(verify_auth)) :
    
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