import { Component, ElementRef, Inject, Injectable, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AppService } from './app.service';
import { AddrInputService } from './addr-input.service';

/*
@Injectable({
  providedIn: 'root'
})*/

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: []
})

export class AppComponent implements OnInit {
  title = 'tusafeliving';
  public inputAddr: any;

constructor(){}
/*
  sendInput(value: string) {
    this.inputAddr = value;
    console.log(this.inputAddr);
    this.addrInputService.setAddr(this.inputAddr);
    this.router.navigateByUrl('/coord-list');
   }
*/
  ngOnInit(): void {
  }
}

