import { Component, OnInit} from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
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

  constructor(private route: ActivatedRoute,
  private appService: AppService,
  private addrInputService: AddrInputService, 
  private router: Router) {}


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

  ngOnInit(): void {
    console.log(this.inputAddr)
  }

  sendToContact(): void {
    this.router.navigate(['contact'])
  }

}
