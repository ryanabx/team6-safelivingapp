import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { AddrInputService } from '../addr-input.service';
import { AppService } from '../app.service';

import { MapsAPILoader } from '@agm/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  lat: number;
  long: number;
  radius: number;
  crimeData: number;
  crimeScore: number;

  zillowLink = ''

  inputAddr: any;
  geoApiFile: any;
  locationData: any;
  state: any;
  county: any;
  city: any;

  weatherApiKey: any = "2883471b37ffc685d279ad06d302d7f5"
  weatherApiFile: any;
  weatherData: any = []

  censusEconDataFile: any = []
  censusEconData: any = []
  censusMedIncome: any;
  censusPovRate: any;
  censusPovCount: any;

  // yearly weather values
  avgTemp: any;
  maxTemp: any;
  minTemp: any;

  avgWind: any;
  
  avgPrecip: any;




  

  constructor(
    private route: ActivatedRoute,
    private appService: AppService,
    private addrInputService: AddrInputService, 
    private router: Router,
    private http: HttpClient) {
    // Dietler Commons: 36.1522971, -95.9481072
    this.lat = 0;
    this.long = 0;
    this.radius = 5000;
    this.crimeData = -1;
    this.crimeScore = 0;

  

    //private mapsAPILoader: MapsAPILoader;

    // poverty and income api
    this.http.get("http://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEPOVALL_PT,SAEPOVRTALL_PT&GEOID=40143&YEAR=2019").toPromise().then(data =>{
      console.log("Heres the data");
      console.log(data);
      this.censusEconDataFile = data
      this.censusEconData = this.censusEconDataFile[1]
      this.censusMedIncome = this.censusEconData[1]
      this.censusPovCount = this.censusEconData[2]
      this.censusPovRate = this.censusEconData[3]
    });

    /*
    // Weather data api call
    this.http.get("https://history.openweathermap.org/data/2.5/aggregated/year?lat=" + 36 + "&lon=" + -96 + "&appid=" + this.weatherApiKey).toPromise().then(data =>{
      console.log(data);
      this.weatherApiFile = data
      this.weatherData = this.weatherApiFile.result

      for (let i = 0; i < this.weatherData.length; i++){
        // temperatures returned in kelvin, need to convert to fahrenheit
        this.avgTemp += this.weatherData[i].temp.mean
        this.maxTemp += this.weatherData[i].temp.average_max
        this.minTemp += this.weatherData[i].temp.average_min

        // wind speeds returned in m/s, need to convert to mph
        this.avgWind += this.weatherData[i].wind.mean

        // precipitation returned in mm, need to convert to inches
        this.avgTemp += this.weatherData[i].precipitation.mean
      }

      // calculate the average from the data points
      this.avgTemp = this.avgTemp / this.weatherData.length
      this.maxTemp = this.maxTemp / this.weatherData.length
      this.minTemp = this.minTemp / this.weatherData.length

      this.avgWind = this.avgWind / this.weatherData.length

      this.avgPrecip = this.avgPrecip / this.weatherData.length

      // perform conversions
      this.avgTemp = ((this.avgTemp - 273.15) * 9/5) + 32   // kelvin to Fahrenheit
      this.maxTemp = ((this.maxTemp - 273.15) * 9/5) + 32
      this.minTemp = ((this.minTemp - 273.15) * 9/5) + 32

      this.avgWind = this.avgWind * 2.237                   // m/s to mph

      this.avgPrecip = this.avgPrecip / 25.4                // mm to in
    })*/


  }

  sendInput(value: string) {
    this.inputAddr = value;
    // this.zillowLink = 'https://www.zillow.com/homes/' + this.inputAddr + '_rb/';
    console.log(this.inputAddr);
    this.addrInputService.setAddr(this.inputAddr);
    this.appService.callGeoApi(this.addrInputService.getAddr()).subscribe(
      (data: any) => {
        console.log("hi i'm here");
        this.geoApiFile = data;
        this.locationData = this.geoApiFile.results[0].locations[0];
        console.log(this.locationData);
        this.lat = this.locationData.latLng.lat;
        this.long = this.locationData.latLng.lng;
        this.state = this.locationData.adminArea3;
        this.county = this.locationData.adminArea4;
        this.city = this.locationData.adminArea5;
        this.router.navigate(['map'], {queryParams: {lat : this.lat, long : this.long}});
      },
      (err: any) => console.error(err),
      () => console.log('done loading coords : ' + this.addrInputService.getAddr() + " : " + this.geoApiFile)
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
