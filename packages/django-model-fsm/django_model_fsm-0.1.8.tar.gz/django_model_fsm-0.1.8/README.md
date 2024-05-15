# django-model-fsm

A package to use transitions with a Django model.


## Usage 

``` python
from django.db import models

from django_model_fsm.dataclasses import StateData, TriggerData, WorkflowData
from django_model_fsm.models import TransitionsMixin

# States
# fmt: off
S_CREATED = StateData(
    id="created",
    label="Created",
)
S_PUBLISHED = StateData(
    id="published",
    label="Published",
)
S_ARCHIVED = StateData(
    id="archived",
    label="Archived",
)
# fmt: on

# Triggers
# fmt: off
T_PUBLISHED_CHALLENGE_MODEL = TriggerData(
    id="published_challenge_model",
    label="Publish",
    order=150,
    need_confirmation=False,
)
T_UNPUBLISHED_CHALLENGE_MODEL = TriggerData(
    id="unpublished_challenge_model",
    label="Unpublish",
    order=175,
    need_confirmation=True,
)
T_ARCHIVE_CHALLENGE_MODEL = TriggerData(
    id="archive_challenge_model",
    label="Archive",
    order=350,
    need_confirmation=True,
)
# fmt: on

challenge_model_workflow = WorkflowData(
    initial_state=S_CREATED,
    transitions_data=[
        # fmt: off
        {"trigger": T_PUBLISHED_CHALLENGE_MODEL, "source": S_CREATED, "dest": S_PUBLISHED},
        {"trigger": T_UNPUBLISHED_CHALLENGE_MODEL, "source": S_PUBLISHED, "dest": S_CREATED},
        {"trigger": T_ARCHIVE_CHALLENGE_MODEL, "source": S_PUBLISHED, "dest": S_ARCHIVED},
        # fmt: on
    ],
)


class MyModel(models.Model, TransitionsMixin):
    workflow_data = challenge_model_workflow
    workflow_callbacks = []

```
