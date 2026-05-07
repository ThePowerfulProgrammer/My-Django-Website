from django.forms import ModelForm
from django import forms

from .models import Set,WorkoutExercise, Workout, Exercise

class SetForm(forms.Form):
    
    # What do I minimally need to track a workout?
    # Reps hit 
    # Weight Hit
    
    reps_hit = forms.IntegerField(label="")
    weight_hit = forms.DecimalField(label="")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control fira-sans-light display-1'  
        

    
class SetModelForm(ModelForm):
    
    
    
    class Meta:
        model = Set 
        fields = ['reps_hit', "weight_hit"]
        widgets = {
            "weight_hit": forms.NumberInput(attrs={'step': 0.5})
        }
                
    def clean_reps_hit(self):
        print(self.instance)
        
        reps_hit = self.cleaned_data.get('reps_hit')
        print(f"Form data: {reps_hit}")
        
        return reps_hit
                        
    def getExercise(self):
        name = self.instance.getExercise()
        return name
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control fira-sans-medium-italic'        
        
        
class WorkoutExerciseForm(ModelForm):
    
    class Meta:
        model = WorkoutExercise
        fields = "__all__"
        
    def __init__(self, *args, name, workout, **kwargs):
        super().__init__(*args, **kwargs)
                
        self.name = name 
        self.workout = workout
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control fira-sans-light'        
        
        
        
# Adds a workoutexericse and a set to that workoutexercise and adds it to a workout        
class AddExerciseForm(forms.Form):
    
    # WorkoutExercise
    workout = forms.ModelChoiceField(queryset=Workout.objects.all())
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all())
    order = forms.IntegerField()
    
    # Set
    
    # workout_exercise FIRST SAVE THE WORKOUT EXERCISE THEN SET workout_exercise to the newly created instance
    reps_target = forms.IntegerField() 
    rest_time = forms.IntegerField()
    weight_target = forms.DecimalField()
    
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control fira-sans-light' 
    
    
        
        
class changeWorkoutNameForm(ModelForm):
    
    class Meta: 
        model = Workout
        fields = ["name"]
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control fira-sans-light'


class trackWorkoutForm(forms.Form):
    
    def __init__(self, sets, *args, **kwargs):
        super().__init__(*args, **kwargs)

        reps_hit = []
        weight_hit = []        
        
        for set in sets:
            self.fields[str(set)] = forms.IntegerField(label=str(set), required=True)
            self.fields["weight"] = forms.IntegerField(required=True)
            
            reps_hit.append(forms.IntegerField(label=str(set), required=True))
            weight_hit.append(forms.IntegerField(required=True))
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control fira-sans-light'    
            

    
    
    pass