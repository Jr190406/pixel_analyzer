from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import CostSetting, DefaultPricingRule, DocumentAnalysis, UserProfile

@admin.register(CostSetting)
class CostSettingAdmin(admin.ModelAdmin):
    list_display = ('business_owner', 'get_color_display', 'coverage_range', 'formatted_cost', 'reason', 'is_active', 'edit_actions')
    list_filter = ('color', 'is_active', 'business_owner')
    search_fields = ('business_owner__username', 'reason')
    ordering = ('business_owner', 'color', 'coverage_min')
    list_editable = ('is_active',)
    
    def get_color_display(self, obj):
        color_class = 'style="color: #007bff; font-weight: bold;"' if obj.color else 'style="color: #6c757d;"'
        return format_html('<span {}>{}</span>', color_class, "Color" if obj.color else "B&W")
    get_color_display.short_description = 'Type'
    
    def coverage_range(self, obj):
        return f"{obj.coverage_min}% - {obj.coverage_max}%"
    coverage_range.short_description = 'Coverage Range'
    
    def formatted_cost(self, obj):
        return f"₱{obj.cost}"
    formatted_cost.short_description = 'Cost'
    
    def edit_actions(self, obj):
        edit_url = reverse('admin:analyzer_costsetting_change', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">✏️ Edit</a>',
            edit_url
        )
    edit_actions.short_description = 'Quick Edit'
    edit_actions.allow_tags = True
    
    actions = ['activate_rules', 'deactivate_rules', 'duplicate_rules']
    
    def activate_rules(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} pricing rules were activated.')
    activate_rules.short_description = "Activate selected pricing rules"
    
    def deactivate_rules(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} pricing rules were deactivated.')
    deactivate_rules.short_description = "Deactivate selected pricing rules"

@admin.register(DefaultPricingRule)
class DefaultPricingRuleAdmin(admin.ModelAdmin):
    list_display = ('get_color_display', 'coverage_range', 'formatted_cost', 'reason', 'is_active', 'edit_actions')
    list_filter = ('color', 'is_active')
    search_fields = ('reason',)
    ordering = ('color', 'coverage_min')
    list_editable = ('is_active',)
    
    def get_color_display(self, obj):
        color_class = 'style="color: #007bff; font-weight: bold;"' if obj.color else 'style="color: #6c757d;"'
        return format_html('<span {}>{}</span>', color_class, "Color" if obj.color else "B&W")
    get_color_display.short_description = 'Type'
    
    def coverage_range(self, obj):
        return f"{obj.coverage_min}% - {obj.coverage_max}%"
    coverage_range.short_description = 'Coverage Range'
    
    def formatted_cost(self, obj):
        return f"₱{obj.cost}"
    formatted_cost.short_description = 'Cost'
    
    def edit_actions(self, obj):
        edit_url = reverse('admin:analyzer_defaultpricingrule_change', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">✏️ Edit</a>',
            edit_url
        )
    edit_actions.short_description = 'Quick Edit'
    edit_actions.allow_tags = True
    
    actions = ['activate_rules', 'deactivate_rules']
    
    def activate_rules(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} default pricing rules were activated.')
    activate_rules.short_description = "Activate selected default rules"
    
    def deactivate_rules(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} default pricing rules were deactivated.')
    deactivate_rules.short_description = "Deactivate selected default rules"
    
    def get_queryset(self, request):
        return super().get_queryset(request)
    
    class Meta:
        verbose_name = "Default Pricing Rule"
        verbose_name_plural = "Default Pricing Rules (Configure System-wide Pricing)"


@admin.register(DocumentAnalysis)
class DocumentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'user', 'get_analysis_summary', 'formatted_cost', 'get_file_info', 'created_at')
    list_filter = ('created_at', 'file_type', 'user')
    search_fields = ('document_name', 'user__username')
    readonly_fields = ('created_at', 'analysis_result')
    ordering = ('-created_at',)
    
    def get_analysis_summary(self, obj):
        return obj.get_analysis_summary()
    get_analysis_summary.short_description = 'Pages Summary'
    
    def formatted_cost(self, obj):
        return f"₱{obj.overall_cost}"
    formatted_cost.short_description = 'Total Cost'
    
    def get_file_info(self, obj):
        size_info = f" ({obj.get_file_size_mb()} MB)" if obj.get_file_size_mb() else ""
        file_type = obj.file_type.upper() if obj.file_type else "Unknown"
        return f"{file_type}{size_info}"
    get_file_info.short_description = 'File Info'
    
    def has_add_permission(self, request):
        # Disable manual addition since these are created automatically
        return False

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'get_role_badge', 'created_at', 'can_manage_pricing', 'can_view_all_users')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('user__username',)
    list_editable = ('role',)
    
    def get_role_badge(self, obj):
        colors = {
            'super_admin': '#dc3545',
            'business_owner': '#28a745', 
            'regular': '#6c757d'
        }
        color = colors.get(obj.role, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">{}</span>',
            color,
            obj.get_role_display()
        )
    get_role_badge.short_description = 'Role Badge'
    
    def can_manage_pricing(self, obj):
        return "✅" if obj.can_manage_pricing() else "❌"
    can_manage_pricing.short_description = 'Can Manage Pricing'
    can_manage_pricing.boolean = True
    
    def can_view_all_users(self, obj):
        return "✅" if obj.can_view_all_users() else "❌"
    can_view_all_users.short_description = 'Can View All Users'
    can_view_all_users.boolean = True
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Permissions', {
            'fields': ('role',),
            'description': 'Select the appropriate role for this user.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['make_business_owner', 'make_regular_user', 'make_super_admin']
    
    def make_business_owner(self, request, queryset):
        updated = queryset.update(role='business_owner')
        self.message_user(request, f'{updated} users were made Business Owners.')
    make_business_owner.short_description = "Make selected users Business Owners"
    
    def make_regular_user(self, request, queryset):
        updated = queryset.update(role='regular')
        self.message_user(request, f'{updated} users were made Regular Users.')
    make_regular_user.short_description = "Make selected users Regular Users"
    
    def make_super_admin(self, request, queryset):
        updated = queryset.update(role='super_admin')
        self.message_user(request, f'{updated} users were made Super Admins.')
    make_super_admin.short_description = "Make selected users Super Admins"
