"""Strangeworks Runtime Client."""

import json
from datetime import datetime as python_datetime
from typing import Any, Dict, List, Optional

import strangeworks
from qiskit import assemble
from qiskit_ibm_runtime.api.clients.runtime import RuntimeClient
from qiskit_ibm_runtime.utils import RuntimeEncoder
from strangeworks.core.client.resource import Resource
from strangeworks.core.errors.error import StrangeworksError
from strangeworks.sw_client import SWClient as SDKClient


class StrangeworksRuntimeClient(RuntimeClient):
    # TODO: we need this for the following reasons:
    # 1. Use our own Runtime to direct requests to our product/service.
    # 2. Return errors for all functions that are related to programs such  as creation,
    #  deletion. Only list currently available programs.
    # 3. Override backend calls to retrieve backends from platform.
    def __init__(
        self,
        channel,
        rsc: Optional[Resource] = None,
        sdk_client: Optional[SDKClient] = None,
        **kwargs,
    ):
        self._channel = channel
        self.rsc = rsc
        self._sdk_client = sdk_client or strangeworks.client

        if channel == "ibm_quantum":
            self._product_slug = "ibm-quantum"
        elif channel == "ibm_cloud":
            self._product_slug = "ibm-qiskit-runtime"
        else:
            raise StrangeworksError(f"Invalid channel: {channel}")

    def program_run(
        self,
        program_id: str,
        backend_name: Optional[str],
        params: Dict,
        image: Optional[str],
        log_level: Optional[str],
        session_id: Optional[str],
        job_tags: Optional[List[str]] = None,
        max_execution_time: Optional[int] = None,
        start_session: Optional[bool] = False,
        session_time: Optional[int] = None,
    ) -> Dict:
        """Execute the program.

        Args:
            program_id: Program ID.
            backend_name: Name of the backend.
            params: Program parameters.
            image: Runtime image.
            hub: Hub to be used.
            group: Group to be used.
            project: Project to be used.
            log_level: Log level to use.
            session_id: ID of the first job in a runtime session.
            job_tags: Tags to be assigned to the job.
            max_execution_time: Maximum execution time in seconds.
            start_session: Set to True to explicitly start a runtime session.
            Defaults to False.
            session_time: Length of session in seconds.

        Returns:
            JSON response.
        """

        payload: Dict[str, Any] = {
            "program_id": program_id,
            "params": params,
        }
        if image:
            payload["image"] = image
        if log_level:
            payload["log_level"] = log_level
        else:
            payload["log_level"] = "WARNING"
        if backend_name:
            payload["backend"] = backend_name
        else:
            backend_name = "ibmq_qasm_simulator"
            payload["backend"] = backend_name
        if session_id:
            payload["session_id"] = session_id
        if job_tags:
            payload["tags"] = job_tags
        if max_execution_time:
            payload["cost"] = max_execution_time
        if start_session:
            payload["start_session"] = start_session
            payload["session_time"] = session_time
        data = json.dumps(payload, cls=RuntimeEncoder)

        circ_params = params.get("parameter_values")
        if circ_params is None or len(circ_params[0]) == 0:
            qobj_dict = [
                assemble(params["circuits"][circ]).to_dict()
                for circ in range(len(params["circuits"]))
            ]
        else:
            qobj_dict = [
                assemble(
                    params["circuits"][circ]
                    .assign_parameters(circ_params[circ])
                    .decompose()
                    .decompose()
                ).to_dict()
                for circ in range(len(params["circuits"]))
            ]

        payload = {
            "data": data,
            "circuit": qobj_dict,
            "program_id": program_id,
            "backend": backend_name,
            "channel": self._channel,
            "runtime": True,
        }

        response = strangeworks.execute(self.rsc, payload, "create_runtime_job")

        return response

    def job_get(self, job_slug, **kwargs):
        return strangeworks.jobs(slug=job_slug)[0]

    def jobs_get(self, **kwargs):
        return strangeworks.jobs(
            product_slugs=self._product_slug, resource_slugs=self.rsc.slug
        )

    def backend_properties(
        self, backend_name: str, datetime: Optional[python_datetime] = None
    ) -> Dict[str, Any]:
        """Return the properties of the IBM backend.

        Args:
            backend_name: The name of the IBM backend.
            datetime: Date and time for additional filtering of backend properties.

        Returns:
            Backend properties.

        Raises:
            NotImplementedError: If `datetime` is specified.
        """
        payload = {
            "backend_name": backend_name,
            "datetime": datetime,
        }
        return strangeworks.execute(self.rsc, payload, "runtime_backend_properties")

    def create_session(
        self,
        backend: Optional[str] = None,
        instance: Optional[str] = None,
        max_time: Optional[int] = None,
        channel: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Create the runtime session.

        Args:
            session_id: Session ID.
        """
        payload = {
            "backend": backend,
            "instance": instance,
            "max_time": max_time,
            "channel": channel,
            "mode": mode,
        }
        return strangeworks.execute(self.rsc, payload, "create_session")

    def close_session(self, session_id: str) -> None:
        """Close the runtime session.

        Args:
            session_id: Session ID.
        """
        payload = {
            "session_id": session_id,
        }
        strangeworks.execute(self.rsc, payload, "close_session")
