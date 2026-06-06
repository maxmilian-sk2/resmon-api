from fastapi import FastAPI, Query, Header, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from docker_func import instantiate_docker_client, get_docker_containers, get_docker_networks, get_docker_volumes, dockerClient, dockerClientFlag
from sys_func import get_cpu_thread_count, get_cpu_load, get_ram_utilization, get_disk_usage

# Load API token and CORS config from .env (plain text line by line)

apiToken = ''
corsOrigins = ''
try :
    with Path('.env').open('r') as envFile :
        for line in envFile :
            if line.startswith('API_TOKEN=') :
                apiToken = line[len('API_TOKEN='):].strip()
            elif line.startswith('CORS_ORIGINS=') :
                corsOrigins = line[len('CORS_ORIGINS='):].strip()
except :
    print("Missing API_TOKEN configuration")
    #logging
    quit()

# Instantiate FastAPI and Docker client

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await instantiate_docker_client()
    yield
    if dockerClientFlag:
        await dockerClient.close()

app = FastAPI(lifespan=lifespan)

# CORS (comma-separated list of allowed origins, or * for all, e.g. CORS_ORIGINS=http://localhost:3000,https://example.com)

allowedOrigins = [origin.strip() for origin in corsOrigins.split(',') if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins = allowedOrigins,
    allow_credentials = allowedOrigins != ['*'],  # credentials + wildcard origin is rejected by browsers
    allow_methods = ["*"],
    allow_headers = ["*"],
)

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

@app.get("/api/docker/volumes/")
async def volumes(bearer: str = Depends(verify_auth)) :

    volList = await get_docker_volumes()

    return {
        "volume_amount" : len(volList)
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

@app.get("/api/sys/ramutilization/")
async def ram_utilization(bearer: str = Depends(verify_auth)) :

    utilization = await get_ram_utilization()

    return {
        "ram_percent" : utilization["percent"],
        "ram_used_gb" : utilization["used_gb"],
        "ram_total_gb" : utilization["total_gb"]
    }

@app.get("/api/sys/diskusage/")
async def disk_usage(path: str = Query("/", description="Filesystem path to check, e.g. /"), bearer: str = Depends(verify_auth)) :

    usage = await get_disk_usage(path)

    return {
        "disk_name" : usage["name"],
        "disk_percent" : usage["percent"],
        "disk_used_gb" : usage["used_gb"],
        "disk_total_gb" : usage["total_gb"]
    }
