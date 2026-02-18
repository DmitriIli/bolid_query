from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.database import sync_engine, async_engine


def get_data_for_a_period(start: str, end: str) -> dict:
    try:

        with sync_engine.connect() as connection:
            qry = text(
                """
                    SELECT 
                        'Bolid' as 'Bolid','Nanolek' as 'Nanolek','Проходные' as 'AccessPoint'
                        , pList.firstname as 'Имя'
                        , pList.midname as 'Отчество'
                        , pList.name as 'Фамилия'
                        , pCompany.Name as 'Company'
                        , pDivision.Name  as 'Division'
                        , pPost.Name as 'Post'
                        , convert(varchar(10), cast(pLogData.TimeVal as date),105) as 'Date'
                        , cast(min(pLogData.TimeVal) as timestamp) as 'First'
                        , cast(max(pLogData.TimeVal) as timestamp) as 'Last'
                         FROM pLogData
                           JOIN pList ON (pList.ID = pLogData.Hozorgan)
                               LEFT JOIN pPost ON (pList.Post = pPost.ID)
                                   LEFT JOIN pDivision ON (pList.Section = pDivision.ID)
                                       LEFT JOIN pCompany ON (pList.Company = pCompany.ID) 
                                           LEFT JOIN AcessPoint ON (pLogData.DoorIndex = AcessPoint.GIndex)
                                               LEFT JOIN Events ON (pLogData.Event = Events.Event)
                         WHERE (pLogData.TimeVal BETWEEN :start + ' 00:00:00.000' AND :end + ' 23:59:59.000')
                           AND pLogdata.DoorIndex IN (31,32,33,34)
                         GROUP BY pLogData.Hozorgan
                                 ,pList.Name
                                 ,pList.FirstName
                                 ,pList.MidName
                                 ,cast(pLogData.Timeval as date)
                                 ,pDivision.Name
                                 ,pCompany.Name
                                 ,pPost.Name
                         ORDER BY pList.Name
                               , pList.FirstName
                               , pList.MidName
                               , cast(min(pLogData.TimeVal) as timestamp)
                               , cast(max(pLogData.TimeVal) as timestamp)
                """
            )
            result = connection.execute(qry, {"start": start, "end": end})
            dict = result.mappings().all()
            print(*dict)
      

    except SQLAlchemyError as e:
        print("Ошибка подключения:", e)
