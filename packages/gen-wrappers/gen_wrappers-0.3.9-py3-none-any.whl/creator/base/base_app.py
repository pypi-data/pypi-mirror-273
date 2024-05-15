from abc import abstractmethod, ABC
from typing import Any, List

from creator.base.base_request import BaseRequest
from creator.base.base_response import BaseResponse, ResponseData, ResponseDataType
from creator.base.job_status import JobStatus


class BaseApp(ABC):
    def __init__(self):
        self.output = None
        self.processing = False
        self.can_queue = False
        self.loaded_models = []

    @abstractmethod
    async def create(self, params: BaseRequest) -> BaseResponse:
        """Create a job and await its completion."""
        pass

    @abstractmethod
    async def create_async(self, params: BaseRequest) -> BaseResponse:
        """Create an asynchronous job and return the job_id."""
        pass

    @abstractmethod
    async def get_status(self, job_id: str) -> BaseResponse:
        """Get the status of an asynchronous job."""
        pass

    @abstractmethod
    async def get_models(self) -> List[Any]:
        pass

    async def get_loaded_models(self) -> BaseResponse:
        base_response = BaseResponse(status=JobStatus.FINISHED)
        base_response_data = ResponseData(data=self.loaded_models, data_type=ResponseDataType.TEXT, total_count=len(self.loaded_models))
        base_response.output = base_response_data
        return base_response

    @abstractmethod
    def upload_image(self, image_data: Any) -> str:
        pass

    @abstractmethod
    async def test(self):
        pass
