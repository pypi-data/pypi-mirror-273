import datetime
import json
import logging
import re
from copy import deepcopy
from json import JSONDecodeError
from typing import Dict, Any, List, Callable, Union

from airflow import DAG
from airflow.exceptions import AirflowSkipException
from airflow.models import BaseOperator, TaskInstance, MappedOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.module_loading import import_string
from airflow.utils.task_group import TaskGroup
from airflow.models.xcom_arg import XComArg

from datamorphairflow import utils
from datamorphairflow.helper_classes import WorkflowDAG, WorkflowDAGNode


class WorkflowDagBuilder:
    """
    Generates tasks and a DAG from a config.
    :param dag_name: the name of the DAG
    :param dag_config: a dictionary containing configuration for the DAG
    :param default_config: a dictionary containing defaults for all DAGs
    """

    def __init__(
            self, dag_name: str, dag_config: Dict[str, Any], default_config: Dict[str, Any],
            workflow_nodes: List[WorkflowDAGNode]
    ) -> None:
        self.dag_name: str = dag_name
        self.dag_config: Dict[str, Any] = deepcopy(dag_config)
        self.default_config: Dict[str, Any] = deepcopy(default_config)
        self.workflow_nodes: List[WorkflowDAGNode] = deepcopy(workflow_nodes)

    def get_dag_params(self) -> Dict[str, Any]:
        """
        Check all the default parameters for DAGs and validate the type.
        TBD
        :return:
        """

        dag_params: Dict[str, Any] = {**self.dag_config, **self.default_config}

        # check if the schedule_interval is set to None
        if (
                utils.check_dict_key(dag_params, "schedule_interval")
                and dag_params["schedule_interval"] == "None"
        ):
            dag_params["schedule_interval"] = None

        try:
            dag_params["start_date"]: datetime = utils.get_datetime(
                date_value=dag_params["start_date"],
                timezone=dag_params.get("timezone", "UTC"),
            )
        except KeyError as err:
            raise Exception(f"{self.dag_name} config is missing start_date") from err

        return dag_params

    def pre_execute(context):
        """
        This function will be triggered before each task execution. Checks the status of the upstream tasks
        and if parent node is in "upstream_failed" state, then skips the current task.
        As of Airflow version 2.2.5, if parent task is in "upstream_failed" state and current task trigger_rule
        is "all_failed/one_failed" then the current task still executes. To work around this behavior, this
        method raises an AirflowSkipException if parent status is upstream failed.
        :param context:
        :return:
        """
        # logging.debug("Running pre_execute...")
        task = context['task']
        upstream_ids = task.upstream_task_ids
        logging.debug(f" Upstream task ids: {task.upstream_task_ids}")
        execution_date = context['execution_date']
        dag_instance = context['dag']
        upstream_failed_count = 0
        for each in upstream_ids:
            operator_instance = dag_instance.get_task(each)
            task_status = TaskInstance(operator_instance, execution_date).current_state()
            logging.debug(f" Status for upstream task {each} is {task_status}")
            if task_status == "upstream_failed" or task_status == "skipped":
                upstream_failed_count = upstream_failed_count + 1
        # raise exception if all the upstream nodes failed or skipped
        # the logic to check this can be changed
        if upstream_failed_count >= 1 and upstream_failed_count == len(upstream_ids):
            raise AirflowSkipException

    @staticmethod
    def replace_expand_values(task_conf: Dict, tasks_dict: Dict[str, BaseOperator]):
        """
        Replaces any expand values in the task configuration with their corresponding XComArg value.
        :param: task_conf: the configuration dictionary for the task.
        :type: Dict
        :param: tasks_dict: a dictionary containing the tasks for the current DAG run.
        :type: Dict[str, BaseOperator]

        :returns: updated conf dict with expanded values replaced with their XComArg values.
        :type: Dict
        """

        for expand_key, expand_value in task_conf["expand"].items():
            if ".output" in expand_value:
                task_id = expand_value.split(".output")[0]
                if task_id in tasks_dict:
                    task_conf["expand"][expand_key] = XComArg(tasks_dict[task_id])
            elif "XcomArg" in expand_value:
                task_id = re.findall(r"\(+(.*?)\)", expand_value)[0]
                if task_id in tasks_dict:
                    task_conf["expand"][expand_key] = XComArg(tasks_dict[task_id])
        return task_conf

    @staticmethod
    def create_task_group(workflow_node_list: List[WorkflowDAGNode], dag: DAG) -> Dict[str, "TaskGroup"]:
        """
        Takes a DAG and node with task group configurations. Creates TaskGroup instances.
        :param node:
        :param dag:
        :return:
        """
        # todo    tooltip can be desc
        # first trial without parallelism or param extract

        task_groups_dict: Dict[str, "TaskGroup"] = {}
        for node in workflow_node_list:
            node_type = node.type
            node_name = node.name

            if node_type == 'taskgroup':
                # create a Task group for each  with the properties
                node.taskparams["group_id"] = node_name
                node.taskparams["dag"] = dag
                task_group = TaskGroup(**node.taskparams)
                task_groups_dict[node_name] = task_group
        return task_groups_dict

    @staticmethod
    def generate_task_group_loop(workflow_node_list: List[WorkflowDAGNode], dag: DAG) -> Dict[str, "TaskGroup"]:
        """
        Takes a DAG and node with task group configurations. Creates TaskGroup instances.
        :param node:
        :param dag:
        :return:
        """
        # todo    tooltip can be desc
        # first trial without parallelism or param extract

        task_groups_dict: Dict[str, "TaskGroup"] = {}
        for node in workflow_node_list:
            node_type = node.type
            node_name = node.name

            if node_type == 'taskgroup':
                # create a Task group for each  with the properties
                node.taskparams["group_id"] = node_name
                node.taskparams["dag"] = dag
                task_group = TaskGroup(**node.taskparams)
                task_groups_dict[node_name] = task_group
                groups = []
                get_files = [1, 2, 3, 4, 5]
                for file in get_files:
                    group_name = node.name + '_' + str(file)
                    node.taskparams["group_id"] = group_name
                    node.taskparams["dag"] = dag
                    node.dependson = node.dependson if len(groups) == 0 else groups[-1]
                    task_group = TaskGroup(**node.taskparams)
                    task_groups_dict[group_name] = task_group
                    groups.append(group_name)
        return task_groups_dict

    @staticmethod
    def create_task(node: WorkflowDAGNode, dag: DAG) -> BaseOperator:
        """
        create task using the information from node and returns an instance of the Airflow BaseOperator
        :param dag:
        :return: instance of operator object
        """
        operator = node.type
        task_params = node.taskparams
        task_params["task_id"] = node.name
        task_params["dag"] = dag

        try:
            operator_obj: Callable[..., BaseOperator] = import_string(operator)
        except Exception as err:
            raise Exception(f"Failed to import operator: {operator}") from err
        try:
            # check for PythonOperator and get Python Callable from the
            # function name and python file with the function.
            if operator_obj in [PythonOperator, BranchPythonOperator]:
                if (
                        not task_params.get("python_callable_name")
                        and not task_params.get("python_callable_file")
                ):
                    raise Exception(
                        "Failed to create task. PythonOperator and BranchPythonOperator requires \
                        `python_callable_name` and `python_callable_file` parameters"
                    )
                if not task_params.get("python_callable"):
                    task_params[
                        "python_callable"
                    ]: Callable = utils.get_python_callable(
                        task_params["python_callable_name"],
                        task_params["python_callable_file"],
                    )
                    # remove DataMorph specific parameters
                    del task_params["python_callable_name"]
                    del task_params["python_callable_file"]

                # loading arguments as json for handling positional arguments, arrays and strings
                if task_params.get("op_args"):
                    op_args_string = task_params["op_args"]
                    try:
                        op_args_json = json.loads(op_args_string)
                    except JSONDecodeError:
                        op_args_json = op_args_string
                    if isinstance(op_args_json, dict):
                        # op_kwargs for dict
                        task_params["op_kwargs"] = op_args_json
                        del task_params["op_args"]
                    else:
                        # op_args is for list of positional arguments or strings
                        task_params["op_args"] = op_args_json

            task_params["pre_execute"] = WorkflowDagBuilder.pre_execute

            # Set expand args and check in the expand feature
            expand_kwargs: Dict[str, Union[Dict[str, Any], Any]] = {}

            # For expand feature:
            if utils.check_dict_key(task_params, 'expand'):
                (task_params, expand_kwargs, partial_kwargs) = utils.get_expand_partial_kwargs(task_params)
                if partial_kwargs:
                    task_params.update(partial_kwargs)

            # create task  from the base operator object with all the task params
            task: Union[BaseOperator, MappedOperator] = (
                operator_obj(**task_params)
                if not expand_kwargs
                else operator_obj.partial(**task_params).expand(**expand_kwargs)
            )
        except Exception as err:
            raise Exception(f"Failed to create {operator_obj} task") from err
        return task

    def build(self) -> WorkflowDAG:
        """
        Generates a DAG from the dag parameters
        step 1: iterate through all the nodes in list of WorkflowDAGNode
        step 2: create task_params for each node
        step 3: set upstream based on the depends on criteria
        step 4: return dag with the dag name as WorkflowDAG object
        :return:
        """

        dag_kwargs = self.get_dag_params()
        dag: DAG = DAG(**dag_kwargs)

        # create task groups here
        workflow_task_groups_dict = WorkflowDagBuilder.create_task_group(self.workflow_nodes, dag)

        # workflow dictionary to maintain node name and Task as Airflow BaseOpertaor
        workflow_dict = {}
        task_conf_dict = {}

        # create node dictionary for actions and triggers
        for node in self.workflow_nodes:
            # logging.debug(f"Node name: {node}")
            if node.type != 'taskgroup':
                name = node.name
                # If any node is part of taskgroup add the taskgroup instance
                if workflow_task_groups_dict and node.taskparams.get("task_group_name"):
                    node.taskparams["task_group"] = workflow_task_groups_dict[node.taskparams.get("task_group_name")]
                    del node.taskparams["task_group_name"]
                if utils.check_dict_key(node.taskparams, 'expand'):
                    node.taskparams = self.replace_expand_values(node.taskparams, workflow_dict)

                task = WorkflowDagBuilder.create_task(node, dag)
                task_conf_dict[name] = task
                workflow_dict[task.task_id] = task

        # todo this loop is to set dependencies with tasks and groups
        # todo will have to move to a different method
        tasks_and_task_group_instances = {**workflow_dict, **workflow_task_groups_dict}
        for node in self.workflow_nodes:
            dependsOn = node.dependson
            dependsOnList = []
            name = node.name
            if task_conf_dict.get(node.name) is not None and task_conf_dict.get(
                    node.name).task_group.group_id is not None:
                name = f"{task_conf_dict.get(node.name).task_group.group_id}.{node.name}"

            if dependsOn is not None:
                baseNode: Union[BaseOperator, "TaskGroup"] = tasks_and_task_group_instances[name]

                for eachDependsOn in dependsOn:
                    # each dependency check if it is part of a taskgroup
                    # if it is part of a taskgroup, set the upstream accordingly with the name
                    dep = utils.remove_node_suffix(eachDependsOn)
                    if task_conf_dict.get(dep) is not None and task_conf_dict.get(dep).task_group.group_id is not None:
                        group_id = task_conf_dict.get(dep).task_group.group_id
                        dep = f"{group_id}.{dep}"

                    dependsOnList.append(tasks_and_task_group_instances[dep])
                baseNode.set_upstream(dependsOnList)

            # logging.debug(f"Depends on list: {dependsOnList}")
        return WorkflowDAG(self.dag_name, dag)
