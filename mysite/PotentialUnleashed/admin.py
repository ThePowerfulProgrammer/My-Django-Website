from django.contrib import admin
from .models import Exercise, Mesocycle, Workout, WorkoutExercise, Set
from django.contrib.admin import AdminSite


# Register your models here.

admin.site.register(Exercise)
admin.site.register(Workout)

class WorkoutInline(admin.TabularInline):
    model = Workout


@admin.register(Mesocycle)
class MesocycleAdmin(admin.ModelAdmin):
    
    list_display = ("name", "startDate" )

    inlines = [
        WorkoutInline
    ]

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    
    list_display = ("getMesocycle","workout", "exercise", "order", "id")


    def getMesocycle(self, other):
        return other.workout.mesocycle 
    
    getMesocycle.short_description = "Mesocycle"

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    
    list_display = ("workout_exercise", "reps_target", "reps_hit", "weight_target", "weight_hit", "rest_time")
    

    fieldsets = (
        ("Exercise Info", {
            "fields": ("workout_exercise",)
        }),
        ("Reps", {
            "fields": ("reps_target", "reps_hit")
        }),
        ("Weight", {
            "fields": ("weight_target", "weight_hit")
        }),
        ("Rest", {
            "fields": ("rest_time",)
        }),
    )


