from airflow.utils.task_group import TaskGroup
from airflow.decorators import task
from airflow import DAG


class CustomTaskGroup(TaskGroup):
    """A task group to create dynamic tasks."""

    # defining defaults of input arguments num1 and num2
    def __init__(self, group_id, dag=None,  num2=0, tooltip="custom", **kwargs):
        """Instantiate a custom task group"""
        super().__init__(group_id=group_id, tooltip=tooltip, **kwargs)