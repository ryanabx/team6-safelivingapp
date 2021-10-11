import { HttpClient, HttpHandler } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { AppComponent } from '../app.component';
import { AppService } from '../app.service';
import { Observable } from 'rxjs';
import { AddrInputService } from '../addr-input.service';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-coord-list',
  templateUrl: './coord-list.component.html',
  styleUrls: ['./coord-list.component.css']
})



export class CoordListComponent implements OnInit{
  navigationSubscription: any;

  constructor (
  private appService: AppService, 
  private addrInputService: AddrInputService, 
  private router: Router) {
    this.navigationSubscription = this.router.events.subscribe((e: any) => {
      // If it is a NavigationEnd event re-initalise the component
      if (e instanceof NavigationEnd) {
        this.reloadComponent();
      }
    });
  }
  
 

 

  // input string containing address
  public input: any = <string>this.addrInputService.getAddr();
  // storage of api call from appService subscription as a JSON object
  public apiFile: any;
  // storage of the location results as an array
  public locationData: any;
  // latitude
  public latitude: any;
  // longitude
  public longitude: any;

  reloadComponent() {
    this.ngOnInit();
  }

  // function uses appService to call api and addrInputService to take input from
  // search bar of app component to pass to api call. Uses set apiFile to json file
  // returned from api, then parses json file to get the location data separately.
  // Ultimately saves lat and long (can be modified to save more from location data),
  // but must do so inside the subsciption call, as data assignment happens asynchronously
  getCoords() {
    this.appService.callGeoApi(this.addrInputService.getAddr()).subscribe(
      (data: any) => {this.apiFile = data
      this.locationData = this.apiFile.results[0].locations[0]
      this.latitude = this.locationData.latLng.lat
      this.longitude = this.locationData.latLng.lng
      },
      (err: any) => console.error(err),
      () => console.log('done loading coords : ' + this.addrInputService.getAddr() + " : " + this.apiFile)
    );

  }

  ngOnInit(): void {
    this.getCoords();
  }

}
