
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.enrollments.base.student.models import Enrollment
from src.modules.enrollments.base.student.interface import Update_Enrollment


async def get_enrollments(current_user, db: AsyncSession):
    try:
        result = await db.execute(select(Enrollment))
        enrollments = result.scalars().all()

        if not enrollments:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "msg": "Enrollments not found",
                },
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Enrollments retrieved successfully",
                "enrollments": [
                    {
                        "id": e.id,
                        "student_id": e.student_id,
                        "course_id": e.course_id,
                        "batch_id": e.batch_id,
                    }
                    for e in enrollments
                ],
            },
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "msg": "Failed to retrieve enrollments",
            },
        )


async def update_enrollments(
    enrollment_id: int,
    data: Update_Enrollment,
    current_user,
    db: AsyncSession,
):
    try:
        result = await db.execute(
            select(Enrollment).where(Enrollment.id == enrollment_id)
        )
        enrollment = result.scalar_one_or_none()

        if enrollment is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "msg": "Enrollment not found",
                },
            )

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(enrollment, field, value)

        await db.commit()
        await db.refresh(enrollment)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Enrollment successfully updated",
                "enrollment": {
                    "id": enrollment.id,
                    "student_id": enrollment.student_id,
                    "course_id": enrollment.course_id,
                    "batch_id": enrollment.batch_id,
                },
            },
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "msg": "Failed to update enrollment",
            },
        )



async def delete_enrollments(
    enrollment_id: int,
    current_user,
    db: AsyncSession,
):
    try:
        result = await db.execute(
            select(Enrollment).where(Enrollment.id == enrollment_id)
        )
        enrollment = result.scalar_one_or_none()

        if enrollment is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "msg": "Enrollment not found",
                },
            )

        await db.delete(enrollment)
        await db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Enrollment successfully deleted",
            },
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "msg": "Failed to delete enrollment",
            },
        )
