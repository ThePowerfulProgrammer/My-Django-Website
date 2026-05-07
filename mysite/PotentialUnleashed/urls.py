from django.urls import path 
from django.contrib import admin

from . import views

app_name = "Potential_Unleashed"

urlpatterns = [
    path("", views.home, name="home"),
    
    path("mesocycles", views.mesocycles, name="mesocycles"),
    
    path("mesocycles/<int:mesocycle_id>/workouts",views.workoutsPerMesocycle, name="workoutsPerMesocycle"),
    
    path("allWorkouts", views.workoutsPage, name="allWorkouts"),
    
    path("mesocycles/<int:mesocycle_id>/workouts/<int:workout_id>/", views.workoutDetails, name="detail"),
    
    path("copyworkout/<int:workout_id>", views.copyWorkout, name="copyWorkout"),

    path("mesocycles/<int:mesocycle_id>/workouts/<int:workout_id>/editWorkout", views.editWorkout, name="editWorkout"),
    
    path("mesocycles/<int:mesocycle_id>/workouts/<int:workout_id>/editWorkout/changeName", views.editWorkoutName, name="editWorkoutName"),
    
    path("mesocycles/<int:mesocycle_id>/history", views.mesocycleHistory, name="mesocycleHistory"),
    
    path("workout/<int:workoutId>/set/<int:setId>/", views.trackWorkout, name="trackWorkout"),
    
    path("workout/<int:workoutId>/track/", views.trackFullWorkout, name="trackFullWorkout"),
    
    path('admin/', admin.site.urls),

]