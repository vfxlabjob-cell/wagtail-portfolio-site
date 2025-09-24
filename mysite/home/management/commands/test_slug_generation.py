from django.core.management.base import BaseCommand
from home.models import ProjectCategory, ProjectPage
from wagtail.models import Page


class Command(BaseCommand):
    help = 'Test automatic slug generation'

    def handle(self, *args, **options):
        self.stdout.write("=== TESTING SLUG GENERATION ===")
        
        # Тест 1: ProjectCategory
        self.stdout.write("Testing ProjectCategory slug generation...")
        try:
            category = ProjectCategory(
                name="Test Clothing Store",
                slug=""  # Пустой slug
            )
            category.save()
            self.stdout.write(f"✅ Category created: {category.name} -> slug: '{category.slug}'")
        except Exception as e:
            self.stdout.write(f"❌ Error creating category: {e}")
        
        # Тест 2: ProjectPage
        self.stdout.write("Testing ProjectPage slug generation...")
        try:
            root_page = Page.objects.filter(depth=1).first()
            if root_page:
                project_page = ProjectPage(
                    title="My Test Project",
                    slug=""  # Пустой slug
                )
                root_page.add_child(instance=project_page)
                self.stdout.write(f"✅ ProjectPage created: {project_page.title} -> slug: '{project_page.slug}'")
            else:
                self.stdout.write("❌ No root page found")
        except Exception as e:
            self.stdout.write(f"❌ Error creating project page: {e}")
        
        self.stdout.write("=== TEST COMPLETE ===")
