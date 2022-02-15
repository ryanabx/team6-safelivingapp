import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AddrInputService } from '../addr-input.service';
import { AppService } from '../app.service';
import { UserService } from '../user.service';

@Component({
  selector: 'app-user-bookmarks',
  templateUrl: './user-bookmarks.component.html',
  styleUrls: ['./user-bookmarks.component.css']
})
export class UserBookmarksComponent {

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

  bookmarks: any = []
  // bookmarks = [
  //   {
  //     address: "Tulsa, OK"
  //   }, 
  //   {
  //     address: "Broken Arrow, OK"
  //   },
  //   {
  //     address: "Kansas, OK"
  //   },
  // ];

  constructor(private appService: AppService,
    private addrInputService: AddrInputService, 
    private router: Router,
    private _userService: UserService) {
    // this._userService.username; <-- current logged-in user; null if none
    //this.bookmarks = this.appService.getBookmarks(this._userService.username);
    this.appService.getBookmarks(this._userService.username).subscribe(
      (data:any) => {
        this.bookmarks = data;
        // console.log(data);
      })
  }

  whatIsBookmark(value: number) {
    return this.bookmarks[value] ? this.bookmarks[value].address : null;
  }

  openBookmark(value: string) {

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
}
