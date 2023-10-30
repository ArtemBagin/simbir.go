import asyncio

from sqlalchemy import select

from database.database import async_session
from models.users import Users

if __name__ == '__main__':
    async def create_admin():
        print('Вы попали в меню создания суперпользователя, следуйте следующим инструкциям.')
        async with async_session() as session:
            username = input('Введите username суперпользователя: ')
            password = input('password суперпользователя: ')

            stmt = select(Users).filter_by(username=username)
            res = await session.execute(stmt)

            if not res.first():
                new_user = Users(
                    username=username,
                    password=password,
                    is_admin=True
                )

                session.add(new_user)
                await session.commit()
            else:
                raise ValueError('Данный username занят')

            print('Суперпользователь успешно создан!')


    asyncio.run(create_admin())
