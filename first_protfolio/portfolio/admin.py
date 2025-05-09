# protfolio/admin.py
from django.contrib import admin
from django.utils.html import mark_safe
from .models import Skill, Project, Course, Education, Testimonial, ProjectSkill, CourseSkill, ContactMessage
import os

# ======================
# SKILL ADMIN
# ======================
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'category', 'showcase', 'icon_preview')
    list_editable = ('proficiency', 'showcase')
    list_filter = ('category', 'showcase')
    search_fields = ('name',)
    ordering = ('category', '-proficiency')
    
    def icon_preview(self, obj):
        return mark_safe(f'<i class="{obj.icon}"></i>') if obj.icon else "-"
    icon_preview.short_description = "Icon"

    

# ======================
# PROJECT ADMIN (with skills)
# ======================
class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 1
    autocomplete_fields = ['skill']
    fields = ('skill', 'importance', 'usage_description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'featured', 'client', 'image_preview')
    list_filter = ('project_type', 'featured', 'skills_used__category')
    search_fields = ('title', 'description', 'client')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectSkillInline]
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            filename = os.path.basename(obj.image.name)
            return mark_safe(f'<img src="/static/protfolio/images/projects/{filename}" width="150" />')
        return "-"
    image_preview.short_description = "Preview"

# ======================
# COURSE ADMIN (with skills)
# ======================
class CourseSkillInline(admin.TabularInline):
    model = CourseSkill
    extra = 1
    autocomplete_fields = ['skill']
    fields = ('skill', 'mastery_level')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'completion_date', 'duration_hours')
    list_filter = ('institution', 'completion_date')
    search_fields = ('title', 'institution', 'instructor')
    inlines = [CourseSkillInline]
    date_hierarchy = 'completion_date'

# ======================
# EDUCATION ADMIN
# ======================
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'field_of_study', 'currently_attending')
    list_filter = ('institution', 'currently_attending')
    search_fields = ('degree', 'institution')
    readonly_fields = ('logo_preview',)
    
    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="100" />')
        return "-"
    logo_preview.short_description = "Logo Preview"

# ======================
# TESTIMONIAL ADMIN
# ======================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'company', 'project_link', 'featured', 'date_received')
    list_filter = ('featured', 'company')
    search_fields = ('author', 'content')
    readonly_fields = ('avatar_preview',)
    
    def project_link(self, obj):
        if obj.project:
            return mark_safe(f'<a href="/admin/protfolio/project/{obj.project.id}/">{obj.project.title}</a>')
        return "-"
    project_link.short_description = "Project"
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" />')
        return "-"
    avatar_preview.short_description = "Avatar Preview"

# ======================
# CONTACT MESSAGE ADMIN
# ======================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message_preview', 'created_at', 'user_ip')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('message_preview',)
    
    def message_preview(self, obj):
        return mark_safe(f'<p>{obj.message[:50]}...</p>') if obj.message else "-"
    message_preview.short_description = "Message Preview"