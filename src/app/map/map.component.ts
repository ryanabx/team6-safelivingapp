import { AfterViewInit, Component, Input, OnInit, SystemJsNgModuleLoader } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { AddrInputService } from '../addr-input.service';
import { AppService } from '../app.service';

import { MapsAPILoader } from '@agm/core';
import { HttpClient } from '@angular/common/http';
import { UserService } from '../user.service';
import { analyzeAndValidateNgModules } from '@angular/compiler';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// import { stringify } from 'querystring';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit, OnInit {

  // star rating
  surveySubmitted = false;
  max = 5;
  rate = 0;
  comment: any;
  avgRating = 0;
  isReadonly = false;

  // recommendation
  radiusValue = 100; 
  minPop = 0;
  maxPop = 10000000000;
  scoreCat = "safe-living";
  
  lat: number;
  long: number;
  latLongArray: any = [];
  cityNameArray: any = [];
  stateNameArray: any = [];
  locations: any = [];
  radius: number;

  centerLat: number = 39.8283;
  centerLong: number = -98.5795;
  mapZoom: number = 3;

  bookmarked: boolean = false;
  emptySearch: boolean = false;
  
  crimeScore: any;
  crimeScoreArray: any = [];

  errorCode: any;
  errorMessage: any;

  zillowLinks: any = [];

  inputAddr: any;
  geoApiFile: any;
  locationData: any;

  formGroup: FormGroup = this.fb.group({'suggestions' : ['']});
  searchSuggestions: any = [];

  weatherApiKey: any = "2883471b37ffc685d279ad06d302d7f5";
  weatherApiFile: any;
  weatherData: any = [];

  censusEconDataFile: any;
  censusEconData: any;

  censusMedIncome: any;
  censusPovRate: any;
  censusPovCount: any;

  recForm: FormGroup;
  maxSizeForm: FormGroup;
  minSizeForm: FormGroup;
  radForm: FormGroup;

  testPaths: any = [
    
    { lat: 30, lng: 30 },
    { lat: 60, lng: 30 },
    { lat: 60, lng: 60 }

  ];

  // testGeoJson: any;

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
    private http: HttpClient,
    private fb: FormBuilder,
    public _userService: UserService) {
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      // Dietler Commons: 36.1522971, -95.9481072
      this.lat = 0;
      this.long = 0;
      this.radius = 5000

      this.crimeScore = "Loading... Please wait!";

      this.recForm = fb.group({
        recPriority: ['safe-living', Validators.required]
      });

      this.maxSizeForm = fb.group({
        maxSize: ['10000000000', Validators.required]
      });

      this.minSizeForm = fb.group({
        minSize: ['0', Validators.required]
      });

      this.radForm = fb.group({
        radSize: ['100', Validators.required]
      });
      

      // private mapsAPILoader: MapsAPILoader;
      

      // poverty and income api
      // this.http.get("http://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEMHI_PT,SAEPOVALL_PT,SAEPOVRTALL_PT&GEOID=40143&YEAR=2019").toPromise().then(data => {
      //   console.log("Heres the data");
      //   console.log(data);
      //   this.censusEconDataFile = data
      //   this.censusEconData = this.censusEconDataFile[1]
      //   this.censusMedIncome = this.censusEconData[1]
      //   this.censusPovCount = this.censusEconData[2]
      //   this.censusPovRate = this.censusEconData[3]
      // });
  }

  // intialize Angular Material Form to track user input as they type
  // if they type more than 3 chars, take that input, call the search 
  // suggestions dataset util, and save the returning array to be loaded
  // for displaying suggestions in the autocomplete box.
  initForm() {
    console.log(this.formGroup)
    this.formGroup.get('suggestions')?.valueChanges.subscribe(
      (data) => {
        console.log(data);
        if (data.length >= 3) {
          ///console.log("it's more than 3!")
          this.getSuggestions(data)
        }
      }
      )
  }

  // method that takes input string, sends it to search suggestions
  // dataset util, and returns an array of cities that contain that
  // string 
  getSuggestions(currentInput: any) {
    console.log(currentInput)
      this.appService.getSearchSuggestions(currentInput).subscribe(
        (data: any) => {
          this.searchSuggestions = data.result;
          console.log(data)
        }
      )
    
  }

  amIBookmarked(bookmarks: any): boolean {
    let addr = this.inputAddr;
    for(let i = 0; i < bookmarks.length; i++)
    {
      let bookmark = bookmarks[i];
      if(bookmark.address == addr) {
        this.bookmarked = true;
        return true;
      }
    }
    this.bookmarked = false;
    return false;
  }

  addBookmark() {
    this.appService.addBookmark(this._userService.username, this.inputAddr).subscribe();
    this.bookmarked = !this.bookmarked;
  }

  delBookmark() {
    this.appService.delBookmark(this._userService.username, this.inputAddr).subscribe();
    this.bookmarked = !this.bookmarked;
  }

  sendInput(value: string) {

    if (value == '') {
      return
    }

    this.inputAddr = value;
    this.zillowLinks.push('https://www.zillow.com/homes/' + value + '_rb/');
    console.log(this.inputAddr);

    this.cityNameArray = [this.inputAddr.split(",")[0]];
    this.stateNameArray = [this.inputAddr.split(", ")[1]];

    console.log("CITY: [" + this.cityNameArray + "] State: [" + this.stateNameArray + "]");
    // this.addrInputService.setAddr(this.inputAddr);
    this.appService.callGeoApi(value).subscribe(
      (data: any) => {
        this.geoApiFile = data;
        this.locationData = this.geoApiFile.results[0].locations;

        // iterate through returned location array
        for (let i = 0; i < this.locationData.length; i++) {

          // if location is not in US, remove
          if (this.locationData[i].adminArea1 != "US") {
            this.locationData.splice(i, 1);
            i--;
          }
        }
        console.log("Here's the Locations:")
        //console.log(this.locationData);
        console.log(this.geoApiFile);

        console.log("Here's the Locations after removing non-us places:")
        //console.log(this.locationData);
        console.log(this.locationData);

        // check if there is anything left in array, if so, initiate search 
        if (this.locationData.length > 0) {
          console.log("There's a valid, US, address here")
          this.latLongArray = [this.locationData[0].latLng.lat, this.locationData[0].latLng.lng]
          // this.cityNameArray = [this.locationData[0].adminArea5];
          // this.stateNameArray = [this.locationData[0].adminArea3]

          var city_result = JSON.stringify(this.cityNameArray);

          if(city_result === "St Louis"){
            city_result = "St. Louis";
          }

          this.router.navigate(['map'], {queryParams: {latLng : JSON.stringify(this.latLongArray), 
          city : city_result, 
          state : JSON.stringify(this.stateNameArray), 
          addr : this.inputAddr}}).then(() => {this.crimeScore = "Loading... Please wait!";});
        }
        // else, flag to prompt user
        else {
          console.log("There's nothin' here boss")
          this.router.navigate(['map'], {queryParams: {emptySearch : true}})
        }
      },
      // (err: any) => console.error(err),
      () => console.log('done loading coords : ' + this.addrInputService.getAddr() + " : " + this.geoApiFile)
    );
  }

  addToInput(value: string) {
    console.log("called")
    if (value == '') {
      return
    }

    this.inputAddr += "|" + value;
    var inputAddresses = this.inputAddr.split("|");
    this.zillowLinks.push('https://www.zillow.com/homes/' + value + '_rb/');
    this.latLongArray = [];
    this.locations = [];
    this.cityNameArray = [];
    this.stateNameArray = []
    console.log("inputaddr: " + this.inputAddr)

    this.appService.callGeoApi(this.inputAddr).subscribe(
      (data: any) => {
        this.geoApiFile = data;
        console.log(this.geoApiFile)
        this.locationData = this.geoApiFile.results
        console.log("before doing anything" + this.locationData)
        /*
        // iterate through returned location array
        for (let i = 0; i < this.locationData.length; i++) {

          // if location is not in US, remove
          if (this.locationData[i].adminArea1 != "US") {
            let removed = this.locationData.splice(i, 1);
            console.log("Current Location: " + this.locationData[i])
            console.log("removed:" + removed)
            i--;
          }
        }*/
        console.log("Here's the Locations:")
        //console.log(this.locationData);
        console.log(this.geoApiFile);

        console.log("Here's the Locations after removing non-us places:")
        //console.log(this.locationData);
        console.log(this.locationData);

        // check if there is anything left in array, if so, initiate search 
        if (this.locationData.length > 0) {
          console.log("There's a valid, US, address here")
          for (let i = 0; i < this.locationData.length; i++) {
            this.latLongArray.push(this.locationData[i].locations[0].latLng.lat)
            this.latLongArray.push(this.locationData[i].locations[0].latLng.lng)
            this.cityNameArray.push(inputAddresses[i].split(",")[0])
            this.stateNameArray.push(inputAddresses[i].split(", ")[1])
          }

          this.router.navigate(['map'], {queryParams: {latLng : JSON.stringify(this.latLongArray), 
          city : JSON.stringify(this.cityNameArray), 
          state : JSON.stringify(this.stateNameArray), 
          addr : this.inputAddr}}).then(() => {this.crimeScore = "Loading... Please wait!";});
        }
        // else, flag to prompt user
        else {
          console.log("There's nothin' here boss")
          /*this.router.navigate(['map'], {queryParams: {emptySearch : true}})*/
        } 
      },
      (err: any) => console.error(err),
      () => console.log()
    );

    // TEMP CODE
    // this.boundariesToPath("owasso", "oklahoma");


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
        console.log("Here's the location data:")
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
      // (err: any) => console.error(err),
      () => console.log()
    );
  }
                                                                                                                           
   zillowRoute(index: number) {
    window.location.href = 'https://www.zillow.com/homes/' + this.locations[index].city + ',' + this.locations[index].state + '_rb/'
    // console.log(this.locations[index].city + ',' + this.locations[index].state)
  }

  submitReview(city: any, state: any) {
    if(this.rate != 0 && city && state)
    {
      this.surveySubmitted = true;
      this.appService.submitReview(city, state, this.rate, this.comment).subscribe(
        (data:any) => {
          console.log(data.success)
        }
      );
    }
  }

  // call in html for recommendation func using filters
  recommendCity(location: any, rad: any, min: any, max: any, category: any) {
      this.appService.recommendCity(location.city, rad, min, max, category).subscribe(
        (data: any) => {
          console.log("Data Under Here: \n");
          console.log(data);

          var recList: any[][] = new Array()
          for(let j=0; j < data["cityPairs"].length; j++) {
            recList.push(["a", 1]);
          }
          for(let x=0; x < data["cityPairs"].length; x++)
          {
            recList[x][0] = (data["cityPairs"][x][0]["city"]);
            recList[x][1] = (data["cityPairs"][x][1]);
          }
          // console.log(recList);
          location.recommendations = recList;
          // this.locations.setRecommendations(recList)
        }
      );
  }






  parsePathData(path: any) {

    let parsedData : any = [];

    for(let idx = 0; idx < path.length; idx++) {
      parsedData.push( { lat: path[idx][1], lng: path[idx][0] } );
    }
    console.log(parsedData);
    return parsedData;

  }

  getBookmarks() {
    this.appService.getBookmarks(this._userService.username).subscribe(
      (data: any) => {
        this.amIBookmarked(data);
      });
  }

  ngAfterViewInit(): void {
    this.getBookmarks();
  }

  ngOnInit(): void {
    this.route.queryParams
    .subscribe(params => {
      // deprecated / depreciated
      // this.lat = params['lat'] ? (parseFloat(params['lat']) ? parseFloat(params['lat']) : 0) : 0;
      // this.long = params['long'] ? (parseFloat(params['long']) ? parseFloat(params['long']) : 0) : 0;
      
      this.initForm();

      this.inputAddr = params['addr']
      this.emptySearch = params['emptySearch']
      
      this.latLongArray = JSON.parse(params['latLng']); // accept the lat/long array for multiple locations
      console.log(this.latLongArray)

      this.cityNameArray = JSON.parse(params['city'])
      this.stateNameArray = JSON.parse(params['state'])

      for (var i = 0; i < this.cityNameArray.length; i++){
        if (this.cityNameArray[i] === "St Louis"){
          this.cityNameArray[i] = "St. Louis";
        }
      }

      // create the location objects for each lat/long pair
      // save their respective lat/long
      // add location to the array
      if (this.latLongArray != null) {
        for (let i = 0; i < this.latLongArray.length; i+=2) {
          let newLoc: Location = new Location()
          console.log(this.latLongArray[i], this.latLongArray[i+1])
          newLoc.setLatLong(this.latLongArray[i], this.latLongArray[i+1])
          this.locations.push(newLoc)

          // Set map params
          if(i == 0) {
            this.centerLat=this.latLongArray[i];
            this.centerLong=this.latLongArray[i+1];
            this.mapZoom=10;
          } else {
            this.centerLat = 39.8283;
            this.centerLong = -98.5795;
            this.mapZoom = 3;
          }

        }
      }

      // set the respective variables to each location in locations array
      if (this.cityNameArray != null || this.stateNameArray != null) {
        for (let i = 0; i < this.locations.length; i++) {
          this.locations[i].setCity(this.cityNameArray[i]);
          this.locations[i].setState(this.stateNameArray[i]);

          this.appService.getBoundaries(this.cityNameArray[i], this.stateNameArray[i]).subscribe(
            (data: any) => {
              this.locations[i].setPath(this.parsePathData(data));
              // this.testGeoJson = data;
              console.log(data);
            }
          )

          this.appService.getCostOfLiving(this.cityNameArray[i], this.stateNameArray[i]).subscribe(
            (data: any) => {
              this.locations[i].setCostOfLiving(data.prices);
              console.log(data.prices);
            }
          )

          this.appService.getAvgRating(this.cityNameArray[i], this.stateNameArray[i]).subscribe(
            (data: any) => {
              console.log(data);
              this.avgRating = Math.ceil(data * 100) / 100;
            },
          );

          // for each location, collect all reviews from the backend that pertain to it
          this.appService.getReview(this.cityNameArray[i], this.stateNameArray[i]).subscribe(
            (data: any) => {
              console.log("got here")

              // save them into its location object
              this.locations[i].setReviews(data);
              console.log("Review(s) Returned: " + data);
            }
          )

          //recommendation
          this.appService.recommendCity(this.locations[i].city, this.radiusValue, this.minPop, this.maxPop, this.scoreCat).subscribe(
            (data: any) => {
              console.log("Data Under Here: \n")
              console.log(data)

              /*console.log("City Name Here:")
              console.log(data["cityPairs"][0][0]["city"]);

              console.log("Score Name Here:");
              console.log(data["cityPairs"][0][1]);*/

              var recList:any[][] = new Array()
              for(let j=0; j < data["cityPairs"].length; j++){
                recList.push(["a",1])
              }
              for(let x=0; x < data["cityPairs"].length; x++)
                {
                  recList[x][0] = (data["cityPairs"][x][0]["city"])
                  recList[x][1] = (data["cityPairs"][x][1])
                }
              console.log(recList)
              this.locations[i].setRecommendations(recList)
            }
          )

          // placeholder for method call to backend for projected score
          /*
          this.appService.getProjectedCrimeScore(this.cityNameArray[i], this.stateNameArray[i]).subscribe(
            (data: any) => {
              this.locations[i].setProjectedScore(data);
            }
          )
          
          
          
          */ 

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
              this.errorCode = data["error_code"];
              this.errorMessage = data["error_message"];
              if(!isNaN(parseFloat(this.crimeScore))){
                this.crimeScore = parseFloat((Math.round(this.crimeScore * 100) / 100).toFixed(2));
              }
              if(!isNaN(parseFloat(this.crimeScore))){
                this.projectedScore = data["projected_score"];
                console.log("Projected score: " + data["projected_score"])
              }
              this.locations[i].setCrimeScore(this.crimeScore);
              this.locations[i].setErrorCode(this.errorCode, this.errorMessage);
              this.locations[i].setProjectedScore(this.projectedScore);
              console.log("Error code: " + this.errorCode + "| Error message: " + this.errorMessage);
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
  public projectedScore: string = "-1";
}



export class Location {

  public lat: number = 0;
  public long: number = 0;
  public crimeScore: string = "Loading... Please Wait :)";
  public projectedScore: string = "-1";
  public city: any;
  public state: any;
  public errorCode: any;
  public errorMessage: any;
  public costOfLiving: any = {
    salary: '',
    apartmentLow: '',
    apartmentHigh: '',
    gas: ''
  };
  public reviews: any;
  public recommendations: any;
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

  setErrorCode(errorCode: any, errorMessage: any){
    this.errorCode = errorCode;
    this.errorMessage = errorMessage;
  }

  setCrimeScore(score: string) {
    this.labelOptions.text = score;
    this.crimeScore = score;
  }

  setCity(city: any) {
    this.city = city;
  }

  setState(state: any) {
    this.state = state;
  }

  setPath(path: any){
    this.testPaths = path;
  }

  // called to save the returned array of json objects containing the reviews
  // reminder, the format of a returned review is {"city": city, "state": state, "rating": rating, "text": text/comments}
  setReviews(reviews: any) { 
    this.reviews = reviews;
  }

  setRecommendations(recommendations: any) { 
    this.recommendations = recommendations;
  }

  setProjectedScore(score: any) {
    this.projectedScore = score;
  }

  setCostOfLiving(col: any) {
    
    let i = 0;
    while (col != null && i < col.length) {
      console.log("this is the " + i + "th time in the loop")

      // check if it's for monthly salary
      if (col[i].item_name === "Average Monthly Net Salary (After Tax), Salaries And Financing") {
        this.costOfLiving.salary = parseFloat(col[i].average_price).toFixed(2).toString();
      }

      // check if it's for apartment rent (low)
      else if (col[i].item_name ===  "Apartment (1 bedroom) Outside of Centre, Rent Per Month") {
        this.costOfLiving.apartmentLow = parseFloat(col[i].average_price).toFixed(2).toString();
      }

      // check if it's for apartment rent (high)
      else if (col[i].item_name ===  "Apartment (3 bedrooms) in City Centre, Rent Per Month") {
        this.costOfLiving.apartmentHigh = parseFloat(col[i].average_price).toFixed(2).toString();
      }

      // check if it's for gasoline prices
      else if (col[i].item_name === "Gasoline (1 liter), Transportation") {
        // need to multiply by 3.78541 to convert Liters (not 'litres'), to gallons of gas.
        // console.log(col[i].item_name)
        // console.log(col[i].average_price)
        this.costOfLiving.gas = (parseFloat(col[i].average_price) * 3.78541).toFixed(2).toString();
      }

      i++;
    }

    if (this.costOfLiving.salary === '') {
      this.costOfLiving.salary = "No Data"
    }
    if (this.costOfLiving.apartmentLow === '') {
      this.costOfLiving.apartmentLow = "No Data"
    }
    if (this.costOfLiving.apartmentHigh === '') {
      this.costOfLiving.apartmentHigh = "No Data"
    }
    if (this.costOfLiving.gas === '') {
      this.costOfLiving.gas = "No Data"
    }
  }
}
