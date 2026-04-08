from fastapi import FastAPI, Query
from docker_func import instantiate_docker_client, get_docker_containers, get_docker_networks

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