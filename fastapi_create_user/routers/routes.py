# Copyright 2025 Quartile (https://www/quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from pydantic import BaseModel

from odoo.addons.fastapi.dependencies import odoo_env

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    login: str
    password: str


@router.post("/users")
def create_user(data: UserCreate, env=Depends(odoo_env)):
    User = env["res.users"]
    if User.search_count([("login", "=", data.login)]):
        raise HTTPException(400, "Login already exists")

    new_user = User.create(
        {
            "name": data.name,
            "login": data.login,
            "password": data.password,
        }
    )
    return {"id": new_user.id, "name": new_user.name}
