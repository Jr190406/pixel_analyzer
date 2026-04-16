#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pixel_cost_optimizer.settings')
django.setup()

from analyzer.models import CostSetting

print("=== FIXING COVERAGE GAPS FOR sndprintmedia ===")

user_name = 'sndprintmedia'

# Fix B&W rules gaps
print("Fixing B&W rules...")
bw_rules = CostSetting.objects.filter(business_owner__username=user_name, color=False, is_active=True).order_by('coverage_min')

gap_fixes = [
    (21.0, 20.0),  # 21% -> 20%
    (41.0, 40.0),  # 41% -> 40%  
    (61.0, 60.0),  # 61% -> 60%
    (81.0, 80.0),  # 81% -> 80%
]

for old_min, new_min in gap_fixes:
    rule = bw_rules.filter(coverage_min=old_min).first()
    if rule:
        print(f"  Updating B&W rule: {rule.coverage_min}%-{rule.coverage_max}% -> {new_min}%-{rule.coverage_max}%")
        rule.coverage_min = new_min
        rule.save()

# Fix Color rules gaps  
print("Fixing Color rules...")
color_rules = CostSetting.objects.filter(business_owner__username=user_name, color=True, is_active=True).order_by('coverage_min')

color_gap_fixes = [
    (11.0, 10.0),  # 11% -> 10%
    (21.0, 20.0),  # 21% -> 20%
    (31.0, 30.0),  # 31% -> 30%
    (41.0, 40.0),  # 41% -> 40%
    (51.0, 50.0),  # 51% -> 50%
    (61.0, 60.0),  # 61% -> 60%
    (71.0, 70.0),  # 71% -> 70%
    (81.0, 80.0),  # 81% -> 80%
    (91.0, 90.0),  # 91% -> 90%
]

for old_min, new_min in color_gap_fixes:
    rule = color_rules.filter(coverage_min=old_min).first()
    if rule:
        print(f"  Updating Color rule: {rule.coverage_min}%-{rule.coverage_max}% -> {new_min}%-{rule.coverage_max}%")
        rule.coverage_min = new_min
        rule.save()

print("\n=== TESTING COVERAGE AFTER FIXES ===")
from analyzer.views import check_business_owner_complete_coverage
from django.contrib.auth.models import User

user = User.objects.get(username=user_name)
result = check_business_owner_complete_coverage(user)
print(f"Coverage result for {user_name}: {result}")

print("\nUpdated rules:")
bw_rules = CostSetting.objects.filter(business_owner=user, color=False, is_active=True).order_by('coverage_min')
color_rules = CostSetting.objects.filter(business_owner=user, color=True, is_active=True).order_by('coverage_min')

print("B&W Rules:")
for rule in bw_rules:
    print(f"  {rule.coverage_min}%-{rule.coverage_max}%")

print("Color Rules:")  
for rule in color_rules:
    print(f"  {rule.coverage_min}%-{rule.coverage_max}%")