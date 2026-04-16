#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pixel_cost_optimizer.settings')
django.setup()

from analyzer.models import CostSetting
from django.contrib.auth.models import User
from analyzer.views import check_business_owner_complete_coverage

print("=== DEBUGGING BUSINESS OWNER COVERAGE ===")

# Find all users with cost settings
users_with_settings = User.objects.filter(costsetting__isnull=False).distinct()
print(f"Users with cost settings: {users_with_settings.count()}")

for user in users_with_settings:
    print(f"\n--- User: {user.username} (ID: {user.id}) ---")
    
    # Check their cost settings
    bw_rules = CostSetting.objects.filter(business_owner=user, color=False, is_active=True).order_by('coverage_min')
    color_rules = CostSetting.objects.filter(business_owner=user, color=True, is_active=True).order_by('coverage_min')
    
    print(f"B&W Rules ({bw_rules.count()}):")
    for rule in bw_rules:
        print(f"  {rule.coverage_min}%-{rule.coverage_max}% = ${rule.cost}")
    
    print(f"Color Rules ({color_rules.count()}):")
    for rule in color_rules:
        print(f"  {rule.coverage_min}%-{rule.coverage_max}% = ${rule.cost}")
    
    # Test coverage function
    coverage_result = check_business_owner_complete_coverage(user)
    print(f"Coverage Complete: {coverage_result}")

print("\n=== ALL USERS ===")
all_users = User.objects.all()
for user in all_users:
    cost_settings_count = CostSetting.objects.filter(business_owner=user).count()
    print(f"User: {user.username} - Cost Settings: {cost_settings_count}")