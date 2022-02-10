from django.shortcuts import render
from reviews.models import Review
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers


# enter a review into the db of [city, state, rating, and text(comments)]
def submitReview(request, city, state, rating, text):

    rating = int(rating)

    # check if each field is the appropriate type before saving to DB
    if (isinstance(city, str) and isinstance(city, str) and isinstance(rating, int) and isinstance(text, str)):
        review = Review(city = city, state = state, rating = rating, text = text)
        review.save()

         # debug statements for a sent review
        print("Sent Review for City: " + city)
        print("In the state of: " + state)
        print("With a rating of: " + str(rating))
        print("And additional text: " + text)
        return JsonResponse({"city": city, "state": state, "rating": rating, "text": text, "success": True})
    else:
        print ("incorrect data type for a field(s)")
        return JsonResponse({"city": city, "state": state, "rating": rating, "text": text, "success": False})

# retrieve all reviews from db that corresponds to the [city, state]
def getReview(request, city, state):

    # debug statement for retrieving review
    print("Retrieving Reviews for: " + city + ", " + state)

    # filter DB based on city, state searched
    relevant = Review.objects.filter(city=city, state=state)
    response = []
    for r in serializers.serialize('python', relevant):
        something = r['fields']
        print (something)
        response.append(something)
    return JsonResponse(response, safe=False)



    

