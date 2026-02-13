from fastapi import APIRouter, UploadFile, File, Depends
from app.services import storage, kafka_producer
from app.models import ImageTask
from app.database import SessionLocal
from app.auth import get_current_user
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime,timezone
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/images")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    content = await file.read()
    s3_url = storage.upload_image(content, file.filename)
    
    image = ImageTask(
        user_id=user.id,
        image_path=s3_url,
        status="success",
        transformation={
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content)
        },
        completed_at = datetime.now(timezone.utc)
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {"id": str(image.id), "url": image.image_path}

@router.post("/images/{image_id}/transform")
def request_transformation(image_id: str, transformations: dict, db: Session = Depends(get_db), user = Depends(get_current_user)):
    image = db.query(ImageTask).filter(ImageTask.id == image_id, ImageTask.user_id == user.id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    # Extraer la key de la imagen desde la URL
    s3_key = image.image_path.split('/')[-2] + '/' + image.image_path.split('/')[-1]

    # Armamos el mensaje separado
    message = {
        "image_path": s3_key,
        "user_id": user.id,
        "task_id": image.id,
        "transformation": transformations
    }

    kafka_producer.send_transformation_task(message)

    return {"message": "Transformación solicitada, se procesará en background."}


@router.get("/images/{image_id}")
def get_image(image_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    image = db.query(ImageTask).filter(ImageTask.id == image_id, ImageTask.user_id == user.id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return{
        "id": str(image.id),
        "url": image.image_path
    }


@router.delete("/images/{image_id}")
def delete_image(image_id: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    image = db.query(ImageTask).filter(ImageTask.id == image_id, ImageTask.user_id == user.id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    storage.delete_image(image.image_path)
    db.delete(image)
    db.commit()

    return {"message": "Imagen eliminada exitosamente"}