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

  getSafeLivingScoreAPI(lat: any, lon: any, radius: any){
    return this.http.get(this.serverURL + "safelivingscore/api/" + lat + "/" + lon + "/" + radius + "/all/");
  }

  getCrimeScoreAPIByType(lat: any, lon: any, radius: any, crimeType: any){
    return this.http.get(this.serverURL + "safelivingscore/api/" + lat + "/" + lon + "/" + radius + "/" + crimeType + "/");
  }

  getCrimeAPI(ORI: any, fromDate: any, toDate: any){
    return this.http.get(this.serverURL + "crimedata/api/" + ORI + "/" + fromDate + "/" + toDate);
  }

  getAmenitiesAPI(lat: any, lon: any, radius: any){
    return this.http.get(this.serverURL + "amenities/api/" + lat + "/" + lon + "/" + radius);
  }

  getWalkScoreAPI(lat: any, lon: any){
    return this.http.get(this.serverURL + "transportation/api/walkscore/" + lat + "/" + lon);
  }

}
