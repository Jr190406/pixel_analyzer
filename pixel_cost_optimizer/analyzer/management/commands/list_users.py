from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from analyzer.models import UserProfile

class Command(BaseCommand):
    help = 'List all users and their roles in the document analyzer system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--role',
            type=str,
            choices=['regular', 'business_owner', 'super_admin'],
            help='Filter by specific role'
        )

    def handle(self, *args, **options):
        filter_role = options.get('role')
        
        self.stdout.write(self.style.SUCCESS('Document Analyzer - User Roles'))
        self.stdout.write('=' * 50)
        
        users = User.objects.all().order_by('username')
        
        for user in users:
            try:
                profile = user.userprofile
                role = profile.role
                
                # Filter by role if specified
                if filter_role and role != filter_role:
                    continue
                    
                # Color coding for roles
                if role == 'super_admin':
                    role_display = self.style.ERROR(f'{role.title().replace("_", " ")} 👑')
                elif role == 'business_owner':
                    role_display = self.style.SUCCESS(f'{role.title().replace("_", " ")} 💼')
                else:
                    role_display = f'{role.title().replace("_", " ")} 👤'
                
                # Display user info
                self.stdout.write(f'Username: {user.username}')
                if user.email:
                    self.stdout.write(f'  Email: {user.email}')
                if user.first_name or user.last_name:
                    self.stdout.write(f'  Name: {user.first_name} {user.last_name}'.strip())
                self.stdout.write(f'  Role: {role_display}')
                self.stdout.write(f'  Joined: {user.date_joined.strftime("%Y-%m-%d")}')
                
                # Show capabilities
                capabilities = []
                if profile.can_manage_pricing():
                    capabilities.append('Manage Pricing')
                if profile.can_view_all_users():
                    capabilities.append('View All Users')
                    
                if capabilities:
                    self.stdout.write(f'  Capabilities: {", ".join(capabilities)}')
                
                self.stdout.write('-' * 30)
                
            except UserProfile.DoesNotExist:
                self.stdout.write(f'Username: {user.username}')
                self.stdout.write(self.style.WARNING('  Role: No profile (will be created automatically)'))
                self.stdout.write('-' * 30)
        
        # Summary
        total_users = User.objects.count()
        super_admins = UserProfile.objects.filter(role='super_admin').count()
        business_owners = UserProfile.objects.filter(role='business_owner').count()
        regular_users = UserProfile.objects.filter(role='regular').count()
        
        self.stdout.write('\nSUMMARY:')
        self.stdout.write(f'Total Users: {total_users}')
        self.stdout.write(f'Super Admins: {super_admins}')
        self.stdout.write(f'Business Owners: {business_owners}')
        self.stdout.write(f'Regular Users: {regular_users}')
