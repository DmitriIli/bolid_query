from src.queries.core import get_data_for_a_period

if __name__ == '__main__':
    get_data_for_a_period(start='2025-12-01', end='2025-12-31')



# if __name__ == "__main__":
#     asyncio.run(main())
#     if "--webserver" in sys.argv:
#         uvicorn.run(
#             app="src.main:app",
#             reload=True,
#         )