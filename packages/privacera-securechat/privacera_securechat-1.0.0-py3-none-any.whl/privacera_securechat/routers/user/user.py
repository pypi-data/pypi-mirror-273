import logging

from fastapi import APIRouter, Request, Depends, Response
from app.api_schemas.user import PostUserLoginRequest, UserLoginResponse
from core.factory.controller_initiator import ControllerInitiator
from app.controllers import UserController
from app.api_schemas import CommonErrorResponse
from core.exceptions import UnauthorizedException
from core.config import load_config_file
from core.security.jwt import JWTHandler
from core.security.okta_verifier import PrivaceraOktaVerifier
logger = logging.getLogger(__name__)
user_router = APIRouter()

Config = load_config_file()
security_conf = Config['security']
okta_conf = security_conf.get('okta', dict())
okta_enabled = okta_conf.get('enabled', "false") == "true"

if okta_enabled:
    privacera_okta_verifier = PrivaceraOktaVerifier(okta_conf)

jwt_handler = JWTHandler()


@user_router.post("/login", responses=CommonErrorResponse)
async def user_login(
        request: Request,
        resonse: Response,
        body_params: PostUserLoginRequest,
        user_controller: UserController = Depends(ControllerInitiator().get_user_controller),
    ) -> UserLoginResponse:
    access_token = request.headers.get("authorization", None)

    if okta_enabled:
        if access_token is not None:
            try:
                access_token = access_token.split(" ")[1]
                await privacera_okta_verifier.verify(access_token)
            except Exception as e:
                logger.error(f"Okta access token validation failed: {e}")
                raise UnauthorizedException("Invalid access token")
        else:
            raise UnauthorizedException("Access token is not provided")
    user_name = body_params.user_name.strip()
    user_object = await user_controller.login_user(user_name)
    resonse.set_cookie(
        key="session",
        value=jwt_handler.encode({"user_id": user_object['user_id'], "user_name": user_object['user_name']}),
        httponly=True
    )
    return user_object


@user_router.post("/logout")
async def user_logout(
            request: Request,
            response: Response,
        ):
    response.delete_cookie("session")
    return {"message": "Logout successful"}