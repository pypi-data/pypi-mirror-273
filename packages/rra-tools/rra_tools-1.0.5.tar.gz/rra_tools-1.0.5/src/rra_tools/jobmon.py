import datetime
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

from rra_tools.shell_tools import mkdir


def get_jobmon_tool(workflow_name: str):  # type: ignore[no-untyped-def]
    """Get a jobmon tool for a given workflow name with a helpful error message.

    Parameters
    ----------
    workflow_name
        The name of the workflow.

    Returns
    -------
    Tool
        A jobmon tool.

    Raises
    ------
    ModuleNotFoundError
        If jobmon is not installed.
    """
    try:
        from jobmon.client.tool import Tool  # type: ignore[import-not-found]
    except ModuleNotFoundError as e:
        msg = (
            "Jobmon is not installed.\n"
            "Ensure you have a file in your home "
            "directory at '~/.pip/pip.conf' with contents\n\n"
            "[global]\n"
            "extra-index-url = https://artifactory.ihme.washington.edu/artifactory/api/pypi/pypi-shared/simple\n"
            "trusted-host = artifactory.ihme.washington.edu/artifactory/api/pypi/pypi-shared\n\n"
            "and run 'pip install jobmon[ihme]' to install jobmon."
        )
        raise ModuleNotFoundError(msg) from e

    return Tool(workflow_name)


def build_parallel_task_graph(  # type: ignore[no-untyped-def]
    jobmon_tool,
    task_name: str,
    log_dir: str | Path,
    node_args: dict[str, list[Any]],
    task_resources: dict[str, str | int],
    runner: str = "rptask",
) -> list[Any]:
    task_template = jobmon_tool.get_task_template(
        default_compute_resources={
            **task_resources,
            "stdout": f"{log_dir}/output",
            "stderr": f"{log_dir}/error",
        },
        template_name=f"{task_name}_task_template",
        default_cluster_name="slurm",
        command_template=(
            f"{runner} {task_name} " + " ".join([f"--{k} {{{k}}}" for k in node_args])
        ),
        node_args=list(node_args),
        task_args=[],
        op_args=[],
    )
    return task_template.create_tasks(**node_args)  # type: ignore[no-any-return]


def run_workflow(  # type: ignore[no-untyped-def]
    workflow,
    log_method: Callable[[str], None] = print,
    **workflow_kwargs,
):
    # Calling workflow.bind() first just so that we can get the workflow id
    workflow.bind()
    log_method("Workflow creation complete.")
    log_method(f"Running workflow with ID {workflow.workflow_id}.")
    log_method("For full information see the Jobmon GUI:")
    log_method(
        f"https://jobmon-gui.ihme.washington.edu/#/workflow/{workflow.workflow_id}/tasks"
    )

    # run workflow
    status = workflow.run(**workflow_kwargs)
    log_method(f"Workflow {workflow.workflow_id} completed with status {status}.")
    return status


def make_log_dir(output_dir: str | Path) -> Path:
    run_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")  # noqa: DTZ005
    log_dir = Path(output_dir) / "zzz_logs" / run_time
    mkdir(log_dir, parents=True)
    return log_dir


def run_parallel(
    task_name: str,
    node_args: dict[str, list[Any]],
    task_resources: dict[str, str | int],
    runner: str,
    log_root: str | Path | None = None,
) -> None:
    """Run a parallel set of tasks using Jobmon.

    This helper function encapsulates one of the simpler workflow patterns in Jobmon:
    a set of tasks that run in parallel, each with the same command but
    different arguments. More complicated workflows should be implemented
    directly.

    Parameters
    ----------
    task_name
        The name of the task to run.  Will also be used as the tool and workflow name.
    node_args
        The arguments to the task script.
    task_resources
        The resources to allocate to the task.
    runner
        The runner to use for the task. Default is 'rptask'.
    log_root
        The root directory for the logs. Default is None.
    """
    if log_root is None:
        if "output-dir" not in node_args:
            msg = (
                "The node_args dictionary must contain an 'output-dir' key if no "
                "log_root is provided."
            )
            raise KeyError(msg)
        log_root = Path(node_args["output-dir"][0])
    log_dir = make_log_dir(log_root)

    tool = get_jobmon_tool(workflow_name=task_name)
    workflow = tool.create_workflow(name=f"{task_name}_{uuid.uuid4()}")

    tasks = build_parallel_task_graph(
        jobmon_tool=tool,
        task_name=task_name,
        log_dir=log_dir,
        node_args=node_args,
        task_resources=task_resources,
        runner=runner,
    )

    workflow.add_tasks(tasks)
    run_workflow(workflow)
