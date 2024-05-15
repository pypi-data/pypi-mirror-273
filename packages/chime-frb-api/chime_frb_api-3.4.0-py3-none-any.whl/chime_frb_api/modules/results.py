"""CHIME/FRB workflow Results API."""

from typing import Any, Dict, List, Optional

from chime_frb_api.core import API


class Results(API):
    """CHIME/FRB Backend workflow Results API."""

    def __init__(
        self,
        debug: bool = False,
        base_url: str = "http://localhost:8005",
        authentication: bool = False,
        **kwargs: Dict[str, Any],
    ):
        """Initialize the workflow Results API.

        Args:
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            base_url (str, optional): The base URL of the API.
                Defaults to "http://localhost:8005".
            authentication (bool, optional): Whether to enable authentication.
                Defaults to False.
        """
        API.__init__(
            self,
            debug=debug,
            default_base_urls=[
                "http://frb-vsop.chime:8005",
                "http://localhost:8005",
                "https://frb.chimenet.ca/results/",
            ],
            base_url=base_url,
            authentication=authentication,
            **kwargs,
        )

    def deposit(self, works: List[Dict[str, Any]]) -> Dict[str, bool]:
        """Deposit works into the results backend.

        Args:
            works (List[Dict[str, Any]]): A list of payloads from Work Objects.
        Note:
            This method is not intended to be called directly by end users.

        Returns:
            Dict[str, bool]: Dictionary of deposit results for each pipeline.

        Examples:
        >>> from chime_frb_api.results import Results
        >>> from chime_frb_api.tasks import Work
        >>> work = Work.fetch(pipeline="sample")
        >>> results = Results()
        >>> status = results.deposit([work.payload])
        """
        for work in works:
            assert work["status"] in [
                "success",
                "failure",
            ], "Work status must be 'success' or 'failure'"
        return self.post(url="/results", json=works)

    def update(self, works: List[Dict[str, Any]]) -> bool:
        """Update works in the results backend.

        Args:
            works (List[Dict[str, Any]]): A list of payloads from Work Objects.
        Note:
            The results need to exist before they can be updated.

        Returns:
            bool: Whether the works were updated successfully.
        """
        response: bool = self.put(url="/results", json=works)
        return response

    def delete_ids(self, pipeline: str, ids: List[str]) -> bool:
        """Delete results from the results backend with the given ids.

        Args:
            pipeline (str): Name of pipeline that the IDs are from.
            ids (List[str]): The IDs of the works to delete.

        Returns:
            bool: Whether the results were deleted successfully.
        """
        return self.delete(url="/results", params={pipeline: ids})

    def view(
        self,
        pipeline: str,
        query: Dict[str, Any],
        projection: Dict[str, bool],
        skip: int = 0,
        limit: Optional[int] = 100,
    ) -> List[Dict[str, Any]]:
        """View works in the workflow results backend.

        Args:
            pipeline (str): Name of pipeline to query results.
            query (Dict[str, Any]): The query to filter the results with.
            projection (Dict[str, bool]): The projection to use to map the output.
            skip (int, optional): The number of works to skip. Defaults to 0.
            limit (Optional[int], optional): The number of works to limit to.
                Defaults to 100. -1 means no limit.

        Returns:
            List[Dict[str, Any]]: The works matching the query.
        """
        query["pipeline"] = pipeline
        if limit == -1:
            limit = 0
        payload = {
            "query": query,
            "projection": projection,
            "skip": skip,
            "limit": limit,
        }
        response: List[Dict[str, Any]] = self.post("/view", json=payload)
        return response

    def count(
        self,
        pipeline: str,
        query: Dict[str, Any],
    ) -> int:
        """Retrieve the number of results filtered by the query parameters.

        Args:
            pipeline (str): Name of pipeline to query results.
            query (Dict[str, Any]): The query to filter the results with.

        Returns:
            int: The number of results that match the query.
        """
        query["pipeline"] = pipeline
        payload = {
            "query": query,
        }
        response: int = self.post("/view/count", json=payload)
        return response

    def status(self) -> Dict[str, int]:
        """Retrieve the overall status of the results backend.

        Returns:
            Dict[str, int]: The status of the results backend.
        """
        response: Dict[str, int] = self.get("/status")
        return response

    def get_by_count(self, pipeline: str, count: int = 10) -> List[Dict[str, Any]]:
        """Retrieves a specified number of results.

        Args:
            pipeline (str): The pipeline to use for querying the database.
            count (int): The number of results to retrieve. Defaults to 10.

        Returns:
            List[Dict[str, Any]]: Retrieved results.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        response = self.view(
            pipeline=pipeline, query={}, projection={}, skip=0, limit=count
        )
        return response

    def get_by_id(self, pipeline: str, ids: List[str]) -> List[Dict[str, Any]]:
        """Retrieves results by IDs from the specified pipeline.

        Args:
            pipeline (str): The name of the pipeline to retrieve results from.
            ids (List[str]): A list of workflow IDs to retrieve results for.

        Returns:
            List[Dict[str, Any]]: Retrieved results.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        response = self.view(
            pipeline=pipeline, query={"id": {"$in": ids}}, projection={}, limit=-1
        )
        return response

    def get_by_event(self, pipeline: str, event_number: int) -> List[Dict[str, Any]]:
        """Retrieves results by event number from the specified pipeline.

        Args:
            pipeline (str): The name of the pipeline to retrieve results from.
            event_number (int): The event number of the event.

        Returns:
            List[Dict[str, Any]]: The work object with the given event ID.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        response = self.view(
            pipeline=pipeline,
            query={"event": [event_number]},
            projection={},
            limit=-1,
        )
        return response

    def get_locked(
        self, pipeline: str, skip: int = 0, count: int = 10
    ) -> List[Dict[str, Any]]:
        """Retrieve locked events from the specified pipeline.

        Args:
            pipeline (str): The name of the pipeline to retrieve locked events from.
            skip (int, optional): The number of works to skip. Defaults to 0.
            count (int, optional): The maximum number of events. Defaults to 10.

        Returns:
            List[Dict[str, Any]]: A list of the locked events.

        Only locked events with valid results, plots and products are returned.
        """
        response = self.view(
            pipeline=pipeline,
            query={"results.locked": True},
            projection={
                "event": True,
                "plots": True,
                "products": True,
                "results": True,
            },
            skip=skip,
            limit=count,
        )
        if not response:
            return response
        else:
            return response

    def get_locked_count(self, pipeline: str) -> int:
        """Retrieves the count of locked events in the given pipeline.

        Args:
            pipeline (str): The name of the pipeline.

        Returns:
            int: The count of locked events.

        Raises:
            Exception: If an error occurs during the count retrieval.
        """
        response = self.count(
            pipeline=pipeline,
            query={"results.locked": True},
        )
        if not response:
            return response
        else:
            return response

    def lock(self, pipeline: str, ids: List[str]) -> bool:
        """Locks the specified events identified by the given IDs.

        Args:
            pipeline (str): The pipeline in which the events are located.
            ids (List[str]): A list of event IDs to be locked.

        Returns:
            Boolean: True if successful, False if not.

        Raises:
            Exception: If an error occurs during the locking process.

        """
        payload: List[Dict[str, Any]] = self.get_by_id(pipeline, ids)
        for work in payload:
            work["results"]["locked"] = True
        response = self.update(payload)
        return True if response else False

    def unlock(self, pipeline: str, ids: List[str]) -> bool:
        """Unlocks a single work/event in the database.

        Args:
            pipeline (str): The pipeline name.
            ids (List[str]): The workflow IDs of the events to be locked,
            e.g. [..., 65e4c9b9c5e8320d351c0d7c, ...,]

        Returns:
            Bool: True if successful, False if not.
            A message is displayed to indicate whether the unlocking process
            was successful or not.
        """
        while True:
            confirm = input(
                f"""
                Are you sure you want to unlock the event in '{pipeline}'?
                Type the pipeline name to confirm:
                """
            )
            if confirm == pipeline:
                break
            print("Pipeline name doesn't match. Please try again.")

        work_object = self.get_by_id(pipeline, ids)
        for work in work_object:
            work["results"]["locked"] = False
        response = self.update(work_object)
        return True if response else False
