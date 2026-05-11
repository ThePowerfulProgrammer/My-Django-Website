from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Workout, Exercise, Set, WorkoutExercise, Mesocycle
from .forms import SetForm, SetModelForm, WorkoutExerciseForm, AddExerciseForm, changeWorkoutNameForm, trackWorkoutForm


# Create your views here.

# Home Page - 1 
def home(request):
    
    print(request.user)
    print(request.user.is_superuser)
    return render(request, "PotentialUnleashed/home.html", context={})

# Show all of my mesocycles
# 2 
def mesocycles(request):
    
    mesocycles = Mesocycle.objects.all().order_by("-id")
    current_mesocycle = Mesocycle.objects.last()
    print("CURRENT MESOCYCLE: ", current_mesocycle)
    print(mesocycles)
    return render(request, "PotentialUnleashed/mesocycles.html", 
                  context={"mesocycles": mesocycles, 
                           "current_mesocycle":current_mesocycle})
    
# Show all workouts under a mesocycle    
# 3
def workoutsPerMesocycle(request, mesocycle_id):

    mesocycle = Mesocycle.objects.get(id=mesocycle_id)    
    mesocycleWorkouts = mesocycle.workouts.all()
    
    return render(request, "PotentialUnleashed/mesocycleWorkouts.html", 
                  context={"mesocycleWorkouts": mesocycleWorkouts,
                           "mesocycle_id": mesocycle_id,
                           "mesocycle": mesocycle})
    
    

# I am going to pass a workout id and get all the details for my workout
# Details, how to track a set, update a workout
# 4
def workoutDetails(request, mesocycle_id,workout_id):    
    
    try:
        # I now have a workout object
        workout = Workout.objects.get(pk=workout_id)
        mesocycle = Mesocycle.objects.get(id=mesocycle_id)
        allWorkouts = mesocycle.workouts.all()
        print(workout)        
        print(workout_id)
        print("TRYING")            
        
        # I need to get all the sets associated with the workoutExercise
        sets = Set.objects.filter(workout_exercise__workout=workout)
            

        # I need the indiviual information relevant to an exercise Rope Pulldown x 1 reps @1.00kgs
        if request.user.is_superuser:
                
            exercise_fields = ["#", "Exercise", "Rep target", "weight target (Kilos)", "", "Reps Hit", "Weight Hit (Kilos)", "Track" ]
                                
            return render(request, "PotentialUnleashed/workoutDetail.html", 
                        context={"sets": sets, 
                                "exercise_fields": exercise_fields,
                                "workout":workout,
                                "mesocycle_id":mesocycle_id, 
                                "workout_id": workout_id,
                                "allWorkouts": allWorkouts})
        else:
                    
            exercise_fields = ["#", "Exercise", "Rep target", "weight target (Kilos)", "", "Reps Hit", "Weight Hit (Kilos)" ]
                                
            return render(request, "PotentialUnleashed/workoutDetail.html", 
                        context={"sets": sets, 
                                "exercise_fields": exercise_fields,
                                "workout":workout,
                                "mesocycle_id":mesocycle_id, 
                                "workout_id": workout_id,
                                "allWorkouts": allWorkouts})
                                
        # I need to get all the workoutExercises related to it
        # workoutExercises = workout.workoutexercises.all()
        
        # print(WorkoutExercise.objects.get(id=9))
        # print(Set.objects.get(workout_exercise=WorkoutExercise.objects.get(id=9)))

        # for workoutExercise in workoutExercises:
        #     s = Set.objects.filter(workout_exercise=workoutExercise)
        #     for i  in s:
        #         print(i)
            
            

        
    except Workout.DoesNotExist:
        print("Workout does not exist")
        return HttpResponse("Workout does not exist")

# I want to be able to copy a workout    
# 5
def copyWorkout(request, workout_id):
    
    workout = Workout.objects.get(id=workout_id)
    newWorkout = Workout()
    
    workout.copyWorkout(newWorkout)
    newWorkout.save()
    # I now have a newly created copied workout with a different date
    return redirect("Potential_Unleashed:mesocycles")

