#!/usr/bin/env  python3
import asyncio
import logging
import threading

from aiohue import HueBridgeV1
from aiohue.v1.lights import Light
from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Statistics.DiscreteStatsCumulative import DiscreteStatsCumulative

from Santa_IW.PluginBase import PluginBase
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly


class AttachHue(PluginBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger

        self.bridge = self.config().get_item("bridge")
        self.light = self.config().get_item("lightname")
        self.hue_app_key = self.config().get_item("hue_app_key", secrets=True)
        self.min_delay = float(self.config().get_item("min_delay"))
        self.max_delay = float(self.config().get_item("max_delay"))
        self.since_last_update = ElapsedTime("since_update")
        self.num_light_updates = 0
        self.last_light_status = None
        # keep last
        self.helper = HueHelper(self.bridge, self.hue_app_key, self.light)
        self.tree_root_subassembly.register_status_observer(self.observe_subject_status)
        self.log_internal_status(Status.OK, message="Started")
        self._observed_status = DiscreteStatsCumulative(self.prefix_name("ObservedStatus"))
        self._light_updates = DiscreteStatsCumulative(self.prefix_name("LightUpdates"))

    # def extendParser(self):
    #     pass
    #     # can set thresholds to allow known count of uncorrectable errors if needed

    # noinspection PyUnusedLocal
    def observe_subject_status(self, sub: Subassembly, status: Status, attention: bool, assess=True) -> None:
        with self._status_lock:
            self._observed_status.sample(status)
            changed = status != self.last_light_status
            must_wait = self.since_last_update.current() <= self.min_delay
            stale = self.since_last_update.current() > self.max_delay
            if not must_wait and (changed or stale):
                self._light_updates.sample(status)
                self.last_light_status = status
                thread= threading.Thread(target=self.helper.run_hue, args=(status,))
                thread.start()
                self.since_last_update.start()
                self.num_light_updates += 1


from Santa_IW.DiscoveryHelper import DiscoveryHelper

plugin_helper: DiscoveryHelper = DiscoveryHelper(AttachHue)
plugin_helper.alias("AttachHue",
                    bridge="hue.home.goncalo.name",
                    hue_app_key="{{__HUE_APP_KEY__}}",
                    lightname="Santa_IW",
                    min_delay=30.0,
                    max_delay=120.0

                    )


class HueHelper:

    def __init__(self, bridge, hue_app_key, lightname):
        self.logger = logging.getLogger(__name__)
        self.bridge = bridge
        self.hue_app_key = hue_app_key
        self.lightname = lightname

    # noinspection PyUnusedLocal
    async def async_hue(self, status: Status) -> None:

        async with HueBridgeV1(self.bridge, self.hue_app_key) as bridge:

            self.logger.info(f"Connected to bridge: {bridge.bridge_id}")
            light: Light = bridge.lights.items[-1]

            for alight in bridge.lights.items:
                # self.logger.info(f"{alight.id} name={alight.name}")
                if alight.name == self.lightname:
                    self.logger.info(f"Found indicator at {alight.id} name={alight.name}")
                    light = alight

            # turn on a light
            self.logger.info("on, 100")
            await light.set_state(on=True, effect="none")
            self.logger.info(f"on, {status}")

            alert = "select"
            # https://developers.meethue.com/develop/hue-api-v2/getting-started/
            if status == Status.OK:
                xy = (0.2, 0.7)  # green
                hue = 25500
            elif status == Status.WARNING:
                hue = 11000
                xy = (0.5, 0.4)  # yellow
            elif status == Status.CRITICAL:
                hue = 0
                xy = (0.5, 0.2)  # red
                alert = "lselect"
            else:
                hue = 46920
                xy = (0.15, 0.1)  # blue

            await light.set_state(bri=200, sat=254, hue=hue, alert=alert, transitiontime=20)
            # await light.set_state(xy=xy,alert="select",transitiontime=10,bri=200)
            self.logger.info(f"Light {status=} {alert=} {hue=} ")
            await asyncio.sleep(2)
            await bridge.lights.update()

    def run_hue(self, status: Status):
        try:
            asyncio.run(self.async_hue(status))
        except KeyboardInterrupt:
            pass
