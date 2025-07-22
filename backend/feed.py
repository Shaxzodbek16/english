from sqlalchemy.ext.asyncio.session import AsyncSession
from faker import Faker
from typing import MutableSequence
import random

from app.core.databases.postgres import get_session_without_depends
from app.api import models


def get_random_int(start: int, stop: int):
    return random.randint(start, stop)


def get_random_element(
        elements: MutableSequence,
):
    random.shuffle(elements)
    return random.choice(list(elements))


class FeedService:
    levels = set()
    themes = set()
    sections = set()
    questions = set()
    options = set()
    questions_options = dict()
    users = set()
    user_answers = set()

    async def feed_users(self):
        seen = set()
        for i in range(1, 10001):
            random_tg_id = self.faker.unique.random_int(min=100000000, max=999999999)
            while random_tg_id in seen:
                random_tg_id = self.faker.unique.random_int(min=100000000, max=999999999)
            user = models.User(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                telegram_id=random_tg_id,
                language="ru",
                phone_number=self.faker.random_int(min=1000000000, max=9999999999),
                is_admin=self.faker.boolean(chance_of_getting_true=1),
                created_at=self.faker.date_time_between(
                    start_date="-1y", end_date="now"
                ),
                updated_at=self.faker.date_time_between(
                    start_date="-1y", end_date="now"
                )
            )
            self.session.add(user)
            self.users.add(user)
            seen.add(random_tg_id)
        await self.session.commit()

    def __init__(self, session: AsyncSession):
        self.session = session
        self.faker: Faker = Faker()

    async def feed_level(
            self,
    ):
        for l, th, s in zip(range(1, 5), range(1, 5), range(1, 5)):
            level = models.Level(
                name=f"Level {l}",
                description=self.faker.text(max_nb_chars=255),
                picture=self.faker.image_url(),
                type="level",
                created_at=self.faker.date_time_between(
                    start_date="-1y", end_date="now"
                ),
                updated_at=self.faker.date_time_between(
                    start_date="-1y", end_date="now"
                ),
            )
            theme = models.Level(
                name=f"Theme {th}",
                description=self.faker.text(max_nb_chars=255),
                picture=self.faker.image_url(),
                type="theme",
                created_at=self.faker.date_time_between(
                    start_date="-1y", end_date="now"
                ),
                updated_at=self.faker.date_time_between(
                    start_date="-1y", end_date="now"
                ),
            )
            section = models.Level(
                name=f"Section {s}",
                description=self.faker.text(max_nb_chars=255),
                picture=self.faker.image_url(),
                type="section",
            )
            self.session.add(theme)
            self.session.add(section)
            self.session.add(level)
            self.levels.add(level)
            self.themes.add(theme)
            self.sections.add(section)
        await self.session.commit()

    async def feed_questions(self):
        pp = ["question"] * 9
        pp.append("daily")
        for i in range(1, 10001):
            question = models.Question(
                name=f"Question {i}",
                picture=self.faker.image_url(),
                answer=self.faker.sentence(),
                type=get_random_element(pp),
                level=get_random_element(list(self.levels)),
                theme=get_random_element(list(self.themes)),
                created_at=self.faker.date_time_between(
                    start_date="-1y", end_date="now"
                ),
                updated_at=self.faker.date_time_between(
                    start_date="-1y", end_date="now"
                ),
            )
            self.session.add(question)
            self.questions.add(question)
        await self.session.commit()

    async def feed_options(self):
        for question in self.questions:
            a = []
            for i in range(4):
                option = models.Option(
                    question_id=question.id,
                    option=self.faker.sentence(nb_words=20),
                    is_correct=(False if i != 0 else True),
                    created_at=self.faker.date_time_between(
                        start_date="-1y", end_date="now"
                    ),
                    updated_at=self.faker.date_time_between(
                        start_date="-1y", end_date="now"
                    ),
                )
                self.session.add(option)
                self.options.add(option)
                a.append(option)
            self.questions_options[question.id] = a.copy()
            a.clear()
        await self.session.commit()

    async def feed_user_answers(self):
        for i in range(1, 10001):
            user = get_random_element(list(self.users))
            question = get_random_element(list(self.questions))
            option = get_random_element(self.questions_options[question.id])
            user_answer = models.UserAnswer(
                user_id=user.id,
                question_id=question.id,
                option_id=option.id,
                created_at=self.faker.date_time_between(
                    start_date="-3y", end_date="now"
                ),
                updated_at=self.faker.date_time_between(
                    start_date="-3y", end_date="now"
                ),
            )
            self.session.add(user_answer)
            self.user_answers.add(user_answer)
        await self.session.commit()


async def main():
    async with get_session_without_depends() as session:
        feed_service = FeedService(session)
        await feed_service.feed_users()
        await feed_service.feed_level()
        await feed_service.feed_questions()
        await feed_service.feed_options()
        await asyncio.sleep(1)
        await feed_service.feed_user_answers()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
