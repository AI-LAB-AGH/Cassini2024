# Team AI Lab

#From dirt to decisions
After heavy rainfalls or other natural disasters, some roads become impassable. It is the case mainly for unpaved roads, making it impossible to pass for emergency services, logistics, agricultural and military equipment.

Our solution makes it possible to plan and route missions in harsh road conditions.

##Bunch of statistics
During floodings, the main public property that get destroyed are roads. In Umbria, in 2012, over 38% of total damage was done to roads. 

Damage done by weather results in even more problems. According to BCI Supply Chain Resilience Report from 2024, over 87% of organizations seek to understand their supply chain exposure to weather related events and natural disasters or plan to in the future. In the same report, researchers indicate that over 25% companies' supply chains were affected either by natural disasters or adverse weather.

##Our solution
###Data

We propose a solution, that utilises data from several sources:
- Sentinel 1 moisture data
- Sentinel 2 RGB data
- SoilGrips local soil content details
- Open Street Map

After fusing the data from all the sources above, we employ our model for mobility prediction.

###Algorithms
We propose a Fuzzy Rule-Based solution which for predicts a mobility index for each location (pixel) taking into account the data described above as well as vehicle type and its parameters.

After the mobility index mapping is complete, we use those values as weights for a pathfinding algorithm which proposes the optimal path for a specified vehicle.

##Our clients
We target primarily:
- Government institutions to supply fresh water, food and other resources during crisis enhancing public safety
- Military during operations in terrain (especially off-road) 
- Civilians in case of evacuation By agriculture to plan and optimize usage of high-weight equipment
- 
