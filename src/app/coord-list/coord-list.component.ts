import { Component, Input, OnInit } from '@angular/core';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-coord-list',
  templateUrl: './coord-list.component.html',
  styleUrls: ['./coord-list.component.css']
})

//@Input('childToMaster' masterName: "app")

export class CoordListComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
