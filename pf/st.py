
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.student.models import Student
from src.modules.profile.student.interface import Update_Student
from src.utils.validations import check_phone



async def get_student_detail(current_user, db: AsyncSession):
    try:
        result = await db.execute(
            select(Student).where(
                Student.id == current_user["user_id"]
            )
        )
        student = result.scalar_one_or_none()

        if not student:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "msg": "Student not found",
                },
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Student details fetched successfully",
                "student": {
                    "id": student.id,
                    "email": student.email,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "age": student.age,
                    "ph_no": student.ph_no,
                },
            },
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "msg": "Failed to fetch student details",
            },
        )




async def update_student_details(data: Update_Student, current_user, db: AsyncSession):
    try:
        result = await db.execute(
            select(Student).where(Student.id == data.id)
        )
        student = result.scalar_one_or_none()

        if not student:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "msg": "Student not found",
                },
            )

        student.first_name = data.first_name
        student.last_name = data.last_name
        student.age = data.age
        student.ph_no = check_phone(data.ph_no)

        await db.commit()
        await db.refresh(student)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Student details updated successfully",
            },
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "success" : False,
                "msg" : "Failed to update student details"
            }
        )
