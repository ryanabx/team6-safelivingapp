from user.models import Bookmark
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

def addBookmark(request, user, address):
	print("addBookmark pinged")
	if Bookmark.objects.filter(user=user, address=address).exists():
		return JsonResponse({"user": user, "address": address, "new": False})
	bookmark = Bookmark(user=user, address=address)
	bookmark.save()

	print(bookmark)
	return JsonResponse({"user": user, "address": address, "new": True})

def getBookmarks(request, user):
	bookmarks = Bookmark.objects.filter(user=user)
	response = []
	for bm in serializers.serialize('python', bookmarks):
		address = bm["fields"]
		response.append(address)
	return JsonResponse(response, safe=False)

def delBookmark(request, user, address):
	if not Bookmark.objects.filter(user=user, address=address).exists():
		return JsonResponse({"user": user, "address": address, "deleted": False})
	bookmarks = Bookmark.objects.filter(user=user, address=address)
	for bookmark in bookmarks:
		bookmark.delete()
	return JsonResponse({"user": user, "address": address, "deleted": True})
