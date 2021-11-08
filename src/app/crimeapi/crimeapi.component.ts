import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { analyzeAndValidateNgModules } from '@angular/compiler';
import { Globals } from '../globals'

@Component({
  selector: 'app-crimeapi',
  templateUrl: './crimeapi.component.html',
  styleUrls: ['./crimeapi.component.css']
})
export class CrimeapiComponent implements OnInit {

  url = '';
  items = [];
  keynames = [];
  ori: string;
  fromstr: string;
  tostr: string;
  from: number;
  to: number;
  returnedstuff;
  specificcrimedata: object;


  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router, public globals: Globals) {
    this.returnedstuff = new Object;
    this.specificcrimedata = new Object;
    this.ori = '';
    this.from = 0;
    this.to = 0;
    this.fromstr = '';
    this.tostr = '';


    this.route.queryParams
    .subscribe(params => {
      this.ori = params['ori'];
      this.fromstr = params['from'];
      this.from = this.fromstr ? (parseInt(params['from']) ? parseInt(params['from']) : new Date().getFullYear() - 5) : new Date().getFullYear() - 5;
      this.tostr = params['to'];
      this.to = this.tostr ? (parseInt(params['to']) ? parseInt(params['to']) : new Date().getFullYear()) : new Date().getFullYear();
      if(params['from'] != parseInt(params['from']) || params['to'] != parseInt(params['to']))
      {
        this.router.navigate(['crimeapi'], {queryParams: {ori: this.ori, from: this.from, to: this.to}}).then(()=>{window.location.reload()});
      }
      if(this.from > this.to)
      {
        var temp = this.to;
        this.to = this.from;
        this.from = temp;
        this.router.navigate(['crimeapi'], {queryParams: {ori: this.ori, from: this.from, to: this.to}}).then(()=>{window.location.reload()});
      }
    });
    this.url = globals.backendUrl;
    this.url += 'crimedata/api/';
    this.url += this.ori;
    this.url += '/';
    this.url += this.fromstr;
    this.url += '/';
    this.url += this.tostr;
    this.url += '/';
    returned_data: JSON;
    
    

   }

  getData(url:any, cb:any){
    fetch(url)
    .then(response => response.json())
    .then(result => cb(result));
  }

  ngOnInit(): void {
    
  }

}
