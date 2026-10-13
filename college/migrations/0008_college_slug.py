
from django.db import migrations, models
from django.utils.text import slugify


def populate_college_slugs(apps, schema_editor):
    College = apps.get_model("college", "College")
    used_slugs = set()

    for college in College.objects.all().order_by("id"):
        base_slug = slugify(college.name)
        slug = base_slug
        counter = 2

        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1

        college.slug = slug
        college.save(update_fields=["slug"])
        used_slugs.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ("college", "0007_notification"),
    ]

    operations = [
        migrations.AddField(
            model_name="college",
            name="slug",
            field=models.SlugField(
                blank=True,
                max_length=220,
                null=True,
                unique=True,
            ),
        ),
        migrations.RunPython(
            populate_college_slugs,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="college",
            name="slug",
            field=models.SlugField(
                max_length=220,
                unique=True,
            ),
        ),
    ]
