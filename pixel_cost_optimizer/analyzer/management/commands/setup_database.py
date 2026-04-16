from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from analyzer.models import DefaultPricingRule, CostSetting, UserProfile
from django.db import transaction

class Command(BaseCommand):
    help = 'Setup default pricing rules and admin user for Pixel Cost Optimizer'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Setting up Pixel Cost Optimizer Database...')
        self.stdout.write('=' * 50)
        
        try:
            with transaction.atomic():
                # Step 1: Create superuser admin
                self.create_admin_user()
                
                # Step 2: Create default pricing rules
                self.create_default_pricing_rules()
                
                # Step 3: Create sample users
                self.create_sample_users()
                
                # Step 4: Create business pricing examples
                self.create_business_pricing_examples()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error during setup: {e}')
            )
            return
            
        self.display_summary()
        
    def create_admin_user(self):
        """Create admin user with super_admin role"""
        self.stdout.write('👤 Creating admin user...')
        
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@pixelcost.com',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'System',
                'last_name': 'Administrator'
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('✅ Created admin user: admin / admin123')
        else:
            self.stdout.write('ℹ️  Admin user already exists')
            
        # Create or update profile
        profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'role': 'super_admin'}
        )
        
        if not created and profile.role != 'super_admin':
            profile.role = 'super_admin'
            profile.save()
            self.stdout.write('✅ Updated admin role to super_admin')
        elif created:
            self.stdout.write('✅ Created admin profile')
            
    def create_default_pricing_rules(self):
        """Create system-wide default pricing rules"""
        self.stdout.write('💰 Creating default pricing rules...')
        
        # Clear existing default rules
        DefaultPricingRule.objects.all().delete()
        
        # Define pricing tiers (coverage_min, coverage_max, bw_cost, color_cost, reason)
        pricing_tiers = [
            (0.0, 25.0, 1.00, 3.00, "Light printing - minimal ink usage"),
            (25.1, 50.0, 1.50, 4.00, "Medium printing - moderate ink usage"), 
            (50.1, 75.0, 2.00, 5.00, "Heavy printing - substantial ink usage"),
            (75.1, 100.0, 2.50, 6.00, "Full printing - maximum ink usage")
        ]
        
        rules_created = 0
        
        for coverage_min, coverage_max, bw_cost, color_cost, reason in pricing_tiers:
            # Create B&W rule
            bw_rule = DefaultPricingRule.objects.create(
                color=False,
                coverage_min=coverage_min,
                coverage_max=coverage_max,
                cost=bw_cost,
                reason=f"B&W {reason}",
                is_active=True
            )
            rules_created += 1
            self.stdout.write(f'✅ B&W Rule: {coverage_min}%-{coverage_max}% = ₱{bw_cost}')
            
            # Create Color rule
            color_rule = DefaultPricingRule.objects.create(
                color=True,
                coverage_min=coverage_min,
                coverage_max=coverage_max,
                cost=color_cost,
                reason=f"Color {reason}",
                is_active=True
            )
            rules_created += 1
            self.stdout.write(f'✅ Color Rule: {coverage_min}%-{coverage_max}% = ₱{color_cost}')
            
        self.stdout.write(f'✅ Created {rules_created} default pricing rules')
        
    def create_sample_users(self):
        """Create sample users for testing"""
        self.stdout.write('👥 Creating sample users...')
        
        sample_users = [
            {
                'username': 'business_owner',
                'email': 'business@example.com',
                'password': 'business123',
                'role': 'business_owner',
                'first_name': 'Maria',
                'last_name': 'Santos'
            },
            {
                'username': 'regular_user',
                'email': 'user@example.com',
                'password': 'user123',
                'role': 'regular',
                'first_name': 'Juan',
                'last_name': 'Cruz'
            }
        ]
        
        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f"✅ Created user: {user_data['username']} / {user_data['password']}")
            
            # Create profile
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': user_data['role']}
            )
            
            if profile_created:
                self.stdout.write(f"✅ Created profile for {user_data['username']}: {user_data['role']}")
                
    def create_business_pricing_examples(self):
        """Create sample business owner pricing rules"""
        self.stdout.write('🏢 Creating business owner pricing examples...')
        
        try:
            business_user = User.objects.get(username='business_owner')
            
            # Clear existing business rules for this user
            CostSetting.objects.filter(business_owner=business_user).delete()
            
            # Create competitive business pricing (20% lower than default)
            business_pricing = [
                # B&W Business Pricing 
                (False, 0.0, 25.0, 0.80, "Business B&W Light - 20% discount"),
                (False, 25.1, 50.0, 1.20, "Business B&W Medium - 20% discount"),
                (False, 50.1, 75.0, 1.60, "Business B&W Heavy - 20% discount"),
                (False, 75.1, 100.0, 2.00, "Business B&W Full - 20% discount"),
                
                # Color Business Pricing
                (True, 0.0, 25.0, 2.40, "Business Color Light - 20% discount"),
                (True, 25.1, 50.0, 3.20, "Business Color Medium - 20% discount"),
                (True, 50.1, 75.0, 4.00, "Business Color Heavy - 20% discount"),
                (True, 75.1, 100.0, 4.80, "Business Color Full - 20% discount"),
            ]
            
            rules_created = 0
            for color, coverage_min, coverage_max, cost, reason in business_pricing:
                rule = CostSetting.objects.create(
                    business_owner=business_user,
                    color=color,
                    coverage_min=coverage_min,
                    coverage_max=coverage_max,
                    cost=cost,
                    reason=reason,
                    is_active=True
                )
                rules_created += 1
                rule_type = "Color" if color else "B&W"
                self.stdout.write(f"✅ {rule_type} Business Rule: {coverage_min}%-{coverage_max}% = ₱{cost}")
                
            self.stdout.write(f'✅ Created {rules_created} business pricing rules')
            
        except User.DoesNotExist:
            self.stdout.write('⚠️  Business owner user not found, skipping business pricing')
            
    def display_summary(self):
        """Display setup summary"""
        self.stdout.write('')
        self.stdout.write('=' * 50)
        self.stdout.write('✅ Database setup completed successfully!')
        self.stdout.write('')
        
        # Count records
        users_count = User.objects.count()
        profiles_count = UserProfile.objects.count()
        default_rules_count = DefaultPricingRule.objects.count()
        business_rules_count = CostSetting.objects.count()
        
        self.stdout.write('📊 DATABASE SUMMARY:')
        self.stdout.write(f'   • Total users: {users_count}')
        self.stdout.write(f'   • User profiles: {profiles_count}')
        self.stdout.write(f'   • Default pricing rules: {default_rules_count}')
        self.stdout.write(f'   • Business pricing rules: {business_rules_count}')
        self.stdout.write('')
        
        self.stdout.write('🔑 LOGIN CREDENTIALS:')
        self.stdout.write('   • Admin: admin / admin123')
        self.stdout.write('   • Business Owner: business_owner / business123')
        self.stdout.write('   • Regular User: regular_user / user123')
        self.stdout.write('')
        
        self.stdout.write('🌐 ACCESS YOUR APPLICATION:')
        self.stdout.write('   • Main site: http://127.0.0.1:8000/')
        self.stdout.write('   • Demo: http://127.0.0.1:8000/demo/')
        self.stdout.write('   • Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('')
        
        self.stdout.write('💡 WHAT WAS CREATED:')
        self.stdout.write('   ✓ Default system pricing (₱1-2.50 B&W, ₱3-6 Color)')
        self.stdout.write('   ✓ Business owner with custom pricing (20% discount)')
        self.stdout.write('   ✓ User roles and permissions')
        self.stdout.write('   ✓ All database tables ready for dynamic pricing')
        self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('🎉 Your Pixel Cost Optimizer is ready to use!'))