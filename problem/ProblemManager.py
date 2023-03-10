from elements.Sensor import Sensor

from elements.Node import Node
from problem.Configs import Configs
import sys
import math

class ProblemManager:
    """Static class to store data structure.\n
    Don't cast to object"""
    
    USSD: int
    """Unify search space dimension"""

    subNet: 'list[list[Sensor]]'
    """Clustered network, each charger will take care of one sub network"""
    subNet = []
    
    chargers: 'list[Charger]'
    """The list of V mobile chargers, indexed from
    0 to V-1"""
    chargers = []
    
    sensors: 'list[Sensor]'
    """List of n sensors. Sensors must be indexed 
    from 1 to n"""
    sensors = []


    serviceStation: Node
    """The node stands for the service station.\n
    The station is indexed 0 and may or may not co-related with the base station
    """""""""

    nodes: 'list[Node]'
    """List of nodes\n
    Including all sensors and the service station"""
    nodes = []

    _map: 'dict[int, Sensor]'
    """Mapping from id to sensor"""
    _map = dict()


    initSensors: int
    """Number of deployed sensors on the network"""
    
    distance: 'list[list[float]]'
    """Matrix to store distance between 2 nodes"""
    distance = []

    maxSensorId: int
    """The maximun sensor id"""

    networkSurvivability: float
    networkSurvivability = 100.00

    networkSurvivabilityOverThousand:float=100
    """Use to track survivability ratio over round loop"""

    @staticmethod
    def readInput(file: str, xp: float):
        #clean up from previous run
        ProblemManager.subNet = []
        ProblemManager.sensors = []
        ProblemManager.distance = []
        ProblemManager._map = dict()
        ProblemManager.nodes = []
        ProblemManager.chargers = []

        #parse input
        with open(file, 'r') as lines:
            lines = lines.readlines()
            id = 0
            firstline = lines.pop(0).split()
            ProblemManager.serviceStation = \
                Node(id, float(firstline[0]), float(firstline[1]))
            for line in lines:
                line = line.split()
                if len(line) != 4:
                    print("Improper input data", sys.stderr)
                    sys.exit(0)
                x = float(line[0])
                y = float(line[1])
                p = float(line[2])
                e0 = float(line[3])
                if e0<Configs.S_EMIN:
                    continue
                id = id+1
                sensor = Sensor(id, x, y, e0, p*xp, Configs.S_EMAX, Configs.S_EMIN)
                ProblemManager.sensors.append(sensor)
                ProblemManager._map[sensor.id] = sensor

            #init ProblemManager.maxSensorId
            ProblemManager.maxSensorId = id

            #init ProblemManager.initSensors
            ProblemManager.initSensors = len(ProblemManager.sensors)
            print("total sensor",ProblemManager.initSensors)
            #init ProblemManager.nodes
            ProblemManager.nodes.append(ProblemManager.serviceStation)
            for sensor in ProblemManager.sensors:
                ProblemManager.nodes.append(sensor)

            #init distance matrix 
            # outF = open("ab.txt", "w")
            # write line to output file
            for nodeX in ProblemManager.nodes:
                templist = []
                for nodeY in ProblemManager.nodes:
                    templist.append(nodeX.getDistance(nodeY))
                #     outF.write(str(nodeX.getDistance(nodeY))+" ")
                # outF.write("\n")

                ProblemManager.distance.append(templist)
            # outF.close()
            # exit(0)
            #print(ProblemManager.distance) #debug

    @staticmethod
    def getSensorDensity() -> float:
        return len(ProblemManager.sensors) / (math.pi * Configs.R * Configs.R)

    @staticmethod
    def getTaskNumber() -> int:
        """Get total task number\n
        A.K.A number of charger"""
        return len(ProblemManager.chargers)        
                
    @staticmethod
    def getMinimumLifeTime() -> float:
        res = 1e9
        for s in ProblemManager.sensors:
            lifetime = (s.E0 - s.Emin) / s.p
            res = min(res,lifetime)
        return res

    @staticmethod
    def getAverageLifeTime() -> float:
        res = 0
        for s in ProblemManager.sensors:
            res += ((s.E0 - s.Emin) / s.p)
        res /= len(ProblemManager.sensors)
        return res
                
    @staticmethod
    def getsumP() -> float:
        res = 0
        for s in ProblemManager.sensors:
            res += s.p
        return res

    @staticmethod
    def getSensorById(id: int) -> Sensor:
        return ProblemManager._map[id]

    @staticmethod
    def getNodeById(id: int) -> Node:
        if id == 0:
            return ProblemManager.serviceStation
        else:
            return ProblemManager.getSensorById(id)

from elements.Charger import Charger