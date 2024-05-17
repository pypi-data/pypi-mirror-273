from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

from datamorphairflow.hooks import WorkflowParameters


class DMAWSGlueRunNowJobOperator(GlueJobOperator):
    """
    Extension of aws glue run operator with custom status push to xcom
    """

    def __init__(self, run_job_kwargs=None, *args, **kwargs):
        super().__init__(run_job_kwargs=run_job_kwargs, **kwargs)
        self.jar_params = None
        if run_job_kwargs is None:
            run_job_kwargs = dict()
        self.run_job_kwargs = run_job_kwargs
        self.args = args
        self.kwargs = kwargs

    def execute(self, context):
        workflow_params = WorkflowParameters(context)
        params = workflow_params.get_params()
        print(params)
        param_list = dict()

        # 1.check if params is not empty
        # 2. If not empty, construct the required string/list "--params key=value"
        # 3. append list to job_param list
        if params:
            for k,v in params.items():
                param_list["--params"] = f'{k}={v}'
        args_list = dict()
        args_list["Arguments"] = param_list
        if self.run_job_kwargs:
            self.run_job_kwargs | args_list
        else:
            self.run_job_kwargs = args_list
        print(self.run_job_kwargs)
        #conn_id = self.kwargs.get("conn_id")
        job_id = self.kwargs.get("job_name")
        task_id = f'{self.kwargs.get("task_id")}_custom'
        run_now = GlueJobOperator(task_id=task_id,job_name=job_id, run_job_kwargs=self.run_job_kwargs, do_xcom_push=True).execute(context)




