import { Injectable } from '@angular/core';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { Observable } from 'rxjs';
import { analyzeAndValidateNgModules } from '@angular/compiler';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  data: any;
  
  serverURL = 'http://localhost:8000/';

  constructor(private http:HttpClient) {}

  /*
  MAKE SURE THE BACKEND SERVER IS RUNNING IN ORDER FOR THESE FUNCTION CALLS TO WORK!
  ALSO PAY ATTENTION TO backend/BACKEND_API.md FOR AN EXAMPLE OF DATA RETURNED FOR EACH API!
  */
  callGeoApi(input:any): any {
    return this.http.get(this.serverURL + 'geocoding/api/' + input + "/"); 
  }

  getSafeLivingScoreAPI(city: any, state: any){
    return this.http.get(this.serverURL + "safelivingscore/api/" + city + "/" + state + "/");
  }

  getCrimeScoreAPIByType(city: any, state: any, crimeType: any){
    return this.http.get(this.serverURL + "safelivingscore/api/" + city + "/" + state + "/" + crimeType + "/");
  }

  getCrimeAPI(ORI: any, fromDate: any, toDate: any){
    return this.http.get(this.serverURL + "crimedata/api/" + ORI + "/" + fromDate + "/" + toDate + "/");
  }

  getAmenitiesAPI(lat: any, lon: any, radius: any){
    return this.http.get(this.serverURL + "amenities/api/" + lat + "/" + lon + "/" + radius + "/");
  }

  getWalkScoreAPI(lat: any, lon: any){
    return this.http.get(this.serverURL + "transportation/api/walkscore/" + lat + "/" + lon + "/");
  }

  getBoundaries(city: any, state: any) {
    return this.http.get(this.serverURL + "boundaries/api/" + city + "/" + state + "/");
  }

  getCostOfLiving(city: any, state: any) {
    return this.http.get(this.serverURL + "costofliving/api/" + city + "/" + state + "/");
  }

  getBookmarks(user: any) {
    return this.http.get(this.serverURL + "user/api/get_bookmarks/" + user + "/");
  }

  addBookmark(user: any, address: any) {
    return this.http.get(this.serverURL + "user/api/add_bookmark/" + user + "/" + address + "/");
  }

  delBookmark(user: any, address: any) {
    return this.http.get(this.serverURL + "user/api/del_bookmark/" + user + "/" + address + "/");
  }

  submitReview(city: any, state: any, rating: any, text: any) {
    return this.http.get(this.serverURL + "reviews/api/submitReview/" + city + "/" + state + "/ " + rating + "/" + text + "/ ")
  }

  getReview(city: any, state: any) {
    return this.http.get(this.serverURL + "reviews/api/getReview/" + city + "/" + state + "/ ")
  }

  getAvgRating(city: any, state: any) {
    return this.http.get(this.serverURL + "reviews/api/getAvgRating/" + city + "/" + state + "/ ")
  }

  getSearchSuggestions(currentInput: any) {
    return this.http.get(this.serverURL + "datasets/api/get/searchsuggestions/" + currentInput + "/")
  }
}
