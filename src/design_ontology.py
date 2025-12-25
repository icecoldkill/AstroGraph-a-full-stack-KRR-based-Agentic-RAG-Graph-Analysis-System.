from owlready2 import *
import types

# Create the ontology
onto = get_ontology("http://krr.org/space_exploration.owl")

with onto:
    # 1. Classes (20+)
    class Entity(Thing): pass
    class Agency(Entity): pass
    class GovernmentAgency(Agency): pass
    class PrivateCompany(Agency): pass
    
    class SpaceMission(Entity): pass
    class CrewedMission(SpaceMission): pass
    class UncrewedMission(SpaceMission): pass
    class MoonMission(SpaceMission): pass
    class MarsMission(SpaceMission): pass
    class InterstellarMission(SpaceMission): pass # NEW
    
    class Rocket(Entity): pass
    class ReusableRocket(Rocket): pass # NEW
    class ExpendableRocket(Rocket): pass # NEW
    
    class Satellite(Entity): pass
    class CommunicationSatellite(Satellite): pass # NEW
    class WeatherSatellite(Satellite): pass # NEW
    class SpySatellite(Satellite): pass # NEW

    class Payload(Entity): pass
    class ScientificInstrument(Payload): pass # NEW
    
    class LaunchSite(Entity): pass
    class SpacePort(LaunchSite): pass
    
    class Person(Entity): pass # NEW
    class Astronaut(Person): pass 
    class SpaceTourist(Person): pass # NEW
    
    class Orbit(Entity): pass
    class LowEarthOrbit(Orbit): pass # NEW
    class GeostationaryOrbit(Orbit): pass # NEW
    
    class CelestialBody(Entity): pass # NEW
    class Planet(CelestialBody): pass # NEW
    class Moon(CelestialBody): pass # NEW
    class Star(CelestialBody): pass # NEW
    
    class Country(Entity): pass
    class Continent(Entity): pass
    class MissionSuccessStatus(Entity): pass

    # 2. Enumeration class
    class LaunchStatus(Thing): pass
    
    onto.Success = LaunchStatus("Success")
    onto.Failure = LaunchStatus("Failure")
    onto.PartialFailure = LaunchStatus("PartialFailure")
    onto.Scheduled = LaunchStatus("Scheduled")
    
    LaunchStatus.equivalent_to = [OneOf([onto.Success, onto.Failure, onto.PartialFailure, onto.Scheduled])]

    # 3. Object Properties (7+)
    class launchedBy(ObjectProperty):
        domain = [SpaceMission]
        range = [Agency]
    
    class launchedFrom(ObjectProperty):
        domain = [SpaceMission]
        range = [LaunchSite]
    
    class carriedPayload(ObjectProperty):
        domain = [SpaceMission]
        range = [Payload]
    
    class hasOrbit(ObjectProperty):
        domain = [SpaceMission]
        range = [Orbit]
    
    class isSuccess(ObjectProperty, FunctionalProperty):
        domain = [SpaceMission]
        range = [LaunchStatus]

    class hasAgency(ObjectProperty):
        domain = [Rocket]
        range = [Agency]

    class refersToCountry(ObjectProperty):
        domain = [Agency]
        range = [Country]

    class inverseLaunchedBy(ObjectProperty):
        inverse_property = launchedBy

    # REQUIREMENT: Inverse Functional Property
    # If MissionA hasID X and MissionB hasID X, then MissionA = MissionB
    class hasUniqueMissionID(ObjectProperty, InverseFunctionalProperty):
        domain = [SpaceMission]
        range = [Thing] 

    # 4. Datatype Properties (7+)
    class hasBudget(DataProperty, FunctionalProperty):
        domain = [SpaceMission]
        range = [float]
    
    class launchDate(DataProperty):
        domain = [SpaceMission]
        range = [str]
    
    class missionCost(DataProperty):
        domain = [SpaceMission]
        range = [float]
    
    class rocketStatus(DataProperty):
        domain = [Rocket]
        range = [str]
    
    class payloadWeight(DataProperty):
        domain = [Payload]
        range = [float]
    
    class environmentalImpact(DataProperty):
        domain = [SpaceMission]
        range = [int]
    
    class missionName(DataProperty):
        domain = [SpaceMission]
        range = [str]

    # 5. Restrictions/Axioms
    Rocket.is_a.append(hasAgency.min(1, Agency))
    
    class HighBudgetMission(SpaceMission):
        equivalent_to = [SpaceMission & hasBudget.some(ConstrainedDatatype(float, min_inclusive = 1000.0))]

    class LaunchEntity(Thing):
        equivalent_to = [GovernmentAgency | PrivateCompany]
    
    class SuccessfulMoonMission(SpaceMission):
        equivalent_to = [MoonMission & isSuccess.value(onto.Success)]

    class FailedMission(SpaceMission):
        equivalent_to = [SpaceMission & Not(isSuccess.value(onto.Success))]

    # NEW: Intersection Axiom
    class CommercialSpaceFlight(SpaceMission):
        equivalent_to = [SpaceMission & launchedBy.some(PrivateCompany)]
        
    # NEW: Complement Axiom
    class NonGovernmentMission(SpaceMission):
        equivalent_to = [SpaceMission & Not(launchedBy.some(GovernmentAgency))]

# Save the ontology
onto.save(file="/Users/ahsansaleem/Desktop/krrfinalproject/ontology/space_exploration.owl", format="rdfxml")
print("Ontology created at /Users/ahsansaleem/Desktop/krrfinalproject/ontology/space_exploration.owl")
