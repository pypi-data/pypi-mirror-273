from __future__ import annotations
import asyncio
import time
import logging
import os
import sys
from asyncio import Lock
from typing import Dict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from azure.identity import DefaultAzureCredential


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    std_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("[%(asctime)s][%(process)d][%(name)s][%(levelname)s] - %(message)s")
    std_handler.setFormatter(formatter)
    logger.addHandler(std_handler)
    return logger


logger = init_logger()
REFRESH_OFFSET = 300
EXPECTED_IDENTITY_HEADER = os.environ.get("IDENTITY_HEADER") or os.environ.get("MSI_SECRET", "Default")

app = FastAPI()
credential: DefaultAzureCredential = None

lock = asyncio.Lock()
scope_lock_map: Dict[str, Lock] = {}
scope_credentials_map: Dict[str, CredentialWrapper] = {}
logger.info("Server started...")


class CredentialWrapper:
    def __init__(self, credential: DefaultAzureCredential = None):
        self.credential = credential if credential else DefaultAzureCredential()
        self.expires_on = 0

    def get_token(self, resource: str):
        token = self.credential.get_token(resource)
        self.expires_on = token.expires_on
        return token

    def should_refresh(self):
        now = int(time.time())
        if self.expires_on - now > REFRESH_OFFSET:
            return False
        return True


async def try_get_token(resource: str):
    """
    1. Check whether there's already a credential created for the resource
    2. if yes, get the credential and check whether it needs to be refreshed
         if no refresh needed, just call the credential to get the token.
         if needs refresh, try to get the scope lock for this resource and refresh the token,
         this is to make sure only 1 call can refresh the token at the same time.
    3. if not, try to create/get the scope lock for this resource, scope lock makes sure there
         is only one credential created for the resource.

    Note that the ManagedIdentityCredential in DefaultAzureCredential already cached the token,
    so we don't need to cache the token again.
    """
    if resource in scope_credentials_map:
        credential = scope_credentials_map[resource]
        if credential.should_refresh():
            scope_lock = await get_scope_lock(resource)
            async with scope_lock:
                if credential.should_refresh():
                    logger.info(f"Refreshing token for resource {resource}......")
                    token = credential.get_token(resource)
                    return token
    else:
        scope_lock = await get_scope_lock(resource)
        async with scope_lock:
            if resource not in scope_credentials_map:
                logger.info(f"Getting token for resource {resource}......")
                cre = CredentialWrapper()
                token = cre.get_token(resource)
                scope_credentials_map[resource] = cre
                return token

    return scope_credentials_map[resource].get_token(resource)


async def get_scope_lock(resource: str):
    """ensure only one lock for each resource"""
    if resource not in scope_lock_map:
        async with lock:
            if resource not in scope_lock_map:
                scope_lock_map[resource] = asyncio.Lock()
    return scope_lock_map[resource]


@app.get("/token")
async def get_token(request: Request):
    resource = request.query_params.get("resource")
    if not resource:
        resource = "https://management.azure.com/"
    logger.info(f"Receiving get token request for {resource}...")

    identity_header = request.headers.get("X-IDENTITY-HEADER")
    if identity_header != EXPECTED_IDENTITY_HEADER:
        logger.error(f"Wrong identity header: {identity_header}, expected: {EXPECTED_IDENTITY_HEADER}")
        return JSONResponse(status_code=403, content={"error": "Forbidden"})
    token = await try_get_token(resource)
    return {"access_token": token.token, "expires_on": token.expires_on, "resource": resource}
