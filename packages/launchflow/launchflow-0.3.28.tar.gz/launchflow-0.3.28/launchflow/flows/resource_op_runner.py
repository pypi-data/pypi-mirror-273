import asyncio
from typing import Dict, List, Optional, Tuple

from launchflow.clients.response_schemas import OperationStatus
from launchflow.operations import AsyncEntityOp
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


async def print_operation_status(
    progress: Progress,
    status: Optional[OperationStatus],
    success_message: Optional[str],
    operation_id: str,
    entity_ref: str,
    operation_type: str,
):
    if status is None:
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} status unknown for [blue]{entity_ref}[/blue]"
        )
    elif status.is_success():
        progress.console.print(
            f"[green]✓[/green] {operation_type} successful for [blue]{entity_ref}[/blue]"
        )
        if success_message:
            progress.console.print(f"    └── {success_message}")
        return True
    elif status.is_error():
        progress.console.print(
            f"[red]✗[/red] {operation_type} failed for [blue]{entity_ref}[/blue]"
        )
        progress.console.print(
            f"    └── View logs for the operation by running `launchflow logs {operation_id}`"
        )
        progress.console.print("")
    elif status.is_cancelled():
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} cancelled for [blue]{entity_ref}[/blue]"
        )
    else:
        progress.console.print(
            f"[yellow]?[/yellow] {operation_type} status unknown for [blue]{entity_ref}[/blue]"
        )
    return False


def _operation_start_title(resource_op: AsyncEntityOp) -> str:
    if resource_op._type == "create":
        op_type = "Creating"
    elif resource_op._type == "replace":
        op_type = "Replacing"
    else:
        raise ValueError(f"Unknown operation type {resource_op._type}")
    return f"{op_type} [blue]{resource_op.entity_ref}[/blue]..."


async def _start_ops(
    ops_to_start: List[Tuple[AsyncEntityOp, int]], progress: Progress
) -> List[Tuple[AsyncEntityOp, int]]:
    results = await asyncio.gather(
        *[op[0].run() for op in ops_to_start], return_exceptions=True
    )
    running_operations: List[Tuple[AsyncEntityOp, int]] = []
    for result, (resource_op, task) in zip(results, ops_to_start):
        if isinstance(result, Exception):
            progress.remove_task(task)
            progress.console.print(
                f"[red]✗[/red] Failed to start operation for [blue]{resource_op.entity_ref}[/blue]"
            )
            progress.console.print(f"    └── {result}")
        else:
            running_operations.append((resource_op, task))
    return running_operations


class ResourceOpRunner:

    def __init__(
        self,
        ops_to_run: List[AsyncEntityOp],
        wait_time: int = 3,
        console: Optional[Console] = None,
    ) -> None:
        self.wait_time = wait_time
        self.console = console
        # Ops with no dependencies or their dependencies are not part
        # of the ops_to_run list
        keyed_ops = {op.resource.name: op for op in ops_to_run}
        self.all_ops = ops_to_run
        self.root_ops = {}
        self.resource_to_children: Dict[str, AsyncEntityOp] = {}
        for op in ops_to_run:
            # If a resource has no dependencies, it is a root op
            if not op.resource._depends_on:
                self.root_ops[op.resource.name] = op
            else:
                if all(
                    resource.name not in keyed_ops
                    for resource in op.resource._depends_on
                ):
                    # If all dependencies are not part of the ops_to_run list
                    # then this is a root op
                    self.root_ops[op.resource.name] = op
                    continue
                # If the resource has dependencies, then add it to the
                # resource_to_deps dict
                for resource in op.resource._depends_on:
                    if resource.name not in keyed_ops:
                        continue
                    if resource.name not in self.resource_to_children:
                        self.resource_to_children[resource.name] = []
                    self.resource_to_children[resource.name].append(op)

    async def run(self) -> None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TextColumn("["),
            TimeElapsedColumn(),
            TextColumn("]"),
            console=self.console,
        ) as progress:
            started_operations: List[Tuple[AsyncEntityOp, int]] = []
            waiting_operations: Dict[str, Tuple[AsyncEntityOp, int]] = {}
            for resource_op in self.all_ops:
                if resource_op.resource.name in self.root_ops:
                    task = progress.add_task(
                        _operation_start_title(resource_op), total=1
                    )
                    started_operations.append((resource_op, task))
                else:
                    task = progress.add_task(
                        f"Waiting for dependencies of [blue]{resource_op.entity_ref}[/blue]...",
                        total=1,
                    )
                    waiting_operations[resource_op.resource.name] = (resource_op, task)
            running_operations: List[Tuple[AsyncEntityOp, int]] = await _start_ops(
                started_operations, progress
            )
            create_successes = 0
            create_failures = 0
            replace_successes = 0
            replace_failures = 0
            successfully_finished_resources = set()
            while running_operations:
                await asyncio.sleep(self.wait_time)
                to_stream_operations = []
                for operation, task in running_operations:
                    status = await operation.get_status()
                    if status.is_final():
                        progress.remove_task(task)
                        success = await print_operation_status(
                            progress=progress,
                            status=status,
                            success_message=operation.success_message,
                            operation_id=operation.operation_id,
                            entity_ref=operation.entity_ref,
                            operation_type=(
                                "Creation"
                                if operation._type == "create"
                                else "Replacement"
                            ),
                        )
                        if success:
                            successfully_finished_resources.add(operation.resource.name)

                            if operation._type == "replace":
                                replace_successes += 1
                            else:
                                create_successes += 1
                            # Once successful start child operations
                            children = self.resource_to_children.get(
                                operation.resource.name, []
                            )
                            to_start = []
                            for child in children:
                                if child.resource.name in waiting_operations:
                                    if all(
                                        resource.name in successfully_finished_resources
                                        for resource in child.resource._depends_on
                                    ):
                                        op, task = waiting_operations[
                                            child.resource.name
                                        ]
                                        progress.update(
                                            task, description=_operation_start_title(op)
                                        )
                                        to_start.append((op, task))
                            to_stream_operations.extend(
                                await _start_ops(to_start, progress)
                            )
                        else:
                            if operation._type == "replace":
                                replace_failures += 1
                            else:
                                create_failures += 1
                            # If a dependent operation fails, then all dependent operations
                            # should be marked as failed
                            children = self.resource_to_children.get(
                                operation.resource.name, []
                            )
                            for child in children:
                                if child.resource.name in waiting_operations:
                                    _, task = waiting_operations[child.resource.name]
                                    progress.remove_task(task)
                                    progress.console.print(
                                        f"[red]✗[/red] Skipping [blue]{child.entity_ref}[/blue] since dependency failed"
                                    )
                    else:
                        to_stream_operations.append((operation, task))
                running_operations = to_stream_operations
        if create_successes:
            progress.console.print(
                f"[green]✓[/green] Successfully created {create_successes} resources"
            )
        if replace_successes:
            progress.console.print(
                f"[green]✓[/green] Successfully replaced {replace_successes} resources"
            )
        if create_failures:
            progress.console.print(
                f"[red]✗[/red] Failed to create {create_failures} resources"
            )
        if replace_failures:
            progress.console.print(
                f"[red]✗[/red] Failed to replace {replace_failures} resources"
            )
