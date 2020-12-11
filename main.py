from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

api = FastAPI()

class DiasTemporada(BaseModel):
    dias_demanda_alta: int
    dias_demanda_media: int
    dias_demanda_baja: int
    
class PorcentajeTemporadaIn(BaseModel):
    porcentaje_temporada_baja: float
    porcentaje_temporada_media: float
    
class PorcentajeTemporadaOut(BaseModel):
    anio : int
    porcentaje_temporada_baja: float
    porcentaje_temporada_media: float    
    porcentaje_temporada_alta: float


porcentajeTemporada = []
cuentaAnios = {"anio": 2020}

@api.get("/")
async def hola():
    return {"Esto es":"GraphCost"}

@api.post("/porcentaje/")
async def computar_porcentajes(diasportemporada: DiasTemporada, porcentajebajamedia: PorcentajeTemporadaIn):
    
    sumaDiasTrabajables = diasportemporada.dias_demanda_alta + diasportemporada.dias_demanda_media + diasportemporada.dias_demanda_baja
    proporcionTemporadaMediaBaja = porcentajebajamedia.porcentaje_temporada_baja*diasportemporada.dias_demanda_baja + porcentajebajamedia.porcentaje_temporada_media*diasportemporada.dias_demanda_media 
    porcentajeTempAlta = (sumaDiasTrabajables - proporcionTemporadaMediaBaja)/diasportemporada.dias_demanda_alta
    cuentaAnios["anio"] = cuentaAnios["anio"] + 1
    p = PorcentajeTemporadaOut(**porcentajebajamedia.dict(), porcentaje_temporada_alta = round(porcentajeTempAlta,2), anio = cuentaAnios["anio"])
    porcentajeTemporada.append(p)
    return porcentajeTemporada

@api.get("/porcentaje/anual/{anio}")
async def obtener_porcentaje_anual(anio: int):
    try:
        for dic in porcentajeTemporada:
            if dic.anio ==anio:
                return dic
    except:
        raise HTTPException(status_code=404, detail="Año No Encontrado")