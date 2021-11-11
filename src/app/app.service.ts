import { Injectable } from '@angular/core';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Globals } from './globals';
import { analyzeAndValidateNgModules } from '@angular/compiler';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  data: any;
  globals : Globals;

  constructor(private http:HttpClient) {this.globals = new Globals();}

  callGeoApi(input:any): any {
    return this.http.get(this.globals.backendUrl + 'geocoding/api/' + input + "/"); //Make sure backend server is running to use this!
  }

  getSafeLivingScoreAPI(lat: any, lon: any, radius: any){
    return this.http.get("http://localhost:8000/safelivingscore/api/" + lon + "/" + lat + "/" + radius + "/");
  }

}
