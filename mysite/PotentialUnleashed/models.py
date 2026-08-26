from django.db import models
import datetime as dt, timedelta
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

    # All models have an implicit ID field which is used as a PK

Muscle_Groups = [
    ("C", "Chest"),
    ("T", "Triceps"),
    ("S", "Shoulders"),
    ("Abs", "Abs"),
    ("B", "Biceps"),
    ("Fr", "Forearms"),
    ("UB", "UpperBack"),
    ("L", "Lats"),
    ("H", "Hamstrings"),
    ("Q", "Quadriceps"),
    ("Ca", "Calves"),
    ("G", "Glutes"),
    ("Tr", "Traps"),
    ("N", "Neck"),
    ("LB", "LowerBack"),
]    
    
# An object representing unique exercise objects    
class Exercise(models.Model):
    
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    target_muscle = models.CharField(max_length=20, choices=Muscle_Groups, blank=False, null=False)
    
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

# An object that will have a one:many relationship with workouts
# One Mesocycles can contain many workouts
# Imposed by foreign key in Workout
class Mesocycle(models.Model):
    
    name = models.CharField(default="Please Add Name", null=False, blank=False, unique=True, max_length=100)
    notes = models.TextField(blank=True)
    startDate = models.DateField(null=False, blank=False)
    endDate = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name 
    
    def __repr__(self):
        return self.name 
    
    def getWorkouts(self):        
        return self.workouts.all() 
    

WorkoutTypes = [
    ("U", "Upper"),
    ("L", "Lower"), 
    ("P", "Push"), 
    ("PU", "Pull"),
    ("LE", "Legs"), 
    ("A", "Arms"),
    ("FB", "FullBody"), 
    ("C","Cardio"),
    ("N", "None")
]

# An object representing a day where I have a workout
class Workout(models.Model):
    
    mesocycle = models.ForeignKey(Mesocycle, on_delete=models.CASCADE, related_name="workouts", null=True, blank=True) # I can call from a parent instance parent.workouts.all()
    name = models.CharField(default="Name", null=False, blank=False, max_length=100)
    date = models.DateField("Workout Date", null=False, default=timezone.now())
    type = models.CharField(blank=False, null=False, choices=WorkoutTypes, max_length=20, default="None")
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name + "-" + str(self.mesocycle) + " " + str(self.date)    
    
    def __repr__(self):
        return self.name
  
    def copyWorkout(self, other):
        if isinstance(other, Workout):
                other.mesocycle = self.mesocycle
                other.name = self.name
                other.date = self.date + dt.timedelta(days=7)
                other.type = self.type
                other.save() # Update other and save it 
                
                
                # Create clones of workoutexercises
                for wk in self.workoutexercises.all():
                    newWk = WorkoutExercise(workout=other,
                                                   exercise=wk.exercise,
                                                   order=wk.order)
                    newWk.save()
                    
                    # Create clones of sets
                    for s in wk.set_set.all():
                        newSet = Set(workout_exercise=newWk,
                                                    reps_target=s.reps_target,
                                                    reps_hit=s.reps_hit,
                                                    rest_time=s.rest_time,
                                                    weight_target=s.weight_target,
                                                    weight_hit=s.weight_hit)
                        newSet.save()
        
        
        else:
            print("Instance is not of type Workout")
            return None        
        
        
  
# An exercise object tied to a workout     
class WorkoutExercise(models.Model):
    
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="workoutexercises") # CASCADE kill parent means nuke all the kids PROTECT means kill kids then can kill parent
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True)
    order = models.IntegerField(blank=False,null=False)
    
    def __str__(self):
        return str(self.workout) + " " + self.exercise.name 
    
    def __repr__(self):
        return self.workout.name + " " + self.exercise.name     
    
    def getDate(self):
        return self.workout.date
    
    class Meta:
        ordering = ['workout__date']

# Details of a workoutexercises - seems redundant    BUT ITS NOT!

ProgressionTypes = [
    ("SS", "Approach: all sets besides last set are done at rep target"),
    ("3's", "Approach: Pick 2 or 3 sets, with a weight you can do 7-8reps with. When you Perform 8+, add minimum Weight."), 
    ("DDP", "Approach: 3 total sets, each progress at the own pace. (Compounds)"), 
    ("Rep Goal", "Approach: Use the same weight for each set, all sets taken to max safe reps, Add up total reps, If reps >=  a predefined rep goal, add weight"), 
    ("Bulldozer", "Approach: Take 3 sets into 5 mini sets"),
    ("N", "None")
]
class Set(models.Model):
    
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    reps_target = models.IntegerField("Rep Target",default=1,blank=False, validators=[MinValueValidator(1), MaxValueValidator(100)] )
    reps_hit = models.IntegerField("Reps Hit", default=1, blank=False, validators=[MinValueValidator(1), MaxValueValidator(100)])
    rest_time = models.IntegerField("Rest", blank=False, default=60)
    
    weight_target = models.DecimalField("Weight Target (Kgs)",default=1.0, blank=False, validators=[MinValueValidator(0), MaxValueValidator(1000)], decimal_places=2, max_digits=8)
    weight_hit = models.DecimalField("Weight Hit (Kgs)",default=1.0, blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(1000)], decimal_places=2, max_digits=8)
    
    progression_model = models.CharField(blank=False, null=False, choices=ProgressionTypes, max_length=500, default="SS")
    
    def __str__(self):
        return str(self.workout_exercise.exercise) + f" x {self.reps_target} reps @{self.weight_target}kgs"

    def getExercise(self):
        return self.workout_exercise.exercise

    def getRepTarget(self):
        return self.reps_target
    
    def getRepsHit(self):
        return self.reps_hit
    
    def getRestTime(self):
        return self.rest_time
    
    def getWeightTarget(self):
        return self.weight_target
    
    def getWeightHit(self):
        return self.weight_hit
    
    def getSetInfo(self):
        return str(self.workout_exercise.exercise) + f" x {self.reps_hit} reps @{self.weight_hit}kgs"
        
        
    class Meta:
        ordering = ["workout_exercise__workout__date"]
        
    
    
    
    
    
    



    
    
    
    