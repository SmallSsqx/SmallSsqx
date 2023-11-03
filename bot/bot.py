import sc2
from sc2 import BotAI, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.player import Bot, Computer

import random


class CompetitiveBot(BotAI):
    NAME: str = "SmallSsqx"
    RACE: Race = Race.Protoss

    def __init__(self):
        sc2.BotAI.__init__(self)
        self.proxy_built = False
        self.scouting_enabled = False

    async def on_start(self):
        self.chat_send("Game Started")
        self.chat_send("I am a Starcraft 2 bot. For now im getting tested. I cannot surrender, so you have to destroy all of my buildings")
        self.chat_send("I can't call gg at the end of the game, so I'm calling it now: GG")

    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_gateway()
        await self.build_assimilator()
        await self.build_cyber_core()
        await self.train_stalkers()
        await self.build_more_gates()
        await self.chrono_boost()
        await self.warpgate_research()
        await self.attack()
        await self.warp_stalkers()
        await self.stalker_micro()
        await self.disruptor_micro()
        await self.immortal_micro()
        await self.expand()
        await self.attack_enemy_expansions()
        await self.scouting()
        await self.robotics_bay()
        await self.train_disruptor()
        await self.robotics_facility()
        await self.train_immortal()
        await self.defense_normal()

    def on_building_destroyed(self, unit):
        if not self.enemy_structures:
            self.scouting_enabled = True
        else:
            self.scouting_enabled = False

    async def build_workers(self):
        nexus_units = self.townhalls.ready.random
        worker_count = self.workers.amount
        if (
            self.can_afford(UnitTypeId.PROBE)
            and workers.amount < townhalls.amount * 21
            and nexus.is_idle
        ):
            nexus.train(UnitTypeId.PROBE)

    async def build_pylons(self):
         nexus = self.townhalls.ready.random
         pos =  nexus.position.towards(self.enemy_start_locations[0],10)

         if (
             self.supply_left < 6
             and self.already_pending(UnitTypeId.PYLON) == 0
             and self.can_afford(UnitTypeId.PYLON)
         ):
             await self.build(UnitTypeId.PYLON, near = pos)

         if(
             (self.structures(UnitTypeId.GATEWAY).amount + self.structures(UnitTypeId.WARPGATE).amount) >= 4
             and not self.proxy_built
             and self.can_afford(UnitTypeId.PYLON)
         ):
             pos = self.game_info.map_center.towards(self.enemy_start_locations[0], 20)
             await self.build(UnitTypeId.PYLON, near = pos)

    async def build_gateway(self):
          if (
              self.structures(UnitTypeId.PYLON).ready
              and self.can_afford(UnitTypeId.GATEWAY)
              and not self.structures(UnitTypeId.GATEWAY)
          ):
              pylon = self.structures(UnitTypeId.PYLON).ready.random
              await self.build(UnitTypeId.GATEWAY, near = pylon)
              self.proxy_built = True

    async def build_assimilator(self):
          if self.structures(UnitTypeId.GATEWAY):
              for nexus in self.townhalls.ready:
              vgs = self.vespene_geyser.closer_than(15, nexus)
              for vg in vgs:
                  if not self.can_afford(UnitTypeId.ASSIMILATOR):
                      break
                  worker = self.select_build_worker(vg.position)
                  if worker is None:
                      break
                  if not self.gas_buildings or not self.gas_buildings.closer_than(1, vg):
                      worker.build(UnitTypeId.ASSIMILATOR, vg)
                      worker.stop(queue=True)

    async def build_cyber_core(self):
        if self.structures(UnitTypeId.PYLON).ready:
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            if self.structures(UnitTypeId.GATEWAY).ready:
                if not self.structures(UnitTypeId.CYBERNETICSCORE):
                    if (
                        self.can_afford(UnitTypeId.CYBERNETICSCORE)
                        and self.already_pending(UnitTypeId.CYBERNETICSCORE) == 0
                    ):
                        await self.build(UnitTypeId.CYBERNETICSCORE, near = pylon)

    async def train_stalkers(self):
        for gateway in self,structures(UnitTypeId.GATEWAY).ready:
            if (
                self.can_afford(UnitTypeId.STALKER)
                and gateway.is_idle
            ):
                gateway.train(UnitTypeId.STALKER)

    async def build_more_gates(self):
        if (
            self.structures(UnitTypeId.PYLON).ready
            and self.can_afford(UnitTypeId.GATEWAY)
            and self.structures(UnitTypeId.GATEWAY).amount < self.townhalls.amount * 3
        ):
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.GATEWAY, near = pylon)

    async def chrono_boost(self):
        if self.structures(UnitTypeId.PYLON):
            nexus = self.townhalls.ready.random
            if (
                not self.structures(UnitTypeId.CYBERNETICS_CORE).ready
                and self.structures(UnitTypeId.PYLON).amount > 0
            ):
                if nexus.energy >= 50:
                    nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus)
            else:
                if nexus.energy >= 50:
                    cybercore = self.structures(UnitTypeId.CYBERNETICS_CORE).ready.random
                    nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, cybercore)

    async def expand(self):
        if (
            self.can_afford(UnitTypeId.NEXUS)
            and not self.already_pending(UnitTypeId.NEXUS)
            and self.worker.amount * self.townhalls.amount < 22
        ):

            expand_location = await self.get_next_expansion()
            if expand_location:
                await self.build(UnitTypeId.NEXUS, near=expand_location)

    async def robotics_bay(self):
        if (
            self.structures(UnitTypeId.CYBERNETICS_CORE)
            and self.can_afford(UnitTypeId_ROBOTICS_BAY)
            and self.townhalls.amount > 1
            and self.structures(UnitTypeId.ROBOTICS_BAY).amount < 3
        ):
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.ROBOTICS_BAY, near = pylon)

    async def robotics_facility(self):
        if (
            self.structures(UnitTypeId.ROBOTICS_BAY)
            and self.can_afford(UnitTypeId.ROBOTICS_FACILITY)
            and not self.already_pending(UnitTypeId.ROBOTICS_FACILITY)
            and not self.structures(UnitTypeId.ROBOTICS_FACILITY).amount =< 1
        ):
            pylon = self.build(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.ROBOTICS_FACILITY, near = pylon)

    async def warpgate_research(self):
        if (
            self.structures(UnitTypeId.CYBERNETICS_CORE).ready
            and self.can_afford(AbilityId.WARPGATE_RESEARCH)
            and self.already_pending_upgrade(UpgradeId.WARPGATERESEARCH) == 0
        ):
            cybercore = self.structures(UnitTypeId.CYBERNETICS_CORE).ready.first
            cybercore.research(UpgradeId.WARPGATERESEARCH)

    async def attack(self):
        stalkercount = self.units(UnitTypeId.STALKER).amount
        stalkers = self.units(UnitTypeId.STALKER).ready.idle
        disruptors = self.units(UnitTypeId.DISRUPTOR).ready.idle
        immortals = self.units(UnitTypeId.IMMORTAL).ready.idle
        if self.structures(UnitTypeId.PYLON).ready:
            proxy = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])
            proxyposition = proxy.position.random_on_distance(3)
        for stalker in stalkers:
            if stalkercount < 10:
                stalker.attack(self.enemy_start_locations[0])
            else:
                stalker.attack(proxyposition)
        for disruptor in disruptors:
            if stalkercount < 10:
                disruptor.attack(self.enemy_start_locations[0])
            else:
                disruptor.attack(proxyposition)
        for immortal in immortals:
            if stalkercount < 10:
                immortal.attack(self.enemy_start_locations[0])
            else:
                immortal.attack(proxyposition)


    async def warp_stalkers(self):
        for warpgate in self.structures(UnitTypeId.WARPGATE).ready:
            abilities = await self.get_available_abilities(warpgate)
            proxy = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])
            if AbilityId.WARPGATETRAIN_STALKER in abilities and self.can_afford(UnitTypeId.STALKER):
                placement = proxy.position.random_on_distance(3)
                warpgate.warp_in(UnitTypeId.STALKER, placement)

    async def stalker_micro(self):
        stalkers = self.units(UnitTypeId.STALKER)
        enemy_location = self.enemy_start_location[0]

        if self.structures(UnitTypeId.PYLON).ready:
            pylon = self.structures(UnitTypeId.PYLON).closest_to(enemy_location)
            for stalker in stalkers:
                if stalker.weapon_cooldown == 0:
                    stalker.attack(enemy_location)
                elif stalker.weapon_cooldown < 0:
                    stalker.move(pylon)
                else:
                    stalker.move(pylon)

    async def disruptor_micro(self):
        disruptors = self.units(UnitTypeId.DISRUPTOR)
        enemy_location = self.enemy_start_location[0]
        if self.structures(UnitTypeId.PYLON).ready:
            pylon = self.structures(UnitTypeId.PYLON).closest_to(enemy_location)
            for disruptor in disruptors:
                if AbilityId.PURIFICATIONNOVA_cooldown == 0:
                    await self.do(disruptor(AbilityId.PURIFICATIONNOVA, enemy_location)
                elif AbilityId.PURIFICATIONNOVA_cooldown < 0:
                    await disruptor.move(pylon)
                else:
                    await disruptor.move(pylon)

    async def immortal_micro(self):
        immortals = self.units(UnitTypeId.IMMORTAL)
        enemy_location = self.enemy_start_location[0]
        if self.structures(UnitTypeId.PYLON).ready:
            pylon = self.structures(UnitTypeId.PYLON).closest_to(enemy_location)
            for immortal in immortals:
                if immortal.weapon_cooldown == 0:
                    immortal.attack(enemy_location)
                elif immortal.weapon_cooldown < 0:
                    immortal.move(pylon)
                else:
                    immortal.move(pylon)

    async def attack_enemy_expansions(self):
    if (
        self.enemy_structures(UnitTypeId.NEXUS).amount == 0
        or self.enemy_structures(UnitTypeId.HATCHERY).amount == 0
        or self.enemy_structures(UnitTypeId.LAIR).amount == 0
        or self.enemy_structures(UnitTypeId.HIVE).amount == 0
        or self.enemy_structures(UnitTypeId.COMMANDCENTER).amount == 0
        or self.enemy_structures(UnitTypeId.ORBITALCOMMAND).amount == 0
        or self.enemy_structures(UnitTypeId.PLANETARYFORTRESS).amount == 0
    ):
        stalker = self.units(UnitTypeId.STALKER)
        location = Point2((randint(0, self.game_info.map_size[0]), randint(0, self.game_info.map_size[1])))
                can_reach_location = await self.client.query_pathing(stalker, location)

                if can_reach_location:
                    stalker.attack(location)

    async def scouting(self):
        scout = self.units(UnitTypeId.PROBE).first
        if scout:
            if self.scouting_enabled:
                location = Point2((randint(0, self.game_info.map_size[0]), randint(0, self.game_info.map_size[1])))
                can_reach_location = await self.client.query_pathing(scout, location)

                if (
                    self.structures(UnitTypeId.PYLON).ready
                    and self.already_pending(UnitTypeId.PYLON) == 0
                    and can_reach_location
                ):
                    scout.move(location)

    async def train_disruptor(self):
        for robotics_bay in self.structures(UnitTypeId.ROBOTICS_BAY):
            if (
                self.can_afford(UnitTypeId.DISRUPTOR)
                and robotics_bay.is_idle
                and self.units(UnitTypeId.DISRUPTOR).amount < 3
            ):
                robotics_bay.train(UnitTypeId.DISRUPTOR)

    async def train_immortal(self):
        for robotics_bay in self.structures(UnitTypeId.ROBOTICS_BAY):
            if (
                self.can_afford(UnitTypeId.IMMORTAL)
                and robotics_bay.is_idle
            ):
                robotics_bay.train(UnitTypeId.IMMORTAL)

     async def defense_normal(self):
         if self.known_enemy_units.closer_than(10, self.structures)
             stalkers = self.units(UnitTypeId.STALKER)
                 if stalkers:
                     target = enemy_units_near_buildings.closest_to(stalkers.first)
                     for stalker in stalkers
                         stalker.attack(target)

     def on_end(self, result):
        print("Game Ended")
