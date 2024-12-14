from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Post, Category
from accounts.models import User, Profile


class Command(BaseCommand):
    help = 'Insert data into the database'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **kwargs):
        user = User.objects.create_user(
            email=self.faker.email(),
            password=self.faker.password(),
        )
        profile = Profile.objects.get(user=user)
        profile.first_name = self.faker.first_name()
        profile.last_name = self.faker.last_name()
        profile.description = self.faker.text()
        profile.save()
        for _ in range(10):

            Post.objects.create(
                title=self.faker.sentence(),
                content=self.faker.text(),
                author=profile,
                category=Category.objects.get_or_create(name=self.faker.word())[0],  # Get or create category
                status=self.faker.boolean(),
                published_date=self.faker.date_time(),
            )

        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))

