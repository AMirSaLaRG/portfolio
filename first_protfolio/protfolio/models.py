from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    proficiency = models.PositiveIntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    category = models.CharField(max_length=20, choices=[
        ('webdev', 'WebDev'),
        ('ai', 'AI'), 
        ('devops', 'DevOps'),
        ('design', 'Design'),
        ('language', 'Language'),
        ('all', "All"),
    ])
    icon = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Font Awesome icon class (e.g. fa-python)"
    )
    years_experience = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        default=1.0
    )
    showcase = models.BooleanField(
        default=True,
        help_text="Display on skills section"
    )

    class Meta:
        ordering = ['-proficiency', 'name']
        
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    title_fa = models.CharField(max_length=200, null=True)
    description_fa = models.TextField(null=True)
    detailed_description_fa = models.TextField(blank=True,null=True)
    image = ProcessedImageField(
        upload_to='protfolio/static/protfolio/images/projects',
        processors=[ResizeToFill(500, 400)],
        format='JPEG',
        options={'quality': 100},
        blank=True
    )
    thumbnail = ProcessedImageField(
        upload_to='protfolio/static/protfolio/images/projects/thumbnails',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 80},
        blank=True
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    skills_used = models.ManyToManyField(Skill, through='ProjectSkill')
    featured = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    client = models.CharField(max_length=100, blank=True)
    project_type = models.CharField(max_length=20, choices=[
        ('personal', 'Personal Project'),
        ('client', 'Client Work'), 
        ('open-source', 'Open Source')
    ], default='personal')
    
    def image_basename(self):
        if self.image:
            return str(self.image)[len('protfolio/static/protfolio/images/projects')+1:] 
        return ""
    
    def thumbnail_basename(self):
        if self.image:
            return str(self.image)[len('protfolio/static/protfolio/images/projects/thumbnails')+1:] 
        return ""

    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title

class ProjectSkill(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    importance = models.PositiveIntegerField(
        default=5,
        choices=[(1, 'Basic'), (3, 'Medium'), (5, 'Core')]
    )
    usage_description = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = [['project', 'skill']]
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=100)
    certificate_id = models.CharField(max_length=50, blank=True)
    certificate_url = models.URLField(blank=True)
    completion_date = models.DateField()
    skills_covered = models.ManyToManyField(Skill, through='CourseSkill')
    duration_hours = models.PositiveIntegerField(blank=True, null=True)
    instructor = models.CharField(max_length=100, blank=True)
    accreditation = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-completion_date']

class CourseSkill(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    mastery_level = models.CharField(
        max_length=20,
        choices=[
            ('introduced', 'Introduced'),
            ('practiced', 'Practiced'),
            ('mastered', 'Mastered')
        ]
    )

    class Meta:
        unique_together = [['course', 'skill']]

class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    skills_gained = models.ManyToManyField(Skill)
    currently_attending = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='education/logos/', blank=True)

    class Meta:
        verbose_name_plural = "Education"

class Testimonial(models.Model):
    author = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    project = models.ForeignKey(
        Project, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='testimonials'
    )
    avatar = models.ImageField(upload_to='testimonials/', blank=True)
    featured = models.BooleanField(default=False)
    date_received = models.DateField()

    class Meta:
        ordering = ['-date_received']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=1000)
    phone = models.CharField(max_length=15, blank=True, default="")  # Add null=True
    created_at = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"Message from {self.name}"