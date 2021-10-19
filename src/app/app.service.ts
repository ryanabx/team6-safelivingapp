import { Injectable } from '@angular/core';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  constructor(private http:HttpClient) { }

  private apiKey: string = 'c7qYTGBjRaRkGF7ucqOvpNy6L1Q857oD'

  callGeoApi(input:any): any {
    return this.http.get('http://www.mapquestapi.com/geocoding/v1/address?key=' + this.apiKey + '&location=' + input);
}
}
