from flask import Blueprint, current_app, request


bp = Blueprint("options", __name__)


@bp.get("/api/crops")
def crops():
    return {"crops": current_app.extensions["data_service"].values("Crop")}


@bp.get("/api/states")
def states():
    return {"states": current_app.extensions["data_service"].values("State")}


@bp.get("/api/districts")
def districts():
    state = request.args.get("state")
    return {"districts": current_app.extensions["data_service"].districts(state)}


@bp.get("/api/seasons")
def seasons():
    return {"seasons": current_app.extensions["data_service"].values("Season")}


@bp.get("/api/soil-types")
def soil_types():
    return {"soil_types": current_app.extensions["data_service"].values("Soil Type")}


@bp.get("/api/years")
def years():
    return {"years": current_app.extensions["data_service"].years()}
