from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from datetime import datetime
from database import database, models
from app import schemas, auth

router = APIRouter(
    prefix='/report',
    tags=['Reports']
)

@router.get('/', response_model=List[schemas.ReportOut])
def get_all_reports(
    db: Session = Depends(database.get_db)
):
    reports = db.query(models.Report)
    return reports.all()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ReportOut)
def create_report(
    report: schemas.CreateReport,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(auth.get_current_user)
):
    report_model = models.Report(**report.model_dump(), user_id = current_user.id)
    db.add(report_model)
    db.commit()
    db.refresh(report_model)
    return report_model

@router.patch('/{id}', response_model = schemas.ReportOut)
def updae_report(
    id: int,
    report: schemas.UpdateReport,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(auth.get_current_user)
):
    updated_report = db.query(models.Report).filter(models.Report.id == id)
    if not updated_report.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Report with ID: {id} doesn't exist")
    if updated_report.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this action")
    updated_data = report.model_dump(exclude_unset=True)
    updated_data["updated_at"] = datetime.now()
    updated_report.update(updated_data, synchronize_session=False)
    db.commit()
    return updated_report.first()

@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_report(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(auth.get_current_user)
):
    report = db.query(models.Report).filter(models.Report.id == id)
    if not report.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Report with ID: {id} doesn't exist")
    if report.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this action")
    report.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)