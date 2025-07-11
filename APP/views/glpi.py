from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os
from APP.utils.require_login import require_login
from APP.db import get_db
from APP.models import user as User
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[Depends(require_login)]) 
templates = Jinja2Templates(directory="APP/template")

GLPI_URL = os.getenv("GLPI_API_URL")  
APP_TOKEN = os.getenv("GLPI_APP_TOKEN")
USER_TOKEN = os.getenv("GLPI_USER_TOKEN")

def listar_campos():
    token = iniciar_sesion()
    headers = {
        "Session-Token": token,
        "App-Token": APP_TOKEN
    }
    response = requests.get(f"{GLPI_URL}/listSearchOptions/Phone", headers=headers, verify=False)
    campos = response.json()
    for key, val in campos.items():
        if isinstance(val, dict):
            print(f"{key}: {val.get('name')}")
        else:
            print(f"{key}: {val}")

def iniciar_sesion():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"user_token {USER_TOKEN}",
        "App-Token": APP_TOKEN
    }
    response = requests.get(f"{GLPI_URL}/initSession", headers=headers,verify=False)
    response.raise_for_status()
    return response.json()["session_token"]

@router.get("/glpi", response_class=HTMLResponse)
def glpi_get(request: Request,db: Session = Depends(get_db)):
    '''try:
        print("🛠 Listando campos disponibles para búsqueda en GLPI:")
        listar_campos_search_computer()
    except Exception as e:
        print(f"Error: {e}")'''
    user = db.query(User).filter(User.id == request.session["user_id"]).first()    
    return templates.TemplateResponse("glpi.html", {"request": request, "user": user})


@router.post("/glpi", response_class=HTMLResponse)
def glpi_post(request: Request, tipo: str = Form(...), nombre: str = Form(...),db: Session = Depends(get_db)):
    token = iniciar_sesion()
    headers = {
        "Content-Type": "application/json",
        "Session-Token": token,
        "App-Token": APP_TOKEN
    }

    if tipo == "Computer":
        endpoint = "/search/Computer"
        params = {
            "criteria[0][field]": 1,
            "criteria[0][searchtype]": "contains",
            "criteria[0][value]": nombre,
            "range": "0-20",
            "forcedisplay[0]": 1,        # Name
            "forcedisplay[1]": 23,       # Manufacturer
            "forcedisplay[2]": 5,        # Serial Number
            "forcedisplay[3]": 4,        # Type
            "forcedisplay[4]": 40,       # Model
            "forcedisplay[5]": 3,        # Locations
            "forcedisplay[6]": 76671,    
            "forcedisplay[7]": 76675,    
            "forcedisplay[8]": 76674,   
            "forcedisplay[9]": 76673,   
            "forcedisplay[10]": 31,      # Status
            "forcedisplay[11]": 9,       # Last Inventory Date
            "forcedisplay[12]": 70,      # User
            "forcedisplay[13]": 17       # Processor
        }
    elif tipo == "Phone":
        endpoint = "/search/Phone"
        params = {
            "criteria[0][field]": 1,
            "criteria[0][searchtype]": "contains",
            "criteria[0][value]": nombre,
            "range": "0-20",
            "forcedisplay[0]": 1,
            "forcedisplay[1]": 2,
            "forcedisplay[2]": 5,
            "forcedisplay[3]": 40,
            "forcedisplay[4]": 4,
            "forcedisplay[5]": 31,
            "forcedisplay[6]": 10,
            "forcedisplay[7]": 70,
            "forcedisplay[8]": 23,
            "forcedisplay[9]": 76680,
            "forcedisplay[10]": 76681,
            "forcedisplay[11]": 76682
        }
    elif tipo == "Colaborador_computer":
        endpoint = "/search/Computer"
        params = {
            "criteria[0][field]": 76671,
            "criteria[0][searchtype]": "contains",
            "criteria[0][value]": nombre,
            "range": "0-20",
            "forcedisplay[0]": 1,        # Name
            "forcedisplay[1]": 23,       # Manufacturer
            "forcedisplay[2]": 5,        # Serial Number
            "forcedisplay[3]": 4,        # Type
            "forcedisplay[4]": 40,       # Model
            "forcedisplay[5]": 3,        # Locations
            "forcedisplay[6]": 76671,    
            "forcedisplay[7]": 76675,   
            "forcedisplay[8]": 76674,  
            "forcedisplay[9]": 76673,   
            "forcedisplay[10]": 31,      # Status
            "forcedisplay[11]": 9,       # Last Inventory Date
            "forcedisplay[12]": 70,      # User
            "forcedisplay[13]": 17       # Processor
        }
    elif tipo == "Colaborador_phone":
        endpoint = "/search/Phone"
        params = {
            "criteria[0][field]": 70,
            "criteria[0][searchtype]": "contains",
            "criteria[0][value]": nombre,
            "range": "0-20",
            "forcedisplay[0]": 1,
            "forcedisplay[1]": 2,
            "forcedisplay[2]": 5,
            "forcedisplay[3]": 40,
            "forcedisplay[4]": 4,
            "forcedisplay[5]": 31,
            "forcedisplay[6]": 10,
            "forcedisplay[7]": 70,
            "forcedisplay[8]": 23,
            "forcedisplay[9]": 76680,
            "forcedisplay[10]": 76681,
            "forcedisplay[11]": 76682
        }
    else:
        user = db.query(User).filter(User.id == request.session["user_id"]).first()
        return templates.TemplateResponse("glpi.html", {"request": request, "error": "Tipo de búsqueda inválido", "user": user})

    response = requests.get(f"{GLPI_URL}{endpoint}", headers=headers, params=params, verify=False)
    resultados = response.json().get("data", [])
    
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("glpi.html", {
        "request": request,
        "resultados": resultados,
        "busqueda": nombre,
        "tipo": tipo,
        "user": user
    })
