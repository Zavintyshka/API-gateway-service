from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.orm import Session

from database.database import get_db
from ..schemas import ComponentStatus
from ..api_gateway_types import StatusType
from ..api_gateway_tools import check_db, check_redis
from grpc_services.api_gateway_grpc import VideoMicroserviceGrpc

status_router = APIRouter(prefix="/status", tags=["Status"])


@status_router.get("/", response_model=List[ComponentStatus])
def get_status(db: Session = Depends(get_db)):
    status = [ComponentStatus(component_name="API-Gateway", status=StatusType.serving),
              VideoMicroserviceGrpc().check_status(), check_db(db), check_redis()]
    return status
