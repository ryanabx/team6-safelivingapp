import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { AddrInputService } from '../addr-input.service';
import { AppService } from '../app.service';

import { MapsAPILoader } from '@agm/core';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  lat: number;
  long: number;
  radius: number;

  zillowLink = ''

  inputAddr: any;
  apiFile: any;
  locationData: any;

  constructor(
    private route: ActivatedRoute,
    private appService: AppService,
    private addrInputService: AddrInputService, 
    private router: Router) {
    // Dietler Commons: 36.1522971, -95.9481072
    this.lat = 0;
    this.long = 0;
    this.radius = 5000;

    //private mapsAPILoader: MapsAPILoader;

  }

  sendInput(value: string) {
    this.inputAddr = value;
    this.zillowLink = 'https://www.zillow.com/homes/' + this.inputAddr + '_rb/';
    console.log(this.inputAddr);
    this.addrInputService.setAddr(this.inputAddr);
    this.appService.callGeoApi(this.addrInputService.getAddr()).subscribe(
      (data: any) => {this.apiFile = data
      this.locationData = this.apiFile.results[0].locations[0]
      console.log(this.locationData)
      this.lat = this.locationData.latLng.lat
      this.long = this.locationData.latLng.lng
      this.router.navigate(['map'], {queryParams: {lat : this.lat, long : this.long}});
      },
      (err: any) => console.error(err),
      () => console.log('done loading coords : ' + this.addrInputService.getAddr() + " : " + this.apiFile)
    );
   }

   zillowRoute(){
    window.location.href = this.zillowLink;
  }

  ngOnInit(): void {
    this.route.queryParams
    .subscribe(params => {
      this.lat = params['lat'] ? (parseFloat(params['lat']) ? parseFloat(params['lat']) : 0) : 0;
      this.long = params['long'] ? (parseFloat(params['long']) ? parseFloat(params['long']) : 0) : 0;
      if(params['lat'] != parseFloat(params['lat']) || params['long'] != parseFloat(params['long']))
      {
        this.router.navigate(['map'], {queryParams: {lat : this.lat, long : this.long}});
      }
      console.log(this.lat + " : " + this.long)
    })
  }
}
