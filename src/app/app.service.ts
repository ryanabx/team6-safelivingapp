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
    console.log("calling geo api");
    this.data = this.http.get(this.globals.backendUrl + 'geocoding/api/' + input + "/");
    console.log(this.data);
    return this; //Make sure backend server is running to use this!
}
}
