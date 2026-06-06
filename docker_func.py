import aiodocker

dockerClient = None
dockerClientFlag = False

def instantiate_docker_client() :

    global dockerClient
    global dockerClientFlag

    try :
        dockerClient = aiodocker.Docker()
        dockerClientFlag = True
    except :
        pass
        # logging

async def get_docker_containers(status) :

    containerResult = None
    containerList = list()

    if dockerClientFlag :
        try :
            containerResult = await dockerClient.containers.list(all = True, filters={"status": [status]})
            for container in containerResult :
                containerList.append(container._id)
        except :
            pass
            # logging

    return containerList

async def get_docker_networks() :

    netResult = None
    netList = list()

    if dockerClientFlag :
        try :
            netResult = await dockerClient.networks.list()
            for net in netResult :
                netList.append(net["Name"])
        except :
            pass
            # logging

    return netList

async def get_docker_volumes() :

    volResult = None
    volList = list()

    if dockerClientFlag :
        try :
            volResult = await dockerClient.volumes.list()
            for vol in volResult["Volumes"] :
                volList.append(vol["Name"])
        except :
            pass
            # logging

    return volList