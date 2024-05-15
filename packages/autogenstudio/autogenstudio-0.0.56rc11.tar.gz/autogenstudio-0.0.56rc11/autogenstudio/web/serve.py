# loads a fast api api endpoint with a single endpoint that takes text query and return a response

import os
from fastapi import FastAPI
import json
from ..workflowmanager import WorkflowManager
from ..datamodel import Response

app = FastAPI()
workflow_file_path = os.environ.get("AUTOGENSTUDIO_WORKFLOW_FILE",  None)


if workflow_file_path:
    workflow_manager = WorkflowManager(workflow=workflow_file_path)
else:
    raise ValueError("Workflow file must be specified")


@app.get("/predict/{task}")
async def predict(task: str):
    response = Response(
        message="Task successfully completed", status=True, data=None)
    try:
        workflow_manager.run(message=task, clear_history=False)
        response.data = {
            "messages": workflow_manager.agent_history,
        }
    except Exception as e:
        response.message = str(e)
        response.status = False
    return response
