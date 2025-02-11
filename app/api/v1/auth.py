import json
import requests
from app.schemas.common import LoginData
import os
from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.providers.config import configs
from app.providers.zitadel import Zitadel
from app.utils.jwt import JWTUtils
from app.schemas.common import CommonResponse
from app.providers.middleware import verify_token
from typing import Optional
from app.providers.config import configs
import app.services.user as svc
import app.schemas.user as schemas
from app.utils.database import get_db
from sqlalchemy.orm import Session
import app.api.v1.commons as commons

login = APIRouter()
zitadel = Zitadel()

@login.post("/login")
def login_user(response: Response, user: LoginData):
    if not user.username or not user.password:
        return {
            "status": False,
            "status_code": 401,
            "message": "Invalid credentials",
            "data": None,
            "error": None,
        }

    try:
        response = requests.post(
            f"{configs.zitadel_domain}/v2/sessions",
            json={"checks": {"user": {"loginName": user.username}}},
            headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
            },
        )
        
        response.raise_for_status()
        session_data = response.json()
        session_id = session_data.get("sessionId")
        #add condition to check sessionId
        sessionToken = session_data.get("sessionToken")
        validate_response = requests.patch(
            f"{configs.zitadel_domain}/v2/sessions/{session_id}",
            json={"checks": {"password": {"password": user.password}}},
            headers={
                "Authorization": f"Bearer {configs.zitadel_cctoken}",
                "Content-Type": "application/json",
            },
        )
        
        validate_response.raise_for_status()
        validated_session_data = validate_response.json()
        
        return {
            "session_data" : validated_session_data,
            "session_id" : session_id
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to create session", "details": str(e)}, 500
    
# will redirect to idp when called with ipdId
# need to set successurl and failureUrl dynamically *****
@login.get("/login/idp/{idp_id}")
def idp_login(response: Response, idp_id : int):
    return zitadel.redirect_to_idp(idp_id)

# if idp login is success then is redirected to this endpoint with which we get the user
# details from the idp (currently only tested with google) need to send the userdata to front-end
@login.get("/idp/success")
def idp_success(request: Request,db: Session = Depends(get_db)):
    query_params = request.query_params
    # print(query_params)
    idp_intent_id = query_params.get("id")
    idp_token = query_params.get("token")
    user_id = query_params.get("user")
    # print(user_id)
    try:
        response = zitadel.get_idp_intent_data(idp_intent_id, idp_token)
        user_data = response.json()
        # print(user_data)
        if(user_id):
            session_response = zitadel.create_user_session(user_id, idp_intent_id, idp_token)
        else:
            session_response = zitadel.create_user(user_data, idp_intent_id, idp_token)
            response_data = json.loads(session_response.body.decode("utf-8"))
            session_id = response_data.get("session_id")
            user_info = zitadel.get_user_info(session_id)
            username = user_info.get("session").get("factors").get("user").get("displayName")
            zitadel_user_id = user_info.get("session").get("factors").get("user").get("id")
            new_user = schemas.UserCreate(
                                    user_id=int(zitadel_user_id),
                                    username=username,
                                )
            result, error = svc.create_user(new_user, db)
            if error:
                return commons.is_error_response("DB Error", result, {"user": {}})

            if not result:
                return commons.is_none_reponse("User Not Found", {"user": {}})
            
        if session_response.status_code == 201:
            redirect_response = RedirectResponse(url="/ui", status_code=303)

            # Copy cookies from session_response to redirect_response
            for cookie in session_response.headers.getlist("set-cookie"):
                redirect_response.headers.append("set-cookie", cookie)

            return redirect_response

        return session_response
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to create session", "details": str(e)}, 500


# endpoint to retreive all the available idp providers that is setup in Zitadel
@login.get("/idp/list")
def list_idp(response: Response):
    return zitadel.list_idp_providers()


@login.get("/user_info", dependencies=[Depends(verify_token)])
def get_user_info(request: Request, session_id: Optional[str] = Depends(verify_token)):
    user_info = zitadel.get_user_info(session_id)
    username = user_info.get("session").get("factors").get("user").get("displayName")
    return CommonResponse(
        status=True,
        status_code=200,
        message="User info retrieved successfully",
        data={ "username": username, "auth_enabled": configs.auth_enabled },
        error=None
    )
        
# get userinfo from database
    
    
@login.post("/logout",dependencies=[Depends(verify_token)])
def logout_user(response: Response, session_id: Optional[str] = Depends(verify_token)):
    return zitadel.logout_user(session_id)

