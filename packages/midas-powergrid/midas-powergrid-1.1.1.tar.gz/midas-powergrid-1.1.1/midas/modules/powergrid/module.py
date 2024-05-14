"""This module contains the MIDAS powergrid upgrade."""

import logging
import os

import numpy as np

from midas.util.upgrade_module import UpgradeModule

from .analysis.grid import analyze_grid

LOG = logging.getLogger(__name__)


class PowergridModule(UpgradeModule):
    """The MIDAS powergrid update module."""

    def __init__(self):
        super().__init__(
            module_name="powergrid",
            default_scope_name="midasmv",
            default_sim_config_name="Powergrid",
            default_import_str=(
                "midas.modules.powergrid.simulator:PandapowerSimulator"
            ),
            default_cmd_str=(
                "%(python)s -m midas.modules.powergrid.simulator %(addr)s"
            ),
            log=LOG,
        )

        self.models = {
            "Line": [
                ("loading_percent", "float", 0.0, 200.0),
                ("in_service", "bool", 0, 2),
            ],
            "Trafo": [
                ("loading_percent", "float", 0.0, 200.0),
                ("in_service", "bool", 0, 2),
            ],
            "Bus": [
                ("vm_pu", "float", 0.0, 1.2),
                ("va_degree", "float", -180.0, 180.0),
                ("p_mw", "float", -np.inf, np.inf),
                ("q_mvar", "float", -np.inf, np.inf),
                ("in_service", "bool", 0, 2),
            ],
            "Load": [
                ("p_mw", "float", 0, np.inf),
                ("q_mvar", "float", -np.inf, np.inf),
                ("in_service", "bool", 0, 2),
            ],
            "Sgen": [
                ("p_mw", "float", 0, np.inf),
                ("q_mvar", "float", -np.inf, np.inf),
                ("in_service", "bool", 0, 2),
            ],
            "Storage": [
                ("p_mw", "float", -np.inf, np.inf),
                ("q_mvar", "float", -np.inf, np.inf),
                ("in_service", "bool", 0, 2),
            ],
            "Ext_grid": [
                ("p_mw", "float", -np.inf, np.inf),
                ("q_mvar", "float", -np.inf, np.inf),
            ],
            "Switch": [("closed", "bool", 0, 2)],
        }
        self._double_actuator_values: bool = False

    def check_module_params(self, module_params: dict):
        """Check the module params for this upgrade."""

        module_params.setdefault("plotting", False)
        module_params.setdefault(
            "plot_path",
            os.path.abspath(
                os.path.join(self.scenario.base.output_path, "plots")
            ),
        )
        module_params.setdefault("save_grid_json", False)
        module_params.setdefault("use_constraints", False)
        module_params.setdefault("constraints", [])

    def check_sim_params(self, module_params: dict):
        """Check simulator params for a certain simulator."""

        self.sim_params.setdefault("gridfile", self.default_scope_name)
        self.sim_params.setdefault("grid_params", {})
        self.sim_params.setdefault("plotting", module_params["plotting"])
        self.sim_params.setdefault("plot_path", module_params["plot_path"])
        self.sim_params.setdefault(
            "save_grid_json", module_params["save_grid_json"]
        )
        self.sim_params.setdefault(
            "use_constraints", module_params["use_constraints"]
        )
        self.sim_params.setdefault("constraints", module_params["constraints"])
        self.sim_params.setdefault("grid_mapping", {})

    def start_models(self):
        """Start all models for this simulator.

        Since we want the grids to be able to be interconnected with
        each other, each grid model should have its own simulator.

        Parameters
        ----------
        sim_name : str
            The sim name, not to be confused with *sim_name* for
            mosaik's *sim_config*. **This** sim_name is the simulator
            key in the configuration yaml file.

        """
        model_key = self.scenario.generate_model_key(self)
        # self.sim_params["grid_params"]["gridfile"] = self.sim_params[
        # "gridfile"
        # ]
        grid_params = {
            "gridfile": self.sim_params["gridfile"],
            "grid_params": self.sim_params["grid_params"],
        }
        if self.sim_params["use_constraints"]:
            grid_params["use_constraints"] = True
            grid_params["constraints"] = self.sim_params["constraints"]
        self.start_model(model_key, "Grid", grid_params)
        self._double_actuator_values = grid_params["grid_params"].get(
            "double_actuator_values", False
        )

        for entity in self.scenario.get_model(
            model_key, self.sim_key
        ).children:
            parts = entity.eid.split("-")
            child_key = f"{model_key}"
            for part in parts[1:]:
                child_key += f"_{part}"

            self.scenario.script.model_start.append(
                f"{child_key} = [e for e in {model_key}.children "
                f'if e.eid == "{entity.eid}"][0]\n'
            )
            self.scenario.add_model(child_key, self.sim_key, entity)

    def connect(self, *args):
        # Nothing to do so far
        # Maybe to other grids in the future?
        pass

    def connect_to_db(self):
        """Add connections to the database."""

        grid_key = self.scenario.generate_model_key(self)
        db_key = self.scenario.find_first_model("store", "database")[0]

        for key, entity in self.scenario.get_models(self.sim_key).items():
            if grid_key not in key:
                continue
            mod_key = key

            # We only want to connect those attributes that are present
            # in the grid. That's why we iterate over existing entities
            # and not simply use the models defined above.
            if entity.type in self.models:
                self.connect_entities(
                    mod_key,
                    db_key,
                    [a[0] for a in self.models[entity.type]],
                )

        additional_attrs = ["health"]
        if self.sim_params["save_grid_json"]:
            additional_attrs.append("grid_json")

        self.connect_entities(grid_key, db_key, additional_attrs)

    def get_sensors(self):
        grid_key = self.scenario.generate_model_key(self)
        grid = self.scenario.get_model(grid_key)
        for entity in grid.children:
            if entity.type in self.models:
                for attr in self.models[entity.type]:
                    name, dtype, low, high = attr
                    # if entity.type == "bus" and name in ["p_mw", "q_mvar"]:
                    #     # We don't want p and q of buses to be sensors
                    #     continue
                    if dtype in ["bool", "int"]:
                        space = f"Discrete({high})"
                    else:
                        space = (
                            f"Box(low={low}, "
                            f"high={high}, shape=(), dtype=np.float32)"
                        )

                    self.scenario.sensors.append(
                        {
                            "uid": f"{entity.sid}.{entity.eid}.{name}",
                            "space": space,
                        }
                    )
        self.scenario.sensors.append(
            {
                "uid": f"{grid.full_id}.health",
                "space": ("Box(low=0, high=1.2, shape=(), dtype=np.float32)"),
            }
        )
        # self.scenario.sensors.append(
        #     {
        #         "uid": f"{grid.full_id}.grid_json",
        #         "space": ("Box(low=0, high=1, shape=(), dtype=np.float32)"),
        #     }
        # )

    def get_actuators(self):
        grid_key = self.scenario.generate_model_key(self)
        grid = self.scenario.get_model(grid_key)
        for entity in grid.children:
            if entity.type == "Trafo":
                self.scenario.actuators.append(
                    {
                        "uid": f"{entity.sid}.{entity.eid}.tap_pos",
                        "space": (
                            "Box(low=-10, high=10, shape=(), dtype="
                            "np.int32)"
                        ),
                    }
                )
            if entity.type in ("Load", "Sgen"):
                q_min = 0
                p_min = 0
                try:
                    try:
                        pp_grid = list(
                            self.scenario.get_sim(
                                self.sim_key
                            )._sim._inst.models.values()
                        )[0].grid
                    except AttributeError:
                        pp_grid = list(
                            self.scenario.get_sim(
                                self.sim_key
                            )._proxy.sim.models.values()
                        )[0].grid

                    _, etype, eidx, _ = entity.eid.split("-")
                    try:
                        p_max = pp_grid.get_value(etype, int(eidx), "max_p_mw")
                        p_min = pp_grid.get_value(etype, int(eidx), "min_p_mw")
                    except KeyError:
                        LOG.info(
                            "No max_p_mw or min_p_mw found, using p_mw as p_max and set p_min to 0"
                        )
                        p_max = pp_grid.get_value(etype, int(eidx), "p_mw")

                    try:
                        q_max = pp_grid.get_value(
                            etype, int(eidx), "max_q_mvar"
                        )
                        q_min = pp_grid.get_value(
                            etype, int(eidx), "min_q_mvar"
                        )
                    except KeyError:
                        LOG.info(
                            "No max_p_mw or min_p_mw found, using q_mvar as q_max and set q_min to 0"
                        )
                        q_max = pp_grid.get_value(etype, int(eidx), "q_mvar")

                except Exception as err:
                    LOG.warning(
                        "Caught an error composing actuator information for "
                        f"{etype} with eid {entity.eid}: {type(err), err}. "
                        "Continuing with p_max=0.5, q_max=0.5, and "
                        "p_min=q_min=0."
                    )
                    p_max = 0.5
                    q_max = 0.5

                if self._double_actuator_values:
                    p_max *= 2
                    q_max *= 2

                if q_max < q_min:
                    q_min = q_max
                    q_max = 0

                self.scenario.actuators.append(
                    {
                        "uid": f"{entity.sid}.{entity.eid}.p_mw",
                        "space": (
                            f"Box(low={p_min}, high={p_max}, shape=(), dtype="
                            "np.float32)"
                        ),
                    }
                )
                self.scenario.actuators.append(
                    {
                        "uid": f"{entity.sid}.{entity.eid}.q_mvar",
                        "space": (
                            f"Box(low={q_min}, high={q_max}, shape=(), dtype="
                            "np.float32)"
                        ),
                    }
                )

    def analyze(
        self,
        name,
        data,
        output_folder,
        start,
        end,
        step_size,
        full,
    ):
        grid_sim_keys = [
            sim_key for sim_key in data.keys() if "Powergrid" in sim_key
        ]
        for sim_key in grid_sim_keys:
            grid_data = data[sim_key]
            if start > 0:
                grid_data = grid_data.iloc[start:]
            if end > 0:
                grid_data = grid_data.iloc[:end]

            analyze_grid(
                grid_data,
                step_size,
                f"{name}-{sim_key.replace('/', '')}",
                output_folder,
                full,
            )

    def download(self, *args):
        # No downloads, suppress logging output
        pass
