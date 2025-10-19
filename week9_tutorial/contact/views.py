from django.http import HttpResponse
from django.shortcuts import render, redirect

from contact.forms import ContactForm

def contact_us(request):

    if request.method == "POST":
        # bind data to form
        form = ContactForm(request.POST)
        # validate data in the form
        if form.is_valid():
            # access cleaned_data
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            print("Subject", subject)
            print("Message", message)
            print("Sender", sender)
            print("CC myself?", cc_myself)

            # Assume that this view send email
            # recipients = ["info@example.com"]
            # if cc_myself:
            #     recipients.append(sender)

            # send_mail(subject, message, sender, recipients)

            # redirect to "thanks" page when the email has been sent
            return redirect("thanks")
    else:
        form = ContactForm()
    
    return render(request, "contact_us.html", {"form": form})

def thanks(request):
    return HttpResponse("THANKS!!!")