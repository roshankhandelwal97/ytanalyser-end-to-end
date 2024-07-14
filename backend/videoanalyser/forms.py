from django import forms

class VideoQueryForm(forms.Form):
    youtube_url = forms.URLField(label='YouTube URL')
    question = forms.CharField(widget=forms.Textarea, label='Question')
