from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src import crud, schemas
from src.dependencies import get_db

router = APIRouter(
    prefix="/campaigns",
    tags=["campaigns"],
)


@router.post("/", response_model=schemas.Campaign, status_code=201)
def create_campaign(campaign: schemas.CampaignCreate, db: Session = Depends(get_db)):
    return crud.create_campaign(db, campaign)


@router.patch("/", response_model=schemas.Campaign)
def update_campaign(campaign: schemas.CampaignEdit, db: Session = Depends(get_db)):
    return crud.update_campaign(db, campaign)


@router.get("/{campaign_id}", response_model=schemas.Campaign)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = crud.read_campaign(db, campaign_id)
    if campaign is None:
        raise HTTPException(404, "Campaign not found")
    return campaign


@router.get("/", response_model=LimitOffsetPage[schemas.Campaign])
def get_campaigns(
    db: Session = Depends(get_db),
):
    # TODO order by
    query = crud.read_campaigns(db)
    return paginate(query)
