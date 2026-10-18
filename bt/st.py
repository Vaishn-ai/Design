async def get_batch(current_user, db: AsyncSession):
    try:
        result = await db.execute(select(Batch))
        batches = result.scalars().all()


        l1 = []

        for b in batches: 
            l1.extend([b.id, b.batch_name, b.start_date, b.end_date, b.starting_time, b.ending_time, b.seats, b.course_id]) 
        

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg": "Data retrieved successfully",
                "data": l1,
            }
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Failed to retrieve batches",
            },
        )