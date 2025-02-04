"""Contains the DelegatingVerbCallback definition."""
from datashaper import VerbDetails
from datashaper.execution.execution_node import ExecutionNode
from datashaper.progress.types import Progress
from datashaper.workflow.verb_callbacks.verb_callbacks import VerbCallbacks
from datashaper.workflow.workflow_callbacks.workflow_callbacks import WorkflowCallbacks


class RunnerCallbacks(VerbCallbacks):
    """A wrapper that implements VerbCallbacks that delegates to the underlying WorkflowCallbacks."""

    _workflow_callbacks: WorkflowCallbacks

    def __init__(self, workflow_callbacks: WorkflowCallbacks):
        """Create a new instance of DelegatingVerbCallbacks."""
        self._workflow_callbacks = workflow_callbacks

    def progress(self, progress: Progress) -> None:
        """Handle when progress occurs."""

        self._workflow_callbacks.on_step_progress(ExecutionNode(
            node_id="node_id",
            has_explicit_id=False,
            verb=VerbDetails(
                name="name",
                func=lambda: print("func")
            ),
            node_input="node_input",
        ), progress)

    def error(
        self,
        message: str,
        cause: BaseException | None = None,
        stack: str | None = None,
        details: dict | None = None,
    ) -> None:
        """Handle when an error occurs."""
        self._workflow_callbacks.on_error(message, cause, stack, details)

    def warning(self, message: str, details: dict | None = None) -> None:
        """Handle when a warning occurs."""
        self._workflow_callbacks.on_warning(message, details)

    def log(self, message: str, details: dict | None = None) -> None:
        """Handle when a log occurs."""
        self._workflow_callbacks.on_log(message, details)

    def measure(self, name: str, value: float, details: dict | None = None) -> None:
        """Handle when a measurement occurs."""
        self._workflow_callbacks.on_measure(name, value, details)