# 6 edit workout to add new set
def editWorkout(request,  mesocycle_id,workout_id):
    workout = Workout.objects.get(id=workout_id)
    # mesocycle = Mesocycle.objects.get(id=mesocycle_id)
    
    if request.method == "POST":
                        
        addExerciseForm = AddExerciseForm(request.POST)
        
        if addExerciseForm.is_valid():
            print(addExerciseForm.cleaned_data)
            
            selectedWorkout = addExerciseForm.cleaned_data.get("workout")
            exercise = addExerciseForm.cleaned_data.get("exercise")
            order = addExerciseForm.cleaned_data.get("order")
            
            workoutexercise = WorkoutExercise(workout=selectedWorkout, exercise=exercise, order=order)
            workoutexercise.save()
            
            repsTarget = addExerciseForm.cleaned_data.get("reps_target")
            restTime = addExerciseForm.cleaned_data.get("rest_time")
            weightTarget = addExerciseForm.cleaned_data.get("weight_target")
            
            set = Set(workout_exercise=workoutexercise, reps_target=repsTarget, rest_time=restTime, weight_target=weightTarget)
            set.save() 

            # Create a workout exercise object    


        return redirect("Potential_Unleashed:mesocycles")
    
    
    else:
        # render form
        order = workout.workoutexercises.last().order + 1
        addExerciseForm = AddExerciseForm(initial={"workout":workout, "order": order})
        
        # render changeWorkoutNameForm
        changeworkoutnameForm = changeWorkoutNameForm(initial={"name": workout.name})
        
        return render(request, "PotentialUnleashed/editWorkouts.html", context={"addExerciseForm": addExerciseForm,
                                                                                "changeworkoutnameForm": changeworkoutnameForm,
                                                                                "workout_id": workout_id,
                                                                                "mesocycle_id": mesocycle_id})
        
# 7 edit a workouts name
def editWorkoutName(request, workout_id, mesocycle_id):

    if request.method == "POST":
        
        workout = Workout.objects.get(id=workout_id)
        changeworkoutnameForm = changeWorkoutNameForm(request.POST)
        if changeworkoutnameForm.is_valid():
            workout.name = changeworkoutnameForm.cleaned_data.get("name")
            
            workout.save()
            
            return redirect("Potential_Unleashed:mesocycles")
        
    else:
        return redirect("Potential_Unleashed:home")

# Track progress in a workout by updating repsHit and WeightHit for an exercise in a workout    
# 8
def trackWorkout(request, workoutId, setId):
    # I need a form for every set
    print("In track workout")
    workout = Workout.objects.get(id=workoutId)
    mesocycle = workout.mesocycle
    
    
    if request.method == "POST":
        
        print("POST")
        # Process data and return to workout information
        form_data = request.POST
        print(form_data)
        print(workoutId)
        print(setId)
        reps_hit = form_data.get("reps_hit")
        weight_hit = form_data.get("weight_hit")
        set = Set.objects.get(id=setId)
        set.reps_hit = reps_hit
        set.weight_hit = weight_hit
        set.save()
        print("SET: ", set)
        print(reps_hit)
        print(weight_hit)

        return redirect("Potential_Unleashed:detail", workout_id=workoutId, mesocycle_id=mesocycle.id)
        

   
    else:
        # We need to present the user with data to edit
        print("GET")
        set = Set.objects.get(id=setId)
        
        setForm = SetModelForm(instance=set, initial={"reps_hit": set.reps_target, 
                                                      "weight_hit": set.weight_target})
                
        return render(request, "PotentialUnleashed/trackWorkout.html", 
                      context={"workout_id": workoutId,
                               "workout":workout,
                               "set_id":setId, 
                                "setForm": setForm,
                                "set":set})        

# Use a mesocycle object to present all associated workouts ordered by date 
# 9 
def mesocycleHistory(request, mesocycle_id):
    
    mesocycle = Mesocycle.objects.get(id=mesocycle_id)
    workouts = mesocycle.workouts.all().order_by("date")
    workoutInfo = []
    sets = []    
    
    for workout in workouts:
        workoutInfo.append(workout.name + " - " + str(workout.date))
        set = Set.objects.filter(workout_exercise__workout=workout)
        sets.append(set)
    
    sets_workout_info = zip(sets, workoutInfo)
    exercise_fields = ["#", "Exercise", "Rep target", "weight target (Kilos)", "", "Reps Hit", "Weight Hit (Kilos)" ]


    return render(request,"PotentialUnleashed/workoutHistory.html", 
                  context={ "sets_workout_info": sets_workout_info,
                           "exercise_fields": exercise_fields})   

# Still working on this        
def trackFullWorkout(request, workoutId):
    print(workoutId)
    workout = Workout.objects.get(id=workoutId)
    mesocycle = workout.mesocycle
    allWorkouts = mesocycle.workouts.all()
          
        
    # I need to get all the sets associated with the workoutExercise
    sets = Set.objects.filter(workout_exercise__workout=workout)

    form = trackWorkoutForm(sets)
    return render(request, "PotentialUnleashed/trackFullWorkout.html", context={"form": form})

 
    

# NOT USING THIS ONE!
# I need a view that shows all my Workout Objects
def workoutsPage(request):
    allWorkouts = Workout.objects.all()
    try:
        
            
        print(allWorkouts)
        return render(request, "PotentialUnleashed/workoutsPage.html",
                    context={"allWorkouts": allWorkouts})

    except Exception as e:
        print(e)
        return HttpResponse(e)