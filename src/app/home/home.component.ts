import { Component, OnInit } from '@angular/core';
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

  constructor(private route: ActivatedRoute,
  private appService: AppService,
  private addrInputService: AddrInputService, 
  private router: Router) {}


  sendInput(value: string) {
    this.inputAddr = value;
    console.log(this.inputAddr);
    this.addrInputService.setAddr(this.inputAddr);
    this.appService.callGeoApi(this.addrInputService.getAddr()).subscribe(
      (data: any) => {
      console.log(data);
      this.apiFile = data;
      this.locationData = this.apiFile.results[0].locations[0];
      this.lat = this.locationData.latLng.lat;
      this.long = this.locationData.latLng.lng;
      console.log(document.location.href);
      this.router.navigate(['map'], {queryParams: {lat : this.lat, long : this.long}}).then(() => {window.location.reload()});
      console.log("should route");
      },
      (err: any) => console.error(err),
      () => console.log('done loading coords : ' + this.addrInputService.getAddr() + " : " + this.apiFile)
    );
   }

  ngOnInit(): void {
    console.log(this.inputAddr)
  }

}
