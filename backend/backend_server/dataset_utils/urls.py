from django.urls import path
from . import dataset_downloader

urlpatterns = [
    path('api/updatedataset/crime', dataset_downloader.download_newest_crime_data),
    path('api/updatedataset/scores', dataset_downloader.refresh_crime_scores),
    path('api/updatedataset/population', dataset_downloader.fix_population_dataset),
    
]