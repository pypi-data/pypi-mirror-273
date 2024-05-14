from pydantic import BaseModel, Field


class RunExperimentBody(BaseModel):
    experiment_id: str = Field(..., description="Id")
    requirements_file: str = Field(..., description="STAGING|PRODUCTION")
    model_pkl_file: str = Field(..., description="STAGING|PRODUCTION")


class ExperimentBody(BaseModel):
    experiment_name: str = Field(..., description="Id")
    experiment_tags: dict = Field(None, description="Tags")
    requirements_file: str = Field(None, description="STAGING|PRODUCTION")
    model_pkl_file: str = Field(None, description="STAGING|PRODUCTION")


class PredictModelBody(BaseModel):
    run_id: str = Field(None, description="Run ID")
    modelname: str = Field(..., description="DEPENDENCY|PREDICT")
    stage: str = Field(..., description="STAGING|PRODUCTION")
