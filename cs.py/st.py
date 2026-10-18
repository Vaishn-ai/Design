
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.course.base.admin.models import Course


async def get_course(current_user, db: AsyncSession):
    try:
        result = await db.execute(select(Course))
        courses = result.scalars().all()

        if not courses:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "msg": "Course not found",
                },
            )

        course_list = []

        for course in courses:
            
            course_list.append({
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "overview": course.overview,
            })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Courses retrieved successfully",
                "courses": course_list,
            },
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "msg": "Failed to retrieve courses",
            },
        )
