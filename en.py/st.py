
from src.modules.enrollments.base.student.interface import Create_Enrollment
from src.modules.enrollments.base.student.models import Enrollment
from src.modules.course.base.admin.models import Course
from src.modules.auth.student.models import Student
from src.modules.batch.base.admin.models import Batch

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status
from fastapi.responses import JSONResponse


async def create_enrollments(
    data: Create_Enrollment,
    current_user,
    db: AsyncSession,
):
    try:
        result = await db.execute(select(Course).where(Course.id == data.course_id))
        course = result.scalar_one_or_none()

        if not course:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Course not found"},
            )

        result = await db.execute(select(Student).where(Student.id == data.student_id))
        student = result.scalar_one_or_none()

        if not student:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Student not found"},
            )

        result = await db.execute(select(Batch).where(Batch.id == data.batch_id))
        batch = result.scalar_one_or_none()

        if not batch:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Batch not found"},
            )


        enrollment = Enrollment(
            course_id=data.course_id,
            student_id=data.student_id,
            batch_id=data.batch_id,
        )

        db.add(enrollment)
        await db.commit()
        await db.refresh(enrollment)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "msg": "Successfully enrolled",
                "enrollment_id": enrollment.id,
            },
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "msg": "Failed to create enrollment",
            },
        )
