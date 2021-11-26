import { Component, Input, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { AddrInputService } from '../addr-input.service';
import { AppService } from '../app.service';

import { MapsAPILoader } from '@agm/core';
import { HttpClient } from '@angular/common/http';
//import { stringify } from 'querystring';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  lat: number;
  long: number;
  latLongArray: any = [];
  cityNameArray: any = [];
  stateNameArray: any = [];
  locations: any;
  radius: number;
  
  crimeScore: any;
  crimeScoreArray: any = [];

  zillowLinks: any = [];

  inputAddr: any;
  geoApiFile: any;
  locationData: any;
  state: any;
  county: any;
  city: any;

  weatherApiKey: any = "2883471b37ffc685d279ad06d302d7f5"
  weatherApiFile: any;
  weatherData: any = []

  censusEconDataFile: any;
  censusEconData: any;

  censusMedIncome: any;
  censusPovRate: any;
  censusPovCount: any;

  constructor(
    private route: ActivatedRoute,
    private appService: AppService,
    private addrInputService: AddrInputService, 
    private router: Router,
    private http: HttpClient) {
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    // Dietler Commons: 36.1522971, -95.9481072
    this.lat = 0;
    this.long = 0;
    this.radius = 5000

    this.crimeScore = "Loading... Please wait!";
    
  

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
  }

  sendInput(value: string) {

    if (value == '') {
      return
    }

    this.inputAddr = value;
    this.zillowLinks.push('https://www.zillow.com/homes/' + value + '_rb/');
    console.log(this.inputAddr);
    //this.addrInputService.setAddr(this.inputAddr);
    this.appService.callGeoApi(value).subscribe(
      (data: any) => {
        this.geoApiFile = data;
        this.locationData = this.geoApiFile.results[0].locations[0];
        console.log(this.locationData);
        this.latLongArray = [this.locationData.latLng.lat, this.locationData.latLng.lng]
        this.cityNameArray = [this.locationData.adminArea5];
        this.stateNameArray = [this.locationData.adminArea3]
        this.router.navigate(['map'], {queryParams: {latLng : JSON.stringify(this.latLongArray), 
        city : JSON.stringify(this.cityNameArray), 
        state : JSON.stringify(this.stateNameArray), 
        addr : this.inputAddr}}).then(() => {this.crimeScore = "Loading... Please wait!";});
      },
      (err: any) => console.error(err),
      () => console.log('done loading coords : ' + this.addrInputService.getAddr() + " : " + this.geoApiFile)
    );
  }

  addToInput(value: string) {

    if (value == '') {
      return
    }

    this.inputAddr += "|" + value;
    this.zillowLinks.push('https://www.zillow.com/homes/' + value + '_rb/');
    this.latLongArray = [];
    this.locations = [];
    this.cityNameArray = [];
    this.stateNameArray = []

    this.appService.callGeoApi(this.inputAddr).subscribe(
      (data: any) => {
        this.geoApiFile = data;
        this.locationData = this.geoApiFile.results
        console.log(this.locationData)
        for (let i = 0; i < this.locationData.length; i++) {
          this.latLongArray.push(this.locationData[i].locations[0].latLng.lat)
          this.latLongArray.push(this.locationData[i].locations[0].latLng.lng)
          this.cityNameArray.push(this.locationData[i].locations[0].adminArea5)
          this.stateNameArray.push(this.locationData[i].locations[0].adminArea3)
        }

        this.router.navigate(['map'], {queryParams: {latLng : JSON.stringify(this.latLongArray), 
          city : JSON.stringify(this.cityNameArray), 
          state : JSON.stringify(this.stateNameArray), 
          addr : this.inputAddr}}).then(() => {this.crimeScore = "Loading... Please wait!";});      },
      (err: any) => console.error(err),
      () => console.log()
    );
  }

  reveal() {
    console.log(this.crimeScoreArray)
  }

  // send an array of three addresses for the backend to process
  // need to configure backend to process either single or multiple inputs (shouldn't be too hard)
  // adds lat/long to an array as follows: [lat1, long1, lat2, long2, ..., lat{n}, long{n}]
  // for addresses in order of address 1, address 2, ..., address {n}
  threeAddressTest() {
    this.inputAddr = "tulsa, ok|denver, co|austin, tx";
    this.zillowLinks.push('https://www.zillow.com/homes/tulsa, ok_rb/');
    this.zillowLinks.push('https://www.zillow.com/homes/denver, co_rb/');
    this.zillowLinks.push('https://www.zillow.com/homes/austin, tx_rb/');
    this.latLongArray = [];
    this.locations = [];
    this.cityNameArray = [];
    this.stateNameArray = [];

    this.appService.callGeoApi(this.inputAddr).subscribe(
      (data: any) => {
        this.geoApiFile = data;
        this.locationData = this.geoApiFile.results
        console.log(this.locationData)
        for (let i = 0; i < this.locationData.length; i++) {
          this.latLongArray.push(this.locationData[i].locations[0].latLng.lat)
          this.latLongArray.push(this.locationData[i].locations[0].latLng.lng)
          this.cityNameArray.push(this.locationData[i].locations[0].adminArea5)
          this.stateNameArray.push(this.locationData[i].locations[0].adminArea3)
        }

        this.router.navigate(['map'], {queryParams: {latLng : JSON.stringify(this.latLongArray), 
          city : JSON.stringify(this.cityNameArray), 
          state : JSON.stringify(this.stateNameArray), 
          addr : this.inputAddr}}).then(() => {this.crimeScore = "Loading... Please wait!";});      },
      (err: any) => console.error(err),
      () => console.log()
    );
  }
                                                                                                                           
   zillowRoute(index: number){
    window.location.href = 'https://www.zillow.com/homes/' + this.locations[index].city + ',' + this.locations[index].state + '_rb/'
    //console.log(this.locations[index].city + ',' + this.locations[index].state)
  }


  ngOnInit(): void {
    this.route.queryParams
    .subscribe(params => {
      this.lat = params['lat'] ? (parseFloat(params['lat']) ? parseFloat(params['lat']) : 0) : 0;
      this.long = params['long'] ? (parseFloat(params['long']) ? parseFloat(params['long']) : 0) : 0;
      
      this.inputAddr = params['addr']
      
      this.latLongArray = JSON.parse(params['latLng']); // accept the lat/long array for multiple locations
      console.log(this.latLongArray)

      this.cityNameArray = JSON.parse(params['city'])
      this.stateNameArray = JSON.parse(params['state'])

      /*
      if(params['lat'] != parseFloat(params['lat']) || params['long'] != parseFloat(params['long']))
      {
        this.router.navigate(['map'], {queryParams: {lat : this.lat, long : this.long}});
      }*/
      console.log(this.lat + " : " + this.long)
      if(this.lat != 0 && this.long != 0){
        this.appService.getSafeLivingScoreAPI(this.long, this.lat, 1.0).subscribe(
          (data: any)=>{
            this.crimeScore = data["safe-living-score"];
            this.crimeScore = parseFloat((Math.round(this.crimeScore * 100) / 100).toFixed(2));
          }
        );
        console.log(this.crimeScore);
      }

      // if latLongArray is passed, find crimeScore for all the lat/long pairs in the array
      // save to a crime score array (should be in order of searched locations)
      if (this.latLongArray != null) {
        let tempCSArray: any[] = []
        for (let i = 0; i < this.latLongArray.length; i+=2) {
          this.appService.getSafeLivingScoreAPI(this.latLongArray[i], this.latLongArray[i+1], 1.0).subscribe(
            (data: any)=>{
              this.crimeScore = data["safe-living-score"];
              this.crimeScore = parseFloat((Math.round(this.crimeScore * 100) / 100).toFixed(2));
              tempCSArray.push(this.crimeScore);
            }
          );
        }
        this.crimeScoreArray = tempCSArray
        console.log(this.crimeScoreArray)
      }

      // add new location object based on number of returned coords
      let temp: any = []
      for (let i = 0; i < this.latLongArray.length; i+=2) {
        temp.push(new Location(this.latLongArray[i], this.latLongArray[i+1], this.crimeScoreArray[i/2], this.cityNameArray[i/2], this.stateNameArray[i/2]))
      }
      this.locations = temp
      console.log(this.locations)
      console.log(this.locations[0].lat)
      
    })
  }
}

export class Location {

  constructor(
    public lat: number,
    public long: number,
    public crimeScore: number,
    public city: any,
    public state: any) {

  }
}
