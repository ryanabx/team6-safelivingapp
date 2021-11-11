import { Injectable } from '@angular/core';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Globals } from './globals';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  globals : Globals;

  constructor(private http:HttpClient) {this.globals = new Globals();}

  callGeoApi(input:any): any {
    return this.http.get(this.globals.backendUrl + 'addrtoloc/api/' + input + "/"); //Make sure backend server is running to use this!
}
}
