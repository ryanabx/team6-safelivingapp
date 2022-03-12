import { Component, OnInit} from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { empty } from 'rxjs';
import { AddrInputService } from '../addr-input.service';
import { AppService } from '../app.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit { 
  inputAddr: any;
  apiFile: any;
  locationData: any;
  lat: any;
  long: any;
  geoApiFile: any;
  latLongArray: any = [];
  cityNameArray: any = [];
  crimeScore: string | undefined;
  stateNameArray: any = [];

  emptySearch: boolean = false;

  searchSuggestions: any;
  formGroup: FormGroup = this.fb.group({'suggestions' : ['']});

  constructor(private route: ActivatedRoute,
  private appService: AppService,
  private addrInputService: AddrInputService, 
  private router: Router,
  private fb: FormBuilder) {}

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

  sendInput(value: string) {

    if (value == '') {
      return
    }

    this.inputAddr = value;
    //this.zillowLinks.push('https://www.zillow.com/homes/' + value + '_rb/');
    console.log(this.inputAddr);
    //this.addrInputService.setAddr(this.inputAddr);
    this.appService.callGeoApi(value).subscribe(
      (data: any) => {
        this.geoApiFile = data;
        this.locationData = this.geoApiFile.results[0].locations;
        console.log("original length: " + this.locationData.length)
        console.log(this.locationData)

        // iterate through returned location array
        for (let i = 0; i < this.locationData.length; i++) {

          console.log(this.locationData[i].adminArea1)
          // if location is not in US, remove
          if (this.locationData[i].adminArea1 != "US") {
            console.log("eliminated" + i)
            this.locationData.splice(i, 1);
            i--;
            console.log(this.locationData.length)
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
          this.cityNameArray = [this.locationData[0].adminArea5];
          this.stateNameArray = [this.locationData[0].adminArea3]

          this.router.navigate(['map'], {queryParams: {latLng : JSON.stringify(this.latLongArray), 
          city : JSON.stringify(this.cityNameArray), 
          state : JSON.stringify(this.stateNameArray), 
          addr : this.inputAddr}}).then(() => {this.crimeScore = "Loading... Please wait!";});
        }
        // else, flag to prompt user
        else {
          console.log("There's nothin' here boss")
          this.router.navigate(['home'], {queryParams: {emptySearch : true}})
        }
       
      },
      (err: any) => console.error(err),
      () => console.log('done loading coords : ' + this.addrInputService.getAddr() + " : " + this.geoApiFile)
    );
  }

  ngOnInit(): void {
    this.initForm()

    this.route.queryParams
    .subscribe(params => {
      this.emptySearch = params['emptySearch']
    })
    console.log(this.inputAddr)
  }

  sendToContact(): void {
    this.router.navigate(['contact'])
  }

}
