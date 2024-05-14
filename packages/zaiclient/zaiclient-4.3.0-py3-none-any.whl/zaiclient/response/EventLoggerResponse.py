from pydantic import BaseModel, confloat, conint, constr


class EventLoggerResponse(BaseModel):
    message: constr(min_length=0, max_length=500)
    failure_count: conint(ge=0, le=10000)
    timestamp: confloat(ge=1_648_871_097.0, le=2_147_483_647.0)

    class Config:
        schema_extra = {
            "example": {
                "message": "The given event was handled successfully.",
                "failure_count": 0,
                "timestamp": 1_648_871_097.0,
            }
        }
