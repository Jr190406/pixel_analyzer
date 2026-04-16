from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from analyzer.models import UserProfile

class Command(BaseCommand):
    help = 'Set user roles for the document analyzer system'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to modify')
        parser.add_argument(
            '--role',
            type=str,
            choices=['regular', 'business_owner', 'super_admin'],
            default='regular',
            help='Role to assign to the user'
        )

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        
        try:
            user = User.objects.get(username=username)
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            old_role = profile.role
            profile.role = role
            profile.save()
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for user "{username}" with role "{role}"')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Updated user "{username}" role from "{old_role}" to "{role}"')
                )
                
            # Display current capabilities
            self.stdout.write('\nUser capabilities:')
            self.stdout.write(f'  - Can manage pricing: {profile.can_manage_pricing()}')
            self.stdout.write(f'  - Can view all users: {profile.can_view_all_users()}')
            self.stdout.write(f'  - Is business owner: {profile.is_business_owner()}')
            self.stdout.write(f'  - Is super admin: {profile.is_super_admin()}')
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
