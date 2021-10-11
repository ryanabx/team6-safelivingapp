import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  lat: number;
  long: number;

  constructor(private route: ActivatedRoute) {
    // Dietler Commons: 36.1522971, -95.9481072
    this.lat = 0;
    this.long = 0;
  }

  ngOnInit(): void {
    this.route.queryParams
    .subscribe(params => {
      this.lat = params['lat'] ? parseFloat(params['lat']) : 0;
      this.long = params['long'] ? parseFloat(params['long']) : 0;
      console.log(this.lat + " : " + this.long)
    })
  }
}
