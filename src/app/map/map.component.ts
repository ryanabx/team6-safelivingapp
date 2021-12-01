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
  locations: any = [];
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

  testPaths: any = [
    
    {lat: 30, lng: 30},
    {lat: 60, lng: 30},
    {lat: 60, lng: 60}

  ];

  labelOptions: any = {
    color: 'white',
    fontFamily: '',
    fontSize: '14px',
    fontWeight: 'bold',
    text: '2'
  };

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

    //TEMP CODE

    this.boundariesToPath("owasso", "oklahoma");


  }

  reveal() {
    console.log(this.crimeScoreArray)

  }

  boundariesToPath(city: any, state: any) {
    this.appService.getBoundaries(city, state).subscribe(
      (data:any) => {
        this.testPaths = data.results;
      }
    );
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
      // deprecated / depreciated
      //this.lat = params['lat'] ? (parseFloat(params['lat']) ? parseFloat(params['lat']) : 0) : 0;
      //this.long = params['long'] ? (parseFloat(params['long']) ? parseFloat(params['long']) : 0) : 0;
      
      this.inputAddr = params['addr']
      
      this.latLongArray = JSON.parse(params['latLng']); // accept the lat/long array for multiple locations
      console.log(this.latLongArray)

      this.cityNameArray = JSON.parse(params['city'])
      this.stateNameArray = JSON.parse(params['state'])

      /* deprecated / depreciated
      console.log(this.lat + " : " + this.long)
      if(this.lat != 0 && this.long != 0){
        this.appService.getSafeLivingScoreAPI(this.long, this.lat, 2.0).subscribe(
          (data: any)=>{
            this.crimeScore = data["safe-living-score"];
            this.crimeScore = parseFloat((Math.round(this.crimeScore * 100) / 100).toFixed(2));
          }
        );
        console.log(this.crimeScore);
      }*/

      // create the location objects for each lat/long pair
      // save their respective lat/long
      // add location to the array
      if (this.latLongArray != null) {
        for (let i = 0; i < this.latLongArray.length; i+=2) {
          let newLoc: Location = new Location()
          console.log(this.latLongArray[i], this.latLongArray[i+1])
          newLoc.setLatLong(this.latLongArray[i], this.latLongArray[i+1])
          this.locations.push(newLoc)
        }
      }

      // set the respective city and state name to each location in locations array
      if (this.cityNameArray != null || this.stateNameArray != null) {
        for (let i = 0; i < this.locations.length; i++) {
          this.locations[i].setCity(this.cityNameArray[i]);
          this.locations[i].setState(this.stateNameArray[i]);
        }
      }
      console.log("Locations initially created: " + this.locations)

      // if latLongArray is passed, find crimeScore for all the lat/long pairs in the array
      // save the crimeScore to each location it belongs to, done inside the call, so asynchronicity is no longer a problem
      if (this.latLongArray != null) {
        let tempCSArray: any[] = []
        for (let i = 0; i < this.locations.length; i++) {
          this.appService.getSafeLivingScoreAPI(this.locations[i].city, this.locations[i].state).subscribe(
            (data: any)=>{
              this.crimeScore = data["safe-living-score"];
              if(!isNaN(parseFloat(this.crimeScore))){
                this.crimeScore = parseFloat((Math.round(this.crimeScore * 100) / 100).toFixed(2));
              }
              this.locations[i].setCrimeScore(this.crimeScore);
              this.crimeScoreArray.push(this.crimeScore);
            }
          );
        }
        console.log(this.locations)
      }

      console.log(this.locations)
      console.log(this.locations[0].lat)
      
    })
  }
}

export class Location {

  public lat: number = 0;
  public long: number = 0;
  public crimeScore: string = "";
  public city: any;
  public state: any;
  public labelOptions: any = {
    color: 'white',
    fontFamily: '',
    fontSize: '14px',
    fontWeight: 'bold',
    text: '?'
  };
  public testPaths: any = [];

  constructor() {

  }

  setLatLong(lat: number, long: number) {
    this.lat = lat;
    this.long = long;
  }

  setCrimeScore(score: string) {
    //this.labelOptions.text = score;
    this.crimeScore = score;
  }

  setCity(city: any) {
    this.city = city;
  }

  setState(state: any) {
    this.state = state;
  }
}
