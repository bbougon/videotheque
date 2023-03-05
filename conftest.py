import random
import re
import immobilus  # noqa
from typing import Optional

from faker import Faker
from faker.providers import BaseProvider

faker = Faker()


class FileNameProvider(BaseProvider):
    def custom_file_name(
        self, category: str = "video", language: Optional[str] = None, *args
    ) -> str:
        name: str = " ".join(faker.words(nb=5))
        extension = faker.file_extension(category=category, *args)
        if language is not None:
            indices = [
                index.start() for index in (re.finditer(pattern=" ", string=name))
            ]
            index = random.choice(indices)
            name = f"{name[:index]} {language}{name[index:]}"
        return f"{name}.{extension}"


faker.add_provider(FileNameProvider)
