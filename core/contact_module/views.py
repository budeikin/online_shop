from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMessage


# Create your views here.
def contactus(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        content = request.POST['content']
        msg = subject + '\n' + email + '\n' + content
        message = EmailMessage(subject='contact', body=msg, from_email=email, to=('budeikin52@gmail.com',))
        message.send(fail_silently=False)

    return render(request, 'contact_module/contact_us.html')
