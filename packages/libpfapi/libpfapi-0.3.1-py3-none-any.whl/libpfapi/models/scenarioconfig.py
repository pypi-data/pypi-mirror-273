"""
    ScenarioConfig is a low level configuration model, most desired actions can
    be performed directly from the :class:`~libpfapi.models.scenario.Scenario`
    model instead.

    It is provided for consistency purposes and can be used to push changes but
    it's not the recommeded approach.
"""
from . import base


class ScenarioConfig(base.Model):
    """
        Pathfinder ScenarioConfig model
    """
    def __init__(self, api=None):
        self.pdefaults = {
            "id": None,
            "layer_weight_enabled": False,
            "category_values_setting": "3",
            "layer_min_resistance": -3,
            "layer_max_resistance": 3,
            "layer_weight_values": [],
            "threshold_multiplier": 0,
            "pylon_max_m": 230,
            "pylon_min_m": 120,
            "price_currency": "EUR",
            "corridor_threshold_method": "percentage",
            "mcda_dist_weight_factor": 0.1,
            "loaded": True,
            "weight_intervals": [1, 2, 3],
            "pylon": 9,
            "path_price_per_km": 1,
            "cost_data": {},
            "routing_model": None,
            "mcda_class_model": "GilyticsMCDA",
            "angle_cost_function": "linear",
            "angle_weight": 0.2,
            "edge_weight": 0.2,
            "max_angle": 90,
            "max_direction_deviation": 90,
            "between_points_allowed": True,
            "cost_models": []}

        # Dirty parameters are used to handle direct patches to parameters that
        # did not exist in the api when the current version of the library was
        # implemented. This lets us give support to unexisting configurations
        # before releasing a new library version (making version transition
        # easier and less stressful for us)
        self.__dirty_parameters = []

        # Internal handling of what to POST on update
        self.__pload_items = []
        super(ScenarioConfig, self).__init__(api)

    @classmethod
    def NewFromDict(cls, ddict, api=None):
        """
            Return a new LayerConfig instance from a JSON dictionary
        """
        result = cls(api)
        result._raw = ddict

        for k, v in ddict.items():
            if k == "scenario":
                # do not build an scenario, simply keep ID and
                # we can generate it if ever called
                setattr(result, "scenario_id", v)
                continue
            setattr(result, k, v)

        return result

    def add_dirty_parameter(self, pname):
        self.__dirty_parameters.append(pname)

    def push_changes_to_server(self):
        """
            Update this LayerConfig in the server with performed
            modifications
        """
        # payload = {k: getattr(self, k) for k in self.__pload_items}

        # TODO for the moment we push as a block since we modify
        # this config liberally
        payload = {k: getattr(self, k) for k in self.pdefaults.keys()}

        # Dirty parameters get preference
        payload.update({k: getattr(self, k) for k in self.__dirty_parameters})

        self._api.patch_scenario_config(self.id, **payload)
        self.__pload_items = []
        self.__dirty_parameters = []
