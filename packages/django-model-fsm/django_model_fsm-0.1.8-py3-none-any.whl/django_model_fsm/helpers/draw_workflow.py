import copy
import subprocess
from pathlib import Path

from transitions.extensions import GraphMachine


class DrawWorkflow:
    def __init__(self, model: object, name: str, workflow: dict, export_path: Path):
        self.model = model
        self.name = name
        self.workflow = workflow
        self.export_path = export_path

    def _get_translated_states(self) -> list:
        states = []
        for state in self.workflow.states:
            new_state = copy.deepcopy(state)
            new_state._name = self.model.workflow_data.get_state_as_label(
                new_state.name,
            )
            states.append(new_state)

        return states

    def _get_translated_transitions(self) -> list:
        return [
            {
                "trigger": self.model.workflow_data.get_labels_for_triggers()[transition["trigger"]],
                "source": self.model.workflow_data.get_state_as_label(
                    transition["source"],
                ),
                "dest": self.model.workflow_data.get_state_as_label(
                    transition["dest"],
                ),
            }
            for transition in self.workflow.transitions
        ]

    def draw(self):
        class _MP:
            pass

        mp = _MP()

        transitions = self._get_translated_transitions()
        states = self._get_translated_states()
        initial_state = states[0]

        _machine = GraphMachine(
            model=mp,
            states=states,
            transitions=transitions,
            show_auto_transitions=False,
            initial=initial_state,
            title=f"- Cycle de vie de {self.model.__name__} -",
        )

        dot = mp.get_graph().string().replace("\\n", "\n").replace("\\t", "\t").replace("\\l", "")

        mp.get_status_as_label = self.model.workflow_data.get_state_as_label

        mp.fsm_initial_state = "initiée"
        mp.fsm_states = states
        mp.fsm_transitions = transitions

        path = self.export_path / Path(f"{self.name}_workflow.dot")
        with path.open("w") as f:
            f.write(dot)

        self._transform_to_png(path=path)

        for key in self.workflow.states:
            state = key.name

            this_dot = dot.replace(
                f'label="{self.model.workflow_data.get_state_as_label(state)}"',
                f'label="{self.model.workflow_data.get_state_as_label(state)}", fillcolor=green',
            )

            path = self.export_path / Path(f"{self.name}_workflow-{state}.dot")
            with path.open("w") as f:
                f.write(this_dot)

            self._transform_to_png(path=path)

    @staticmethod
    def _transform_to_png(path: Path):
        png = str(path).replace(".dot", ".png")
        subprocess.run(
            ["/usr/bin/dot", "-Tpng", f"-o{png}", path],  # NOQA: S603
            check=True,
        )
        subprocess.run(
            ["/usr/bin/optipng", png],  # NOQA: S603
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
